import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
import bbport_paths


class ProfileMigrationTests(unittest.TestCase):
    def test_rename_preserves_saves_and_cache_and_rewrites_only_profile_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            local = Path(folder)
            old = local / 'bbgl'
            (old / 'user/cache').mkdir(parents=True)
            (old / 'user/save.bin').write_bytes(b'save')
            (old / 'user/cache/shader.bin').write_bytes(b'shader')
            (old / 'settings.json').write_text(json.dumps({
                'user_dir': str(old / 'user'), 'mods_dir': str(local / 'external-mods'),
                'play_mode': 'huntersdream', 'thd_token': 'obsolete', 'online_pool': 'huntersdream'}))
            with patch.dict(os.environ, {'LOCALAPPDATA': folder, 'APPDATA': str(local / 'roaming')}):
                root = bbport_paths.profile_dir()
                self.assertEqual(root, local / 'Bloodborne Game Launcher')
                self.assertFalse(old.exists())
                self.assertEqual((root / 'user/save.bin').read_bytes(), b'save')
                self.assertEqual((root / 'cache/shader.bin').read_bytes(), b'shader')
                settings = json.loads((root / 'settings.json').read_text())
                self.assertEqual(settings['user_dir'], str(root / 'user'))
                self.assertEqual(settings['mods_dir'], str(local / 'external-mods'))
                self.assertEqual(settings['play_mode'], 'offline')
                self.assertNotIn('thd_token', settings)
                (root / 'user/save.bin').write_bytes(b'new save')
                bbport_paths.profile_dir()
                self.assertEqual((root / 'user/save.bin').read_bytes(), b'new save')

    def test_merge_never_overwrites_existing_data(self):
        with tempfile.TemporaryDirectory() as folder:
            local = Path(folder)
            old, new = local / 'bbgl', local / 'Bloodborne Game Launcher'
            old.mkdir()
            new.mkdir()
            (old / 'save').write_bytes(b'old')
            (new / 'save').write_bytes(b'current')
            (old / 'another-save').write_bytes(b'keep')
            with patch.dict(os.environ, {'LOCALAPPDATA': folder, 'APPDATA': str(local / 'roaming')}):
                bbport_paths.profile_dir()
                self.assertEqual((new / 'save').read_bytes(), b'current')
                self.assertEqual((new / 'another-save').read_bytes(), b'keep')


if __name__ == '__main__':
    unittest.main()
