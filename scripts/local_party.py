"""BBGL --script entrypoint for an explicit three-player test on this PC."""
import argparse
import hmac
import os
from pathlib import Path
import runpy
import sys
import traceback


def individual_party(env, cfg, profile):
    from bbport_party import configuration, write_json

    # Independent Player shortcuts have no coordinator keeping a closed
    # game's voter alive. Use the normal host-owned worlds on loopback.
    offers = []
    for member in cfg['members']:
        who = member['id']
        seed = hmac.digest(bytes.fromhex(cfg['secret']), who.encode('ascii'), 'sha256').hex()
        offers.append(dict(member, name=who, seed=seed))
    own = next(peer for peer in offers if peer['id'] == env['BB_PARTY_MEMBER'])
    home = configuration([own])
    home['members'][0].update(port=own['port'], p2p=own['p2p'])
    home.update(mode='dynamic-worlds-v1', identity=own)
    directory = profile / 'coop/local-test'
    config_path, peers_path = directory/'home.json', directory/'peers.json'
    write_json(config_path, home)
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
        individual_party(env, cfg, entry['profile'])
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
