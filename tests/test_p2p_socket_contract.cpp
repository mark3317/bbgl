// Execute the native PS4 recv API against real production P2P sockets.
#include "core/libraries/net/net.h"
#include "core/net/guest_net.h"
#include "core/net/p2p_codec.h"
#include <array>
#include <cassert>
#include <chrono>
#include <cstdio>
#include <thread>
using namespace Core::Net;
using namespace Core::Net::P2P;
using namespace Libraries::Net;
using namespace std::chrono_literals;

int main() {
    assert(Host::Initialize());
    Host::Error error{};
    auto a=Transport::Create(AF_INET,Endpoint::IPv4("127.0.0.1",0),
        std::make_unique<FramingCodec>(std::make_shared<Keyring>()),TransportConfig{},&error);
    auto b=Transport::Create(AF_INET,Endpoint::IPv4("127.0.0.1",0),
        std::make_unique<FramingCodec>(std::make_shared<Keyring>()),TransportConfig{},&error);
    assert(a && b);
    auto sender=a->CreateDatagram();
    assert(sender->Bind(40)==Host::Error::Ok);
    SetP2PTransport(AF_INET,b);
    const auto created=P2PSocketCreate(AF_INET,false);
    assert(created.error==Host::Error::Ok);
    const auto socket=static_cast<s32>(created.value);
    assert(P2PSocketBind(socket,40).error==Host::Error::Ok);
    const auto target=Endpoint::IPv4("127.0.0.1",b->BoundPort());
    const std::array<u8,5> payload{1,2,3,4,5};
    assert(sender->SendTo(payload,&target,40).error==Host::Error::Ok);
    std::this_thread::sleep_for(50ms);
    // Original BBSC returns 5 here. Previously BBGL returned 0.
    assert(sceNetRecvfrom(socket,nullptr,0,ORBIS_NET_MSG_PEEKLEN,nullptr,nullptr)==5);
    assert(sceNetRecvfrom(socket,nullptr,100,ORBIS_NET_MSG_PEEKLEN,nullptr,nullptr)==5);
    std::array<u8,2> small{};
    assert(sceNetRecvfrom(socket,small.data(),small.size(),ORBIS_NET_MSG_PEEKLEN,nullptr,nullptr)==5);
    assert(small[0]==1 && small[1]==2);
    assert(sceNetRecvfrom(socket,small.data(),small.size(),ORBIS_NET_MSG_PEEK,nullptr,nullptr)==2);
    std::array<u8,5> received{};
    assert(sceNetRecvfrom(socket,received.data(),received.size(),0,nullptr,nullptr)==5);
    assert(received==payload);
    assert(P2PSocketRecvFrom(socket,received.data(),received.size(),false,true,nullptr,nullptr).error==Host::Error::WouldBlock);
    // Normal short receive still consumes one datagram and discards its tail.
    assert(sender->SendTo(payload,&target,40).error==Host::Error::Ok);
    std::this_thread::sleep_for(50ms);
    assert(sceNetRecvfrom(socket,small.data(),small.size(),0,nullptr,nullptr)==2);
    assert(P2PSocketRecvFrom(socket,received.data(),received.size(),false,true,nullptr,nullptr).error==Host::Error::WouldBlock);
    assert(SocketClose(socket).error==Host::Error::Ok);
    std::puts("PASS: native sceNetRecvfrom PEEKLEN null/short/full size, PEEK, consume and truncation");
}
