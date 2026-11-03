"""Bundled BBSC-GL fork and local co-op services.
Client binaries ship with the launcher; mutable accounts, saves and journals stay in
LOCALAPPDATA. Upstream authors and licences are recorded in THIRD_PARTY.md.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile

REPO = 'mark3317/bbsc-gl'
RELEASES = f'https://github.com/{REPO}/releases'
DISCORD = 'https://discord.gg/Df7BCmfWdt'
# The BBSC packages this launcher uses, found by name in BBSC's GitHub releases: the newest
# release that has one is installed, so a new BBSC version needs no launcher update.
#   client: BBSC-<version>-BBport.zip (bbsc.dll, bbsc-launch.exe, the account tool, BBSC's own
#           BBport build in emulator\)
#   server: BBSC-<version>-Server.zip (shadnet.exe, BBSC-GameServer.exe) - only for hosting
ASSET_PATTERNS = {'client': r'BBSC-(?P<version>[0-9][^-]*)-BBport\.zip',
                  'server': r'BBSC-(?P<version>[0-9][^-]*)-Server\.zip'}
# Where each package lives under %LOCALAPPDATA%\bbport-coop, and the folders of the 0.0.1 era
# (fixed names) still used when they are all there is.
PACKAGE_FOLDERS = {'client': 'bbsc-client', 'server': 'bbsc-server'}
LEGACY_FOLDERS = {'client': 'BBSC-0.0.1-BBport', 'server': 'BBSC-0.0.1-Server'}
VERSION_FILE = 'bbport-package.json'
# What survives an update of a package: logs, backups and BBSC's own files about the player's
# world; the host's server keeps its accounts and registration key.
KEEP_ON_UPDATE = {'client': ('bbsc/logs', 'bbsc/save-backups', 'bbsc/own-world', 'bbsc/captures',
                             'tools/account.dat'),
                  'server': ('server/shadnet.cfg', 'server/db', 'server/logs')}
SHADNET_PORT, MATCHING_PORT, WEBAPI_PORT, GAME_PORT, RELAY_PORT = 31313, 31314, 31315, 20443, 20444
INVITE_PREFIX = 'BBCOOP-'
NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
# Tailscale's own address on every tailnet: a route to it goes out through the Tailscale adapter.
TAILSCALE_DNS = '100.100.100.100'
# Inbound rules for hosting: the server ports, from Tailscale's range and this PC's own networks
# only. The game itself takes the other players' P2P connections from anywhere (a co-op server
# on the internet: the players' PCs talk directly, or through the server's relay).
FIREWALL_RANGES = ('100.64.0.0/10', 'LocalSubnet')
FIREWALL_PORTS = (('party control', 'TCP', 37600), ('discovery', 'TCP', 37601),
                  ('discovery UDP', 'UDP', 37601), ('native gameplay', 'UDP', 37658))
RULE_PREFIX = 'Bloodborne co-op'
# Shipped with a launcher package (next to Bloodborne.exe):
#   coop-server.json  {"name": "...", "invite": "BBCOOP-..."} - the co-op server players join when
#                     their own invite code is empty (a friends' package: name, password, Play)
#   coop/bbsc/        a BBSC build of our own (bbsc.dll, bbsc-launch.exe) with coop/bbsc.json
#                     {"base": "<BBSC version>"}: put over the official files of that version only
DEFAULT_SERVER_FILE = 'coop-server.json'
OVERRIDE_DIR = Path('coop') / 'bbsc'
OVERRIDE_FILE = Path('coop') / 'bbsc.json'


class CoopError(Exception):
    pass


def port_dir():
    frozen = getattr(sys, 'frozen', False)
    return Path(sys.executable).resolve().parent if frozen else Path(__file__).resolve().parent.parent


def coop_dir():
    from bbport_paths import profile_dir
    return profile_dir() / 'coop'


def package_dir(kind):
    return port_dir() / 'coop' / kind


def installed(kind):
    folder = package_dir(kind)
    if kind == 'client':
        return all((folder / p).is_file() for p in ('bbsc/bbsc-launch.exe', 'bbsc/bbsc.dll'))
    return all((folder / 'server' / p).is_file() for p in ('shadnet.exe', 'BBSC-GameServer.exe',
                                                            'shadnet.cfg'))


def installed_version(kind):
    try:
        return str(json.loads((package_dir(kind) / 'bundle.json').read_text(encoding='utf-8'))['version'])
    except (OSError, ValueError, KeyError, TypeError):
        return ''


def _version_key(version):
    return tuple(int(part) if part.isdigit() else 0 for part in re.split(r'[.\-_]', version))


# --- Download -------------------------------------------------------------------------------------

def _github(path):
    request = urllib.request.Request(f'https://api.github.com/repos/{REPO}/{path}',
                                     headers={'User-Agent': 'bbport-launcher',
                                              'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(request, timeout=30) as reply:
        return json.load(reply)


def latest_release(kind):
    """(version, tag, asset name, url, sha256) of the newest BBSC release with this package."""
    pattern = re.compile(ASSET_PATTERNS[kind])
    found = []
    for release in _github('releases?per_page=30'):
        if release.get('draft'):
            continue
        for asset in release.get('assets', []):
            match = pattern.fullmatch(str(asset.get('name', '')))
            if not match:
                continue
            digest = str(asset.get('digest') or '')
            if not digest.startswith('sha256:'):
                continue  # nothing to check it against
            found.append((match['version'], str(release.get('tag_name', '')), asset['name'],
                          asset['browser_download_url'], digest.split(':', 1)[1].lower(),
                          str(release.get('published_at', ''))))
    if not found:
        raise CoopError(f'No BBSC release has a {ASSET_PATTERNS[kind]} package ({RELEASES}).')
    found.sort(key=lambda item: (_version_key(item[0]), item[5]))
    return found[-1][:5]


def update_available(kind):
    have = installed_version(kind) if installed(kind) else ''
    source = port_dir() / 'coop' / kind / 'bundle.json'
    if not source.is_file():
        raise CoopError('Bundled co-op files are missing. Re-extract the launcher release.')
    newest = json.loads(source.read_text(encoding='utf-8'))['version']
    return have, newest if have != newest else ''


def _safe_extract(archive, destination):
    root = destination.resolve()
    for member in archive.infolist():
        target = (destination / member.filename).resolve()
        if root != target and root not in target.parents:
            raise CoopError(f'Unsafe path in the package: {member.filename}')
    archive.extractall(destination)


def _package_root(staging):
    """The package's own folder inside an unpacked zip (BBSC-<version>-BBport\\), or the zip's root."""
    entries = [entry for entry in staging.iterdir() if not entry.name.startswith('__MACOSX')]
    return entries[0] if len(entries) == 1 and entries[0].is_dir() else staging


def _install(kind, zip_path, version, source):
    staging = Path(tempfile.mkdtemp(prefix='.bbsc-unpack-', dir=coop_dir()))
    try:
        with zipfile.ZipFile(zip_path) as archive:
            _safe_extract(archive, staging)
        new = _package_root(staging)
        probe = 'bbsc/bbsc.dll' if kind == 'client' else 'server/shadnet.exe'
        if not (new / probe).is_file():
            raise CoopError(f'{Path(zip_path).name} is not a BBSC {kind} package (no {probe}).')
        old = package_dir(kind)
        if old.is_dir():
            for keep in KEEP_ON_UPDATE[kind]:
                if (old / keep).exists():
                    target = new / keep
                    if target.is_dir():
                        shutil.rmtree(target)
                    elif target.exists():
                        target.unlink()
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(old / keep), str(target))
        if not version and kind == 'client':
            try:
                version = str(json.loads((new / 'bbsc' / 'mod.json').read_text(encoding='utf-8'))['version'])
            except (OSError, ValueError, KeyError, TypeError):
                version = ''
        (new / VERSION_FILE).write_text(json.dumps({'version': version, 'source': source}, indent=2) + '\n',
                                        encoding='utf-8')
        folder = coop_dir() / PACKAGE_FOLDERS[kind]
        if folder.exists():
            shutil.rmtree(folder)
        shutil.move(str(new), str(folder))
        legacy = coop_dir() / LEGACY_FOLDERS[kind]
        if legacy.is_dir() and legacy != folder:
            shutil.rmtree(legacy, ignore_errors=True)  # its kept files moved over above
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    if kind == 'client':
        apply_override()
    return folder


def download(kind, progress=None):
    """Compatibility entry point: validate installed binaries, never copy them to the profile."""
    from bbport_bundle import verify
    try:
        return verify(package_dir(kind))
    except (OSError, ValueError, KeyError) as error:
        raise CoopError(f'Bundled co-op files are damaged. Re-extract the launcher release: {error}') from error


def install_zip(kind, zip_path, progress=None):
    """Installs a BBSC package zip the player downloaded (a test build, or no GitHub access)."""
    coop_dir().mkdir(parents=True, exist_ok=True)
    if progress:
        progress(f'Installing {Path(zip_path).name}…')
    _install(kind, Path(zip_path), '', str(zip_path))
    return installed_version(kind)


def apply_override():
    """Synchronize the pinned fork; old package versions are no longer a dependency."""
    return download('client')


def bbsc_emulator():
    """BBSC's own BBport build in the client package (emulator\\bb-probe.exe), or None."""
    probe = package_dir('client') / 'emulator' / 'bb-probe.exe'
    return probe if probe.is_file() else None


