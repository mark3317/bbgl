"""Three native P2P players on loopback, using the existing Player 1/2/3 profiles."""
import datetime
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import time

from bbport_party import write_json

PROFILE = 'Bloodborne Game Launcher'
LOCAL_GUARD_PORT = 37609


def profiles(local_appdata):
    result = []
    for index in range(1, 4):
        profile = Path(local_appdata) / f'{PROFILE} Player {index}'
        settings_file = profile / 'settings.json'
        if not settings_file.is_file():
            raise ValueError(f'Player {index}: existing profile settings.json is missing.')
        settings = json.loads(settings_file.read_text(encoding='utf-8-sig'))
        user = Path(settings.get('user_dir') or profile / 'user')
        game = Path(settings.get('game_dir') or '')
        if not user.is_absolute() or not user.is_dir():
            raise ValueError(f'Player {index}: the existing saves folder is unavailable.')
        if not game.is_absolute() or not (game / 'eboot.bin').is_file():
            raise ValueError(f'Player {index}: the configured game folder is unavailable.')
        result.append({'index': index, 'profile': profile, 'user': user.resolve(),
                       'game': game, 'settings': settings})
    if len({os.path.normcase(str(p['user'])) for p in result}) != 3:
        raise ValueError('Local players must use three separate saves folders.')
    return result


def configuration(local_appdata):
    members = [{'id': f'LocalPlayer{i}', 'host': '127.0.0.1', 'port': 37609+i,
                'p2p': 3657+i} for i in range(1, 4)]
    path = Path(local_appdata) / PROFILE / 'coop/local-test/config.json'
    if path.exists():
        cfg = json.loads(path.read_text(encoding='utf-8'))
        if (cfg.get('members') != members or cfg.get('version') != 1 or
                len(bytes.fromhex(cfg['secret'])) != 32 or len(cfg['group']) != 32):
            raise ValueError('Local test configuration is invalid; it was preserved.')
    else:
        cfg = {'version': 1, 'epoch': 1, 'group': secrets.token_hex(16),
               'secret': secrets.token_hex(32), 'members': members}
        write_json(path, cfg)
    return cfg, path


def reserve_ports(cfg):
    """Check the exact native/control ports before any game starts; no partial launch."""
    reserved = []
    try:
        for peer in cfg['members']:
            for kind, port in ((socket.SOCK_STREAM, peer['port']), (socket.SOCK_DGRAM, peer['p2p'])):
                sock = socket.socket(socket.AF_INET, kind)
                reserved.append(sock)
                if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
                sock.bind(('127.0.0.1', port))
    except OSError as error:
        raise ValueError('A local player port is already in use. Close the previous test games first.') from error
    finally:
        for sock in reserved:
            sock.close()


def child_environment(profile, base=None):
    env = dict(os.environ if base is None else base)
    for key in ('BB_CONFIG', 'BB_DATA_DIR', 'BB_USER_DIR', 'BBSC_DATA_DIR', 'BB_PARTY_CONFIG',
                'BB_PARTY_MEMBER', 'BBSC_PARTY_INSTANCE', 'BBSC_PARTY_PORT', 'BBSC_PARTY_TOKEN',
                'BB_HOST_OVERRIDES', 'BB_P2P_PORT', 'BBSC_SAVE_DIR'):
        env.pop(key, None)
    env.update(BBGL_PROFILE_DIR=str(profile), PYINSTALLER_RESET_ENVIRONMENT='1')
    return env


def launch_environment(bbgl, entry, cfg_path):
    # BBGL resolves profile constants on process startup. Reject an incorrectly
    # started child instead of accidentally preparing the main profile's saves.
    profile = entry['profile']
    if Path(os.environ.get('BBGL_PROFILE_DIR', '')).resolve() != profile.resolve():
        raise ValueError('The local player process has the wrong profile.')
    settings = bbgl.app_settings(entry['settings'])
    settings.update(game_dir=str(entry['game']), user_dir=str(entry['user']),
                    fps_mode='60', frame_cap='60', fullscreen=False)
    env = bbgl.game_environment(settings)
    env.update(BB_PARTY_CONFIG=str(cfg_path), BB_PARTY_MEMBER=f"LocalPlayer{entry['index']}",
               BBGL_PROFILE_DIR=str(profile), BB_DATA_DIR=str(profile),
               BB_CONFIG=str(profile / 'bbport.ini'), BB_USER_DIR=str(entry['user']),
               BB_MODS_CONFIG=str(profile / 'mods.json'), BB_PATCHES_CONFIG=str(profile / 'patches.json'),
               BB_FPS='60', BB_FPS_LIMIT='60', BB_FULLSCREEN='0',
               BB_WINDOW_SIZE='1280x720', BB_OUTPUT_RES='1280x720', BB_COOP='1', BB_TIMEOUT='0')
    patches = [name.strip() for name in env.get('BB_PATCHES', '').split(';') if name.strip()]
    if 'Skip Intro' not in patches:
        patches.append('Skip Intro')
    env['BB_PATCHES'] = ';'.join(patches)
    for key in tuple(env):
        if key.startswith('BB_THD_') or key == 'BB_NET_BACKEND':
            env.pop(key, None)
    return env


def run_three(port, local_appdata=None, popen=subprocess.Popen):
    port = Path(port)
    local_appdata = Path(local_appdata or os.environ['LOCALAPPDATA'])
    entries = profiles(local_appdata)  # validate every profile before starting any child
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as guard:
        if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
            guard.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        try:
            guard.bind(('127.0.0.1', LOCAL_GUARD_PORT)); guard.listen(1)
        except OSError as error:
            raise ValueError('A three-player local test is already running.') from error
        cfg, cfg_path = configuration(local_appdata)
        reserve_ports(cfg)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')
        run = cfg_path.parent / 'runs' / stamp
        metadata = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    'group': cfg['group'], 'fps': 60, 'players': [], 'status': 'starting'}
        processes = []
        for entry in entries:
            log = run / f"player-{entry['index']}-runner.log"
            log.parent.mkdir(parents=True, exist_ok=True)
            command = [str(port / 'Bloodborne.exe'), '--script', str(port / 'scripts/local_party.py'),
                       '--player', str(entry['index']), '--config', str(cfg_path)]
            with log.open('w', encoding='utf-8') as stream:
                proc = popen(command, cwd=port, env=child_environment(entry['profile']),
                             stdin=subprocess.DEVNULL, stdout=stream, stderr=subprocess.STDOUT,
                             creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            processes.append(proc)
            metadata['players'].append({'index': entry['index'], 'pid': proc.pid,
                                        'profile': str(entry['profile']), 'user_dir': str(entry['user'])})
            write_json(run / 'run.json', metadata)
            time.sleep(.7)
        metadata['status'] = 'runners started; gameplay pending'
        write_json(run / 'run.json', metadata)
        # Keep the single-instance guard while any native game belongs to a runner.
        # Do not kill or restart another game when one player exits or fails.
        codes = [proc.wait() for proc in processes]
        metadata.update(status='all runners exited', exit_codes=codes)
        write_json(run / 'run.json', metadata)
        return max(codes, default=0)
