#include "bbsc_network_attempt.h"
#include "bbsc_relay_io.h"
#include <cassert>
#include <cstring>
#include <iostream>
#include <string>
using namespace BbscMod;
int main() {
    NetworkAttemptTrace trace;
    trace.State(0,false); trace.Claim(); auto first=trace.serial.load();
    assert(!trace.State(0,true)); assert(!trace.State(4,true));
    assert(!trace.State(6,false)); assert(trace.serial==first);
    // Repeated state/lamp/death loads while already guest cannot renew forever.
    for (int i=0;i<100;++i) assert(!trace.State(6,false));
    assert(!trace.State(-1,false));assert(!trace.State(6,false));assert(trace.serial==first);
    trace.State(7,false); trace.State(0,false); trace.Claim();
    assert(trace.serial==first+1); trace.State(4,true);trace.State(6,false);
    trace.State(0,false);assert(trace.State(4,false));assert(!trace.State(4,false));
    trace.State(6,false);trace.State(0,false);assert(trace.State(6,false)); // short join missed by polling
    auto serial=trace.serial.load();trace.State(3,false);trace.State(3,false);assert(trace.serial==serial);
    const std::string packet="length-prefixed-frame";
    std::uint64_t clock=0; std::string sent; int calls=0,waits=0;
    auto now=[&]{return clock;};
    auto result=RelayIo::SendFrame(packet.data(),packet.size(),now,
        [&](const char* p,int n) { ++calls; if(calls%2==1)return RelayIo::Attempt{-1,10035,true};
            int bytes=std::min(n,3);sent.append(p,bytes);return RelayIo::Attempt{bytes,0,false}; },
        [&](int ms){++waits;clock+=ms;return 0;},[](int){});
    assert(!result.timeout && !result.error && sent==packet && result.bytes==packet.size() && waits);
    clock=0;
    result=RelayIo::SendFrame(packet.data(),packet.size(),now,
        [](const char*,int){return RelayIo::Attempt{-1,10035,true};},
        [&](int ms){clock+=ms;return 0;},[](int){});
    assert(result.timeout && clock==10000 && result.bytes==0);
    // Slow partial progress cannot keep the same frame alive past its absolute deadline.
    clock=0;
    result=RelayIo::SendFrame(packet.data(),packet.size(),now,
        [&](const char*,int){clock+=2000;return RelayIo::Attempt{1,0,false};},
        [](int){return 0;},[](int){});
    assert(result.timeout && result.bytes==5 && clock==10000);
    clock=0;
    result=RelayIo::SendFrame(packet.data(),packet.size(),now,
        [](const char*,int){return RelayIo::Attempt{-1,10054,false};},
        [](int){return 0;},[](int){});
    assert(!result.timeout && result.error==10054 && result.bytes==0);
    result=RelayIo::SendFrame(packet.data(),packet.size(),now,
        [](const char*,int){return RelayIo::Attempt{-1,10035,true};},
        [](int){return 10038;},[](int){});
    assert(result.error==10038);
    result=RelayIo::SendFrame(packet.data(),packet.size(),now,
        [](const char*,int){return RelayIo::Attempt{-1,10035,true};},
        [&](int ms){clock+=ms;return 0;},[](int){},500);
    assert(result.timeout && clock==500); // queue age consumes the same budget
    std::cout<<"PASS: real lifecycle serial + bounded writer loop: reused joins, claim debounce, load states, partial send, deadline, errors, queue age\n";
}
