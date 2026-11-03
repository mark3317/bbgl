"""Run current transport source (not the previously built archive object) with diagnostics."""
from pathlib import Path
import os, subprocess, tempfile

ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='bbgl-p2p-snapshot-') as tmp:
    folder=Path(tmp);exe=folder/'test.exe'
    env=dict(os.environ,PATH='C:/msys64/clang64/bin;'+os.environ.get('PATH',''),
             BB_COOP='1',BB_NET_DIAGNOSTICS='1',BB_GPU_LOG='warning',BB_GPU_USER_DIR=str(folder/'profile'))
    # Explicit source precedes the archive: its old transport object is not used.
    subprocess.run(['C:/msys64/clang64/bin/clang++.exe','-std=c++23','-DNOMINMAX','-DWIN32_LEAN_AND_MEAN',
        '-I'+str(ROOT/'gpu/bbnet/include'),'-I'+str(ROOT/'gpu/shim'),
        '-I'+str(ROOT/'gpu/shadps4'),'-I'+str(ROOT/'gpu/bbnet/vendor/shadps4'),
        str(ROOT/'tests/test_p2p_latency_transport.cpp'),
        str(ROOT/'gpu/bbnet/vendor/shadps4/core/net/p2p_transport.cpp'),
        str(ROOT/'gpu/bbnet/vendor/shadps4/core/net/p2p_relay.cpp'),
        str(ROOT/'out/gpu/libbbnet.a'),str(ROOT/'gpu/shim/common/logging/log.cpp'),
        '-lfmt','-lssl','-lcrypto','-lws2_32','-lbcrypt','-liphlpapi','-o',str(exe)],env=env,check=True)
    for mode in ('release','diagnostic'):
        launch=dict(env, BB_NET_DIAGNOSTICS='1' if mode=='diagnostic' else '0')
        log=folder/(mode+'.log')
        with log.open('w',encoding='utf-8') as output:
            try:
                subprocess.run([str(exe)],env=launch,stdout=output,stderr=output,check=True,timeout=30)
            except (subprocess.SubprocessError, OSError):
                output.flush()
                print(log.read_text(encoding='utf-8',errors='replace')[-5000:])
                raise
        text=log.read_text(encoding='utf-8',errors='replace')
        assert ('P2P diagnostic:' in text) == (mode=='diagnostic')
        assert ('P2P sample:' in text) == (mode=='diagnostic')
        print(mode+': '+next(line for line in text.splitlines() if line.startswith('PASS:')))
print('PASS: current transport in release and diagnostic modes, real codec and flush boundary')
