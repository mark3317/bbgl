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
from PySide6.QtCore import QObject, QPoint, QUrl, Qt
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
import bbport_launcher_win as core
from bbport_launcher_backend import LauncherBackend


class ModWorkspaceTests(unittest.TestCase):
    def test_russian_workspace_renders(self):
        app = QApplication.instance() or QApplication([])
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.object(core, 'PORT_DIR', root), patch.object(core, 'DATA_DIR', root), \
                 patch.object(core, 'CONFIG_DIR', root), \
                 patch.object(core, 'CONFIG_FILE', root / 'settings.json'), \
                 patch.object(LauncherBackend, 'start_background_checks'), \
                 patch.dict(core.APP_DEFAULTS, ui_language='ru'), \
                 patch.dict(os.environ, BB_CONFIG=str(root / 'bbport.ini')):
                backend = LauncherBackend()
                backend.app.update(mods_dir='D:/Games/Bloodborne/mods', patches_dir='D:/Games/Bloodborne/patches')
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
                backend.app.update(play_mode='coop', coop_name='Hunter')
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
                mod_names = ['Diamond Sword', 'Меч охотника — улучшенные модели оружия и доспехов для совместного прохождения',
                             'Тёмные доспехи охотника']
                mods_dir = root / 'mods'
                for name in mod_names:
                    (mods_dir / name / 'parts').mkdir(parents=True)
                backend.app['mods_dir'] = str(mods_dir)
                backend.refresh_addons()
                engine = QQmlApplicationEngine()
                engine.rootContext().setContextProperty('launcher', backend)
                warnings = []
                engine.warnings.connect(lambda rows: warnings.extend(str(row) for row in rows))
                engine.load(QUrl.fromLocalFile(str(ROOT / 'launcher/qml/Main.qml')))
                self.assertTrue(engine.rootObjects())
                window: QQuickWindow = engine.rootObjects()[0]
                window.resize(1200, 760)
                window.setProperty('page', 'Home')

                def click(item):
                    self.assertTrue(item.isVisible() and item.isEnabled())
                    point = item.mapToScene(item.boundingRect().center())
                    QTest.mouseClick(window, Qt.LeftButton, Qt.NoModifier, QPoint(round(point.x()), round(point.y())))
                    QTest.qWait(100)

                def items(root):
                    yield root
                    for child in root.childItems():
                        yield from items(child)

                def find(name):
                    item = next((item for item in items(window.contentItem()) if item.objectName() == name), None)
                    if item is None:
                        item = window.findChild(QObject, name)
                    self.assertIsNotNone(item, name)
                    return item

                try:
                    QTest.qWait(200)
                    trophy, rail_mods = find('railTrophies'), find('railMods')
                    self.assertEqual(rail_mods.y(), trophy.y() + trophy.height())
                    click(rail_mods)
                    self.assertEqual(window.property('page'), 'Mods')
                    table = find('installedModsTable')
                    up = [item for item in items(table) if item.objectName() == 'moveModUp']
                    down = [item for item in items(table) if item.objectName() == 'moveModDown']
                    self.assertEqual([item.isEnabled() for item in up], [False, True, True])
                    self.assertEqual([item.isEnabled() for item in down], [True, True, False])
                    for upper, lower in zip(up, down):
                        self.assertEqual(upper.mapToScene(QPoint()).x(), lower.mapToScene(QPoint()).x())
                        self.assertLess(upper.mapToScene(QPoint()).y(), lower.mapToScene(QPoint()).y())
                    click(up[1])
                    self.assertEqual([mod['name'] for mod in backend.contentMods], [mod_names[1], mod_names[0], mod_names[2]])
                    click(find('moveModDown'))
                    self.assertEqual([mod['name'] for mod in backend.contentMods], mod_names)
                    QTest.mouseMove(window, QPoint(window.width() - 15, window.height() - 15))
                    QTest.qWait(100)
                    target = ROOT / 'out/mods-ui-preview.png'
                    self.assertTrue(window.grabWindow().save(str(target)))
                    self.assertTrue(table.isVisible())
                    mods_switch = find('modsEnabledSwitch')
                    self.assertTrue(mods_switch.property('checked'))
                    click(mods_switch)
                    self.assertFalse(backend.modsEnabled)
                    self.assertTrue(backend.modTableRows[1]['enabled'])
                    backend.setValue('mods_enabled', True)
                    self.assertTrue(mods_switch.property('checked'))
                    for width in (1280, 1050):
                        window.setWidth(width)
                        QTest.qWait(50)
                        self.assertGreater(table.property('nameWidth'), 160)
                        self.assertGreater(table.property('height'), 80)
                    self.assertTrue(window.grabWindow().save(str(ROOT/'out/mods-ui-preview-narrow.png')))
                    window.setWidth(1200)
                    click(find('cheatsTab'))
                    self.assertFalse(table.isVisible())
                    self.assertEqual(find('modsPage').property('section'), 'Cheats')
                    self.assertTrue(window.grabWindow().save(str(ROOT/'out/mods-cheats-preview.png')))
                    click(find('installedModsTab'))
                    click(find('modsSettingsButton'))
                    self.assertEqual(window.property('page'), 'Settings')
                    settings = find('settingsWorkspace')
                    self.assertEqual(settings.property('section'), 'Mod settings')
                    self.assertFalse(table.isVisible())
                    self.assertFalse(mods_switch.isVisible())
                    self.assertEqual(backend.categorySections('Mods & Patches'), ['Mod settings', 'Built-in enhancements'])
                    self.assertTrue(window.grabWindow().save(str(ROOT/'out/mods-settings-preview.png')))
                    search = next(item for item in items(settings)
                                  if item.property('placeholderText') == backend.tr('Find a setting'))
                    search.setProperty('text', 'free camera')
                    QTest.qWait(100)
                    cheat = backend.searchSettings('free camera')[0]
                    self.assertEqual(cheat['category'], 'Mods')
                    result = next(item for item in items(settings) if item.isVisible() and item.property('label') == cheat['label'])
                    click(result)
                    self.assertEqual(window.property('page'), 'Mods')
                    self.assertEqual(find('modsPage').property('section'), 'Cheats')
                    self.assertGreater(find('modsScroll').property('contentY'), 0)
                    window.setProperty('page', 'Home')
                    backend.modSyncWarning.emit()
                    QTest.qWait(100)
                    dialog = find('modSyncWarningDialog')
                    self.assertTrue(dialog.property('visible'))
                    self.assertTrue(window.grabWindow().save(str(ROOT/'out/mods-warning-preview.png')))
                    click(find('modWarningSettings'))
                    self.assertEqual(window.property('page'), 'Mods')
                    self.assertTrue(table.isVisible())
                    errors = [w for w in warnings if any(s in w for s in ('ReferenceError', 'TypeError', 'Binding loop', 'Cannot assign'))]
                    self.assertEqual(errors, [])
                finally:
                    window.close()
                    engine.deleteLater()
                    app.processEvents()
                    backend.shutdown_coop()


if __name__ == '__main__':
    unittest.main()
