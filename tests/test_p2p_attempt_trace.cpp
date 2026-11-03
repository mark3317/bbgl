// Exercise actual relay implementation, including private diagnostic budget state.
#include "core/net/p2p_relay.cpp"
#include <cassert>
#include <cstdio>
using namespace Core::Net::P2P::Relay;
int main() {
    SetServer(htonl(0x4d4943af)); SetLocalId("attempt-self");
    RememberPeer("attempt-peer", htonl(0xc0000201), htons(40001));
    auto& s=S(); const auto id=PadId("attempt-peer");
    std::vector<std::vector<u8>> sent;
    RawSend send=[&](std::span<const u8> p,u32,u16) {
        sent.emplace_back(p.begin(),p.end()); return SendResult{static_cast<s64>(p.size()),0};
    };
    const std::vector<u8> frame{0xff,0x83,0,40,0,40,1,2,3};
    Route(htonl(0xc0000201),htons(40001),frame,send);
    assert(sent.size()==1 && sent[0][4]==3);
    if (!Common::Log::CoopDiagnosticsEnabled()) {
        assert(s.traces.empty());
        BeginAttempt("attempt-peer");
        assert(s.traces.empty() && TraceGeneration()==0);
        // Even a remote diagnostic notification must not enable tracing locally.
        std::vector<u8> marker{'B','B','R','1',7};
        marker.insert(marker.end(), id.begin(), id.end());
        const auto self=PadId("attempt-self");
        marker.insert(marker.end(),self.begin(),self.end());
        marker.insert(marker.end(),8,1);
        std::span<const u8> decoded; u32 addr; u16 port;
        Receive(marker,&decoded,&addr,&port);
        assert(s.traces.empty());
        puts("PASS: actual relay forwards payload with no release trace maps, hashes or markers");
        return 0;
    }
    assert(s.traces[id].token==0 && s.traces[id].remaining==4095); // before ACK
    sent.clear();
    BeginAttempt("attempt-peer");
    const auto first=s.traces[id].token;
    const auto generation=TraceGeneration();
    Route(htonl(0xc0000201),htons(40001),frame,send);
    assert(sent.size()==2 && sent[0][4]==6 && sent[1][4]==3);
    assert(std::equal(frame.begin(),frame.end(),sent[1].begin()+43));
    assert(s.traces[id].remaining==4095);
    auto ack=sent[0]; ack[4]=7;
    std::span<const u8> decoded; u32 addr; u16 port;
    Receive(ack,&decoded,&addr,&port);
    s.traces[id].remaining=0;
    Receive(ack,&decoded,&addr,&port);
    assert(s.traces[id].remaining==0 && TraceGeneration()==generation);
    s.traces[id].next_marker={};
    KeepAlive(send); // retries even after own ACK, to recover lost receiver notification
    assert(s.traces[id].markers==2);
    BeginAttempt("attempt-peer");
    assert(s.traces[id].token>first && s.traces[id].remaining==4096);
    assert(TraceGeneration()>generation);
    Receive(ack,&decoded,&addr,&port); // stale notification cannot replace new attempt
    assert(s.traces[id].token>first && s.traces[id].remaining==4096);
    s.traces[id].expires=Clock::now()-std::chrono::seconds(1);
    TraceLocked(s,id,"SOCKET_TX",frame,{-1,55});
    assert(s.traces[id].remaining==4096);
    BeginAttempt("attempt-peer");
    const std::vector<u8> bulk{0xff,0x83,0,30,0,30};
    TraceLocked(s,id,"SOCKET_TX",bulk,{-1,55});
    assert(s.traces[id].remaining==4096);
    TraceLocked(s,id,"SOCKET_TX",frame,{-1,55});
    assert(s.traces[id].remaining==4095);
    const auto old_generation=TraceGeneration();
    s.traces[id].remaining=0;
    ObserveAttemptSerialLocked(s, 1);
    assert(s.traces[id].remaining==4096 && TraceGeneration()>old_generation);
    s.traces[id].remaining=0;
    ObserveAttemptSerialLocked(s, 1);
    assert(s.traces[id].remaining==0); // polling cannot replenish
    const auto previous=s.traces[id].token;
    ObserveAttemptSerialLocked(s, 2); // same signaling peer/conn, actual native rejoin
    assert(s.traces[id].token>previous && s.traces[id].remaining==4096);
    puts("PASS: actual relay attempt renewal, marker ordering/retry, stale/duplicate ACK, expiry, filtering, socket failure");
}
