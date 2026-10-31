import io
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import bbport_game_download as download
from package_game import package


class GameDownloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        (self.source / 'eboot.bin').write_bytes(b'example boot')
        (self.source / 'dvdroot_ps4').mkdir()
        (self.source / 'dvdroot_ps4' / 'test.dcx').write_bytes(b'assets' * 100)
        self.assets = self.root / 'assets'
        self.manifest = package(self.source, self.assets, 'https://example.test', limit=70000)
        self.install = self.root / 'launcher'
        self.install.mkdir()
        self.requests = []

    def request(self, url):
        self.requests.append(url)
        if url == download.MANIFEST_URL:
            return io.BytesIO(json.dumps(self.manifest).encode())
        return (self.assets / url.rsplit('/', 1)[1]).open('rb')

    def run_install(self, event=None):
        with patch.object(download, 'request', self.request):
            return download.install(self.install, lambda *args: None, event or threading.Event())

    def test_roundtrip_and_existing_folder(self):
        target = self.run_install()
        for source in self.source.rglob('*'):
            if source.is_file():
                self.assertEqual(source.read_bytes(), (target / source.relative_to(self.source)).read_bytes())
        with self.assertRaisesRegex(ValueError, 'already exists'):
            self.run_install()

    def test_cancellation_keeps_completed_parts_for_retry(self):
        cancel = threading.Event()
        def progress(value, message):
            if message.startswith('Unpacking'):
                cancel.set()
        with patch.object(download, 'request', self.request), self.assertRaises(download.Cancelled):
            download.install(self.install, progress, cancel)
        self.assertFalse((self.install / 'game').exists())
        self.assertFalse((self.install / '.game-installing').exists())
        self.requests.clear()
        self.run_install()
        self.assertNotIn(self.manifest['parts'][0]['url'], self.requests)

    def test_bad_checksum_never_installs(self):
        self.manifest['parts'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'checksum'):
            self.run_install()
        self.assertFalse((self.install / 'game').exists())
        with download.installation_lock(self.install / '.game-install.lock'):
            pass

    def test_unsafe_paths(self):
        for name in ('../eboot.bin', '/eboot.bin', 'C:/eboot.bin', 'a\\b', 'AUX.txt', 'a./b'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                download.safe_name(name)

    def test_lock_prevents_second_installer(self):
        with download.installation_lock(self.install / '.game-install.lock'):
            with self.assertRaisesRegex(OSError, 'already running'):
                self.run_install()

    def test_disk_full_never_installs(self):
        with patch.object(download.shutil, 'disk_usage', return_value=type('Space', (), {'free': 0})()):
            with self.assertRaisesRegex(OSError, 'free space'):
                self.run_install()
        self.assertFalse((self.install / 'game').exists())


if __name__ == '__main__':
    unittest.main()
