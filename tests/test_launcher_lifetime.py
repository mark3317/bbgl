"""Exercise Qt's real event loop and window closing in isolated processes."""
import os
from pathlib import Path
import subprocess
import sys
import unittest


class LauncherLifetimeTests(unittest.TestCase):
    def run_case(self, running, finish_while_visible=False):
        code = '''
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickWindow
from bbport_launcher_qml import manage_window_lifetime
class Backend(QObject):
    gameFinished = Signal(int, bool)
backend = Backend()
backend.running = RUNNING
app = QApplication([])
window = QQuickWindow()
window.show()
manage_window_lifetime(app, backend, window)
events = []
def finish():
    events.append('finished')
    backend.running = False
    backend.gameFinished.emit(0, True)
def close():
    events.append('closed')
    window.close()
def timeout():
    events.append('timeout')
    app.quit()
QTimer.singleShot(20, finish if VISIBLE else close)
QTimer.singleShot(150, close if VISIBLE else finish)
QTimer.singleShot(2000, timeout)
app.exec()
print(','.join(events))
'''.replace('RUNNING', repr(running)).replace('VISIBLE', repr(finish_while_visible))
        env = dict(os.environ, QT_QPA_PLATFORM='offscreen',
                   PYTHONPATH=str(Path(__file__).resolve().parents[1] / 'launcher'))
        result = subprocess.run([sys.executable, '-c', code], env=env,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def test_close_without_game_exits(self):
        self.assertEqual(self.run_case(False), 'closed')

    def test_hidden_launcher_waits_for_game_then_exits(self):
        self.assertEqual(self.run_case(True), 'closed,finished')

    def test_game_exit_keeps_visible_launcher_usable(self):
        self.assertEqual(self.run_case(True, True), 'finished,closed')