# --- Network ---------------------------------------------------------------------------------------

def tailscale_exe():
    """tailscale.exe: on PATH (the installer adds it, wherever it was installed), else the default folder."""
    # Full name, not bare 'tailscale': what which() returns is then unambiguously the
    # file we hand to subprocess.run, not 'tailscale' + whichever PATHEXT entry matched.
    found = shutil.which('tailscale.exe')
    if found:
        return Path(found)
    for variable in ('ProgramW6432', 'ProgramFiles'):
        folder = os.environ.get(variable)
        if folder and (Path(folder) / 'Tailscale' / 'tailscale.exe').is_file():
            return Path(folder) / 'Tailscale' / 'tailscale.exe'
    return None


def tailscale_ip():
    return _tailscale_ip_from_cli() or _tailscale_ip_from_route()


def _tailscale_ip_from_cli():
    exe = tailscale_exe()
    if not exe:
        return None
    try:
        out = subprocess.run([str(exe), 'ip', '-4'], capture_output=True, text=True,
                             timeout=10, creationflags=NO_WINDOW).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    for line in out.split():
        if is_tailscale(line):
            return line
    return None


def _tailscale_ip_from_route():
    """This PC's address on the Tailscale adapter, when the CLI can't be run (no packet is sent)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        try:
            probe.connect((TAILSCALE_DNS, 9))
            ip = probe.getsockname()[0]
        except OSError:
            return None
    return ip if is_tailscale(ip) else None


def is_tailscale(address):
    parts = address.split('.')
    return len(parts) == 4 and parts[0] == '100' and parts[1].isdigit() and 64 <= int(parts[1]) <= 127


def local_ip():
    """This PC's address on its home network (no packet is sent)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        try:
            probe.connect(('192.0.2.1', 9))
            return probe.getsockname()[0]
        except OSError:
            return None


