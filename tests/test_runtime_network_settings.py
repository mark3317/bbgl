"""Run production bridge settings installation before the first native P2P use."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'gpu/bbnet/bbnet_glue.cpp').read_text(encoding='utf-8')
body = source[source.index('void InstallRuntimeNetworkSettings()'):source.index('extern "C" void bbnet_initialize')]
register = source[source.index('extern "C" void bbnet_register') :]
assert register.index('InstallRuntimeNetworkSettings();') < register.index('Libraries::Net::RegisterLib(sym);')
fixture = r'''
#include <cassert>
#include <functional>
#include <utility>
#include "core/emulator_settings.h"
using u16 = unsigned short;
namespace Libraries::Net {
struct Hooks { std::function<bool()> is_online; std::function<u16()> p2p_port;
    std::function<void(u16)> p2p_started; } hooks;
Hooks GetSystemHooks() { return hooks; }
void SetSystemHooks(Hooks value) { hooks = std::move(value); }
}
BODY
int main() {
    using namespace Libraries::Net;
    bool preserved=false;
    hooks.p2p_started=[&](u16){preserved=true;};
    assert(!hooks.p2p_port); // the former bridge always fell back to 3658 here
    InstallRuntimeNetworkSettings();
    for (const auto* value : {"3658", "3659", "3660", "0", "65535"}) {
        _putenv_s("BB_P2P_PORT", value);
        assert(hooks.p2p_port()==std::atoi(value));
    }
    for (const auto* value : {"-1", "65536"}) {
        _putenv_s("BB_P2P_PORT", value); assert(hooks.p2p_port()==3658);
    }
    _putenv_s("BB_P2P_PORT", ""); assert(hooks.p2p_port()==3658);
    _putenv_s("BB_ONLINE", "1"); assert(hooks.is_online());
    _putenv_s("BB_ONLINE", "0"); assert(!hooks.is_online());
    hooks.p2p_started(3660); assert(preserved);
}
'''.replace('BODY', body)
with tempfile.TemporaryDirectory(prefix='bbnet-settings-') as tmp:
    cpp, exe = Path(tmp)/'test.cpp', Path(tmp)/'test.exe'
    cpp.write_text(fixture, encoding='utf-8')
    subprocess.run([r'C:\msys64\clang64\bin\clang++.exe', '-std=c++23',
        '-I'+str(ROOT/'gpu/bbnet/include'), str(cpp), '-o', str(exe)], check=True)
    env = dict(os.environ)
    env['PATH'] = r'C:\msys64\clang64\bin;' + env['PATH']
    subprocess.run([str(exe)], env=env, check=True, timeout=10)
print('PASS: production native bridge port/online hooks, registration order, overrides and existing hooks')
