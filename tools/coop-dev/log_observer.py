"""Read-only log collector; the Codex chat heartbeat handles triage and project chats.

No model process, game control, settings writes or save reads occur here.
"""
import argparse
import ctypes
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

REPO = Path(__file__).resolve().parents[2]
STATE = REPO / 'out/log-observer'
PROJECT_ID = 'b25db2d0-df72-4c85-acba-249ef647359a'
CHUNK = 64 * 1024


def utc():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temporary, path)


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except FileNotFoundError:
        return default


def redact(text):
    text = re.sub(r'(?i)(Bearer\s+)[\w.\-]+', r'\1[REDACTED]', text)
    return re.sub(r'''(?ix)(["']?(?:token|secret|password|authorization|api_key|BBSC_PARTY_TOKEN)["']?\s*[:=]\s*["']?)[^\s,"'}]+''',
                  r'\1[REDACTED]', text)


def alive(pid):
    if os.name == 'nt':
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
        kernel.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            return False
        try:
            code = ctypes.c_ulong()
            return bool(kernel.GetExitCodeProcess(handle, ctypes.byref(code))) and code.value == 259
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


class Singleton:
    """OS releases the lock on crash; no PID-file stale lock recovery needed."""
    def __init__(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.file = path.open('a+b')
        self.file.write(b'0')
        self.file.flush()
        self.file.seek(0)

    def acquire(self):
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(self.file.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            self.file.close()
            return False

    def close(self):
        self.file.close()


class Collector:
    def __init__(self, state, local_appdata):
        self.state = Path(state)
        self.local = Path(local_appdata)
        self.data = load_json(self.state / 'cursors.json', {'files': {}, 'users': {}})

    def sources(self, players):
        result = {}
        for player in players:
            profile = self.local / f'Bloodborne Game Launcher Player {player}'
            settings = load_json(profile / 'settings.json', {})
            user = Path(settings.get('user_dir') or profile / 'user')
            roots = {profile / 'user', user, profile / 'out'}
            roots.update(Path(p) for p in self.data['users'].get(str(player), []))
            for root in roots:
                if root.is_absolute() and root.is_dir():
                    for pattern in ('run_*.log', 'last_run*.log'):
                        for path in root.glob(pattern):
                            result[path] = player
            # Only known log directories; never enumerate save/journal payloads.
            for folder in (profile / 'coop/bbsc/logs', profile / 'coop/party/logs'):
                if folder.is_dir():
                    for pattern in ('*.log', '*.jsonl'):
                        for path in folder.rglob(pattern):
                            result[path] = player
            path = profile / 'coop/local-test/start-error.log'
            if path.is_file():
                result[path] = player
        return result

    def scan(self, players, since, final=False):
        packets = []
        for path, player in self.sources(players).items():
            try:
                stat = path.stat()
                key = str(path.resolve())
                identity = [stat.st_dev, stat.st_ino, getattr(stat, 'st_birthtime_ns', 0)]
                cursor = self.data['files'].get(key)
                if cursor is None:
                    aliases = [c for c in self.data['files'].values() if c['identity'] == identity]
                    if aliases:
                        cursor = dict(max(aliases, key=lambda c: c['offset']))
                # Ignore historical runs on first attachment. New files start at byte 0.
                if cursor is None:
                    cursor = {'identity': identity, 'offset': 0 if stat.st_mtime >= since - 2 else stat.st_size}
                if cursor['identity'] != identity or stat.st_size < cursor['offset']:
                    cursor = {'identity': identity, 'offset': 0}
                offset = cursor['offset']
                if stat.st_size > offset:
                    with path.open('rb') as stream:
                        stream.seek(offset)
                        raw = stream.read(CHUNK)
                    # Keep an unfinished line (and UTF-8 character) for the next poll.
                    end = raw.rfind(b'\n')
                    if end >= 0:
                        raw = raw[:end + 1]
                    elif len(raw) < CHUNK and not final:
                        continue
                    text = raw.decode('utf-8', errors='replace').replace('\r\n', '\n')
                    for match in re.finditer(r'"BB_USER_DIR"\s*:\s*("(?:[^"\\]|\\.)*")', text):
                        discovered = json.loads(match[1])
                        if Path(discovered).is_absolute():
                            known = self.data['users'].setdefault(str(player), [])
                            if discovered not in known:
                                known.append(discovered)
                    # Stable packet name makes a retry after a cursor-write crash idempotent.
                    import hashlib
                    name = hashlib.sha256((key + repr(identity) + str(offset)).encode()).hexdigest()[:24] + '.json'
                    packet = {'id': name, 'projectId': PROJECT_ID, 'player': player,
                              'source': key, 'observedUtc': utc(), 'sourceMtimeUtc':
                              datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                              'offset': offset, 'endOffset': offset + len(raw),
                              'text': redact(text)}
                    destination = self.state / 'pending' / name
                    if not destination.exists() and not (self.state / 'done' / name).exists():
                        write_json(destination, packet)
                    packets.append(name)
                    cursor['offset'] += len(raw)
                self.data['files'][key] = cursor
            except FileNotFoundError:
                continue  # Log rotated between discovery and open.
        write_json(self.state / 'cursors.json', self.data)
        return packets


def request(args):
    state = args.state
    name = f'{args.parent_pid}-{args.player}.json'
    write_json(state / 'requests' / name, {'player': args.player, 'parentPid': args.parent_pid,
                                         'since': time.time(), 'requestedUtc': utc()})
    command = [sys.executable, str(Path(__file__).resolve()), '--state', str(state), 'run']
    options = {'cwd': str(REPO), 'stdin': subprocess.DEVNULL,
               'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}
    if os.name == 'nt':
        options['creationflags'] = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
    subprocess.Popen(command, **options)


def run(args):
    state = args.state
    lock = Singleton(state / 'observer.lock')
    if not lock.acquire():
        return
    collector = Collector(state, args.local_appdata)
    leases = {}
    idle = None
    try:
        while True:
            for path in (state / 'requests').glob('*.json'):
                lease = load_json(path, None)
                if lease:
                    leases[path.name] = lease
                path.unlink(missing_ok=True)
            active = [lease for lease in leases.values() if alive(lease['parentPid'])]
            # Keep collecting for a short drain after the last launcher exits.
            if active:
                idle = None
            elif idle is None:
                idle = time.monotonic()
            players = sorted({lease['player'] for lease in leases.values()})
            since = min((lease['since'] for lease in leases.values()), default=time.time())
            collector.scan(players, since)
            write_json(state / 'status.json', {'pid': os.getpid(), 'updatedUtc': utc(),
                       'status': 'watching' if active else 'draining', 'players': players,
                       'pending': len(list((state / 'pending').glob('*.json')))})
            if idle is not None and time.monotonic() - idle >= 30:
                # Do not abandon unread bytes from the final scan.
                while collector.scan(players, since, final=True):
                    pass
                break
            time.sleep(5)
        write_json(state / 'status.json', {'status': 'stopped', 'updatedUtc': utc()})
    except Exception as error:
        write_json(state / 'status.json', {'status': 'failed', 'updatedUtc': utc(),
                   'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        lock.close()


def main():
    if sys.stdout is not None and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, default=STATE)
    parser.add_argument('--local-appdata', default=os.environ.get('LOCALAPPDATA', str(Path.home())))
    sub = parser.add_subparsers(dest='action', required=True)
    start = sub.add_parser('request')
    start.add_argument('--player', type=int, choices=(1, 2, 3), required=True)
    start.add_argument('--parent-pid', type=int, required=True)
    sub.add_parser('run')
    sub.add_parser('pending')
    ack = sub.add_parser('ack')
    ack.add_argument('names', nargs='+')
    args = parser.parse_args()
    if args.action == 'request':
        request(args)
    elif args.action == 'run':
        run(args)
    elif args.action == 'pending':
        paths = sorted((args.state / 'pending').glob('*.json'),
                       key=lambda p: p.stat().st_mtime_ns, reverse=True)
        print(json.dumps({'packets': [str(p.resolve()) for p in paths[:8]],
                         'remaining': max(0, len(paths) - 8),
                         'registry': load_json(args.state / 'issues.json', {}),
                         'followups': load_json(args.state / 'followups.json', {}),
                         'observer': load_json(args.state / 'status.json', {})}, ensure_ascii=False))
    elif args.action == 'ack':
        for name in args.names:
            if Path(name).name != name or not re.fullmatch(r'[a-f0-9]{24}\.json', name):
                raise ValueError('ack expects packet basenames, not paths')
            source = args.state / 'pending' / name
            destination = args.state / 'done' / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.exists():
                os.replace(source, destination)


if __name__ == '__main__':
    main()
