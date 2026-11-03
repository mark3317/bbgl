"""Assemble the bundled BBSC client and in-process Party runtime from mods-src/BBSC."""
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
FORK = ROOT / 'mods-src/BBSC'
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
