"""Execute production packet admission and callback guards with reused room slots."""
import os
from pathlib import Path
import subprocess
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
base = 'gpu/bbnet/vendor/shadps4/core/libraries/np/np_matching2/'
baseline = '--baseline' in sys.argv
def read(name):
    if baseline:
        return subprocess.check_output(['git','-C',str(ROOT),'show','HEAD:'+base+name],text=True)
    return (ROOT/base/name).read_text()
source = read('np_matching2_signaling.cpp')
internal = read('np_matching2_internal.cpp')
def function(name):
    start=re.search(r'^(?:bool|void) '+re.escape(name),source,re.M).start()
    opening=source.index('{',start); depth=1; end=opening+1
    while depth:
        depth += (source[end]=='{')-(source[end]=='}'); end+=1
    return source[start:end]
packet=source[source.index('enum class Matching2HandshakeKind'):source.index('#pragma pack(pop)')+len('#pragma pack(pop)')]
branch=internal[internal.index('    case PendingEvent::SIGNALING_CB:'):internal.index('    case PendingEvent::LOBBY_EVENT_CB:')]
cpp=r'''
#include <cassert>
#include <cstring>
#include <algorithm>
#include <limits>
#include "core/libraries/error_codes.h"
#include "core/libraries/np/np_error.h"
#include "core/libraries/np/np_matching2/np_matching2_internal.h"
#include "core/libraries/np/np_matching2/np_matching2_signaling.h"
#define LOG_INFO(...)
#define LOG_DEBUG(...)
#define LOG_WARNING(...)
namespace Libraries::Np::NpMatching2 {
constexpr s32 kMatching2ConnActive=2, kMatching2ConnPending=1;
PACKET
ContextObject* current;
std::vector<PendingEvent> queued;
unsigned sends=0,callbacks=0;
void ScheduleEvent(PendingEvent event) { queued.push_back(std::move(event)); }
ContextObject* FindContextForMatching2Packet(const Matching2HandshakePacket& p) {
    return current && current->room_id==p.room_id && current->my_member_id==p.to_member_id ? current : nullptr;
}
bool SendMatching2Handshake(ContextObject&,OrbisNpMatching2RoomId,OrbisNpMatching2RoomMemberId,
                           Matching2HandshakeKind,u64) { ++sends; return true; }
FUNCTIONS
void Dispatch(ContextObject* ctx,const PendingEvent& ev) {
    switch(ev.type) { BRANCH default: break; }
}
void PS4_SYSV_ABI Callback(OrbisNpMatching2ContextId,OrbisNpMatching2RoomId,
    OrbisNpMatching2RoomMemberId,OrbisNpMatching2Event,s32,void*) { ++callbacks; }
void PS4_SYSV_ABI RoomCallback(OrbisNpMatching2ContextId,OrbisNpMatching2RoomId,
    OrbisNpMatching2Event,const void*,void*) { ++callbacks; }
void Test() {
    ContextObject ctx; current=&ctx; ctx.ctx_id=1;ctx.room_id=15;ctx.my_member_id=17;
    ctx.signaling_callback=Callback;
    auto& room=ctx.room_cache[15]; room.signaling_type=ORBIS_NP_MATCHING2_SIGNALING_TYPE_MESH;
    auto& old=room.members[34];old.member_id=34;old.join_date=100;
    std::memcpy(old.np_id.handle.data,"guest-a",7);
    room.members[51].member_id=51;room.members[51].join_date=50;
    ctx.peers[51].member_id=51;ctx.peers[51].status=2;ctx.peers[51].addr=99;
    Matching2HandshakePacket p{};p.kind=3;p.room_id=15;p.to_member_id=17;p.from_member_id=34;
    std::memcpy(p.online_id_from,"guest-a",7);
    HandleMatching2HandshakePacket(1,2,p);
    assert(ctx.peers.at(34).status==2 && queued.size()==1);
    auto old_event=queued.back(); Dispatch(&ctx,old_event); assert(callbacks==1);
    room.members.erase(34);ctx.peers.erase(34);
    auto& fresh=room.members[36];fresh.member_id=36;fresh.join_date=200;
    std::memcpy(fresh.np_id.handle.data,"guest-b",7);
    // The native slot (id>>4) is reused; the old member is no longer authoritative.
    assert((34>>4)==(36>>4));
    const auto before=queued.size();const auto before_sends=sends;
    HandleMatching2HandshakePacket(1,2,p);
    assert(!ctx.peers.contains(34) && queued.size()==before && sends==before_sends);
    MarkMatching2PeerActive(ctx,15,34,1,2); assert(!ctx.peers.contains(34));
    Dispatch(&ctx,old_event); assert(callbacks==1); // queued before MEMBER_LEFT
    p.from_member_id=36; // wrong online ID must not replace the slot's new identity
    HandleMatching2HandshakePacket(1,2,p); assert(!ctx.peers.contains(36));
    std::memset(p.online_id_from,0,16);std::memcpy(p.online_id_from,"guest-b",7);
    p.kind=99;HandleMatching2HandshakePacket(1,2,p);assert(!ctx.peers.contains(36));
    p.kind=3;HandleMatching2HandshakePacket(1,2,p);
    assert(ctx.peers.at(36).status==2 && !ctx.peers.contains(34));
    auto retired=p;retired.from_member_id=34;
    HandleMatching2HandshakePacket(8,9,retired);
    assert(ctx.peers.at(36).status==2 && ctx.peers.at(36).addr==1);
    assert(ctx.peers.at(51).status==2 && ctx.peers.at(51).addr==99);
    auto event=queued.back();Dispatch(&ctx,event);assert(callbacks==2);
    ctx.room_id=16;Dispatch(&ctx,event);assert(callbacks==2);ctx.room_id=15;
    ctx.my_member_id=18;Dispatch(&ctx,event);assert(callbacks==2);ctx.my_member_id=17;
    fresh.join_date=300;Dispatch(&ctx,event);assert(callbacks==2); // full ID wrap/reuse
    auto stale_dead=event;stale_dead.sig_event=ORBIS_NP_MATCHING2_SIGNALING_EVENT_DEAD;
    Dispatch(&ctx,stale_dead);assert(callbacks==2); // old DEAD cannot evict new incarnation
    // A genuine current-room DEAD remains deliverable after roster removal.
    QueueMatching2SignalingEvent(ctx,15,36,ORBIS_NP_MATCHING2_SIGNALING_EVENT_DEAD,0);
    auto dead=queued.back();room.members.erase(36);Dispatch(&ctx,dead);assert(callbacks==3);
    // Another healthy slot and the host/self are never overwritten by old traffic.
    assert(ctx.my_member_id==17 && !ctx.peers.contains(17));
    ctx.room_event_callback=RoomCallback;
    auto join=event;join.type=PendingEvent::ROOM_EVENT_CB;
    join.room_event=ORBIS_NP_MATCHING2_ROOM_EVENT_MEMBER_JOINED;
    Dispatch(&ctx,join);assert(callbacks==3); // JOIN queued before this member left
    auto& newcomer=room.members[36];newcomer.join_date=400;join.peer_join_date=400;
    Dispatch(&ctx,join);assert(callbacks==4);
    join.room_event=ORBIS_NP_MATCHING2_ROOM_EVENT_MEMBER_JOINED_A;
    Dispatch(&ctx,join);assert(callbacks==5);
    ctx.room_id=16;Dispatch(&ctx,join);assert(callbacks==5);
}
}
int main(){Libraries::Np::NpMatching2::Test();}
'''.replace('PACKET',packet).replace('FUNCTIONS','\n'.join(function(x) for x in [
    'HasMatching2Magic(', 'ShouldConnectToPeer(', 'QueueMatching2SignalingEvent(',
    'MarkMatching2PeerActive(', 'HandleMatching2HandshakePacket('])).replace('BRANCH',branch)
with tempfile.TemporaryDirectory(prefix='bbgl-rejoin-') as temp:
    path=Path(temp);(path/'fixture.cpp').write_text(cpp)
    env=dict(os.environ);env['PATH']=r'C:\msys64\clang64\bin;'+env['PATH']
    subprocess.run([r'C:\msys64\clang64\bin\clang++.exe','-std=c++23',
        '-I'+str(ROOT/'gpu/bbnet/include'),'-I'+str(ROOT/'gpu/shim'),
        '-I'+str(ROOT/'gpu/bbnet/vendor/shadps4'),'-I'+str(ROOT/'gpu/shadps4'),
        str(path/'fixture.cpp'),'-o',str(path/'fixture.exe')],env=env,check=True)
    result=subprocess.run([str(path/'fixture.exe')],env=env,capture_output=True,text=True,timeout=10)
    if baseline:
        assert result.returncode != 0 and 'failed' in result.stderr.lower(),result
        print('PASS: baseline resurrects a departed member into an already reused slot (reproduced)')
    else:
        result.check_returncode()
        print('PASS: roster identity, reused slot, delayed old room/self/member callbacks, genuine DEAD')
