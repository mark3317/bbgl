"""Small, non-destructive checks for the launcher's Game page."""

import json
from pathlib import Path
import re
import struct
import tempfile

from bbport_trophy_catalog import BLOODBORNE_TROPHY_SET, bloodborne_catalogue


def valid_trophy_key(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-fA-F]{32}', value) is not None


def _trophy_pack(game):
    if game:
        directory = game / 'sce_sys' / 'trophy'
        return next((directory / name for name in ('trophy00.trp', 'TROPHY.TRP')
                     if (directory / name).is_file()), None)


def _trophy_pack_size(pack):
    if pack:
        try:
            with pack.open('rb') as source:
                if source.read(4) == bytes.fromhex('DCA24D00'):
                    return source.seek(0, 2)
        except OSError:
            pass


def _trophy_cache(user, pack_size):
    if pack_size is not None:
        try:
            cached = json.loads((user / 'trophy_cache' / 'metadata.json').read_text(encoding='utf-8'))
            if isinstance(cached, dict) and cached.get('source_size') == pack_size:
                return cached
        except (OSError, ValueError):
            pass
    return {}


def _bloodborne_pack_ids(game, pack, pack_size):
    if pack_size is None:
        return set()
    try:
        with (game / 'sce_sys' / 'npbind.dat').open('rb') as binding:
            npbind = binding.read(64 * 1024 + 1)
        match = re.search(rb'NPWR[0-9]{5}_[0-9]{2}', npbind)
        if len(npbind) > 64 * 1024 or not match or match[0] != BLOODBORNE_TROPHY_SET:
            return set()
        # Match the native TRP directory layout. Only read the table, never the
        # encrypted descriptions or image payloads.
        with pack.open('rb') as source:
            header = source.read(96)
            if len(header) != 96 or header[:4] != bytes.fromhex('DCA24D00'):
                return set()
            count, stride = struct.unpack_from('>II', header, 16)
            if not (0 < count <= 512 and 64 <= stride <= 4096 and 96 + count * stride <= pack_size):
                return set()
            table = source.read(count * stride)
        if len(table) != count * stride:
            return set()
    except OSError:
        return set()
    ids = set()
    for start in range(0, len(table), stride):
        name = table[start:start + 32].partition(b'\0')[0]
        match = re.fullmatch(rb'TROP([0-9]{3})\.PNG', name, re.IGNORECASE)
        offset, size, flag = struct.unpack_from('>QQI', table, start + 32)
        if match and flag == 0 and 0 < size and 96 + len(table) <= offset <= pack_size - size:
            ids.add(int(match[1]))
    return ids


def _unlocked_trophies(user):
    unlocked = {}
    try:
        with (user / 'trophies.txt').open(encoding='utf-8', errors='replace') as history:
            for line in history:
                # The native port treats any signed timestamp for a valid ID as unlocked.
                record = re.fullmatch(r'\s*([+-]?)0*([0-9]{1,3})\s+([+-]?[0-9]+)\s*', line)
                if record:
                    trophy_id = int(record[1] + record[2])
                    if 0 <= trophy_id < 128:
                        timestamp = record[3].lstrip('+').lstrip('0')
                        when = int(timestamp) if timestamp.isdigit() and len(timestamp) <= 12 else 0
                        unlocked[trophy_id] = when if when <= 253402300799 else 0
    except FileNotFoundError:
        pass
    return unlocked


def _trophy_icons(user):
    icons = {}
    try:
        for image in (user / 'trophy_cache' / 'icons').iterdir():
            match = re.fullmatch(r'TROP([0-9]{3})\.PNG', image.name, re.IGNORECASE)
            if match and image.is_file():
                icons[int(match[1])] = image.absolute().as_uri()
    except OSError:
        pass
    return icons


def trophy_snapshot(game_dir, user, *, russian=False):
    """Read one profile's history with native or built-in trophy details."""
    try:
        unlocked = _unlocked_trophies(user)
    except OSError:
        unlocked = None
    game = Path(game_dir) if game_dir else None
    pack = _trophy_pack(game)
    pack_size = _trophy_pack_size(pack)
    cache = _trophy_cache(user, pack_size)
    cached = cache.get('entries')
    catalogue = {entry['id']: entry for entry in cached
                 if isinstance(entry, dict) and type(entry.get('id')) is int
                 and 0 <= entry['id'] < 128} if isinstance(cached, list) else {}
    has_metadata = cache.get('complete') is True and bool(catalogue)
    bloodborne = bloodborne_catalogue(_bloodborne_pack_ids(game, pack, pack_size), russian)
    built_in = {}
    if not has_metadata:
        built_in = bloodborne
        if built_in:
            catalogue = built_in
    ids = catalogue.keys() or (unlocked or {}).keys()
    icons = _trophy_icons(user) if catalogue else {}
    entries = []
    for trophy_id in ids:
        entry = catalogue.get(trophy_id, {})
        when = unlocked.get(trophy_id) if unlocked is not None else None
        name, description = entry.get('name'), entry.get('description')
        if trophy_id == 0 and bloodborne:
            description = bloodborne[0]['description']
        has_name = isinstance(name, str) and bool(name.strip()) and name != f'Trophy #{trophy_id}'
        secret = entry.get('hidden') is True and when is None
        entries.append({
            'id': trophy_id,
            'name': name if has_name and not secret else '',
            'description': description if isinstance(description, str) and not secret else '',
            'secret': secret,
            'icon': icons.get(trophy_id, '') if when is not None or (has_name and not secret) else '',
            'status': 'earned' if when is not None else 'unknown' if unlocked is None else 'locked',
            'unlockedAt': when or 0,
        })
    entries.sort(key=lambda entry: (entry['status'] != 'earned', -entry['unlockedAt'], entry['id']))
    earned = sum(entry['status'] == 'earned' for entry in entries)
    return {
        'entries': entries,
        'hasMetadata': has_metadata or bool(built_in),
        'builtIn': bool(built_in),
        'progress': {'earned': earned if unlocked is not None else -1,
                     'total': len(catalogue) if unlocked is not None else 0},
    }


