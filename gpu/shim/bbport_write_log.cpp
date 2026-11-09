// SPDX-License-Identifier: GPL-2.0-or-later
#include "bbport_write_log.h"

#include <array>
#include <atomic>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#ifdef _WIN32
#include <windows.h>
#undef near
#else
#include <ucontext.h>
#include <unistd.h>
#endif
#include <x86intrin.h>

namespace BbWriteLog {
namespace {
struct Entry {
    std::uint64_t address, size, first, tsc;
    std::uint32_t source, tid;
};
constexpr std::size_t Size = 1 << 20;
std::array<Entry, Size> ring;
std::uint64_t head = 0;
// Writes that contained the suspicious qword (see Note), with the exact address.
std::array<Entry, 256> hits;
std::uint64_t hits_head = 0;
std::atomic_flag ring_busy;
std::atomic<std::uint64_t> dropped{0};
constexpr std::uint64_t Pattern = 0x0000005300000000ull;

struct RingAccess {
    const bool acquired = !ring_busy.test_and_set(std::memory_order_acquire);
    ~RingAccess() {
        if (acquired) ring_busy.clear(std::memory_order_release);
    }
};

} // namespace

void Record(std::uint64_t address, const void* data, std::uint64_t size, Source source);

int Mode() {
    static const int mode = [] {
        const char* env = std::getenv("BB_WRITE_LOG");
        return env ? std::atoi(env) : 0;
    }();
    return mode;
}

bool Enabled() {
    return Mode() == 1;
}

void NoteIntent(std::uint64_t address, const void* data, std::uint64_t size, Source source) {
    if (Mode() == 2) {
        Record(address, data, size, source);
    }
}

void Note(std::uint64_t address, const void* data, std::uint64_t size, Source source) {
    if (Enabled()) {
        Record(address, data, size, source);
    }
}

void Record(std::uint64_t address, const void* data, std::uint64_t size, Source source) {
    static thread_local const std::uint32_t tid = static_cast<std::uint32_t>(gettid());
    Entry e{address, size, 0, __rdtsc(), source, tid};
    std::memcpy(&e.first, data, size < 8 ? size : 8);
    const RingAccess access;
    if (!access.acquired) {
        dropped.fetch_add(1, std::memory_order_relaxed);
        return;
    }
    ring[head++ % ring.size()] = e;
    // Only small writes are scanned: scanning downloads of megabytes delays them enough to hide
    // the race this log is for.
    if (size > 64) {
        return;
    }
    const auto* bytes = static_cast<const unsigned char*>(data);
    for (std::uint64_t at = (8 - (address & 7)) & 7; at + 8 <= size; at += 8) {
        std::uint64_t v;
        std::memcpy(&v, bytes + at, 8);
        if (v == Pattern) {
            Entry hit = e;
            hit.address = address + at;
            hit.first = v;
            hits[hits_head++ % hits.size()] = hit;
        }
    }
}
} // namespace BbWriteLog

