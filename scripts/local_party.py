"""BBGL --script entrypoint for an explicit three-player test on this PC."""
import argparse
import os
from pathlib import Path
import runpy
import sys
import traceback


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
