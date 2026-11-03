// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include <array>
#include <atomic>
#include <cstddef>
#include <functional>
#include <semaphore>
#include <thread>
#include <utility>

namespace Libraries::VideoOut {
// Single frame-thread producer, one writer. Full queue drops diagnostics, never
// stalls a frame. The consumer releases its slot before touching a slow sink.
template<class T, size_t Capacity = 2>
class AsyncDiagnosticQueue {
    static_assert(Capacity > 0);
public:
    explicit AsyncDiagnosticQueue(std::function<void(const T&)> output)
        : output(std::move(output)), worker([this] { Run(); }) {}
    ~AsyncDiagnosticQueue() {
        stopping.store(true, std::memory_order_release);
        ready.release();
        worker.join();
    }
    bool Submit(T report) {
        const auto pos = written.load(std::memory_order_relaxed);
        if (pos - read.load(std::memory_order_acquire) == Capacity) return false;
        slots[pos % Capacity] = std::move(report);
        written.store(pos + 1, std::memory_order_release);
        ready.release();
        return true;
    }
private:
    void Run() {
        for (;;) {
            ready.acquire();
            const auto pos = read.load(std::memory_order_relaxed);
            if (pos == written.load(std::memory_order_acquire)) {
                if (stopping.load(std::memory_order_acquire)) return;
                continue;
            }
            const T report = std::move(slots[pos % Capacity]);
            read.store(pos + 1, std::memory_order_release);
            output(report);
        }
    }
    std::array<T, Capacity> slots{};
    std::atomic<size_t> written{0}, read{0};
    std::atomic<bool> stopping{false};
    std::counting_semaphore<> ready{0};
    std::function<void(const T&)> output;
    std::thread worker;
};
}
