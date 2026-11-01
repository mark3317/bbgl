"""Qt Quick front end for the Windows Bloodborne launcher."""
from pathlib import Path
import sys

from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtWidgets import QApplication

from bbport_launcher_backend import LauncherBackend
import bbport_launcher_backend

def manage_window_lifetime(app, backend, window):
    """Keep the log reader alive only while a game owns the hidden launcher."""
    app.setQuitOnLastWindowClosed(False)

    def quit_if_idle(*_args):
        if not window.isVisible() and not backend.running:
            app.quit()

    window.visibleChanged.connect(quit_if_idle)
    backend.gameFinished.connect(quit_if_idle)
    timer = QTimer(app)
    timer.setInterval(1000)
    timer.timeout.connect(quit_if_idle)
    timer.start()
    return timer


def run_ui(route=None):
    """ROUTE comes from bbport_startup.route(); without one the launcher opens on Home."""
    QQuickStyle.setStyle('Basic')
    app = QApplication(sys.argv)
    app.setApplicationName('Bloodborne Game Launcher')
    icon_path = (Path(sys.executable).resolve().parent / 'launcher' / 'assets' / 'hunter-icon.ico') if getattr(sys, 'frozen', False) else (Path(__file__).resolve().parent / 'assets' / 'hunter-icon.ico')
    app.setWindowIcon(QIcon(str(icon_path)))
    backend = LauncherBackend(route)
    backend.finish_graphics_detection()
    app.processEvents()  # Deliver queued GPU capabilities before any combo box is created.
    if bbport_launcher_backend.RUSSIAN:
        # Qt's own texts (Yes/No, Open, Cancel in the dialogs) in Russian too.
        from PySide6.QtCore import QLibraryInfo, QTranslator
        translator = QTranslator(app)
        if translator.load('qtbase_ru', QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)):
            app.installTranslator(translator)
    backend.connect_workers()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('launcher', backend)
    qml = Path(__file__).resolve().parent / 'qml'
    if getattr(sys, 'frozen', False):
        import bbport_launcher_win as core
        qml = core.PORT_DIR / 'launcher' / 'qml'

    def load(name):
        loaded = len(engine.rootObjects())
        engine.load(QUrl.fromLocalFile(str(qml / name)))
        if len(engine.rootObjects()) == loaded:
            raise RuntimeError(f'Could not load Qt Quick launcher: {qml / name}')
        return engine.rootObjects()[-1]

    launcher_window = []

    def open_launcher(page=None, step=0):
        if launcher_window:
            return
        if page:
            backend.open_at(page, step)
        backend.start_background_checks()
        window = load('Main.qml')
        launcher_window.append(window)
        manage_window_lifetime(app, backend, window)
        def close_after_launch():
            # The pipe reader writes last_run.log and must survive window closure
            # for every game, including guests and offline play. Hosted servers
            # also stay alive until the game exits.
            window.close()

        backend.closeRequested.connect(close_after_launch)
        app.aboutToQuit.connect(backend.shutdown_coop)

    open_launcher()
    return app.exec()

if __name__ == "__main__":
    sys.exit(run_ui())