def _item(label, level, detail):
    return {'label': label, 'level': level, 'detail': detail}


def save_title_id(game):
    """Use the save title declared by the game, which can differ from TITLE_ID."""
    if game:
        try:
            from prepare import sfo
            values = sfo((game / 'sce_sys' / 'param.sfo').read_bytes())
            title = values.get('INSTALL_DIR_SAVEDATA') or values.get('TITLE_ID')
            if isinstance(title, str) and re.fullmatch(r'CUSA[0-9]{5}', title):
                return title
        except (OSError, ValueError, ImportError):
            pass
    return game.name if game and re.fullmatch(r'CUSA[0-9]{5}', game.name) else 'CUSA03173'


def check_readiness(game_dir, user_dir, game_info, *, built_in_trophies=False):
    """Return Game, Trophies and Saves checks without touching game or save data."""
    game = Path(game_dir) if game_dir else None
    user = Path(user_dir)
    result = []

    info = game_info(str(game)) if game and (game / 'eboot.bin').is_file() else None
    if not info:
        result.append(_item('Game files', 'error', 'Choose your game folder or download the game.'))
    else:
        missing = [name for name in ('dvdroot_ps4', 'sce_module', 'sce_sys') if not (game / name).is_dir()]
        if missing:
            result.append(_item('Game files', 'error', 'Missing: ' + ', '.join(missing)))
        elif info[1] != '01.09':
            result.append(_item('Game files', 'warning', f'Version {info[1]} found; update 1.09 is recommended.'))
        else:
            result.append(_item('Game files', 'ready', 'Bloodborne 1.09 and required folders found.'))

    pack = _trophy_pack(game)
    if pack is None:
        result.append(_item('Trophies', 'warning', 'No trophy pack found; achievements can show IDs only.'))
    else:
        pack_size = _trophy_pack_size(pack)
        if pack_size is None:
            result.append(_item('Trophies', 'error', 'Trophy pack cannot be read or has an invalid header.'))
        else:
            key_file = user / 'keys.json'
            try:
                data = json.loads(key_file.read_text(encoding='utf-8-sig'))
                has_key = valid_trophy_key(data['TrophyKeySet']['ReleaseTrophyKey'])
            except (OSError, ValueError, KeyError, TypeError):
                has_key = False
            cached = _trophy_cache(user, pack_size)
            cached_complete = cached.get('complete') is True and bool(cached.get('entries'))
            if cached_complete:
                detail = 'Trophy names have been loaded by the game.'
                level = 'ready'
            elif built_in_trophies:
                detail = 'The launcher uses its built-in catalogue for trophy names and descriptions.'
                level = 'ready'
            elif has_key:
                detail = 'Pack and key format found; launch the game to verify decryption.'
                level = 'warning'
            else:
                detail = 'Names and descriptions are unavailable for this trophy pack.'
                level = 'warning'
            history = user / 'trophies.txt'
            if history.is_file():
                try:
                    unlocked = _unlocked_trophies(user)
                    detail += f' {len(unlocked)} local unlocks recorded.'
                except OSError:
                    detail += ' Unlock history cannot be read.'
            result.append(_item('Trophies', level, detail))

    if not user.exists():
        result.append(_item('Saves', 'warning', 'Save folder will be created on first launch.'))
    elif not user.is_dir():
        result.append(_item('Saves', 'error', 'Save path is a file, not a folder.'))
    else:
        try:
            with tempfile.NamedTemporaryFile(prefix='.bbport-check-', dir=user, delete=True):
                pass
        except OSError:
            result.append(_item('Saves', 'error', 'Save folder is not writable.'))
        else:
            save_root = user / 'savedata'
            save_id = save_title_id(game)
            saves = list(save_root.glob(f'*/{save_id}/SPRJ*/userdata*')) if save_root.is_dir() else []
            try:
                found_save = any(path.is_file() and path.stat().st_size > 0 for path in saves)
            except OSError:
                found_save = False
            # shadPS4's own savedata folder (…\home\1000\savedata) holds <title>\SPRJ* directly;
            # chosen as the Saves folder (or its parent, home\1000), the game misses that save and
            # starts a new, empty one. Only looked for when no save is where the port reads them.
            shadps4_save = False
            if not found_save:
                try:
                    shadps4_save = any(path.is_file() and path.stat().st_size > 0
                                       for pattern in (f'{save_id}/SPRJ*/userdata*',
                                                       f'savedata/{save_id}/SPRJ*/userdata*')
                                       for path in user.glob(pattern))
                except OSError:
                    pass
            if found_save:
                result.append(_item('Saves', 'ready', 'Save data found.'))
            elif shadps4_save:
                result.append(_item('Saves', 'warning',
                                    f'This looks like shadPS4\'s savedata folder: its {save_id} save is not '
                                    f'where this port reads saves, so the game would start a new one. Choose '
                                    f'another Saves folder and copy {save_id} into its savedata\\1 folder.'))
            else:
                result.append(_item('Saves', 'warning', 'A new save will be created when you play.'))
    return result
