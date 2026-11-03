// bbport: see log.h.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <chrono>
#include <ctime>
#include <mutex>
#include <string>
#include <filesystem>
#ifdef _WIN32
#include <windows.h>
#endif
#include "common/logging/log.h"

namespace Common::Log {
#ifdef _WIN32
// Read the process environment, including values changed through Win32 after CRT startup.
static std::wstring ProcessEnv(const wchar_t* name) {
    const DWORD size = GetEnvironmentVariableW(name, nullptr, 0);
    if (!size || size > 32768) return {};
    std::wstring value(size, L'\0');
    const DWORD length = GetEnvironmentVariableW(name, value.data(), size);
    if (!length || length >= size) return {};
    value.resize(length);
    return value;
}
#endif
bool DiagnosticsEnabled() {
    static const bool enabled = [] {
#ifdef _WIN32
        return ProcessEnv(L"BB_DIAGNOSTICS") == L"1";
#else
        const char* value = std::getenv("BB_DIAGNOSTICS");
        return value && std::strcmp(value, "1") == 0;
#endif
    }();
    return enabled;
}
bool CoopDiagnosticsEnabled() {
    static const bool enabled = [] {
#ifdef _WIN32
        const auto value = ProcessEnv(L"BB_NET_DIAGNOSTICS");
        return value.empty() ? DiagnosticsEnabled() : value == L"1";
#else
        const char* value = std::getenv("BB_NET_DIAGNOSTICS");
        return value ? std::strcmp(value, "1") == 0 : DiagnosticsEnabled();
#endif
    }();
    return enabled;
}
static Level threshold() {
    static const Level level = [] {
        const char* v = std::getenv("BB_GPU_LOG");
        if (!v) return DiagnosticsEnabled() ? Level::debug : (CoopDiagnosticsEnabled() ? Level::warn : Level::err);
        static const char* names[] = {"trace", "debug", "info", "warning", "error", "critical"};
        for (int i = 0; i < 6; ++i)
            if (!std::strcmp(v, names[i])) return Level(i);
        return DiagnosticsEnabled() ? Level::debug : (CoopDiagnosticsEnabled() ? Level::warn : Level::err);
    }();
    return level;
}
bool ShouldLog(Level level) { return level >= threshold(); }
bool ShouldLogClass(std::string_view log_class, Level level) {
    if (level >= threshold()) return true;
    static const std::string classes = [] {
        const char* v = std::getenv("BB_GPU_LOG_CLASSES");
        if (v) return std::string(v);
        return std::string{};
    }();
    if (classes.empty() || level < Level::info) return false;
    size_t pos = 0;
    while (pos <= classes.size()) {
        size_t end = classes.find(',', pos);
        if (end == std::string::npos) end = classes.size();
        if (classes.compare(pos, end - pos, log_class) == 0 && end - pos == log_class.size()) return true;
        pos = end + 1;
    }
    return false;
}
void Write(std::string_view log_class, Level level, const char* file, int line, const char* function,
           std::string&& message) {
    static std::mutex mutex;
    // BB_GPU_LOG_FILE=<path>: the log also goes there (the launcher does not always keep stderr).
    static std::FILE* log_file = [] {
        const char* v = std::getenv("BB_GPU_LOG_FILE");
        if (v && *v) return std::fopen(v, "a");
        return static_cast<std::FILE*>(nullptr);
    }();
    static const char* names[] = {"Trace", "Debug", "Info", "Warning", "Error", "Critical"};
    const char* base = std::strrchr(file, '/');
    std::scoped_lock lock{mutex};
    const auto now = std::chrono::system_clock::now();
    const std::time_t secs = std::chrono::system_clock::to_time_t(now);
    std::tm local{};
#ifdef _WIN32
    localtime_s(&local, &secs);
#else
    localtime_r(&secs, &local);
#endif
    const int ms = int(std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count() % 1000);
    // stderr is unbuffered in the native runner. Passing a large P2P report to
    // fprintf's %s performs tiny writes on Windows and can stall the receive
    // thread for hundreds of milliseconds. Submit the complete record in bulk.
    const auto record = fmt::format("[{:02d}:{:02d}:{:02d}.{:03d}] GPU [{}] <{}> {}:{} {}: {}\n",
                                    local.tm_hour, local.tm_min, local.tm_sec, ms, log_class,
                                    names[int(level)], base ? base + 1 : file, line, function,
                                    message);
    std::fwrite(record.data(), 1, record.size(), stderr);
    if (log_file) {
        std::fwrite(record.data(), 1, record.size(), log_file);
        std::fflush(log_file);
    }
}
} // namespace Common::Log
