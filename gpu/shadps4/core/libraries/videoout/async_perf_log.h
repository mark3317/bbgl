// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include <array>
#include <cstdio>
#include "async_diagnostic_queue.h"

namespace Libraries::VideoOut {
using PerfLine = std::array<char, 512>;
inline unsigned long long& PerfLinesDropped() {
    static unsigned long long dropped = 0; // single producer: PresentThread
    return dropped;
}
inline AsyncDiagnosticQueue<PerfLine, 16>& PerfLineOutput() {
    static AsyncDiagnosticQueue<PerfLine, 16> output([](const PerfLine& line) {
        std::fputs(line.data(), stdout);
    });
    return output;
}
// Legacy Perf window/stall lines must not wait for stdout's lock or a slow pipe
// while the larger pacing report is being written by the diagnostic worker.
template<class... Args>
bool QueuePerfLine(const char* format, Args... args) {
    PerfLine line{};
    const int size = std::snprintf(line.data(), line.size(), format, args...);
    const bool queued = size >= 0 && static_cast<size_t>(size) < line.size() && PerfLineOutput().Submit(line);
    if (!queued) ++PerfLinesDropped();
    return queued;
}
}