def host_address():
    """(address, network name): Tailscale when it is connected, else the home network."""
    ip = tailscale_ip()
    if ip:
        return ip, 'Tailscale'
    ip = local_ip()
    if ip:
        return ip, 'your home network only (Tailscale is not connected)'
    return None, None


# --- One-time setup (one administrator prompt) ---------------------------------------------------

def network_candidates():
    """Active IPv4 adapters; discovery does not claim remote reachability."""
    script = """Get-NetAdapter | Where-Object Status -eq 'Up' | ForEach-Object {
      $adapter = $_
      Get-NetIPAddress -InterfaceIndex $_.ifIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue |
      Where-Object AddressState -eq 'Preferred' | ForEach-Object {
        [pscustomobject]@{id=[string]$adapter.InterfaceGuid; name=$adapter.Name;
          description=$adapter.InterfaceDescription; address=$_.IPAddress; prefix=$_.PrefixLength}
      }
    } | ConvertTo-Json -Compress"""
    try:
        result = subprocess.run(['powershell.exe', '-NoProfile', '-Command', script],
                                capture_output=True, text=True, timeout=12, creationflags=NO_WINDOW)
        if result.returncode:
            return []
        rows = json.loads(result.stdout or '[]')
    except (OSError, ValueError, subprocess.SubprocessError):
        return []
    groups = {}
    for row in ([rows] if isinstance(rows, dict) else rows):
        try:
            address = ipaddress.IPv4Address(row['address'])
        except (ValueError, KeyError):
            continue
        if address.is_loopback or address.is_link_local or address.is_unspecified or address.is_multicast:
            continue
        name = row['name']
        description = (name + ' ' + row.get('description', '')).lower()
        vpn = any(word in description for word in ('tailscale', 'radmin', 'wireguard', 'zerotier',
                                                  'hamachi', 'openvpn', 'tap-windows', 'wintun', 'vpn'))
        key = 'adapter:' + row['id']
        group = groups.setdefault(key, {'value': key, 'text': name, 'vpn': vpn, 'provider': 'tailscale' if 'tailscale' in description else 'radmin' if 'radmin' in description else '', 'addresses': [], 'ranges': []})
        if str(address) not in group['addresses']:
            group['addresses'].append(str(address))
        subnet = str(ipaddress.IPv4Network(f'{address}/{row.get("prefix", 32)}', strict=False))
        if subnet not in group['ranges']:
            group['ranges'].append(subnet)
    return sorted(groups.values(), key=lambda item: (not item['vpn'], item['text'].lower()))



