"""BBGL --script entrypoint for an explicit three-player test on this PC."""
import argparse
import hmac
import json
import os
from pathlib import Path
import re
import runpy
import sys
import traceback


def local_identity(member, secret, profile):
    from bbport_party import configuration, write_json

    def home_config(identity):
        home = configuration([identity])
        home['members'][0].update(port=member['port'], p2p=member['p2p'])
        home.update(mode='dynamic-worlds-v1', identity=identity)
        return home

    who = member['id']
    path = profile / 'coop/local-test/home.json'
    if not path.exists():
        seed = hmac.digest(secret, who.encode('ascii'), 'sha256').hex()
        identity = dict(member, name=who, seed=seed)
        write_json(path, home_config(identity), create_only=True)
    home = json.loads(path.read_text(encoding='utf-8'))
    stored = home.get('identity') if isinstance(home, dict) else None
    seed = stored.get('seed') if isinstance(stored, dict) else None
    if not isinstance(seed, str) or not re.fullmatch('[0-9a-f]{64}', seed):
        raise ValueError(f'Invalid stored Party identity for {who}')
    identity = dict(member, name=who, seed=seed)
    if home != home_config(identity):
        raise ValueError(f'Invalid stored Party identity for {who}')
    return identity


def individual_party(env, cfg, entries, profile):
    from bbport_party import write_json

    # The shared secret bootstraps identities. The existing per-profile homes
    # keep their identities and journals when other players restart.
    secret = bytes.fromhex(cfg['secret'])
    offers = [local_identity(member, secret, entry['profile'])
              for member, entry in zip(cfg['members'], entries)]
    directory = profile / 'coop/local-test'
    config_path, peers_path = directory/'home.json', directory/'peers.json'
    write_json(peers_path, offers)
    env.update(BB_PARTY_CONFIG=str(config_path), BB_PARTY_PEERS=str(peers_path))


def main(bbgl):
    import bbport_local_test as local
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--player', type=int, choices=(1, 2, 3))
    parser.add_argument('--config')
    args = parser.parse_args()
    port = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parents[1]
    # The observer is opt-in for this development install; it never blocks a game.
    if (port / 'tools/log-observer.json').is_file():
        try:
            observer_start = runpy.run_path(str(port / 'scripts/start_log_observer.py'))['start']
            for player in ((1, 2, 3) if args.all else (args.player,)):
                if player is not None:
                    observer_start(port, player)
        except Exception as error:
            import warnings
            warnings.warn(f'Log observer unavailable: {error}', RuntimeWarning)
    if args.all:
        return local.run_three(port)
    if args.player is None or not args.config:
        parser.error('Use --all or --player N --config PATH')
    entries = local.profiles(Path(os.environ['LOCALAPPDATA']))
    cfg, expected = local.configuration(Path(os.environ['LOCALAPPDATA']))
    if Path(args.config).resolve() != expected.resolve():
        raise ValueError('Unexpected local test group configuration')
    entry = entries[args.player-1]
    env = local.launch_environment(bbgl, entry, expected)
    if not env.get('BB_LOCAL_PARTY_RUN'):
        individual_party(env, cfg, entries, entry['profile'])
    os.environ.update(env)
    sys.argv = [str(port / 'run.py')]
    return runpy.run_path(str(port / 'run.py'), run_name='__main__')


if 'BBGL_RUNTIME' in globals():
    try:
        result = main(BBGL_RUNTIME)
        if isinstance(result, int):
            sys.exit(result)
    except Exception:
        profile = Path(os.environ.get('BBGL_PROFILE_DIR') or Path(os.environ['LOCALAPPDATA']) / 'Bloodborne Game Launcher')
        target = profile / 'coop/local-test/start-error.log'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(traceback.format_exc(), encoding='utf-8')
        raise
