"""Package the optional sword as deltas; never include original game archives."""
import argparse
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'bundled-mods/diamond-sword'


def generate(game):
    import bsdiff4
    sys.path.insert(0, str(ROOT / 'scripts'))
    from fromsoft import dcx_decompress
    source = ROOT / 'mods-src/BBSC/tools/diamond_sword'
    sys.path.insert(0, str(source))
    spec = importlib.util.spec_from_file_location('diamond_sword_build', source / 'build.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    output = ROOT / 'out/vendor/diamond-sword'
    builder.build(game / 'dvdroot_ps4', output)
    ASSETS.mkdir(parents=True, exist_ok=True)
    entries = []
    for path in sorted((output / 'dvdroot_ps4').rglob('*.dcx')):
        relative = path.relative_to(output).as_posix()
        base_name = relative.replace('wp_a_9800', 'wp_a_1030').replace('menu_knowledge_01042', 'menu_knowledge_01010')
        original = dcx_decompress((game / base_name).read_bytes())
        result = dcx_decompress(path.read_bytes())
        patch = f'{len(entries):03}.bsdiff'
        (ASSETS / patch).write_bytes(bsdiff4.diff(original, result))
        entries.append(dict(target=relative, base=base_name, patch=patch,
                            base_sha256=hashlib.sha256(original).hexdigest(),
                            sha256=hashlib.sha256(result).hexdigest()))
    (ASSETS / 'bbgl-delta.json').write_text(json.dumps(dict(format=1, price=builder.SHOP_PRICE, files=entries), indent=2) + '\n', encoding='utf-8')
    shutil.copy2(source / 'SOURCE.txt', ASSETS / 'SOURCE.txt')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--generate', type=Path, help='Build deltas from original 1.09 game (development only)')
    args = parser.parse_args()
    if args.generate:
        generate(args.generate)
    target = args.destination / 'mods/Diamond Sword'
    target.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ASSETS / 'bbgl-delta.json').read_text(encoding='utf-8'))
    for name in ['bbgl-delta.json', 'SOURCE.txt', *(entry['patch'] for entry in manifest['files'])]:
        shutil.copy2(ASSETS / name, target / name)
    print('Diamond Sword packaged (default off, price 10000).')


if __name__ == '__main__':
    main()
