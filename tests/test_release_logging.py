"""Compile actual GPU/DLL sinks and verify release filtering and unified output."""
from pathlib import Path
import ast, os, subprocess, tempfile, sys
ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mods-src/BBSC'

def function(source, signature):
    start = source.index(signature + ' {'); end = source.index('{', start) + 1; depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}'); end += 1
    return source[start:end]

native = r'''
#include <cassert>
#include <cstdlib>
#include "common/logging/log.h"
extern int ModProbe(bool);
int main() {
    const bool diagnostic = Common::Log::DiagnosticsEnabled();
    const char* net = std::getenv("BB_NET_DIAGNOSTICS");
    const bool network = net ? std::string_view(net) == "1" : diagnostic;
    assert(Common::Log::CoopDiagnosticsEnabled() == network);
    int evaluated = 0;
    LOG_DEBUG(Lib_Net, "gpu diagnostic {}", ++evaluated);
    assert(evaluated == (diagnostic ? 1 : 0));
    LOG_ERROR(Lib_Net, "gpu error survives");
    assert(ModProbe(diagnostic) == (diagnostic ? 3 : 0));
}
'''
source = (MOD/'emulator/mod/bbsc_mod.cpp').read_text(encoding='utf-8')
core = (MOD/'emulator/src/core/bloodborne_re.cpp').read_text(encoding='utf-8')
mod = r'''
#include <windows.h>
#include <cstdio>
#include <mutex>
#include <cassert>
#include <string_view>
#include "common/logging/log.h"
std::mutex log_mutex;
FILE* log_file = stderr;
namespace BbscMod {
''' + function(source, 'void LogLine(char level, const char* category, const std::string& text)') + r'''
}
''' + function(core, 'bool BbscPerfEnabled()') + '\n' + function(core, 'bool BbscTimelineEnabled()') + r'''
int ModProbe(bool diagnostic) {
    assert(BbscMod::DiagnosticsEnabled() == diagnostic);
    assert(BbscPerfEnabled() == diagnostic);
    assert(BbscTimelineEnabled() == diagnostic);
    int evaluated = 0;
    LOG_TRACE(Mod, "mod trace {}", ++evaluated);
    LOG_INFO(Mod, "mod diagnostic {}", ++evaluated);
    LOG_WARNING(Mod, "mod warning {}", ++evaluated);
    LOG_ERROR(Mod, "mod error survives");
    return evaluated;
}
'''
with tempfile.TemporaryDirectory(prefix='bbgl-release-log-') as tmp:
    folder=Path(tmp); gpu=folder/'gpu.cpp'; dll=folder/'mod.cpp'; obj=folder/'mod.o'; exe=folder/'test.exe'
    gpu.write_text(native, encoding='utf-8'); dll.write_text(mod, encoding='utf-8')
    env=dict(os.environ, PATH='C:/msys64/clang64/bin;'+os.environ.get('PATH',''))
    for key in tuple(env):
        if key.startswith(('BB_GPU_LOG','BB_DIAGNOSTICS','BB_NET_DIAGNOSTICS','BBSC_LOG','SHADPS4_BBSC_PERF','SHADPS4_BBSC_TIMELINE')):env.pop(key)
    cc='C:/msys64/clang64/bin/clang++.exe'
    subprocess.run([cc,'-std=c++23','-O2','-I'+str(MOD/'emulator/mod/shim'),'-c',str(dll),'-o',str(obj)],env=env,check=True)
    subprocess.run([cc,'-std=c++23','-O2','-I'+str(ROOT/'gpu/shim'),'-I'+str(ROOT/'gpu/shadps4'),str(gpu),str(obj),str(ROOT/'gpu/shim/common/logging/log.cpp'),'-lfmt','-o',str(exe)],env=env,check=True)
    for mode in ('release','diagnostic','network'):
        launch=dict(env,BB_COOP='1',BB_USER_DIR=str(folder),BB_DIAGNOSTICS='1' if mode=='diagnostic' else '0')
        if mode=='network':launch['BB_NET_DIAGNOSTICS']='1'
        result=subprocess.run([str(exe)],env=launch,check=True,capture_output=True,text=True,timeout=10)
        assert 'gpu error survives' in result.stderr and 'mod error survives' in result.stderr
        assert ('mod diagnostic' in result.stderr) == (mode=='diagnostic')
        assert ('gpu diagnostic' in result.stderr) == (mode=='diagnostic')
        assert not list(folder.rglob('bbnet-*.log')) and not list(folder.rglob('bbsc-mod-*.log'))
    sys.path.insert(0,str(ROOT/'launcher')); sys.path.insert(0,str(ROOT/'scripts'))
    import bbport_launcher_win as launcher
    from unittest.mock import patch
    settings=launcher.app_settings({})
    with patch.dict(os.environ,{},clear=True):
        assert launcher.game_environment(settings)['BB_DIAGNOSTICS']=='0'
        assert not settings['gpu_logs']
        assert launcher.game_environment(settings)['BB_GPU_LOG']=='error'
        settings['gpu_logs']=True
        gpu_only=launcher.game_environment(settings)
        assert gpu_only['BB_GPU_LOG']=='debug' and gpu_only['BB_DIAGNOSTICS']=='0'
        settings['gpu_logs']=False
        settings['diagnostic_logs']=True
        compact = launcher.game_environment(settings)
        assert compact['BB_DIAGNOSTICS']=='1'
        assert compact['BB_GPU_LOG']=='error' and compact['BBSC_LOG']=='warning'
        for key in ('BB_NET_DIAGNOSTICS', 'BB_PARTY_DIAGNOSTICS', 'BB_PERF_CAPTURE', 'SHADPS4_BBSC_PERF'):
            assert compact[key]=='0'
        settings['gpu_logs']=True
        assert launcher.game_environment(settings)['BB_GPU_LOG']=='debug'
        settings['gpu_logs']=False
        settings['extra_env']='BB_GPU_LOG=debug BB_NET_DIAGNOSTICS=1'
        custom = launcher.game_environment(settings)
        assert custom['BB_GPU_LOG']=='debug' and custom['BB_NET_DIAGNOSTICS']=='1'
        settings['extra_env']='BB_DIAGNOSTICS=0'
        assert launcher.game_environment(settings)['BB_DIAGNOSTICS']=='0'
    with patch.dict(os.environ,{'BB_GPU_LOG':'trace'},clear=True):
        assert launcher.game_environment(settings)['BB_GPU_LOG']=='trace'
    # Validate the Qt settings model without requiring a GUI runtime.
    tree=ast.parse((ROOT/'launcher/bbport_launcher_backend.py').read_text(encoding='utf-8'))
    rows=[node for node in ast.walk(tree) if isinstance(node,ast.Call)
          and isinstance(node.func,ast.Name) and node.func.id=='row' and node.args
          and isinstance(node.args[0],ast.Constant) and node.args[0].value=='diagnostic_logs']
    assert len(rows)==1 and rows[0].args[2].value=='toggle'
    sections=next(node.value for node in tree.body if isinstance(node,ast.Assign)
                  and any(isinstance(t,ast.Name) and t.id=='SETTINGS_SECTIONS' for t in node.targets))
    groups=eval(compile(ast.Expression(sections),'settings-sections','eval'),{'core':launcher})
    assert sum(keys.count('diagnostic_logs') for _,keys in groups['System'])==1
    assert sum(keys.count('gpu_logs') for _,keys in groups['System'])==1
print('PASS: release skips formatting and profiling; explicit diagnosis, GPU/DLL stderr and launcher switch')
