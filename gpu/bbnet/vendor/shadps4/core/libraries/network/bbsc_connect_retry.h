#pragma once

#include <string_view>
#include <chrono>

namespace Libraries::Http {
inline std::chrono::seconds BbscConnectTimeout(bool enabled, std::chrono::seconds requested) {
    // The game's 15ms setting is rounded to one second by the bridge. That
    // expires at the first TCP SYN retransmission on Windows, so a lost SYN
    // starts a new connection instead of letting TCP recover it. Only private
    // BBSC requests opt in; preserve longer explicit and default deadlines.
    return enabled && requested < std::chrono::seconds(3) ? std::chrono::seconds(3) : requested;
}
inline bool BbscConnectRetryEnabled(bool seamless) {
    return seamless;
}

// Only retry a failed TCP connect: no HTTP body has been sent. Never replay a
// consuming POST after a read/write failure or an HTTP response (including 5xx).
template <class Send, class ConnectTimedOut, class Notify>
auto SendBbscHttp(bool enabled, Send send, ConnectTimedOut timed_out, Notify notify) {
    auto result = send();
    for (unsigned retry = 1; enabled && retry <= 2 && timed_out(result); ++retry) {
        notify(retry);
        result = send();
    }
    return result;
}
} // namespace Libraries::Http
