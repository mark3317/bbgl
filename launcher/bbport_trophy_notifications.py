"""Read and update the game's per-profile notifications.ini."""

import math
import os
from pathlib import Path
import re
from tempfile import NamedTemporaryFile


THEMES = ('original', 'card', 'card_cinematic', 'corner')
DEFAULTS = {'theme': 'original', 'volume': 80, 'muted': False, 'hold_seconds': 0.0,
            'cinematic_intensity': 70, 'grade_label': False, 'platinum_animation': True}
TEXT_KEYS = ('text_unlocked', 'text_banner', 'name_bronze', 'name_silver', 'name_gold', 'name_platinum')


class ProfileInUse(OSError):
    pass


def _value(key, value):
    if key == 'theme':
        if value in THEMES:
            return value
    elif isinstance(DEFAULTS[key], bool):
        if value in ('1', 'true', 'yes', 'on'):
            return True
        if value in ('0', 'false', 'no', 'off'):
            return False
    elif key == 'hold_seconds':
        if re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?', value):
            number = float(value)
            if math.isfinite(number):
                return min(20.0, max(0.0, number))
    elif re.fullmatch(r'-?[0-9]{1,11}', value):
        number = int(value)
        if -2147483648 <= number <= 2147483647:
            return min(100, max(0, number))
    raise ValueError(key)


def _assignment(line):
    key, sep, value = line.partition('=')
    if sep and not key.lstrip(' \t').startswith('#'):
        return key.strip(' \t\r'), value.strip(' \t\r\n')
    return '', ''


def _read(path):
    try:
        return path.read_bytes().decode('utf-8-sig')
    except FileNotFoundError:
        return ''


def load(folder):
    values = {**DEFAULTS, **dict.fromkeys(TEXT_KEYS, '')}
    for line in _read(folder / 'notifications.ini').split('\n'):
        key, raw = _assignment(line)
        if key in DEFAULTS:
            try:
                values[key] = _value(key, raw)
            except ValueError:
                pass
        elif key in TEXT_KEYS:
            values[key] = raw.encode('utf-8')[:200].decode('utf-8', errors='ignore').replace('\t', ' ')
    return values


def save_option(folder, key, value):
    if key not in DEFAULTS:
        raise ValueError(key)
    if key in ('volume', 'cinematic_intensity') and isinstance(value, float) and value.is_integer():
        value = int(value)
    value = _value(key, str(value).lower() if isinstance(value, bool) else str(value))
    text = str(int(value)) if isinstance(value, bool) else str(value)
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / 'notifications.lock').open('a+b') as lock:
        lock.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise ProfileInUse from error
        path = folder / 'notifications.ini'
        original = _read(path)
        newline = '\r\n' if '\r\n' in original else '\n'
        lines = original.split('\n')
        index = next((i for i in range(len(lines) - 1, -1, -1) if _assignment(lines[i])[0] == key), None)
        if index is None:
            separator = newline if original and not original.endswith('\n') else ''
            updated = original + separator + f'{key}={text}{newline}'
        else:
            lines[index] = f'{key}={text}' + ('\r' if lines[index].endswith('\r') else '')
            updated = '\n'.join(lines)
        staged = None
        try:
            with NamedTemporaryFile(dir=folder, prefix='notifications-', suffix='.part', delete=False) as file:
                staged = Path(file.name)
                file.write(updated.encode('utf-8'))
            os.replace(staged, path)
        finally:
            if staged is not None:
                staged.unlink(missing_ok=True)
