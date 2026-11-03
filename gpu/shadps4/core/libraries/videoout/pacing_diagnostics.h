// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once

#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdio>
#include <memory>
#include "async_diagnostic_queue.h"

namespace Libraries::VideoOut {

// All frame accounting belongs to PresentThread. Only swap totals cross threads.
// No per-frame allocation, CPU query, logging, or change to limiter deadlines.
struct PacingWindow {
    using Clock = std::chrono::steady_clock;
    using Time = Clock::time_point;
    static double Ms(Clock::duration d) {
        return std::chrono::duration<double, std::milli>(d).count();
    }
    struct Metric {
        double sum = 0, max = 0;
        unsigned count = 0;
        void Add(double ms) { sum += ms; max = std::max(max, ms); ++count; }
        double Mean() const { return count ? sum / count : 0; }
    };
    struct Cpu {
        double process_ms = 0, thread_ms = 0, busy_ms = 0, total_ms = 0;
        unsigned long pid = 0;
        bool valid = false;
    };
    Time window_start{}, previous{};
    Cpu cpu{};
    Metric interval, queue_age, prepare, ready_late, dispatch_late, flip_work;
    Metric cap_wait, cap_wake, tail_wake, tail_overrun, producer_wait, period;
    unsigned frames = 0, ready_by_deadline = 0;
    double previous_report_ms = 0;
    size_t queue_max = 0;
    struct Slow {
        long long epoch_ms;
        double frame_ms, ready_ms, dispatch_ms, queue_ms, prepare_ms, flip_ms;
    };
    std::array<Slow, 8> slow{};
    unsigned slow_count = 0, slow_omitted = 0;

    void WriteReport(unsigned limit, bool strict, bool grid, double duration_ms,
                     Cpu next, long long epoch, unsigned long long swaps,
                     unsigned long long swap_queue, unsigned long long swap_work,
                     unsigned long long dropped) const {
        const bool valid = cpu.valid && next.valid;
        const double system_ms = next.total_ms - cpu.total_ms;
        std::printf("Perf pacing: epoch_ms=%lld pid=%lu duration_ms=%.3f frames=%u "
                    "limit=%u strict=%u grid=%u tail_precise=%u interval_ms=%.3f period_ms=%.3f "
                    "period_max_ms=%.3f producer_waits=%u producer_wait_ms=%.3f "
                    "ready_by_deadline=%u ready_late_ms=%.3f ready_late_max_ms=%.3f "
                    "dispatch_ms=%.3f dispatch_max_ms=%.3f queue_ms=%.3f queue_max_ms=%.3f "
                    "queue_depth_max=%zu prepare_ms=%.3f prepare_max_ms=%.3f "
                    "flip_ms=%.3f flip_max_ms=%.3f cap_waits=%u cap_wait_ms=%.3f "
                    "cap_wake_ms=%.3f cap_wake_max_ms=%.3f tail_waits=%u "
                    "tail_wake_ms=%.3f tail_wake_max_ms=%.3f tail_overruns=%u "
                    "tail_overrun_max_ms=%.3f cpu_valid=%u "
                    "process_cores=%.3f present_cores=%.3f system_busy_pct=%.3f "
                    "swaps=%llu swap_queue_us=%llu swap_work_us=%llu slow_omitted=%u "
                    "previous_report_ms=%.3f report_async=1 reports_dropped=%llu\n",
                    static_cast<long long>(epoch), next.pid, duration_ms, frames,
                    limit, unsigned(strict), unsigned(grid), unsigned(strict && limit != 0), interval.Mean(),
                    period.Mean(), period.max, producer_wait.count, producer_wait.Mean(), ready_by_deadline,
                    ready_late.Mean(), ready_late.max, dispatch_late.Mean(), dispatch_late.max,
                    queue_age.Mean(), queue_age.max, queue_max, prepare.Mean(), prepare.max,
                    flip_work.Mean(), flip_work.max, cap_wait.count, cap_wait.Mean(),
                    cap_wake.Mean(), cap_wake.max, tail_wake.count, tail_wake.Mean(), tail_wake.max,
                    tail_overrun.count, tail_overrun.max,
                    unsigned(valid), valid ? (next.process_ms - cpu.process_ms) / duration_ms : -1,
                    valid ? (next.thread_ms - cpu.thread_ms) / duration_ms : -1,
                    valid && system_ms > 0 ? 100 * (next.busy_ms - cpu.busy_ms) / system_ms : -1,
                    swaps, swap_queue, swap_work, slow_omitted, previous_report_ms, dropped);
        for (unsigned i = 0; i < slow_count; ++i) {
            const auto& s = slow[i];
            std::printf("Perf pacing slow: epoch_ms=%lld pid=%lu frame_ms=%.3f "
                        "ready_late_ms=%.3f dispatch_ms=%.3f queue_ms=%.3f "
                        "prepare_ms=%.3f flip_ms=%.3f\n", s.epoch_ms, next.pid, s.frame_ms,
                        s.ready_ms, s.dispatch_ms, s.queue_ms, s.prepare_ms, s.flip_ms);
        }
    }
};

struct PacingDiagnostics : PacingWindow {
    static Cpu ReadCpu();
    struct ReportData {
        PacingWindow window;
        Cpu next;
        long long epoch;
        double duration_ms;
        unsigned limit;
        bool strict, grid;
        unsigned long long swaps, swap_queue, swap_work, dropped;
    };
    std::unique_ptr<AsyncDiagnosticQueue<ReportData>> reports;
    unsigned long long reports_dropped = 0;
    std::atomic<unsigned long long> swap_count{0}, swap_queue_us{0}, swap_work_us{0};

