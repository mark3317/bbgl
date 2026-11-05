"""Real Windows process/job/pipe regressions for the hidden launcher."""
import os
from pathlib import Path
import subprocess
import sys
import unittest


@unittest.skipUnless(sys.platform == 'win32', 'Windows game jobs')
class GameProcessLifetimeTests(unittest.TestCase):
    def run_case(self, scenario):
        code = r'''
import os, subprocess, sys, tempfile, threading, time
from pathlib import Path
from unittest.mock import patch
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtQuick import QQuickWindow
from PySide6.QtWidgets import QApplication
from bbport_launcher_backend import LauncherBackend
from bbport_launcher_qml import manage_window_lifetime
import bbport_launcher_win as core
class Backend(QObject):
    _outputLine = Signal(str)
    _gameExited = Signal(int)
    gameFinished = Signal(int, bool)
    _read_output = LauncherBackend._read_output
    _wait_for_game = LauncherBackend._wait_for_game
    _queue_output = lambda self, line: self._outputLine.emit(line)
app = QApplication([])
window = QQuickWindow()
window.show()
backend = Backend()
backend.running = True
manage_window_lifetime(app, backend, window)
events = []
keeper = None
with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    backend.app = {'user_dir': temporary}
    env = dict(os.environ)
    release = root / 'release'
    if SCENARIO == 'restart':
        successor = root / 'successor.py'
        successor.write_text("import time\nfrom pathlib import Path\nwhile not Path(" + repr(str(release)) + ").exists(): time.sleep(.02)\nprint('successor tail', flush=True)\n")
        command = "import subprocess,sys,time; time.sleep(.3); subprocess.Popen([sys.executable," + repr(str(successor)) + "]); print('root exited', flush=True)"
    else:
        command = "import time; print('Entering original x86-64 code', flush=True); time.sleep(.3); print('final tail', flush=True)"
    if SCENARIO == 'inherited_writer':
        # A writer outside the game's job keeps EOF open after the game exits.
        read_fd, write_fd = os.pipe()
        keeper = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], stdout=write_fd, env=env)
        process = subprocess.Popen([sys.executable, '-c', command], stdout=write_fd, env=env)
        os.close(write_fd)
        process.stdout = os.fdopen(read_fd, 'rb')
    else:
        process = subprocess.Popen([sys.executable, '-c', command], stdout=subprocess.PIPE, env=env)
    job = core.GameJob(process)
    assert job.handle, 'test requires an assigned Windows job'
    def line(text):
        events.append(text.strip())
    backend._outputLine.connect(line)
    def finished(code):
        assert code == 0
        if SCENARIO == 'restart':
            assert release.exists(), 'launcher exited while successor was running'
        backend.running = False
        events.append('finished')
        backend.gameFinished.emit(code, True)
    backend._gameExited.connect(finished)
    window.close()
    reader = threading.Thread(target=backend._read_output, args=(process,), daemon=True)
    waiter = threading.Thread(target=backend._wait_for_game, args=(process, job, reader), daemon=True)
    def timeout():
        events.append('TIMEOUT')
        app.quit()
    QTimer.singleShot(8000, timeout)
    if SCENARIO == 'restart':
        def release_successor():
            assert process.poll() == 0
            assert backend.running
            release.write_text('go')
        QTimer.singleShot(1200, release_successor)
    started = time.monotonic()
    try:
        with patch.object(core, 'open_run_log', side_effect=OSError('log unavailable')) if SCENARIO == 'log_failure' else patch.object(core, 'MAX_LOG_LINES', core.MAX_LOG_LINES):
            reader.start()
            waiter.start()
            app.exec()
        assert 'TIMEOUT' not in events, events
        assert 'finished' in events, events
        if SCENARIO == 'inherited_writer':
            assert keeper.poll() is None
            assert time.monotonic() - started < 5
        if SCENARIO == 'log_failure':
            assert 'final tail' in events, events
            assert any('Could not open game log' in e for e in events), events
        else:
            log = next(root.glob('run_*.log')).read_text()
            assert ('successor tail' if SCENARIO == 'restart' else 'final tail') in log, log
    finally:
        if keeper is not None:
            keeper.terminate()
            keeper.wait()
        job.terminate()
        waiter.join(3)
        reader.join(3)
        job.close()
        process.stdout.close()
print('PASS')
'''.replace('SCENARIO', repr(scenario))
        env = dict(os.environ, QT_QPA_PLATFORM='offscreen',
                   PYTHONPATH=str(Path(__file__).resolve().parents[1] / 'launcher'))
        result = subprocess.run([sys.executable, '-c', code], env=env,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(result.stdout.strip(), 'PASS')

    def test_exit_does_not_wait_for_unrelated_pipe_writer(self):
        self.run_case('inherited_writer')

    def test_log_failure_still_drains_output_and_finishes(self):
        self.run_case('log_failure')

    def test_restart_successor_keeps_launcher_and_log_alive(self):
        self.run_case('restart')
