"""On-demand BB PC Remaster archives and their private, versioned mod layer."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from bbport_game_download import BLOCK, Cancelled, installation_lock, safe_name
from mods import ARCHIVE_SUFFIXES, mod_files


PAGE = 'https://www.nexusmods.com/bloodborne/mods/45?tab=files'
API = 'https://api.nexusmods.com/v1/games/bloodborne/mods/45/files'
# Pinned Nexus file IDs and byte sizes, verified with modFiles(modId: 45, gameId: 2708).
FILES = ((3116, 21_268_261_222), (3379, 5_697_806_185))
TOTAL_BYTES = sum(size for _, size in FILES)
DOWNLOAD_PORTION = 0.85
PACK_FOLDER = 'BB PC Remaster 1.10 + PATCH 1.13'
READY_MARKER = '.complete'


def directory(mods_dir):
    return Path(mods_dir) / '.bb-pc-remaster'


def installed(root):
    layer = root / PACK_FOLDER
    return layer if (layer / READY_MARKER).is_file() and (layer / 'dvdroot_ps4').is_dir() else None


def cached_archives(root):
    files = tuple(root / f'{file_id}.archive' for file_id, _ in FILES)
    try:
        return files if all(f.stat().st_size == size for f, (_, size) in zip(files, FILES)) else ()
    except OSError:
        return ()


def match_archives(paths):
    """Identify the two specific Nexus downloads, even if the player renamed them."""
    paths = tuple(Path(p) for p in paths)
    by_size = {p.stat().st_size: p for p in paths if p.is_file() and p.suffix.lower() in ARCHIVE_SUFFIXES}
    if len(paths) != len(FILES) or set(by_size) != {size for _, size in FILES}:
        raise ValueError('Choose the BB PC Remaster 1.10 main archive and PATCH 1.13 from Nexus Mods.')
    return tuple(by_size[size] for _, size in FILES)


def _check_cancel(cancel):
    if cancel.is_set():
        raise Cancelled('BB PC Remaster operation cancelled.')


def _progress(callback):
    last = -1.0

    def report(fraction, status):
        nonlocal last
        now = time.monotonic()
        if last < 0 or now - last >= 0.12:
            last = now
            callback(fraction, status)

    return report


def _download_url(file_id, api_key):
    request = Request(f'{API}/{file_id}/download_link.json',
                      headers={'User-Agent': 'BBGL', 'Application-Name': 'BBGL'})
    request.add_unredirected_header('apikey', api_key)
    try:
        with urlopen(request, timeout=30) as response:
            links = json.load(response)
    except HTTPError as error:
        if error.code in (401, 403):
            raise ValueError('Nexus Mods requires a valid Premium key for direct downloads. Download the archives on Nexus Mods or try again.') from None
        raise
    url = next((link['URI'] for link in links if urlsplit(link.get('URI', '')).scheme == 'https'), '')
    if not url:
        raise ValueError('Nexus Mods did not provide a download link.')
    return url


def _transfer(url, partial, size, cancel, report):
    received = partial.stat().st_size if partial.is_file() else 0
    if received > size:
        partial.unlink()
        received = 0
    if received == size:
        return
    headers = {'Range': f'bytes={received}-'} if received else {}
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        if response.status == 200:
            received = 0  # CDN can decline to resume and return the whole archive.
        elif (response.status != 206 or not received or
              response.headers.get('Content-Range') != f'bytes {received}-{size - 1}/{size}'):
            raise ValueError('Nexus Mods returned an unexpected download range.')
        with partial.open('ab' if received else 'wb') as output:
            while chunk := response.read(BLOCK):
                _check_cancel(cancel)
                received += len(chunk)
                if received > size:
                    raise ValueError('The archive size does not match the Nexus Mods download.')
                output.write(chunk)
                report(received)
    if received != size:
        raise ValueError('The download was incomplete. Try again to resume it.')


def download(root, api_key, progress, cancel):
    root.mkdir(parents=True, exist_ok=True)
    with installation_lock(root / '.lock', 'BB PC Remaster is already being prepared in another launcher.'):
        if installed(root):
            return
        report = _progress(progress)
        done = 0
        for (file_id, size), status in zip(FILES, ('Downloading BB PC Remaster 1.10…', 'Downloading PATCH 1.13…')):
            _check_cancel(cancel)
            archive = root / f'{file_id}.archive'
            progress(DOWNLOAD_PORTION * done / TOTAL_BYTES, status)
            if not archive.is_file() or archive.stat().st_size != size:
                try:
                    url = _download_url(file_id, api_key)
                    partial = archive.with_suffix('.part')
                    _transfer(url, partial, size, cancel,
                              lambda received: report(DOWNLOAD_PORTION * (done + received) / TOTAL_BYTES, status))
                    partial.replace(archive)
                except OSError as error:
                    # The CDN link includes a short-lived credential. Keep URLs out of UI/logs.
                    raise ValueError('Nexus Mods download interrupted. Try again to resume it.') from error
            done += size


def _tar_command():
    windows_tar = Path(os.environ.get('SystemRoot', r'C:\Windows')) / 'System32' / 'tar.exe'
    return str(windows_tar if os.name == 'nt' and windows_tar.is_file() else 'bsdtar')


def _extract(archive, target, progress, cancel):
    tar = _tar_command()
    flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
    with subprocess.Popen([tar, '-tvf', str(archive)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                          text=True, errors='replace', creationflags=flags) as process:
        count = 0
        try:
            for line in process.stdout:
                _check_cancel(cancel)
                # libarchive's verbose listing starts each entry with its type. Refuse links,
                # devices and FIFOs before unpacking. bsdtar checks path containment on extract.
                if line[:1] not in ('-', 'd') or ' link to ' in line:
                    raise ValueError('The BB PC Remaster archive contains unsupported files.')
                count += 1
            if process.wait() or not count:
                raise ValueError('Could not read the BB PC Remaster archive.')
        finally:
            if process.poll() is None:
                process.kill()
    target.mkdir()
    with subprocess.Popen([tar, '-xvf', str(archive), '-C', str(target)], stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, errors='replace', creationflags=flags) as process:
        extracted = 0
        try:
            for line in process.stdout:
                _check_cancel(cancel)
                if line.startswith('x '):
                    extracted += 1
                    progress(min(extracted / count, 0.99))
            if process.wait():
                raise ValueError('Could not unpack BB PC Remaster. Check the archives and free disk space.')
        finally:
            if process.poll() is None:
                process.kill()


def install(root, archives, progress, cancel, start=0.0):
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    with installation_lock(root / '.lock', 'BB PC Remaster is already being prepared in another launcher.'):
        if installed(root):
            return
        scratch = root / 'installing'
        payload = root / PACK_FOLDER
        for folder in (scratch, payload):
            if folder.is_symlink() or getattr(folder, 'is_junction', lambda: False)():
                raise ValueError('The BB PC Remaster installation folder is a link.')
            if folder.exists():
                shutil.rmtree(folder)
        scratch.mkdir()
        report = _progress(progress)
        done = 0
        try:
            for archive, (_, size), status in zip(archives, FILES, ('Installing BB PC Remaster 1.10…', 'Applying PATCH 1.13…'), strict=True):
                _check_cancel(cancel)
                if not archive.is_file() or archive.stat().st_size != size:
                    raise ValueError('The archive size does not match the Nexus Mods download.')
                progress(start + (1 - start) * done / TOTAL_BYTES, status)
                unpacked = scratch / 'archive'
                _extract(archive, unpacked, lambda part: report(
                    start + (1 - start) * (done + part * size) / TOTAL_BYTES, status), cancel)
                count = 0
                for relative, source in mod_files(unpacked):
                    _check_cancel(cancel)
                    name = safe_name(relative.as_posix().casefold())
                    destination = payload / name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    source.replace(destination)
                    count += 1
                if not count:
                    raise ValueError('The BB PC Remaster archive has no game files.')
                shutil.rmtree(unpacked)
                done += size
            _check_cancel(cancel)
            # Both versions share a layer. Commit it only when a launch may use every file.
            # Creating a marker keeps publication independent of Windows directory rename locks.
            (payload / READY_MARKER).touch(exist_ok=False)
            for archive in archives:
                if archive.parent == root and archive.suffix == '.archive':
                    try:
                        archive.unlink(missing_ok=True)
                    except OSError:
                        pass  # Installed layer is complete even if an archive is still open.
            progress(1.0, '')
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
            if not installed(root):
                shutil.rmtree(payload, ignore_errors=True)
