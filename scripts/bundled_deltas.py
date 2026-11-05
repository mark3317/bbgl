"""Materialize optional file mods from deltas and the player's own game files."""
import hashlib
import json
from pathlib import Path


def safe_path(root, relative):
    root = Path(root).resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root) or target == root:
        raise ValueError('Invalid bundled mod path')
    return target


def materialize(folder, game, destination):
    folder, destination = Path(folder), Path(destination)
    recipe = folder / 'bbgl-delta.json'
    if not recipe.is_file():
        return folder
    import bsdiff4
    from fromsoft import dcx_decompress, dcx_compress
    manifest = json.loads(recipe.read_text(encoding='utf-8'))
    if manifest.get('format') != 1:
        raise ValueError('Unsupported bundled mod format')
    for entry in manifest['files']:
        relative = entry['target']
        if not relative.startswith('dvdroot_ps4/'):
            raise ValueError('Bundled mods can only replace game assets')
        target = safe_path(destination, relative)
        base = safe_path(game, entry['base']).read_bytes()
        original = dcx_decompress(base)
        if hashlib.sha256(original).hexdigest() != entry['base_sha256']:
            raise ValueError(f'{folder.name}: original Bloodborne 1.09 file required: {entry["base"]}')
        delta = safe_path(folder, entry['patch']).read_bytes()
        result = bsdiff4.patch(original, delta)
        if hashlib.sha256(result).hexdigest() != entry['sha256']:
            raise ValueError(f'{folder.name}: damaged bundled mod: {relative}')
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + '.tmp')
        temporary.write_bytes(dcx_compress(result, base))
        temporary.replace(target)
    return destination