extern "C" void bbgpu_dump_guest_writes(void* ucontext, std::uintptr_t pointer_field) {
    using namespace BbWriteLog;
    if (Mode() == 0) {
        return;
    }
    // The fault can interrupt the writer itself. Never wait in this handler
    // or read entries while another thread is publishing them.
    const RingAccess access;
    if (!access.acquired) {
        std::fprintf(stderr, "Write log: unavailable (writer active)\n");
        return;
    }
#ifdef _WIN32
    // The loader passes EXCEPTION_POINTERS (see signal_context.cpp).
    const CONTEXT* c = static_cast<const EXCEPTION_POINTERS*>(ucontext)->ContextRecord;
    const std::uint64_t regs[] = {c->Rax, c->Rbx, c->Rcx, c->Rdx, c->Rsi, c->Rdi, c->R14, c->R15};
#else
    const auto* uc = static_cast<const ucontext_t*>(ucontext);
    const auto* g = uc->uc_mcontext.gregs;
    const std::uint64_t regs[] = {std::uint64_t(g[REG_RAX]), std::uint64_t(g[REG_RBX]),
                                  std::uint64_t(g[REG_RCX]), std::uint64_t(g[REG_RDX]),
                                  std::uint64_t(g[REG_RSI]), std::uint64_t(g[REG_RDI]),
                                  std::uint64_t(g[REG_R14]), std::uint64_t(g[REG_R15])};
#endif
    const char* names[] = {"rax", "rbx", "rcx", "rdx", "rsi", "rdi", "r14", "r15"};
    for (int i = 0; i < 8; ++i) {
        std::fprintf(stderr, "Write log: %s=%#llx\n", names[i], (unsigned long long)regs[i]);
    }
    const char* sources[] = {"backing",      "WriteData",           "fence",
                             "EOP (decoded)", "WriteData (decoded)", "EOS (decoded)"};
    const std::uint64_t now = __rdtsc();
    const auto print = [&](const Entry& e, const char* what) {
        std::fprintf(stderr,
                     "Write log: %s %s %#llx +%llu first %#llx tid %u, %.3f s before the fault\n",
                     what, e.source < 6 ? sources[e.source] : "?", (unsigned long long)e.address,
                     (unsigned long long)e.size, (unsigned long long)e.first, e.tid,
                     double(now - e.tsc) / 3.0e9);
    };
    if (pointer_field) {
        const std::uint64_t n = head;
        const std::uint64_t retained = n < Size ? n : Size;
        unsigned matches = 0;
        for (std::uint64_t i = n; i > n - retained; ) {
            const Entry& e = ring[--i % Size];
            // Subtract only from the greater address, so a malformed range
            // cannot wrap around and hide a write crossing the start.
            const bool overlaps = e.size && (e.address >= pointer_field
                ? e.address - pointer_field < 8 : pointer_field - e.address < e.size);
            if (overlaps) {
                print(e, "pointer field");
                if (++matches == 32) break;
            }
        }
        std::fprintf(stderr, "Write log: pointer field %#llx matches=%u%s retained=%llu total=%llu dropped=%llu mode=%d\n",
                     (unsigned long long)pointer_field, matches, matches == 32 ? " (limit)" : "",
                     (unsigned long long)retained, (unsigned long long)n,
                     (unsigned long long)dropped.load(std::memory_order_relaxed), Mode());
        return;
    }
    const std::uint64_t nh = hits_head;
    for (std::uint64_t i = nh > hits.size() ? nh - hits.size() : 0; i < nh; ++i) {
        print(hits[i % hits.size()], "pattern");
    }
    // The block the guest read (rax) and all logged writes into it or its neighbours.
    const std::uint64_t block = regs[0];
    for (std::uint64_t at = block - 0x30; at < block + 0x60; at += 8) {
        std::uint64_t value = 0;
#ifdef _WIN32
        SIZE_T got;
        if (!ReadProcessMemory(GetCurrentProcess(), reinterpret_cast<const void*>(at),
                               &value, sizeof(value), &got) || got != sizeof(value)) continue;
#else
        std::memcpy(&value, reinterpret_cast<const void*>(at), 8);
#endif
        std::fprintf(stderr, "Write log: [%#llx] = %#llx\n", (unsigned long long)at,
                     (unsigned long long)value);
    }
    {
        const std::uint64_t n = head;
        int shown = 0;
        for (std::uint64_t i = n; i-- > (n > Size ? n - Size : 0) && shown < 200;) {
            const Entry& e = ring[i % Size];
            if (e.address + e.size > block - 0x30 && e.address < block + 0x60) {
                print(e, "in block");
                ++shown;
            }
        }
        shown = 0;
        for (std::uint64_t i = n; i-- > (n > Size ? n - Size : 0) && shown < 40;) {
            const Entry& e = ring[i % Size];
            if ((e.first & 0xffffffffull) == 0x53 || (e.first >> 32) == 0x53) {
                print(e, "value 0x53");
                ++shown;
            }
        }
    }
    // Writes that cover the chunk header the guest read (rax..rax+0x40) or the registers.
    const std::uint64_t n = head;
    int shown = 0;
    for (std::uint64_t i = n; i-- > (n > Size ? n - Size : 0) && shown < 64;) {
        const Entry& e = ring[i % Size];
        bool near = false;
        for (const auto r : regs) {
            near |= r + 0x1000 > e.address && r < e.address + e.size + 0x1000;
        }
        if (near) {
            print(e, "near");
            ++shown;
        }
    }
    std::fprintf(stderr, "Write log: %llu writes logged, %llu dropped\n", (unsigned long long)n,
                 (unsigned long long)dropped.load(std::memory_order_relaxed));
}
