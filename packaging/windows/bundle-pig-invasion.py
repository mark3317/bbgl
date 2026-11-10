"""Package the optional Pig Invasion as deltas, without original game archives."""
import argparse
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    source = ROOT / 'bundled-mods/pig-invasion'
    target = args.destination / 'mods/Pig Invasion'
    manifest = json.loads((source / 'bbgl-delta.json').read_text(encoding='utf-8'))
    target.mkdir(parents=True, exist_ok=True)
    for name in ['bbgl-delta.json', 'SOURCE.txt', *(entry['patch'] for entry in manifest['files'])]:
        if Path(name).name != name:
            raise ValueError('Expected a flat bundled patch path')
        shutil.copy2(source / name, target / name)
    print(f"Pig Invasion packaged ({len(manifest['files'])} deltas; default off).")


if __name__ == '__main__':
    main()