def _quoted(text):
    """A PowerShell single-quoted string: a path with an apostrophe (C:\\Users\\O'Neil) broke the
    script, and the setup then never finished."""
    return "'" + str(text).replace("'", "''") + "'"


def _firewall_script(game_exe, remote_ranges=None):
    validated = [('Any' if r == 'Any' else 'LocalSubnet' if r == 'LocalSubnet' else
                  str(ipaddress.IPv4Network(r, strict=False))) for r in
                 (FIREWALL_RANGES if remote_ranges is None else remote_ranges)]
    ranges = ','.join(f"'{r}'" for r in validated)
    lines = ['$ErrorActionPreference = "Stop"', f'$ranges = @({ranges})']
    for label, protocol, port in FIREWALL_PORTS:
        rule = f'{RULE_PREFIX} {label} {port}'
        lines.append(f"Remove-NetFirewallRule -DisplayName '{rule}' -ErrorAction SilentlyContinue")
        lines.append(f"New-NetFirewallRule -DisplayName '{rule}' -Direction Inbound -Protocol {protocol} "
                     f"-LocalPort {port} -RemoteAddress $ranges -Action Allow | Out-Null")
    rule = f'{RULE_PREFIX} game'
    lines.append(f"Remove-NetFirewallRule -DisplayName '{rule}' -ErrorAction SilentlyContinue")
    lines.append(f"New-NetFirewallRule -DisplayName '{rule}' -Direction Inbound -Program {_quoted(game_exe)} "
                 "-Action Allow | Out-Null")
    return '\r\n'.join(lines) + '\r\n'


def setup_done(game_exe):
    command = (f"$r = Get-NetFirewallRule -DisplayName '{RULE_PREFIX} game' -ErrorAction SilentlyContinue; "
               f"if ($r -and (($r | Get-NetFirewallApplicationFilter).Program -eq {_quoted(game_exe)})) {{ exit 0 }} else {{ exit 1 }}")
    try:
        return subprocess.run(['powershell', '-NoProfile', '-Command', command], timeout=30,
                              creationflags=NO_WINDOW).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def run_setup(game_exe):
    """Firewall rules (Tailscale and home network only) and the C++ runtime the servers need.
    Windows asks the player once for administrator rights."""
    script = coop_dir() / 'setup-firewall.ps1'
    result_file = coop_dir() / 'firewall-setup-result.json'
    request = secrets.token_hex(16)
    coop_dir().mkdir(parents=True, exist_ok=True)
    # Verify in the elevated process as well: a normal Windows 10 process may
    # not be able to read NetSecurity's CIM rules after successful elevation.
    names = [f'{RULE_PREFIX} {label} {port}' for label, _, port in FIREWALL_PORTS]
    names.append(f'{RULE_PREFIX} game')
    verify = '\n'.join(
        f"$r = Get-NetFirewallRule -DisplayName {_quoted(name)} -ErrorAction Stop; "
        f"if (-not ($r | Where-Object {{ $_.Enabled -eq 'True' -and $_.Action -eq 'Allow' }})) "
        f"{{ throw {_quoted('Firewall rule is not enabled: ' + name)} }}"
        for name in names)
    body = (
        '$ErrorActionPreference = "Stop"\n'
        f"$result = @{{ok=$false; error=''; request='{request}'}}\n"
        'try {\n' + _firewall_script(game_exe) + verify + '\n'
        f"$r = Get-NetFirewallRule -DisplayName {_quoted(names[-1])} -ErrorAction Stop\n"
        f"if (($r | Get-NetFirewallApplicationFilter).Program -ne {_quoted(game_exe)}) "
        "{ throw 'Firewall game path verification failed.' }\n"
        '$result.ok = $true\n'
        '} catch { $result.error = ($_ | Out-String) }\n'
        'finally { $result | ConvertTo-Json -Compress | '
        f'Set-Content -LiteralPath {_quoted(result_file)} -Encoding UTF8 }}\n'
        'if (-not $result.ok) { exit 1 }\n')
    with script.open('w', encoding='utf-8-sig', newline='') as output:
        output.write(body)
    if not run_as_administrator('powershell.exe', f'-NoProfile -ExecutionPolicy Bypass -File "{script}"'):
        raise CoopError('Co-op needs a Yes on the Windows administrator prompt (firewall rules); '
                        'the answer was No. Try Configure firewall again, or continue without it.')
    try:
        result = json.loads(result_file.read_text(encoding='utf-8-sig'))
    except (OSError, ValueError) as error:
        raise CoopError(f'Firewall setup did not return a result. See {script}.') from error
    if not isinstance(result, dict) or result.get('request') != request:
        raise CoopError(f'Firewall setup did not return a result. See {script}.')
    if result.get('ok') is not True:
        raise CoopError(f"Firewall setup failed: {result.get('error') or 'Unknown Windows error'}")


