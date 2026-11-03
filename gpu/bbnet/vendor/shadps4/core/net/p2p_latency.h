// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include <array>
#include <cstdint>
#include <span>

namespace Core::Net::P2P {
// Correlate application datagrams across peers without retaining their contents.
// Fixed storage; a full diagnostic batch never changes delivery of a game packet.
struct LatencySamples {
    struct Sample {
        char kind;
        std::uint16_t local, peer;
        std::uint32_t size;
        std::uint64_t hash;
        std::int64_t wall_us, queue_us;
        std::uint32_t header, endpoint_addr;
        std::uint16_t endpoint_port;
    };
    std::array<Sample, 1024> samples{};
    std::size_t count = 0;
    std::uint64_t omitted = 0;
    std::uint64_t remaining = 65536; // bounded per transport, even in an hours-long session
    void Record(char kind, std::uint16_t local, std::uint16_t peer,
                std::span<const std::uint8_t> payload, std::int64_t wall_us,
                std::int64_t queue_us = 0, std::uint32_t endpoint_addr = 0,
                std::uint16_t endpoint_port = 0) {
        if (count == samples.size() || remaining == 0) { ++omitted; return; }
        --remaining;
        std::uint64_t hash = 14695981039346656037ULL;
        for (auto byte : payload) { hash ^= byte; hash *= 1099511628211ULL; }
        std::uint32_t header = 0;
        for (std::size_t i = 0; i < 4 && i < payload.size(); ++i)
            header |= static_cast<std::uint32_t>(payload[i]) << (24 - 8 * i);
        samples[count++] = {kind, local, peer, static_cast<std::uint32_t>(payload.size()),
                            hash, wall_us, queue_us, header, endpoint_addr, endpoint_port};
    }
    void Clear() { count = 0; omitted = 0; }
};
} // namespace Core::Net::P2P
