"""Qt Quick front end for the Windows Bloodborne launcher."""
from pathlib import Path
import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtWidgets import QApplication

from bbport_launcher_backend import LauncherBackend
import bbport_launcher_backend

def run_ui(route=None):
    """ROUTE comes from bbport_startup.route(); without one the launcher opens on Home."""
    QQuickStyle.setStyle('Basic')
    app = QApplication(sys.argv)
    app.setApplicationName('Bloodborne Game Launcher')
    icon_path = (Path(sys.executable).resolve().parent / 'launcher' / 'assets' / 'hunter-icon.ico') if getattr(sys, 'frozen', False) else (Path(__file__).resolve().parent / 'assets' / 'hunter-icon.ico')
    app.setWindowIcon(QIcon(str(icon_path)))
    backend = LauncherBackend(route)
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
        def close_after_launch():
            # Hosting belongs to this process. Keep it and the log reader alive
            # without a window until the game exits, then stop both servers.
            if backend.coopHosting and backend.running:
                app.setQuitOnLastWindowClosed(False)
                backend.gameFinished.connect(lambda _code, _started: app.quit())
            window.close()

        backend.closeRequested.connect(close_after_launch)
        app.aboutToQuit.connect(backend.shutdown_coop)
        app.setQuitOnLastWindowClosed(True)

    open_launcher()
    return app.exec()

if __name__ == "__main__":
    sys.exit(run_ui())