def run_as_administrator(program, parameters, verb='runas'):
    """Runs program with administrator rights, hidden, and waits for it. False when the player
    said No. The launcher asks Windows itself: a prompt requested by a process in the background
    (it was a hidden PowerShell's Start-Process -Verb RunAs) opens only as a flashing taskbar
    button, and players saw no prompt at all (#49). Asked by the launcher, whose window is in
    front after the click, it opens over it."""
    import ctypes
    from ctypes import wintypes

    class ShellExecuteInfo(ctypes.Structure):
        _fields_ = [('cbSize', wintypes.DWORD), ('fMask', ctypes.c_ulong), ('hwnd', wintypes.HWND),
                    ('lpVerb', wintypes.LPCWSTR), ('lpFile', wintypes.LPCWSTR), ('lpParameters', wintypes.LPCWSTR),
                    ('lpDirectory', wintypes.LPCWSTR), ('nShow', ctypes.c_int), ('hInstApp', wintypes.HINSTANCE),
                    ('lpIDList', ctypes.c_void_p), ('lpClass', wintypes.LPCWSTR), ('hkeyClass', wintypes.HKEY),
                    ('dwHotKey', wintypes.DWORD), ('hIconOrMonitor', wintypes.HANDLE), ('hProcess', wintypes.HANDLE)]

    shell32 = ctypes.WinDLL('shell32', use_last_error=True)
    shell32.ShellExecuteExW.argtypes = [ctypes.POINTER(ShellExecuteInfo)]
    user32, kernel32 = ctypes.windll.user32, ctypes.windll.kernel32
    user32.GetForegroundWindow.restype = wintypes.HWND
    window = user32.GetForegroundWindow()
    owner = wintypes.DWORD()
    user32.GetWindowThreadProcessId(window, ctypes.byref(owner))
    ctypes.windll.ole32.CoInitializeEx(None, 0x2 | 0x4)  # the shell wants COM on this thread
    info = ShellExecuteInfo(cbSize=ctypes.sizeof(ShellExecuteInfo),
                            fMask=0x40 | 0x100 | 0x400,  # NOCLOSEPROCESS, NOASYNC, FLAG_NO_UI (errors come back)
                            hwnd=window if owner.value == os.getpid() else None,
                            lpVerb=verb, lpFile=program, lpParameters=parameters, nShow=0)
    if not shell32.ShellExecuteExW(ctypes.byref(info)):
        error = ctypes.get_last_error()
        if error == 1223:  # ERROR_CANCELLED: the player said No
            return False
        raise CoopError(f'Windows could not run the co-op setup: {ctypes.FormatError(error)}')
    if info.hProcess:
        kernel32.WaitForSingleObject(wintypes.HANDLE(info.hProcess), 0xFFFFFFFF)
        kernel32.CloseHandle(wintypes.HANDLE(info.hProcess))
    return True


def active_save_dir(user_dir):
    """The game's save folder (SPRJ0005, userdata0000...) written most recently, or None."""
    newest = None
    for folder in Path(user_dir).glob('savedata/*/CUSA00207/SPRJ0005'):
        times = [f.stat().st_mtime for f in folder.glob('userdata00*') if f.is_file()]
        if times and (newest is None or max(times) > newest[0]):
            newest = (max(times), folder)
    return newest[1] if newest else None


def backup_saves(user_dir):
    """A copy of the saves before every co-op session (BBSC 0.0.1 is a first test)."""
    saves = Path(user_dir) / 'savedata'
    if not saves.is_dir():
        return None
    target = Path(user_dir) / 'coop-backups' / time.strftime('%Y%m%d-%H%M%S') / 'savedata'
    shutil.copytree(saves, target)
    return target.parent
