"""Verified, cancellable game installation from independent release ZIP assets."""
import hashlib
import contextlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import urllib.request
import zipfile

MANIFEST_URL = 'https://github.com/mark3317/bbgl/releases/download/game-1.09/game-manifest.json'
BLOCK = 1024 * 1024


@contextlib.contextmanager
def installation_lock(path):
    """The OS releases this lock even when the launcher is terminated."""
    with Path(path).open('a+b') as handle:
        if Path(path).stat().st_size == 0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise OSError('Another game installation is already running.') from error
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


class Cancelled(Exception):
    pass


def safe_name(name):
    path = PurePosixPath(name)
    if (not name or '\\' in name or ':' in name or path.is_absolute()
            or any(p in ('', '.', '..') for p in name.split('/'))
            or any(p.endswith((' ', '.')) for p in path.parts)
            or any(re.match(r'(?i)^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)', p) for p in path.parts)):
        raise ValueError(f'Unsafe archive path: {name}')
    return path


def request(url):
    if not url.startswith('https://'):
        raise ValueError('Download URL must use HTTPS')
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'BBGL'}), timeout=45)


def install(root, progress, cancel, manifest_url=MANIFEST_URL, target=None):
    root = Path(target).resolve().parent if target is not None else Path(root)
    root.mkdir(parents=True, exist_ok=True)
    with installation_lock(root / '.game-install.lock'):
        return _install(root, progress, cancel, manifest_url, target)


def _install(root, progress, cancel, manifest_url, target=None):
    target = Path(target).resolve() if target is not None else root / 'game'
    if target.exists():
        raise ValueError('The game folder already exists. Choose it using the folder button.')
    with request(manifest_url) as response:
        manifest = json.loads(response.read(4 * BLOCK))
    parts = manifest['parts']
    if (manifest.get('format') != 1 or not parts or len(parts) > 1000
            or not isinstance(manifest.get('file_count'), int) or manifest['file_count'] <= 0):
        raise ValueError('Unsupported game manifest')
    names = set()
    for part in parts:
        name = part['name']
        if len(safe_name(name).parts) != 1 or name in names:
            raise ValueError('Invalid or duplicate asset name')
        names.add(name)
        if (not isinstance(part['size'], int) or not 0 < part['size'] < 2**31
                or not isinstance(part['unpacked_size'], int) or part['unpacked_size'] <= 0
                or not re.fullmatch('[a-f0-9]{64}', part['sha256'])):
            raise ValueError('Invalid game manifest sizes or checksum')
    total = sum(p['size'] for p in parts)
    unpacked = sum(p['unpacked_size'] for p in parts)
    stage = root / '.game-installing'
    cache = root / '.game-downloads'
    def check():
        if cancel.is_set():
            raise Cancelled('Installation cancelled. Downloaded parts are kept for the next attempt.')
    try:
        if stage.is_symlink() or cache.is_symlink():
            raise ValueError('Installation folders cannot be symbolic links')
        if stage.exists():
            shutil.rmtree(stage)
        stage.mkdir()
        cache.mkdir(exist_ok=True)
        needed = unpacked + total + 256 * BLOCK
        if shutil.disk_usage(root).free < needed:
            raise OSError(f'Not enough free space: need {needed / 2**30:.1f} GiB')
        done = 0
        seen = set()
        for index, part in enumerate(parts):
            check()
            archive = cache / part['name']
            if archive.is_symlink():
                raise ValueError('Download cache cannot contain symbolic links')
            digest = hashlib.sha256()
            valid = archive.is_file() and archive.stat().st_size == part['size']
            if valid:
                with archive.open('rb') as source:
                    while data := source.read(BLOCK):
                        check()
                        digest.update(data)
                valid = digest.hexdigest() == part['sha256']
            if not valid:
                digest = hashlib.sha256()
                count = 0
                with request(part['url']) as response, archive.open('wb') as output:
                    while data := response.read(BLOCK):
                        check()
                        count += len(data)
                        if count > part['size']:
                            raise ValueError('Download exceeds declared size')
                        digest.update(data)
                        output.write(data)
                        progress((done + count * 0.8) / total,
                                 f'Downloading {index + 1}/{len(parts)} · {(done + count) / 2**30:.2f} / {total / 2**30:.2f} GiB')
                if count != part['size'] or digest.hexdigest() != part['sha256']:
                    archive.unlink()
                    raise ValueError('Downloaded ZIP checksum does not match. Please retry.')
            extracted = 0
            with zipfile.ZipFile(archive) as source:
                entries = source.infolist()
                if sum(e.file_size for e in entries) != part['unpacked_size']:
                    raise ValueError('Archive size does not match manifest')
                for entry in entries:
                    check()
                    name = safe_name(entry.filename)
                    folded = str(name).casefold()
                    if entry.is_dir() or stat.S_ISLNK(entry.external_attr >> 16) or folded in seen:
                        raise ValueError('Duplicate or unsupported ZIP entry')
                    seen.add(folded)
                    destination = stage.joinpath(*name.parts)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with source.open(entry) as src, destination.open('xb') as dst:
                        while data := src.read(BLOCK):
                            check()
                            dst.write(data)
                    extracted += entry.file_size
                    progress((done + part['size'] * (0.8 + 0.2 * extracted / part['unpacked_size'])) / total,
                             f'Unpacking {index + 1}/{len(parts)} · {len(seen)}/{manifest["file_count"]}')
            done += part['size']
        if len(seen) != manifest['file_count'] or not (stage / 'eboot.bin').is_file():
            raise ValueError('Incomplete game archive')
        check()
        stage.rename(target)
        progress(1.0, 'Game installed.')
        for part in parts:
            (cache / part['name']).unlink(missing_ok=True)
        if not any(cache.iterdir()):
            cache.rmdir()
        return target
    finally:
        if stage.exists() and not stage.is_symlink():
            shutil.rmtree(stage)
