"""Execute production activation code with deterministic receive/dispatch interleavings."""
from pathlib import Path
import os
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
source = (root / 'gpu/bbnet/vendor/shadps4/core/libraries/np/np_signaling/np_signaling_state.cpp').read_text()
if '--baseline' in sys.argv:
    source = subprocess.check_output(['git', 'show', 'HEAD:gpu/bbnet/vendor/shadps4/core/libraries/np/np_signaling/np_signaling_state.cpp'], cwd=root, text=True)

def function(name):
    begin = source.index('void ' + name + '(')
    brace = source.index('{', begin)
    depth, end = 1, brace + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[begin:end]

fixture = r'''
#include <cassert>
#include <cstdint>
#include <map>
#include <vector>
#include <string>
using s32=int32_t;using u32=uint32_t;using u16=uint16_t;
using OrbisNpSignalingConnectionId=s32;
#define LOG_INFO(...)
#define LOG_DEBUG(...)
#define LOG_WARNING(...)
enum class ConnState {Inactive, SendingOffer, ConnCheck, Established};
struct ConnectionInfo {ConnState state=ConnState::ConnCheck;bool dead_fired=false;
 bool is_initiator=false,timeout_callout_armed=false,revalidating=false,established_fired=false;
 int status=1;u32 addr=1;u16 port=2;};
struct PendingActivation {s32 conn_id;std::string peer_online_id;bool start_handshake;};
struct SignalingHandshake{};enum class HandshakeKind {Offer};
std::map<s32,ConnectionInfo> g_connections;
std::vector<PendingActivation> g_pending_activations;
struct SignalingMutexGuard{};
int offers=0,timeouts=0,steps=0,callbacks=0,resolve_mode=0;
constexpr int kHandshakeConnectTimeoutMs=30000,kHandshakeRetransmitMs=350;
void SetConnStateLocked(ConnectionInfo& c,ConnState s){c.state=s;c.status=s==ConnState::Established?2:1;}
void ArmTimeoutCalloutLocked(ConnectionInfo& c,int){++timeouts;c.timeout_callout_armed=true;}
void ArmStepCalloutLocked(ConnectionInfo&,int){++steps;}
SignalingHandshake MakeHandshakeLocked(ConnectionInfo&,HandshakeKind){return {};}
void SendHandshakeLocked(ConnectionInfo&,SignalingHandshake){++offers;}
void EstablishConnection(s32 id,bool){auto& c=g_connections.at(id);if(!c.established_fired){c.established_fired=true;++callbacks;}SetConnStateLocked(c,ConnState::Established);}
void SendActivationRequestLocked(ConnectionInfo&){}
u16 sceNetNtohs(u16 n){return n;}
namespace Stubs {
bool ResolvePeer(const std::string&,u32* a,u16* p){
 *a=1;*p=2;
 // The receive thread establishes (or closes) the connection while the
 // dispatcher is waiting for the server to resolve this peer.
 if(resolve_mode==1)EstablishConnection(1,false);
 if(resolve_mode==2)g_connections.at(1).state=ConnState::Inactive;
 return true;
}}
'''
fixture += function('StartHandshakeInitiator') + '\n' + function('ProcessPendingActivations')
fixture += r'''
void reset(){g_connections.clear();g_connections[1]={};g_pending_activations={{1,"peer",true}};
 offers=timeouts=steps=callbacks=resolve_mode=0;}
int main(){
 reset();resolve_mode=1;ProcessPendingActivations();
 assert(g_connections.at(1).state==ConnState::Established);
 assert(g_connections.at(1).status==2&&callbacks==1&&offers==0&&timeouts==0&&steps==0);
 // A receive can also win AFTER the dispatcher checked the state: the
 // initiator must recheck under its own lock, not trust the queued decision.
 StartHandshakeInitiator(1);assert(g_connections.at(1).status==2&&offers==0&&timeouts==0);
 reset();ProcessPendingActivations();assert(offers==1&&timeouts==1&&steps==1);
 reset();resolve_mode=2;ProcessPendingActivations();assert(offers==0&&timeouts==0);
 StartHandshakeInitiator(1);assert(offers==0);
 reset();g_connections.at(1).dead_fired=true;StartHandshakeInitiator(1);assert(offers==0);
 reset();EstablishConnection(1,false);g_connections.at(1).revalidating=true;
 ProcessPendingActivations();assert(offers==0&&g_connections.at(1).revalidating);
 reset();g_connections.clear();StartHandshakeInitiator(1);assert(offers==0);
}
'''
out = root / 'out/tests'
out.mkdir(parents=True, exist_ok=True)
cpp = out / 'signaling_activation_race.cpp'
cpp.write_text(fixture)
exe = cpp.with_suffix('.exe')
subprocess.run(['C:/msys64/clang64/bin/clang++.exe', '-std=c++20', '-O0', str(cpp), '-o', str(exe)], check=True)
env = dict(os.environ, PATH='C:/msys64/clang64/bin;' + os.environ.get('PATH', ''))
subprocess.run([str(exe)], env=env, check=True, timeout=10)
print('PASS: production activation queue/initiator: receive wins during resolution, late initiator, normal start, closed/dead/missing, revalidation')
