"""Assemble a self-contained client and server from the pinned fork and vendor tools.

Only shadNet runtime/account dependencies are taken from the checksum-pinned archive.
The BBSC mod and game server are built from mods-src/BBSC, never from that archive.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
FORK = ROOT / 'mods-src/BBSC'
VENDORS = {
    'BBport': '001efc0a03b47bd6b2660c598fd6d172d2aaae3201a4982134d1f215918acd3c',
}


def vendor(kind):
    name = f'BBSC-0.0.2-{kind}.zip'
    path = ROOT / 'out/vendor' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        temporary = path.with_suffix('.part')
        urllib.request.urlretrieve(f'https://github.com/CLSAMG22/BBSC/releases/download/v0.0.2/{name}', temporary)
        temporary.replace(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != VENDORS[kind]:
        raise RuntimeError(f'Vendor checksum mismatch: {name}')
    return zipfile.ZipFile(path)


def extract_vendor(kind, prefix, destination, allowed):
    with vendor(kind) as archive:
        base = f'BBSC-0.0.2-{kind}/{prefix}/'
        for name in archive.namelist():
            relative = name.removeprefix(base)
            if not name.startswith(base) or not allowed(relative):
                continue
            if '..' in Path(relative).parts or Path(relative).is_absolute():
                raise RuntimeError('Unsafe vendor path')
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(name))


def main():
    dest = ROOT / 'out/stage/Bloodborne Game Launcher/coop'
    client = dest / 'client'
    (client / 'bbsc').mkdir(parents=True, exist_ok=True)
    for name in ('bbsc.dll', 'bbsc-launch.exe', 'mod.json'):
        shutil.copy2(FORK / 'build/mod' / name, client / 'bbsc' / name)
    runtime = dest / 'party'
    runtime.mkdir(parents=True, exist_ok=True)
    for name in ('engine.py', 'compat.py', 'party_workers.py', 'protobuf.py', 'schema.json', 'ss_info_template.xml', 'run_log.py'):
        shutil.copy2(FORK / 'party' / name, runtime / name)
    revision = subprocess.check_output(['git', '-C', str(FORK), 'rev-parse', 'HEAD'], text=True).strip()
    version = json.loads((FORK / 'emulator/mod/mod.json').read_text(encoding='utf-8'))['version']
    (client / 'bundle.json').write_text(json.dumps({'version': version, 'transport': 'p2p',
        'source': f'https://github.com/mark3317/bbsc-gl/tree/{revision}', 'files': {}}), encoding='utf-8')
    licenses = dest.parent / 'licenses'
    shutil.copy2(FORK / 'LICENSE', licenses / 'BBSC-LICENSE.txt')
    shutil.copy2(FORK / 'server/gameserver/LICENSE.NoDreamForHunter', licenses / 'NoDreamForHunter-LICENSE.txt')
    (dest / 'SOURCE.json').write_text(json.dumps({'bbsc_commit': revision, 'version': version,
                                               'transport': 'p2p'}, indent=2) + '\n')


if __name__ == '__main__':
    main()
