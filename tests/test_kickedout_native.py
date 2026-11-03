"""Production KICKEDOUT translation against Bloodborne's native presence guard."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT/'gpu/bbnet/vendor/shadps4/core/libraries/np/np_matching2/np_matching2_mm.cpp').read_text(encoding='utf-8')
helper = source[source.index('OrbisNpMatching2RoomUpdate BuildKickedOutUpdate('):source.index('void HandleRoomEvent(')]
branch = source[source.index('    case ORBIS_NP_MATCHING2_ROOM_EVENT_KICKEDOUT:'):source.index('    case ORBIS_NP_MATCHING2_ROOM_EVENT_UPDATED_ROOM_DATA_INTERNAL:')]
assert 'p.room_event_data = p.room_update.get();' in branch
assert 'ev.request_payload_owner = std::move(payload_owner);' in source
code = r'''
#include <windows.h>
#include <cassert>
#include <cstddef>
#include <cstring>
#include <memory>
#include "core/libraries/np/np_types2.h"
using namespace Libraries::Np::NpMatching2;
#define LOG_WARNING(...)
#define LOG_INFO(...)
HELPER
struct Context { unsigned long long room_id=10; int callbacks=0; } contexts[3];
struct Owner { std::unique_ptr<OrbisNpMatching2RoomUpdate> room_update; void* room_event_data=nullptr; };
std::shared_ptr<Owner> queued;
void dispatch(unsigned target, unsigned long long room_id, OrbisNpMatching2EventCause cause, int status) {
    auto* ctx=&contexts[target];
    struct { unsigned ctx_id; int error_code; unsigned event_cause; } n{target,status,cause};
    auto owner=std::make_shared<Owner>(); auto& p=*owner;
    switch (ORBIS_NP_MATCHING2_ROOM_EVENT_KICKEDOUT) { BRANCH }
    ++ctx->callbacks; queued=owner;
}
int main() {
    static_assert(offsetof(OrbisNpMatching2RoomUpdate,optData)==8);
    static_assert(offsetof(OrbisNpMatching2RoomUpdate,optData)+offsetof(OrbisNpMatching2PresenceOptionData,len)==0x18);
    // Native CC4204: TEST RSI,RSI; CC4209: CMP QWORD [RSI+18],4;
    // native reads the kick reason at +8 only after that guard succeeds.
    const unsigned char code[]={0x48,0x89,0xfe,0x48,0x85,0xf6,0x74,0x0c,
        0x48,0x83,0x7e,0x18,4,0x75,5,0x8b,0x46,8,0xc3,0x90,0x31,0xc0,0xc3};
    auto* fn=VirtualAlloc(nullptr,4096,MEM_RESERVE|MEM_COMMIT,PAGE_EXECUTE_READWRITE);
    assert(fn); std::memcpy(fn,code,sizeof(code));
    using Native=unsigned PS4_SYSV_ABI (*)(const void*);
    auto read=reinterpret_cast<Native>(fn);
    const auto cause=ORBIS_NP_MATCHING2_EVENT_CAUSE_KICKOUT_ACTION;
    constexpr auto status=static_cast<int>(0xff000019u);
    OrbisNpMatching2RoomUpdate old{}; old.eventCause=cause; old.errorCode=status;
    assert(read(&old)==0 && read(nullptr)==0); // reproduced ignored old notification
    dispatch(2,10,cause,status);
    assert(contexts[2].callbacks==1 && contexts[0].callbacks==0 && contexts[1].callbacks==0);
    assert(queued->room_event_data==queued->room_update.get());
    assert(read(queued->room_event_data)==0xff000019u); // owner outlives dispatch
    dispatch(2,9,cause,status); assert(contexts[2].callbacks==1); // stale room ignored
    for (auto other : {0, -1, static_cast<int>(0xff000022u)}) {
        auto u=BuildKickedOutUpdate(cause,other);
        assert(u.errorCode==other && u.optData.len==0 && read(&u)==0);
    }
    auto u=BuildKickedOutUpdate(ORBIS_NP_MATCHING2_EVENT_CAUSE_LEAVE_ACTION,status);
    assert(u.optData.len==0 && read(&u)==0);
    u=BuildKickedOutUpdate(cause,status); u.optData.len=3; assert(read(&u)==0);
    VirtualFree(fn,0,MEM_RELEASE);
}
'''.replace('HELPER',helper).replace('BRANCH',branch)
with tempfile.TemporaryDirectory(prefix='bbnet-kick-') as tmp:
    cpp,exe=Path(tmp)/'test.cpp',Path(tmp)/'test.exe'
    cpp.write_text(code,encoding='utf-8')
    subprocess.run([r'C:\msys64\clang64\bin\clang++.exe','-std=c++23','-DNOMINMAX','-DWIN32_LEAN_AND_MEAN',
        '-I'+str(ROOT/'gpu/bbnet/include'),'-I'+str(ROOT/'gpu/shim'),
        '-I'+str(ROOT/'gpu/bbnet/vendor/shadps4'),'-I'+str(ROOT/'gpu/shadps4'),
        str(cpp),'-o',str(exe)],check=True)
    env=dict(os.environ);env['PATH']=r'C:\msys64\clang64\bin;'+env['PATH']
    subprocess.run([str(exe)],check=True,env=env,timeout=10)
print('PASS: ignored old KICKEDOUT reproduced; native presence guard, targeted/stale events and callback lifetime')
