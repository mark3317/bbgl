"""Optional developer-only hook. The installed config points at the local checkout."""
import json
import os
from pathlib import Path
import subprocess
import sys
import warnings


def start(install, player, parent_pid=None):
    config = Path(install) / 'tools/log-observer.json'
    if not config.is_file():
        return False
    try:
        value = json.loads(config.read_text(encoding='utf-8-sig'))
        if not value.get('enabled'):
            return False
        command = [value['pythonw'], value['script'], 'request', '--player', str(player),
                   '--parent-pid', str(parent_pid or os.getpid())]
        options = {'stdin': subprocess.DEVNULL, 'stdout': subprocess.DEVNULL,
                   'stderr': subprocess.DEVNULL, 'cwd': str(Path(value['script']).resolve().parents[2])}
        if os.name == 'nt':
            options['creationflags'] = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
        subprocess.Popen(command, **options)
        return True
    except (OSError, ValueError, KeyError) as error:
        warnings.warn(f'Log observer could not start: {error}', RuntimeWarning)
        return False
