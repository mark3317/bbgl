"""Build independent ZIP release assets; never modifies the source game folder."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
from bbport_game_download import safe_name


def package(source, output, base_url, limit=1900 * 1024 * 1024):
    source, output = Path(source).resolve(), Path(output).resolve()
    if source == output or source in output.parents:
        raise ValueError('Output must be outside the game folder')
    if not (source / 'eboot.bin').is_file():
        raise ValueError('Choose the game folder containing eboot.bin')
    files = sorted(p for p in source.rglob('*') if p.is_file())
    groups, group, size = [], [], 0
    for file in files:
        name = file.relative_to(source).as_posix()
        safe_name(name)
        if file.is_symlink() or any(p.is_symlink() for p in file.parents):
            raise ValueError(f'Symbolic link: {file}')
        # DEFLATE can slightly expand incompressible files. Reserve overhead per file.
        cost = file.stat().st_size * 1.002 + 65536
        if cost >= limit:
            raise ValueError(f'File too large for an independent ZIP: {file}')
        if group and size + cost >= limit:
            groups.append(group)
            group, size = [], 0
        group.append(file)
        size += cost
    if group:
        groups.append(group)
    output.mkdir(parents=True, exist_ok=False)
    parts = []
    for index, group in enumerate(groups, 1):
        archive = output / f'game-{index:03d}.zip'
        print(f'Packing {archive.name} ({index}/{len(groups)})', flush=True)
        with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=1) as target:
            for file in group:
                target.write(file, file.relative_to(source).as_posix())
        if archive.stat().st_size >= 2**31:
            raise ValueError(f'ZIP exceeds GitHub limit: {archive}')
        with archive.open('rb') as handle:
            digest = hashlib.file_digest(handle, 'sha256').hexdigest()
        parts.append(dict(name=archive.name, size=archive.stat().st_size,
                          unpacked_size=sum(f.stat().st_size for f in group), sha256=digest,
                          url=base_url.rstrip('/') + '/' + archive.name))
    manifest = dict(format=1, file_count=len(files), parts=parts)
    (output / 'game-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(f'Ready: {len(files)} files, {len(parts)} ZIP assets', flush=True)
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path, help='New output directory')
    parser.add_argument('--base-url', default='https://github.com/mark3317/bbgl/releases/download/game-1.09')
    args = parser.parse_args()
    package(args.source, args.output, args.base_url)
