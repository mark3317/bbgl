"""Built-in button images, independent of user mods and their master switch."""
import json
from pathlib import Path
import struct

COMMON = 'dvdroot_ps4/menu/common.tpf.dcx'


def _textures(data):
    """PS4 TPF entry headers and payloads; names keep their original offsets."""
    if data[:4] != b'TPF\0' or data[12:15] != bytes((4, 3, 1)):
        raise ValueError('Unsupported button texture archive')
    result = {}
    for index in range(struct.unpack_from('<I', data, 8)[0]):
        at = 16 + 36 * index
        offset, size = struct.unpack_from('<II', data, at)
        name_at = struct.unpack_from('<I', data, at + 24)[0]
        end = name_at
        while end + 2 <= len(data) and data[end:end + 2] != b'\0\0':
            end += 2
        name = data[name_at:end].decode('utf-16-le')
        if offset + size > len(data):
            raise ValueError('Truncated button texture archive')
        result[name] = (at, data[offset:offset + size])
    return result


def merge_textures(winner, selected):
    """Replace only input glyphs, preserving all other textures from the winning mod."""
    from fromsoft import dcx_decompress, dcx_compress
    base, icons = dcx_decompress(winner), dcx_decompress(selected)
    targets, sources = _textures(base), _textures(icons)
    required = {name for name in sources if name.startswith('KG_') or name == 'MENU_Common_00091'}
    if required - targets.keys():
        raise ValueError('Mod interface archive is missing button textures')
    start = min(struct.unpack_from('<I', base, at)[0] for at, _ in targets.values())
    output = bytearray(base[:start])
    for name, (at, payload) in targets.items():
        if name in required:
            source_at, payload = sources[name]
            output[at + 8:at + 24] = icons[source_at + 8:source_at + 24]
            output[at + 32:at + 36] = icons[source_at + 32:source_at + 36]
        output.extend(b'\0' * (-len(output) % 16))
        offset = len(output)
        output.extend(payload)
        struct.pack_into('<II', output, at, offset, len(payload))
    struct.pack_into('<I', output, 4, len(output) - start)
    return dcx_compress(output, winner)


def apply(layers, game, selected, out):
    """Run after all generated/user layers, so mod count and order cannot override buttons."""
    from mods import mod_files
    winner = Path(game) / COMMON
    for _, folder in layers:
        for relative, source in mod_files(folder):
            if relative.as_posix().casefold() == COMMON:
                winner = source
    selected = Path(selected)
    if winner.resolve() == selected.resolve():
        return layers
    folder = Path(out) / 'button-prompts'
    target = folder / COMMON
    stamp_file = folder / 'sources.json'
    stamp = [[str(p.resolve()), p.stat().st_size, p.stat().st_mtime_ns]
             for p in (winner, selected)]
    try:
        cached = json.loads(stamp_file.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        cached = None
    if cached != stamp or not target.is_file():
        result = merge_textures(winner.read_bytes(), selected.read_bytes())
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix('.tmp')
        temporary.write_bytes(result)
        temporary.replace(target)
        stamp_file.write_text(json.dumps(stamp), encoding='utf-8')
    return [*layers, ('Selected button icons', folder)]

PACKS = {'Xbox': 'Xbox Prompts (Dommo)', 'Keyboard': 'Keyboard Prompts (PCBButtons)'}


def is_prompt(name):
    return name.casefold() in {n.casefold() for n in PACKS.values()}


def choice(profile):
    profile = Path(profile)
    selected = profile / 'button-prompts.json'
    def read(path):
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            return data if isinstance(data, dict) else {}
        except (OSError, ValueError):
            return {}
    value = read(selected).get('choice')
    if value in ('PlayStation', *PACKS):
        return value
    # Preserve existing users' selection without keeping the old folders as mods.
    legacy = profile / 'mods.json'
    settings = read(legacy)
    enabled = set(settings.get('enabled', [])) | set(settings.get('order', []))
    enabled -= set(settings.get('disabled', []))
    for value in ('Keyboard', 'Xbox'):
        if PACKS[value] in enabled:
            return value
    return 'PlayStation'


def layer(port, value):
    if value == 'PlayStation':
        return None
    folder = Path(port) / 'launcher/assets/button-prompts' / PACKS[value]
    if not (folder / 'menu/common.tpf.dcx').is_file():
        raise ValueError('Bundled button images are missing. Re-extract the launcher release.')
    return folder
