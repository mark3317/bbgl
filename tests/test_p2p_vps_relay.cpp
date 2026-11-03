// Two independent instances of the production transport, communicating via a real VPS.
// No game/account DB changes: the UDP relay's ephemeral diagnostic online IDs only.
#include "core/net/p2p_codec.h"
#include "core/net/p2p_relay.h"
#include <windows.h>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <set>
#include <string>
#include <thread>
using namespace Core::Net;
using namespace Core::Net::P2P;
using namespace std::chrono_literals;
int main(int argc,char** argv) {
    assert((argc==4 || argc==5) && Host::Initialize());
    using SetSerial = void (*)(unsigned long long);
    SetSerial set_serial=nullptr;
    if(argc==5) { auto mod=LoadLibraryA(argv[4]); assert(mod); set_serial=reinterpret_cast<SetSerial>(GetProcAddress(mod,"SetAttemptSerial")); assert(set_serial); }
    unsigned long long serial=0;
    const int role=std::atoi(argv[1]);
    assert(role==0 || role==1);
    const std::string self=std::string(argv[2])+std::to_string(role);
    const std::string peer=std::string(argv[2])+std::to_string(1-role);
    in_addr server{}; assert(inet_pton(AF_INET,argv[3],&server)==1);
    Relay::SetServer(server.s_addr); Relay::SetLocalId(self);
    // Documentation-range endpoints are carried inside the envelope; the actual
    // datagrams are addressed by online ID and always traverse the VPS relay.
    const auto self_ep=Endpoint::IPv4("192.0.2.1",40000+role);
    const auto peer_ep=Endpoint::IPv4("192.0.2.1",40000+1-role);
    const auto& self_in=*reinterpret_cast<const sockaddr_in*>(&self_ep.addr);
    const auto& peer_in=*reinterpret_cast<const sockaddr_in*>(&peer_ep.addr);
    Relay::SetSelfEndpoint(self_in.sin_addr.s_addr,self_in.sin_port);
    Relay::RememberPeer(peer,peer_in.sin_addr.s_addr,peer_in.sin_port);
    Host::Error error{};
    auto transport=Transport::Create(AF_INET,Endpoint::IPv4("0.0.0.0",0),
        std::make_unique<FramingCodec>(std::make_shared<Keyring>()),TransportConfig{},&error);
    assert(transport);
    auto socket=transport->CreateDatagram(); assert(socket->Bind(40)==Host::Error::Ok);
    std::this_thread::sleep_for(3s); // both relay registrations acknowledged first
    std::set<unsigned> received;
    const auto start=Clock::now();
    unsigned sent=0;
    const auto begin = [&] { if (set_serial) set_serial(++serial); else Relay::BeginAttempt(peer); };
    if (role==0) begin();
    bool second=false;
    while(Clock::now()-start<14s) {
        if (!second && Clock::now()-start>=7s) {
            second=true;
            if (role==0) begin(); // same transport/signaling peer, fresh mod lifecycle serial
        }
        if((sent<60 || (second && sent<120)) &&
           Clock::now()-start >= (sent<60 ? 50ms*sent : 7s+50ms*(sent-60))) {
            std::array<u8,64> body{}; body[0]=0xa1; body[1]=role; body[2]=sent;
            assert(socket->SendTo(body,&peer_ep,40).error==Host::Error::Ok); ++sent;
        }
        std::array<u8,64> body{};
        const auto got=socket->RecvFrom(body,false,nullptr,nullptr);
        if(got.error==Host::Error::Ok) {
            assert(got.bytes==64 && body[0]==0xa1 && body[1]==1-role);
            received.insert(body[2]);
        } else assert(got.error==Host::Error::WouldBlock);
        std::this_thread::sleep_for(1ms);
    }
    std::printf("VPS production transport: role=%d sent=%u received=%zu/120\n",role,sent,received.size());
    return received.size()==120 ? 0 : 2;
}
