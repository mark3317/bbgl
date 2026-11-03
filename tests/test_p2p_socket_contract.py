"""Run production recv adapter + production transport, without loading the game runtime."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT/'gpu/bbnet/vendor/shadps4/core/libraries/net/net.cpp').read_text()
baseline = '--baseline' in sys.argv
if baseline:
    source = subprocess.check_output(['git', '-C', str(ROOT), 'show',
        'HEAD:gpu/bbnet/vendor/shadps4/core/libraries/net/net.cpp'], text=True)
adapter = source[source.index('static s32 sceNetRecvfromImpl('):source.index('s32 PS4_SYSV_ABI sceNetRecvfrom(', source.index('static s32 sceNetRecvfromImpl('))]
prelude = r'''
#include "core/libraries/net/net.h"
#include "core/libraries/net/net_error.h"
#include "core/libraries/net/net_translate.h"
#include "core/libraries/net/net_flag_watch.h"
#include "core/net/guest_net.h"
namespace Libraries::Net {
using Host::Error;
constexpr u64 MaxPeekLen=512*1024;
s32 SetErrno(int e) { return static_cast<s32>(ORBIS_NET_ERROR_BASE | e); }
s32 Return(const Core::Net::NetResult& r) {
    return r.error==Error::Ok ? static_cast<s32>(r.value) : SetErrno(ToOrbisErrno(r.error));
}
P2PKind KindOf(const Core::Net::SocketInfo& info) {
    return info.type==SOCK_STREAM ? P2PKind::Stream : P2PKind::Datagram;
}
ADAPTER
s32 PS4_SYSV_ABI sceNetRecvfrom(OrbisNetId s,void* b,u64 n,s32 f,OrbisNetSockaddr* a,u32* l) {
    return sceNetRecvfromImpl(s,b,n,f,a,l);
}
}
'''.replace('ADAPTER', adapter)
with tempfile.TemporaryDirectory(prefix='bbgl-p2p-contract-') as temporary:
    cpp, exe = Path(temporary)/'contract.cpp', Path(temporary)/'contract.exe'
    cpp.write_text(prelude + (ROOT/'tests/test_p2p_socket_contract.cpp').read_text())
    env = dict(os.environ)
    env['PATH'] = r'C:\msys64\clang64\bin;' + env['PATH']
    subprocess.run([r'C:\msys64\clang64\bin\clang++.exe','-std=c++23',
        '-I'+str(ROOT/'gpu/bbnet/include'), '-I'+str(ROOT/'gpu/shim'),
        '-I'+str(ROOT/'gpu/shadps4'), '-I'+str(ROOT/'gpu/bbnet/vendor/shadps4'),
        str(cpp), str(ROOT/'out/gpu/libbbnet.a'), str(ROOT/'gpu/shim/common/logging/log.cpp'),
        '-lfmt','-lssl','-lcrypto','-lws2_32','-lbcrypt','-liphlpapi','-o',str(exe)],env=env,check=True)
    result = subprocess.run([str(exe)],env=env,capture_output=baseline,text=True,timeout=10)
    if baseline:
        assert result.returncode != 0 and 'failed' in result.stderr.lower(), result
        print('PASS: pre-fix production adapter reproduces the PEEKLEN contract failure')
    else:
        result.check_returncode()
