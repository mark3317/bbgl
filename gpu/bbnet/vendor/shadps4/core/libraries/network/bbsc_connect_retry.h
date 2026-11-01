#pragma once

#include <string_view>

namespace Libraries::Http {
inline bool BbscClaimRetryEnabled(bool post, std::string_view path, bool seamless) {
    return post && seamless && path.substr(0, path.find('?')) == "/summon_messenger/request";
}

// Only retry a failed TCP connect: no HTTP body has been sent. Never replay a
// consuming POST after a read/write failure or an HTTP response (including 5xx).
template <class Send, class ConnectTimedOut, class Notify>
auto SendBbscClaim(bool enabled, Send send, ConnectTimedOut timed_out, Notify notify) {
    auto result = send();
    for (unsigned retry = 1; enabled && retry <= 2 && timed_out(result); ++retry) {
        notify(retry);
        result = send();
    }
    return result;
}
} // namespace Libraries::Http
