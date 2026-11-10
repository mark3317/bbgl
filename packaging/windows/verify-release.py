"""Fail packaging when runtime dependencies, bundled mods or release hygiene are wrong."""
import hashlib
import json
from pathlib import Path
import sys


def verify(root):
    root = Path(root).resolve(strict=True)
    for name in ('Bloodborne.exe', 'bin/Play Bloodborne.exe', 'bin/bb-probe.exe', 'run.py', 'README.ru.md', 'THIRD_PARTY.md',
                 'coop/client/bbsc/bbsc.dll', 'coop/client/bbsc/bbsc-launch.exe',
                 'coop/party/engine.py', 'coop/party/dynamic.py', 'coop/party/compat.py',
                 'coop/party/chalices.py', 'coop/party/retirement.py', 'coop/party/dream_hints.py',
                 'coop/SOURCE.json', 'launcher/assets/button-prompts/manifest.json',
                 'licenses/BBSC-LICENSE.txt', 'mods/Diamond Sword/bbgl-delta.json',
                 'mods/Diamond Sword/SOURCE.txt', 'mods/Pig Invasion/bbgl-delta.json',
                 'mods/Pig Invasion/SOURCE.txt'):
        if not (root / name).is_file():
            raise ValueError(f'Missing release file: {name}')
    if sorted(p.name for p in root.glob('*.exe')) != ['Bloodborne.exe']:
        raise ValueError('Only the launcher EXE may be in the package root')
    for retired in ('coop/server', 'coop/client/account'):
        if (root / retired).exists():
            raise ValueError(f'Retired server payload in P2P release: {retired}')
    source = json.loads((root / 'coop/SOURCE.json').read_text(encoding='utf-8'))
    mod = json.loads((root / 'coop/client/bbsc/mod.json').read_text(encoding='utf-8'))
    if source['version'] != mod['version'] or source.get('transport') != 'p2p':
        raise ValueError('Inconsistent bundled mod version or transport')
    for kind in ('client',):
        folder = root / 'coop' / kind
        manifest = json.loads((folder / 'bundle.json').read_text(encoding='utf-8'))
        for name, expected in manifest['files'].items():
            if hashlib.sha256((folder / name).read_bytes()).hexdigest() != expected:
                raise ValueError(f'Bundle checksum mismatch: {kind}/{name}')
    for name in ('Diamond Sword', 'Pig Invasion'):
        folder = root / 'mods' / name
        delta = json.loads((folder / 'bbgl-delta.json').read_text(encoding='utf-8'))
        for entry in delta['files']:
            if not (folder / entry['patch']).is_file():
                raise ValueError(f'Missing delta: {name}/{entry["patch"]}')
    prompts = root / 'launcher/assets/button-prompts'
    ready = json.loads((prompts / 'manifest.json').read_text(encoding='utf-8'))['files']
    for name, digest in ready.items():
        if hashlib.sha256((prompts / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Damaged ready-made prompt mod')
    allowed_archives = {'launcher/assets/button-prompts/' + name for name in ready if name.endswith('.dcx')}
    if 'coopSetup()' in (root / 'launcher/qml/SettingsWorkspace.qml').read_text(encoding='utf-8'):
        raise ValueError('Obsolete BBSC preparation button in release')
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        name = path.name.lower()
        parts = {p.lower() for p in path.relative_to(root).parts}
        if (name in ('settings.json', 'account.dat', 'eboot.bin', 'param.sfo', 'coop-server.json',
                     'bbport.ini', 'mods.json', 'patches.json', 'online-data.json')
                or (name.endswith(('.dcx', '.tpf', '.bdt', '.bhd', '.dmp', '.log', '.bak', '.pyc'))
                    and path.relative_to(root).as_posix() not in allowed_archives)
                or parts & {'savedata', 'captures', 'own-world', 'bell-pending', 'guest-items',
                            'shared-progress', 'discord rich presence', 'atlas', '__pycache__'}):
            raise ValueError(f'Unexpected release file: {path.relative_to(root)}')
    print('Release payload and hygiene: PASS')


if __name__ == '__main__':
    verify(sys.argv[1])
