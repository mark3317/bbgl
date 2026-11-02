"""Exercise production readiness/keepalive code with deterministic UDP loss."""
from pathlib import Path
import os
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
path = 'gpu/bbnet/vendor/shadps4/core/libraries/np/np_signaling/np_signaling_state.cpp'
source = (root / path).read_text()
if '--baseline' in sys.argv:
    source = subprocess.check_output(['git', 'show', 'HEAD:' + path], cwd=root, text=True)

def function(name):
    match = re.search(r'(?:static )?void (?:PS4_SYSV_ABI )?' + name + r'\([^;]*?\)\s*\{', source)
    assert match, name
    end = source.index('{', match.start()) + 1
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[match.start():end]

fixture = r'''
#include <cassert>
#include <cstdint>
#include <map>
#include <vector>
using s32=int32_t; using s64=int64_t; using u32=uint32_t;
using u64=uint64_t; using u16=uint16_t;
#define PS4_SYSV_ABI
#define LOG_INFO(...)
#define BBSC_TIMELINE(...)
enum class ConnState {Inactive,SendingOffer,WaitAccept,SendingAccept,WaitOffer,ConnCheck,Established};
enum class ControlKind {Established};
enum class HandshakeKind {Offer,Accept,Check};
struct SignalingControl {int sender;};
struct SignalingHandshake {u64 nonce=0;};
struct ConnectionInfo {
 int conn_id=0; ConnState state=ConnState::ConnCheck; int status=1;
 bool peer_activated=false,established_fired=false,locally_activated=true;
 bool peer_activated_fired=false,established_event_fired=false,peer_established=false;
 bool mutual_fired=false,dead_fired=false,deactivate_lingering=false,revalidating=false;
 bool step_callout_armed=false; s64 revalidate_since_us=0,last_peer_rx_us=0;
 u32 addr=1; u16 port=2;
};
struct SignalingMutexGuard {};
std::map<int,ConnectionInfo> g_connections;
std::vector<int> ready;
int established[3]{},mutual[3]{},probes=0,deaths=0; s64 now=1,armed_delay=0;
constexpr int ORBIS_NP_SIGNALING_CONN_STATUS_ACTIVE=2;
constexpr int ORBIS_NP_SIGNALING_EVENT_ESTABLISHED=1,ORBIS_NP_SIGNALING_EVENT_MUTUAL_ACTIVATED=12;
constexpr int ORBIS_NP_SIGNALING_ERROR_TIMEOUT=5;
s64 NowUs(){return now;}
u16 sceNetNtohs(u16 p){return p;}
int OnlineIdToString(...){return 0;}
void CancelTimeoutCalloutLocked(ConnectionInfo&){}
void ArmStepCalloutLocked(ConnectionInfo&,s64 delay){armed_delay=delay;}
void DispatchPeerActivatedEvent(int){}
void DispatchConnectionEvent(int id,int type,int){if(type==1)++established[id];else ++mutual[id];}
void CloseConnectionAndDispatchDead(int id,int){++deaths;g_connections.at(id).dead_fired=true;}
SignalingHandshake MakeHandshakeLocked(const ConnectionInfo&,HandshakeKind){return {};}
void SendHandshakeLocked(const ConnectionInfo&,const SignalingHandshake&){++probes;}
SignalingControl MakeControlLocked(const ConnectionInfo& ci,ControlKind){return {ci.conn_id};}
namespace Stubs {int ControlSendTo(const void* p,int,u32,u16){ready.push_back(static_cast<const SignalingControl*>(p)->sender);return 0;}}
namespace fmt {template<typename... T> int format(T...){return 0;}}
namespace Core::Bloodborne {template<typename... T> void BbscTimelineEvent(T...) {}}
'''
# Logging discards online_id accesses in production LOG_INFO macros.
for name in ('kHandshakeRetransmitMs', 'kKeepaliveIntervalMs', 'kEstablishedLivenessTimeoutMs'):
    fixture += re.search(r'constexpr s64 ' + name + r' = [^;]+;', source)[0] + '\n'
fixture += (function('SendEstablishedLocked') if 'void SendEstablishedLocked(' in source
            else 'static void SendEstablishedLocked(const ConnectionInfo&) {}') + '\n'
fixture += function('EstablishConnection') + '\n' + function('StepCalloutHandler')
fixture += r'''
void deliver(int sender){int receiver=3-sender;g_connections.at(receiver).peer_established=true;EstablishConnection(receiver,false);}
int main(){
 for(int id:{1,2}){g_connections[id].conn_id=id;EstablishConnection(id,false);}
 // Drop peer 2's initial readiness. Peer 2 receives ours and believes both ready;
 // peer 1 must still recover without a new connection, HTTP sign or room join.
 assert(ready.size()==2);ready.clear();deliver(1);
 assert(mutual[1]==0&&mutual[2]==1);
 now+=5'000'000;StepCalloutHandler(2);
 assert(!ready.empty());for(int sender:ready)deliver(sender);ready.clear();
 assert(mutual[1]==1&&mutual[2]==1);
 // Retries repair loss without repeating game callbacks or echoing readiness.
 StepCalloutHandler(2);assert(ready.size()==1);deliver(2);ready.clear();
 assert(ready.empty()&&established[1]==1&&established[2]==1&&mutual[1]==1);
 // Suppress readiness on closed, lingering and revalidating connections.
 auto& ci=g_connections.at(2);
 ci.deactivate_lingering=true;SendEstablishedLocked(ci);assert(ready.empty());
 ci.deactivate_lingering=false;ci.revalidating=true;SendEstablishedLocked(ci);assert(ready.empty());
 ci.revalidating=false;ci.dead_fired=true;SendEstablishedLocked(ci);assert(ready.empty());ci.dead_fired=false;
 // One missed probe must leave several further opportunities before the same
 // 60s deadline; real absence still closes rather than faking readiness.
 assert(kKeepaliveIntervalMs<=kEstablishedLivenessTimeoutMs/3);
 for(int i=0;i<3;++i){now+=kKeepaliveIntervalMs*1000;StepCalloutHandler(2);assert(deaths==0);}
 ci.last_peer_rx_us=now;now+=kEstablishedLivenessTimeoutMs*1000;
 StepCalloutHandler(2);assert(deaths==1);
}
'''
out = root / 'out/tests'
out.mkdir(parents=True, exist_ok=True)
cpp = out / 'signaling_readiness_loss.cpp'
cpp.write_text(fixture)
exe = cpp.with_suffix('.exe')
subprocess.run(['C:/msys64/clang64/bin/clang++.exe', '-std=c++20', '-O0', str(cpp), '-o', str(exe)], check=True)
env = dict(os.environ, PATH='C:/msys64/clang64/bin;' + os.environ.get('PATH', ''))
subprocess.run([str(exe)], env=env, check=True, timeout=10)
print('PASS: lost readiness repaired, callbacks once, no echo, close/revalidation guards, lost probes and true timeout')
