"""Render the actual Mods workspace with long Russian names and network results."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'launcher'), str(ROOT / 'scripts')]
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtCore import QObject, QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow
from PySide6.QtWidgets import QApplication
import bbport_launcher_win as core
from bbport_launcher_backend import LauncherBackend


class ModWorkspaceTests(unittest.TestCase):
    def test_russian_workspace_renders(self):
        app = QApplication.instance() or QApplication([])
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.object(core, 'PORT_DIR', root), patch.object(core, 'DATA_DIR', root), \
                 patch.object(core, 'CONFIG_FILE', root / 'settings.json'), \
                 patch.object(LauncherBackend, 'start_background_checks'), \
                 patch.dict(core.APP_DEFAULTS, ui_language='ru'), \
                 patch.dict(os.environ, BB_CONFIG=str(root / 'bbport.ini')):
                backend = LauncherBackend()
                backend._party_timer.stop()
                backend._party_network_timer.stop()
                backend._addons_timer.stop()
                backend._mods = [{'name': 'Меч охотника — улучшенные модели оружия и доспехов для совместного прохождения', 'enabled': True}]
                backend._network_mods = [dict(name='Новые костюмы охотника', player='Hunter', peer='P1', size=25000000,
                                             status='missing', digest='a' * 64),
                                        dict(name='Меч охотника', player='Hunter', peer='P1', size=50000000,
                                             status='conflict', digest='b' * 64)]
                backend._network_mods.append(dict(name=backend._mods[0]['name'], player='Hunter', peer='P1', size=1,
                                                   status='same', enabled=True, digest='c' * 64))
                rows = backend.modTableRows
                self.assertEqual(len(rows), 3)
                self.assertEqual(rows[0]['status'], '')
                self.assertFalse(rows[1]['enabled'])
                self.assertEqual(rows[1]['status'], 'missing')
                warnings_emitted = []
                backend.modSyncWarning.connect(lambda: warnings_emitted.append(True))
                backend.app['play_mode'] = 'coop'
                with patch.object(backend, 'refresh_addons'), patch.object(backend, 'coopPlay') as launch:
                    backend.playSelected()
                    launch.assert_not_called()
                    self.assertEqual(warnings_emitted, [True])
                    backend.playUnsynchronized()
                    launch.assert_called_once()
                    launch.reset_mock()
                    backend._network_mods = [backend._network_mods[-1]]
                    backend.playSelected()
                    launch.assert_called_once()
                    self.assertEqual(warnings_emitted, [True])
                    launch.reset_mock()
                    backend._network_mods[0]['enabled'] = False
                    backend.playSelected()
                    launch.assert_not_called()
                    self.assertEqual(warnings_emitted, [True, True])
                backend._network_mods = rows[1:]
                engine = QQmlApplicationEngine()
                engine.rootContext().setContextProperty('launcher', backend)
                warnings = []
                engine.warnings.connect(lambda rows: warnings.extend(str(row) for row in rows))
                qml = b'''import QtQuick
import QtQuick.Window
Window { width: 1280; height: 1100; visible: true
SettingsWorkspace { anchors.fill: parent; category: "Mods & Patches"; section: "Installed mods" }
}'''
                engine.loadData(qml, QUrl.fromLocalFile(str(ROOT / 'launcher/qml/ModSharePreview.qml')))
                self.assertTrue(engine.rootObjects())
                window = engine.rootObjects()[0]
                try:
                    for _ in range(30):
                        app.processEvents()
                    target = ROOT / 'out/mods-ui-preview.png'
                    self.assertTrue(window.grabWindow().save(str(target)))
                    table = window.findChild(QObject, 'installedModsTable')
                    self.assertIsNotNone(table)
                    for width in (1280, 1024):
                        window.setWidth(width)
                        for _ in range(10):
                            app.processEvents()
                        self.assertGreater(table.property('nameWidth'), 160)
                        self.assertGreater(table.property('height'), 80)
                    self.assertTrue(window.grabWindow().save(str(ROOT/'out/mods-ui-preview-narrow.png')))
                    main = QQmlApplicationEngine()
                    main.rootContext().setContextProperty('launcher', backend)
                    main.warnings.connect(lambda rows: warnings.extend(str(row) for row in rows))
                    main.load(QUrl.fromLocalFile(str(ROOT / 'launcher/qml/Main.qml')))
                    self.assertTrue(main.rootObjects())
                    main_window = main.rootObjects()[0]
                    backend.modSyncWarning.emit()
                    for _ in range(15):
                        app.processEvents()
                    dialog = main_window.findChild(QObject, 'modSyncWarningDialog')
                    self.assertTrue(dialog.property('visible'))
                    self.assertTrue(main_window.grabWindow().save(str(ROOT/'out/mods-warning-preview.png')))
                    main_window.close()
                    main.deleteLater()
                    errors = [w for w in warnings if any(s in w for s in ('ReferenceError', 'TypeError', 'Binding loop', 'Cannot assign'))]
                    self.assertEqual(errors, [])
                finally:
                    window.close()
                    engine.deleteLater()
                    app.processEvents()
                    backend.shutdown_coop()


if __name__ == '__main__':
    unittest.main()
