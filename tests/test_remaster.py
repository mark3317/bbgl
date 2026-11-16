"""The two archives form one install and the patch wins on overlapping assets."""

from io import BytesIO
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from paths import ROOT

sys.path.insert(0, str(ROOT / 'launcher'))
import bbport_launcher_win as core
import bbport_remaster as remaster
from mods import build_manifest


class RemasterTests(unittest.TestCase):
    def setUp(self):
        storage = tempfile.TemporaryDirectory(dir=ROOT / 'out' if (ROOT / 'out').is_dir() else ROOT)
        self.addCleanup(storage.cleanup)
        self.root = Path(storage.name)
        self.base = self.archive('main.zip', {'main/DVDROOT_PS4/Map/M24.tpf': b'base',
                                             'main/DVDROOT_PS4/Map/original.tpf': b'unchanged by patch'})
        self.patch = self.archive('patch.zip', {'map/m24.tpf': b'patch 1.13'})
        self.sizes = (self.base.stat().st_size, self.patch.stat().st_size)
        sizes = patch.multiple(remaster, FILES=((3116, self.sizes[0]), (3379, self.sizes[1])),
                               TOTAL_BYTES=sum(self.sizes))
        sizes.start()
        self.addCleanup(sizes.stop)

    def archive(self, name, entries):
        target = self.root / name
        with ZipFile(target, 'w') as archive:
            for path, contents in entries.items():
                archive.writestr(path, contents)
        return target

    def test_import_and_install_patch_as_one_layer(self):
        archives = remaster.match_archives((self.patch, self.base))
        self.assertEqual(archives, (self.base, self.patch))
        folder = remaster.directory(self.root / 'mods')
        updates = []
        remaster.install(folder, archives, lambda fraction, status: updates.append((fraction, status)), threading.Event())
        self.assertTrue(self.base.is_file() and self.patch.is_file())
        layer = remaster.installed(folder)
        self.assertEqual((layer / 'dvdroot_ps4/map/m24.tpf').read_bytes(), b'patch 1.13')
        self.assertTrue((layer / 'dvdroot_ps4/map/original.tpf').is_file())
        self.assertIn('Applying PATCH 1.13…', [status for _, status in updates])
        self.assertEqual([p for p, _ in updates], sorted(p for p, _ in updates))
        self.assertEqual(updates[-1][0], 1)

        game = self.root / 'game'
        original = game / 'dvdroot_ps4/map/m24.tpf'
        original.parent.mkdir(parents=True)
        original.write_bytes(b'game original')
        output = self.root / 'launch'
        output.mkdir()
        settings = dict(core.APP_DEFAULTS, mods_dir=str(folder.parent), remaster_enabled=True)
        env = core.game_environment(settings)
        self.assertEqual(Path(env['BB_REMASTER_LAYER']), layer)
        build_manifest(game, output, [(layer.name, layer)])
        self.assertIn((layer / 'dvdroot_ps4/map/m24.tpf').as_posix(), (output / 'mod-files.tsv').read_text(encoding='utf-8'))
        self.assertEqual(original.read_bytes(), b'game original')
        core.apply_graphics_preset('ultra', {}, settings)
        self.assertNotIn('BB_REMASTER_LAYER', core.game_environment(settings))

    def test_failed_patch_does_not_publish_base_and_can_retry(self):
        broken = self.root / 'same-size-corrupt.zip'
        broken.write_bytes(b'0' * self.sizes[1])
        folder = remaster.directory(self.root / 'mods')
        with self.assertRaisesRegex(ValueError, 'Could not read'):
            remaster.install(folder, (self.base, broken), lambda *_: None, threading.Event())
        self.assertIsNone(remaster.installed(folder))
        remaster.install(folder, (self.base, self.patch), lambda *_: None, threading.Event())
        self.assertTrue(remaster.installed(folder))

    def test_traversal_is_refused(self):
        archive = self.archive('unsafe.zip', {'../../escaped.txt': b'escape', 'map/texture.tpf': b'file'})
        with self.assertRaises(ValueError):
            remaster._extract(archive, self.root / 'stage', lambda *_: None, threading.Event())
        self.assertFalse((self.root.parent / 'escaped.txt').exists())

    def test_download_resumes_and_counts_both_archives(self):
        folder = remaster.directory(self.root / 'mods')
        folder.mkdir(parents=True)
        main = self.base.read_bytes()
        (folder / '3116.part').write_bytes(main[:32])
        requests = []

        def serve(request, timeout):
            requests.append(request)
            first = request.get_header('Range') == 'bytes=32-'
            stream = BytesIO(main[32:] if first else self.patch.read_bytes())
            stream.status = 206 if first else 200
            stream.headers = {'Content-Range': f'bytes 32-{len(main) - 1}/{len(main)}'} if first else {}
            return stream

        updates = []
        with patch.object(remaster, '_download_url', side_effect=lambda file_id, _: f'https://example.test/{file_id}'), \
             patch.object(remaster, 'urlopen', side_effect=serve):
            remaster.download(folder, 'test-key', lambda *status: updates.append(status), threading.Event())
        self.assertEqual([r.full_url.rsplit('/', 1)[-1] for r in requests], ['3116', '3379'])
        self.assertFalse(requests[1].has_header('Range'))
        self.assertIn((remaster.DOWNLOAD_PORTION * len(main) / sum(self.sizes), 'Downloading PATCH 1.13…'), updates)
        self.assertEqual([p.read_bytes() for p in remaster.cached_archives(folder)], [main, self.patch.read_bytes()])

    @unittest.skipUnless(os.name == 'nt', 'Windows uses the bundled system bsdtar')
    def test_windows_tar_unpacks_7z_and_reports_progress(self):
        source = self.root / 'source'
        source.mkdir()
        (source / 'file.tpf').write_bytes(b'texture')
        archive = self.root / 'example.7z'
        subprocess.run([remaster._tar_command(), '--format', '7zip', '-cf', str(archive), '-C', str(source), '.'],
                       check=True, capture_output=True)
        progress = []
        remaster._extract(archive, self.root / 'stage', progress.append, threading.Event())
        self.assertEqual((self.root / 'stage/file.tpf').read_bytes(), b'texture')
        self.assertTrue(progress)

    def test_launcher_remaster_row_install_progress_and_switch(self):
        os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
        from PySide6.QtCore import QObject, QPoint, Qt, QUrl
        from PySide6.QtQml import QQmlApplicationEngine
        from PySide6.QtQuick import QQuickItem
        from PySide6.QtQuickControls2 import QQuickStyle
        from PySide6.QtTest import QTest
        from PySide6.QtWidgets import QApplication
        from bbport_launcher_backend import LauncherBackend, QFileDialog

        QQuickStyle.setStyle('Basic')
        app = QApplication.instance() or QApplication([])
        release_install = threading.Event()
        real_install = remaster.install

        def install(*args):
            if not release_install.wait(5):
                raise TimeoutError('Test did not release the installation')
            real_install(*args)

        with patch.multiple(core, PORT_DIR=self.root, DATA_DIR=self.root, CONFIG_DIR=self.root,
                            CONFIG_FILE=self.root / 'settings.json'), \
             patch.dict(core.APP_DEFAULTS, ui_language='ru'), \
             patch.dict(os.environ, BB_CONFIG=str(self.root / 'bbport.ini'), BB_NEXUS_API_KEY=''), \
             patch.object(LauncherBackend, 'start_background_checks'), \
             patch.object(QFileDialog, 'getOpenFileNames', return_value=([str(self.base), str(self.patch)], '')), \
             patch.object(remaster, 'install', side_effect=install):
            backend = LauncherBackend()
            for timer in (backend._party_timer, backend._party_network_timer, backend._addons_timer):
                timer.stop()
            engine = QQmlApplicationEngine()
            warnings = []
            engine.warnings.connect(lambda rows: warnings.extend(str(row) for row in rows))
            engine.rootContext().setContextProperty('launcher', backend)
            engine.load(QUrl.fromLocalFile(str(ROOT / 'launcher/qml/Main.qml')))
            self.assertTrue(engine.rootObjects(), warnings)
            window = engine.rootObjects()[0]
            workspace = window.findChild(QObject, 'settingsWorkspace')
            window.setWidth(1050)
            window.setHeight(650)
            window.setProperty('page', 'Settings')
            workspace.openAt('Visuals', 'Image effects', '')
            QTest.qWait(100)

            def visual_items(item):
                yield item
                for child in item.childItems():
                    yield from visual_items(child)

            def find(name):
                item = window.findChild(QQuickItem, name)
                self.assertIsNotNone(item, name)
                return item

            def click(item):
                self.assertTrue(item.property('visible') and item.property('enabled'))
                point = item.mapToScene(item.boundingRect().center())
                QTest.mouseClick(window, Qt.LeftButton, Qt.NoModifier, QPoint(round(point.x()), round(point.y())))
                QTest.qWait(120)

            try:
                lod = next(item for item in visual_items(window.contentItem())
                           if item.property('settingKey') == 'model_lod')
                toggle = find('remasterSwitch')
                self.assertFalse(toggle.isVisible())
                self.assertTrue(lod.isVisible())
                download = find('remasterDownload')
                self.assertEqual(download.property('text'), 'Скачать')
                with patch('bbport_launcher_backend.webbrowser.open') as browser:
                    click(download)
                    browser.assert_called_once_with(remaster.PAGE)
                choose = find('remasterImport')
                self.assertEqual(choose.property('text'), 'Выбрать')
                click(choose)
                self.assertTrue(find('remasterProgress').property('visible'))
                self.assertFalse(toggle.isVisible())
                release_install.set()
                for _ in range(60):
                    if not backend.remasterBusy:
                        break
                    time.sleep(0.05)
                    app.processEvents()
                QTest.qWait(150)
                self.assertTrue(backend.remasterInstalled, backend.remasterStatus)
                self.assertFalse(backend.remasterSelected)
                self.assertTrue(toggle.isVisible())
                self.assertFalse(download.isVisible() or choose.isVisible())
                click(toggle)
                self.assertTrue(backend.remasterSelected)
                self.assertFalse(lod.isVisible())
                click(toggle)
                self.assertFalse(backend.remasterSelected)
                self.assertTrue(lod.isVisible())
                self.assertFalse(warnings)
            finally:
                release_install.set()
                window.close()
                backend.shutdown_coop()
                engine.deleteLater()
                app.processEvents()
