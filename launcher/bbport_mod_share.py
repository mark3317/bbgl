"""Content-addressed LAN file-mod exchange on the existing discovery TCP socket."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import socket
import stat
import tempfile
import threading
import zipfile

MAX_BYTES = 8 * 1024**3
MAX_FILES = 50000


def linked(path):
    return path.is_symlink() or bool(getattr(path.stat(follow_symlinks=False),
        'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400))


def safe_name(name):
    if (not isinstance(name, str) or not name or len(name) > 180 or
            name.startswith('.') or name.endswith((' ', '.')) or
            re.search(r'[<>:"/\\|?*\x00-\x1f]', name) or
            name.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL',
                *('COM' + str(i) for i in range(10)), *('LPT' + str(i) for i in range(10))}):
        raise ValueError('Invalid mod name')
    return name


def files(folder):
    folder = Path(folder)
    if linked(folder):
        raise ValueError('Linked mod folder')
    result = []
    for base, dirs, names in os.walk(folder, followlinks=False):
        for name in dirs + names:
            p = Path(base) / name
            if linked(p):
                raise ValueError('Linked mod file')
        for name in names:
            p = Path(base) / name
            if not p.is_file():
                raise ValueError('Invalid mod file')
            relative = p.relative_to(folder).as_posix()
            for part in relative.split('/'):
                safe_name(part)
            result.append((relative, p))
            if len(result) > MAX_FILES:
                raise ValueError('Too many mod files')
    if sum(p.stat().st_size for _, p in result) > MAX_BYTES:
        raise ValueError('Mod is too large')
    return sorted(result)


def fingerprint(entries):
    digest = hashlib.sha256()
    for name, path in entries:
        digest.update(name.encode('utf-8') + b'\0')
        h = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                h.update(block)
        digest.update(h.digest())
    return digest.hexdigest()


class Share:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.lock = threading.Lock()
        self.cache = {}
        self.transfer = threading.BoundedSemaphore(2)
        self.selection = None

    def catalog(self):
        from mods import discover
        result = []
        with self.lock:
            for name in discover(self.folder):
                try:
                    safe_name(name)
                    entries = files(self.folder / name)
                    signature = [(n, p.stat().st_size, p.stat().st_mtime_ns) for n, p in entries]
                    cached = self.cache.get(name)
                    key = cached[1] if cached and cached[0] == signature else fingerprint(entries)
                    self.cache[name] = (signature, key)
                    result.append(dict(name=name, digest=key, size=sum(s[1] for s in signature)))
                except (OSError, ValueError):
                    continue
        selection = self.selection
        if selection is not None:
            order, enabled = selection
            result.sort(key=lambda row: order.index(row['name']) if row['name'] in order else len(order))
            for row in result:
                row['enabled'] = row['name'] in enabled
        return result

    def handle(self, body, output):
        # Called only by the discovery server bound to the selected network.
        if body['kind'] == 'mods_catalog':
            raw = json.dumps(dict(ok=True, mods=self.catalog())).encode() + b'\n'
            if len(raw) > 1024 * 1024:
                raise ValueError('Mod catalog is too large')
            output.write(raw)
            return
        if not self.transfer.acquire(blocking=False):
            raise ValueError('Mod transfer busy')
        try:
            name = safe_name(body.get('name'))
            expected = body.get('digest')
            folder = self.folder / name
            from mods import discover
            if name not in discover(self.folder):
                raise ValueError('Mod no longer available')
            entries = files(folder)
            if fingerprint(entries) != expected:
                raise ValueError('Mod changed; wait for the list to update')
            with tempfile.TemporaryFile() as archive:
                with zipfile.ZipFile(archive, 'w', zipfile.ZIP_STORED) as z:
                    for relative, path in entries:
                        z.write(path, relative)
                length = archive.tell()
                if length > MAX_BYTES:
                    raise ValueError('Mod is too large')
                output.write(json.dumps(dict(ok=True, size=length)).encode() + b'\n')
                archive.seek(0)
                shutil.copyfileobj(archive, output, 1024 * 1024)
        finally:
            self.transfer.release()


def request(discovery, peer, kind, **fields):
    from bbport_party import encoded, PROTOCOL
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(20)
        sock.bind((discovery.address, 0))
        sock.connect((peer['host'], discovery.port))
        sock.sendall(encoded(dict(protocol=PROTOCOL, kind=kind, **fields)) + b'\n')
        stream = sock.makefile('rb')
        raw = stream.readline(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024 or not raw.endswith(b'\n'):
            raise ValueError('Invalid mod response')
        reply = json.loads(raw)
        if not reply.get('ok'):
            raise ValueError(reply.get('error', 'Mod exchange failed'))
        return sock, stream, reply
    except Exception:
        sock.close()
        raise


def catalog(discovery, peer):
    from prompt_icons import is_prompt
    sock, stream, reply = request(discovery, peer, 'mods_catalog')
    try:
        rows = reply['mods']
        if not isinstance(rows, list) or len(rows) > 2000:
            raise ValueError('Invalid mod catalog')
        for row in rows:
            safe_name(row['name'])
            if not re.fullmatch('[a-f0-9]{64}', row['digest']) or not 0 <= row['size'] <= MAX_BYTES:
                raise ValueError('Invalid mod catalog')
        # Older launchers advertise personal button images as regular mods.
        # Never download or apply those as part of another player's mod set.
        return [row for row in rows if not is_prompt(row['name'])]
    finally:
        stream.close()
        sock.close()


def download(discovery, peer, mod, folder):
    name = safe_name(mod['name'])
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    if any(p.name.casefold() == name.casefold() for p in folder.iterdir()):
        raise ValueError('A mod with this name is already installed')
    sock, stream, reply = request(discovery, peer, 'mod_download', name=name, digest=mod['digest'])
    try:
        length = reply['size']
        if not isinstance(length, int) or not 0 < length <= MAX_BYTES:
            raise ValueError('Invalid mod size')
        with tempfile.TemporaryDirectory(prefix='.bbgl-download-', dir=folder) as temp:
            temp = Path(temp)
            archive = temp / 'mod.zip'
            with archive.open('wb') as output:
                remaining = length
                while remaining:
                    block = stream.read(min(1024 * 1024, remaining))
                    if not block:
                        raise ValueError('Mod download interrupted')
                    output.write(block)
                    remaining -= len(block)
            unpacked = temp / 'content'
            unpacked.mkdir()
            with zipfile.ZipFile(archive) as z:
                entries = z.infolist()
                if len(entries) > MAX_FILES or sum(i.file_size for i in entries) > MAX_BYTES:
                    raise ValueError('Mod archive is too large')
                seen = set()
                for entry in entries:
                    path = PurePosixPath(entry.filename)
                    if path.is_absolute() or '\\' in entry.filename or not path.parts:
                        raise ValueError('Invalid archive path')
                    for part in path.parts:
                        safe_name(part)
                    key = str(path).casefold()
                    if key in seen or stat.S_ISLNK(entry.external_attr >> 16):
                        raise ValueError('Invalid archive entry')
                    seen.add(key)
                    target = unpacked.joinpath(*path.parts)
                    if entry.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        with z.open(entry) as source, target.open('xb') as output:
                            shutil.copyfileobj(source, output, 1024 * 1024)
            from mods import content_root
            if not content_root(unpacked) or fingerprint(files(unpacked)) != mod['digest']:
                raise ValueError('Downloaded mod does not match its catalog')
            # Windows rename refuses an existing destination, including a concurrent download.
            unpacked.rename(folder / name)
    finally:
        stream.close()
        sock.close()
