"""Bundled BBSC-GL fork and local co-op services.
Client binaries ship with the launcher; mutable accounts, saves and journals stay in
LOCALAPPDATA. Upstream authors and licences are recorded in THIRD_PARTY.md.
"""
import ipaddress
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
import tempfile
import urllib.request
import urllib.parse
import re

NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
# Tailscale's own address on every tailnet: a route to it goes out through the Tailscale adapter.
TAILSCALE_DNS = '100.100.100.100'


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


def download(kind, progress=None):
    """Compatibility entry point: validate installed binaries, never copy them to the profile."""
    from bbport_bundle import verify
    try:
        return verify(package_dir(kind))
    except (OSError, ValueError, KeyError) as error:
        raise CoopError(f'Bundled co-op files are damaged. Re-extract the launcher release: {error}') from error


# --- Network ---------------------------------------------------------------------------------------

def installed_vpns():
    """Installed programs, including stopped/disconnected VPNs."""
    found = set()
    if tailscale_exe():
        found.add('tailscale')
    for variable in ('ProgramW6432', 'ProgramFiles', 'ProgramFiles(x86)'):
        folder = os.environ.get(variable)
        if folder and (Path(folder) / 'Radmin VPN' / 'RvRvpnGui.exe').is_file():
            found.add('radmin')
    if sys.platform == 'win32':
        import winreg
        for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            for view in (winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY):
                try:
                    with winreg.OpenKey(hive, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                                        0, winreg.KEY_READ | view) as root:
                        for i in range(winreg.QueryInfoKey(root)[0]):
                            try:
                                with winreg.OpenKey(root, winreg.EnumKey(root, i)) as entry:
                                    name = winreg.QueryValueEx(entry, 'DisplayName')[0].casefold()
                                    if name == 'radmin vpn':
                                        found.add('radmin')
                                    elif name == 'tailscale':
                                        found.add('tailscale')
                            except OSError:
                                continue
                except OSError:
                    continue
    return sorted(found)


def _vpn_installer_url(provider):
    # Resolve current versions from the publishers, rather than pinning old installers.
    page, pattern, base = {
        'radmin': ('https://www.radmin-vpn.com/',
                   r'https://download\.radmin-vpn\.com/download/files/Radmin_VPN_[\d.]+\.exe', ''),
        'tailscale': ('https://pkgs.tailscale.com/stable/',
                     r'href="(tailscale-setup-[\d.]+\.exe)"', 'https://pkgs.tailscale.com/stable/'),
    }[provider]
    request = urllib.request.Request(page, headers={'User-Agent': 'Mozilla/5.0 BBGL/1.1'})
    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read(4 * 1024 * 1024).decode('utf-8')
    match = re.search(pattern, html)
    if not match:
        raise CoopError('Could not find the VPN installer on the official website.')
    return base + (match.group(1) if base else match.group(0))


def install_vpn(provider, progress=None):
    """Download into a private folder and open the normal Windows installer."""
    if provider not in ('radmin', 'tailscale'):
        raise ValueError('Unknown VPN provider')
    url = _vpn_installer_url(provider)
    folder = Path(tempfile.mkdtemp(prefix='bbgl-vpn-'))
    target = folder / (provider + '-setup.exe')
    partial = target.with_suffix('.part')
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 BBGL/1.1'})
        with urllib.request.urlopen(request, timeout=30) as response, partial.open('wb') as output:
            if urllib.parse.urlparse(response.geturl()).scheme != 'https':
                raise CoopError('Download URL must use HTTPS')
            expected = int(response.headers.get('Content-Length', 0))
            size = 0
            while block := response.read(256 * 1024):
                size += len(block)
                if size > 200 * 1024 * 1024:
                    raise CoopError('VPN installer is too large.')
                output.write(block)
                if progress:
                    progress(size, expected)
        if size < 2 or (expected and size != expected):
            raise CoopError('VPN installer download is incomplete.')
        with partial.open('rb') as stream:
            if stream.read(2) != b'MZ':
                raise CoopError('The VPN download is not a Windows installer.')
        partial.replace(target)
        os.startfile(str(target))
    except Exception:
        shutil.rmtree(folder, ignore_errors=True)
        raise
    # ShellExecute returns before Windows finishes reading the file.
    return target


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


# --- One-time setup (one administrator prompt) ---------------------------------------------------


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
