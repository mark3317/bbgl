import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
import bbport_launcher_win as core




class InstallUpdateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def test_backslash_zip_unpacks_into_folders(self):
        archive = self.root / 'update.zip'
        with core.zipfile.ZipFile(archive, 'w') as package:
            for name, data in (('Bloodborne Game Launcher\\_internal\\_ssl.pyd', b'ssl'),
                               ('Bloodborne Game Launcher/scripts/game_check.py', b'check'),
                               ('Bloodborne Game Launcher\\..\\..\\outside.txt', b'no')):
                entry = core.zipfile.ZipInfo('x')
                entry.filename = name  # as written, without zipfile's separator clean-up
                package.writestr(entry, data)
        core.extract_update(archive, self.root / 'new')
        self.assertEqual((self.root / 'new/Bloodborne Game Launcher/_internal/_ssl.pyd').read_bytes(), b'ssl')
        self.assertEqual((self.root / 'new/Bloodborne Game Launcher/scripts/game_check.py').read_bytes(), b'check')
        self.assertFalse((self.root / 'outside.txt').exists())

    def test_new_files_arrive_and_player_files_stay(self):
        new, old = self.root / 'new', self.root / 'old'
        for path, text in (('run.py', 'new'), ('scripts/game_check.py', 'new'), ('user/save', 'packaged')):
            (new / path).parent.mkdir(parents=True, exist_ok=True)
            (new / path).write_text(text)
        for path, text in (('run.py', 'old'), ('user/save', 'mine'), ('bbport.ini', 'mine')):
            (old / path).parent.mkdir(parents=True, exist_ok=True)
            (old / path).write_text(text)
        self.assertEqual(core.copy_release(new, old), [])
        self.assertEqual((old / 'run.py').read_text(), 'new')
        self.assertEqual((old / 'scripts/game_check.py').read_text(), 'new')
        self.assertEqual((old / 'user/save').read_text(), 'mine')
        self.assertEqual((old / 'bbport.ini').read_text(), 'mine')

    @unittest.skipUnless(sys.platform == 'win32', 'an open file blocks deleting it only on Windows')
    def test_update_folder_kept_while_installing(self):
        folder = self.root / 'bbport-update'
        (folder / 'new/Bloodborne Game Launcher/scripts').mkdir(parents=True)
        with patch.object(core, 'UPDATE_DIR', folder):
            with open(core.update_installing_mark(), 'w'):
                self.assertFalse(core.remove_update_folder())
                self.assertTrue((folder / 'new/Bloodborne Game Launcher/scripts').is_dir())
            self.assertTrue(core.remove_update_folder())
            self.assertFalse(folder.exists())


if __name__ == '__main__':
    unittest.main()
