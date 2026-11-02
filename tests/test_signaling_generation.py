"""Exercise production control dispatch with delayed packets from an old attempt."""
from pathlib import Path
import os
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
source = (root / 'gpu/bbnet/vendor/shadps4/core/libraries/np/np_signaling/np_signaling_state.cpp').read_text()
if '--baseline' in sys.argv:
    source = subprocess.check_output(['git', 'show', 'HEAD:gpu/bbnet/vendor/shadps4/core/libraries/np/np_signaling/np_signaling_state.cpp'], cwd=root, text=True)
begin = source.index('void HandleControlPacket(')
brace = source.index('{', begin)
depth, end = 1, brace + 1
while depth:
    depth += (source[end] == '{') - (source[end] == '}')
    end += 1
fixture = r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <map>
#include <string>
#include <string_view>
using s32=int; using u32=uint32_t; using u16=uint16_t; using u8=uint8_t;
constexpr int ORBIS_NP_ONLINEID_MAX_LENGTH=16;
constexpr int ORBIS_NP_SIGNALING_EVENT_PEER_DEACTIVATED=11;
constexpr int ORBIS_NP_SIGNALING_ERROR_TERMINATED_BY_PEER=1;
constexpr int kHandshakeConnectTimeoutMs=30000;
#define LOG_INFO(...)
enum class ControlKind:u8 {ActivationRequest=1,ActivationAck=2,Close=3,Established=4};
enum class ControlReason:u16 {Terminate=0,Deactivate=1};
enum class ConnState {Inactive,WaitOffer,Established};
struct Id { char data[17]{}; };
struct Npid {Id handle;};
struct ConnectionInfo {
 int conn_id=0,ctx_id=1; ConnState state=ConnState::Established;
 bool dead_fired=false,locally_activated=true,peer_activated=false,peer_established=false;
 bool revalidating=false,timeout_callout_armed=false;
 u32 peer_conn_id=20,addr=1; u16 port=2; Id online_id; Npid npid;
};
struct SignalingControl {u8 kind=0; u8 online_id_from[16]{},online_id_to[16]{};
 u32 from_conn_id=0,mapped_addr=0;u16 mapped_port=0,reason=0;};
struct Context {bool active=true;Id owner_online_id;};
std::map<int,ConnectionInfo> g_connections;
std::map<int,Context> g_contexts;
std::map<int,int> g_npid_to_conn;
struct SignalingMutexGuard {};
bool OnlineIdEqualsString(const Id& id,const std::string& s){return id.data==s;}
void SetNpOnlineId(Id& id,std::string_view s){std::memcpy(id.data,s.data(),16);}
int MakeCtxNpIdKey(int,const Npid&){return 1;}
int AllocateConnectionIdLocked(){return 2;}
int starts=0,establishes=0,deaths=0,deactivates=0,acks=0;
void RestartHandshakeLocked(ConnectionInfo& c,u32 peer,const char*){c.state=ConnState::WaitOffer;c.peer_conn_id=peer;}
void ArmTimeoutCalloutLocked(ConnectionInfo&,int){}
void SendEstablishedLocked(const ConnectionInfo&){}
SignalingControl MakeControlLocked(const ConnectionInfo&,ControlKind){return {};}
namespace Stubs {void ControlSendTo(const void*,int,u32,u16){++acks;}}
void StartHandshakeInitiator(int){++starts;}
void EstablishConnection(int,bool){++establishes;}
void DispatchConnectionEvent(int,int,int){++deactivates;}
void CloseConnectionAndDispatchDead(int,int){++deaths;}
'''
fixture += source[begin:end]
fixture += r'''
void reset(){g_connections.clear();g_connections[1]={};g_connections[1].conn_id=1;
 std::strcpy(g_connections[1].online_id.data,"peer");starts=establishes=deaths=deactivates=acks=0;}
SignalingControl packet(ControlKind kind,int generation,int reason=0){SignalingControl p{};
 p.kind=static_cast<u8>(kind);p.from_conn_id=generation;p.reason=reason;
 std::memcpy(p.online_id_from,"peer",4);return p;}
int main(){
 for(auto kind:{ControlKind::ActivationAck,ControlKind::Established,ControlKind::Close}){
  reset();auto p=packet(kind,19);HandleControlPacket(1,2,p);
  assert(!g_connections[1].peer_activated&&!g_connections[1].peer_established);
  assert(establishes==0&&deaths==0&&deactivates==0);
 }
 reset();auto p=packet(ControlKind::Established,20);HandleControlPacket(1,2,p);
 assert(g_connections[1].peer_established&&establishes==1);
 reset();p=packet(ControlKind::Close,20,1);HandleControlPacket(1,2,p);assert(deactivates==1);
 reset();p=packet(ControlKind::Close,20);HandleControlPacket(1,2,p);assert(deaths==1);
 reset();p=packet(ControlKind::ActivationAck,20);HandleControlPacket(1,2,p);assert(g_connections[1].peer_activated);
 // New activation is still allowed and its subsequent controls use the new generation.
 reset();p=packet(ControlKind::ActivationRequest,21);HandleControlPacket(1,2,p);
 assert(starts==1&&acks==1&&g_connections[1].peer_conn_id==21);
 p=packet(ControlKind::Close,20);HandleControlPacket(1,2,p);assert(deaths==0);
 p=packet(ControlKind::Close,21);HandleControlPacket(1,2,p);assert(deaths==1);
 reset();g_connections[1].peer_conn_id=0;
 p=packet(ControlKind::Close,19);HandleControlPacket(1,2,p);assert(deaths==0);
}
'''
out=root/'out/tests'
out.mkdir(parents=True,exist_ok=True)
cpp=out/'signaling_generation.cpp'
cpp.write_text(fixture)
exe=cpp.with_suffix('.exe')
subprocess.run(['C:/msys64/clang64/bin/clang++.exe','-std=c++20','-O0',str(cpp),'-o',str(exe)],check=True)
subprocess.run([str(exe)],env=dict(os.environ,PATH='C:/msys64/clang64/bin;'+os.environ.get('PATH','')),check=True,timeout=10)
print('PASS: stale controls ignored; current close/readiness/ack and new activation preserved')