    void Start() {
        reports = std::make_unique<AsyncDiagnosticQueue<ReportData>>([](const ReportData& r) {
            r.window.WriteReport(r.limit, r.strict, r.grid, r.duration_ms,
                                 r.next, r.epoch, r.swaps, r.swap_queue, r.swap_work, r.dropped);
        });
        window_start = Clock::now();
        cpu = ReadCpu();
    }
    void Record(Time start, Time finish, Time queued, double prepare_ms,
                Time deadline, bool capped, size_t depth, double period_ms) {
        const double frame_ms = previous == Time{} ? 0 : Ms(start - previous);
        if (previous != Time{}) interval.Add(frame_ms);
        previous = start;
        const double queue_ms = Ms(start - queued);
        const double ready_ms = capped ? std::max(0.0, Ms(queued - deadline)) : 0;
        // Dispatch delay includes OS scheduling, mutex work and vblank handling;
        // it is NOT a measurement of scheduler preemption alone.
        const double dispatch_ms = Ms(start - (capped ? std::max(deadline, queued) : queued));
        queue_age.Add(queue_ms); prepare.Add(prepare_ms);
        if (capped) {
            period.Add(period_ms);
            ready_late.Add(ready_ms);
            ready_by_deadline += queued <= deadline;
        }
        dispatch_late.Add(std::max(0.0, dispatch_ms));
        flip_work.Add(Ms(finish - start));
        queue_max = std::max(queue_max, depth);
        ++frames;
        if (frame_ms > 50 || Ms(finish - start) > 50) {
            if (slow_count < slow.size()) {
                const auto epoch = std::chrono::duration_cast<std::chrono::milliseconds>(
                    (std::chrono::system_clock::now() - (Clock::now() - start)).time_since_epoch()).count();
                slow[slow_count++] = {epoch, frame_ms, ready_ms, dispatch_ms, queue_ms,
                                     prepare_ms, Ms(finish - start)};
            } else ++slow_omitted;
        }
    }
    void Report(unsigned limit, bool strict, bool grid) {
        const auto now = Clock::now();
        const double duration_ms = Ms(now - window_start);
        if (duration_ms < 5000) return;
        const auto report_start = now;
        const Cpu next = ReadCpu();
        const auto epoch = std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::system_clock::now().time_since_epoch()).count();
        ReportData report{static_cast<const PacingWindow&>(*this), next, epoch,
            duration_ms, limit, strict, grid,
            swap_count.exchange(0, std::memory_order_relaxed),
            swap_queue_us.exchange(0, std::memory_order_relaxed),
            swap_work_us.exchange(0, std::memory_order_relaxed), reports_dropped};
        if (!reports->Submit(std::move(report))) ++reports_dropped;
        interval = {}; queue_age = {}; prepare = {}; ready_late = {};
        dispatch_late = {}; flip_work = {}; cap_wait = {}; cap_wake = {}; tail_wake = {};
        tail_overrun = {}; producer_wait = {}; period = {};
        frames = ready_by_deadline = slow_count = slow_omitted = 0; queue_max = 0;
        // Exclude snapshot/queue overhead from the next CPU/wall window.
        // Formatting and printing now run on the bounded diagnostic worker.
        cpu = ReadCpu(); window_start = Clock::now();
        previous_report_ms = Ms(window_start - report_start);
    }
};
} // namespace Libraries::VideoOut
