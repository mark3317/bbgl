import json
from pathlib import Path
import struct
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
from bbport_readiness import check_readiness
from bbport_readiness import save_title_id, trophy_snapshot

TEMP_PARENT = Path(__file__).resolve().parents[1] / 'out'


class LauncherReadinessTests(unittest.TestCase):
    def test_builtin_trophies_before_first_game_launch(self):
        TEMP_PARENT.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            root = Path(temporary)
            game = root / 'game'
            user = root / 'fresh-profile'
            pack = game / 'sce_sys/trophy/trophy00.trp'
            pack.parent.mkdir(parents=True)
            binding = game / 'sce_sys/npbind.dat'
            binding.write_bytes(b'prefix NPWR05818_00 suffix')
            for total in (34, 40):
                with self.subTest(total=total):
                    header = bytearray(96)
                    header[:4] = bytes.fromhex('DCA24D00')
                    struct.pack_into('>II', header, 16, total, 64)
                    rows = b''.join(
                        struct.pack('>32sQQI12x', f'TROP{trophy:03}.PNG'.encode(),
                                    96 + total * 64 + trophy, 1, 0)
                        for trophy in range(total)
                    )
                    pack.write_bytes(header + rows + bytes(total))
                    snapshot = trophy_snapshot(game, user, russian=True)
                    self.assertEqual(snapshot['progress'], {'earned': 0, 'total': total})
                    self.assertTrue(snapshot['hasMetadata'])
                    self.assertTrue(snapshot['builtIn'])
                    entries = {entry['id']: entry for entry in snapshot['entries']}
                    self.assertEqual(entries[5]['name'], 'Сущность охотника')
                    self.assertTrue(entries[5]['description'])
                    self.assertEqual((entries[14]['name'], entries[14]['description'], entries[14]['secret']),
                                     ('', '', True))
                    self.assertEqual(34 in entries, total == 40)
            user.mkdir()
            (user / 'trophies.txt').write_text('14 1728000000\n', encoding='utf-8')
            self.assertEqual(trophy_snapshot(game, user)['entries'][0]['name'], 'Father Gascoigne')
            binding.write_bytes(b'NPWR00000_00')
            snapshot = trophy_snapshot(game, user)
            self.assertFalse(snapshot['builtIn'])
            self.assertEqual(snapshot['progress'], {'earned': 1, 'total': 0})

    def test_trophy_progress_matches_cached_ids_for_each_profile(self):
        TEMP_PARENT.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            root = Path(temporary)
            pack = root / 'game/sce_sys/trophy/trophy00.trp'
            pack.parent.mkdir(parents=True)
            pack.write_bytes(bytes.fromhex('DCA24D00'))
            profile = root / 'profile'
            cache = profile / 'trophy_cache/metadata.json'
            cache.parent.mkdir(parents=True)
            history = profile / 'trophies.txt'
            history.write_text('1 42\n1 43\n+002 -1\n7 10\n128 50\n3 4 incomplete\n', encoding='utf-8')
            entries = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 3}, {'id': True}, {'id': 128}, None]
            cache.write_text(json.dumps({'source_size': 4, 'entries': entries}), encoding='utf-8')

            self.assertEqual(trophy_snapshot(root / 'game', profile)['progress'], {'earned': 2, 'total': 3})
            self.assertEqual(trophy_snapshot(root / 'game', root / 'fresh')['progress'], {'earned': 0, 'total': 0})
            pack.write_bytes(pack.read_bytes() + b'new pack')
            self.assertEqual(trophy_snapshot(root / 'game', profile)['progress'], {'earned': 3, 'total': 0})
            history.unlink()
            history.mkdir()
            self.assertEqual(trophy_snapshot(root / 'game', profile)['progress'], {'earned': -1, 'total': 0})

    def test_trophy_details_mask_secrets_until_earned(self):
        TEMP_PARENT.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            root = Path(temporary)
            pack = root / 'game/sce_sys/trophy/trophy00.trp'
            pack.parent.mkdir(parents=True)
            pack.write_bytes(bytes.fromhex('DCA24D00'))
            user = root / 'Профиль'
            icons = user / 'trophy_cache/icons'
            icons.mkdir(parents=True)
            secret = {'id': 1, 'hidden': True, 'name': 'Secret name', 'description': 'Secret detail'}
            unknown = {'id': 2, 'hidden': False, 'name': 'Trophy #2', 'description': ''}
            for trophy in (1, 2):
                (icons / f'TROP{trophy:03}.PNG').touch()
            cache = {'source_size': 4, 'complete': True, 'entries': [secret, unknown]}
            (icons.parent / 'metadata.json').write_text(json.dumps(cache), encoding='utf-8')

            snapshot = trophy_snapshot(root / 'game', user)
            self.assertTrue(snapshot['hasMetadata'])
            hidden, unnamed = snapshot['entries']
            self.assertEqual((hidden['secret'], hidden['name'], hidden['description'], hidden['icon']),
                             (True, '', '', ''))
            self.assertEqual((unnamed['secret'], unnamed['name'], unnamed['icon']), (False, '', ''))
            (user / 'trophies.txt').write_text('1 1728000000\n', encoding='utf-8')
            unlocked = trophy_snapshot(root / 'game', user)['entries'][0]
            self.assertEqual((unlocked['secret'], unlocked['status'], unlocked['unlockedAt']),
                             (False, 'earned', 1728000000))
            self.assertEqual((unlocked['name'], unlocked['description'], unlocked['icon']),
                             (secret['name'], secret['description'], (icons / 'TROP001.PNG').as_uri()))

    def test_fresh_install_then_game_and_save_are_detected(self):
        TEMP_PARENT.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            root = Path(temporary)
            game = root / 'CUSA03173'
            user = root / 'user'
            self.assertEqual([row['level'] for row in check_readiness(game, user, lambda _: None)],
                             ['error', 'warning', 'warning'])
            for directory in ('dvdroot_ps4', 'sce_module', 'sce_sys/trophy'):
                (game / directory).mkdir(parents=True)
            (game / 'eboot.bin').write_bytes(b'game')
            (game / 'sce_sys/trophy/trophy00.trp').write_bytes(bytes.fromhex('DCA24D00'))
            user.mkdir()
            (user / 'keys.json').write_text(json.dumps({'TrophyKeySet':
                {'ReleaseTrophyKey': 'AB' * 16}}), encoding='utf-8')
            save = user / 'savedata/1/CUSA03173/SPRJ0005/userdata0010'
            save.parent.mkdir(parents=True)
            save.write_bytes(b'saved game')
            rows = check_readiness(game, user, lambda _: ('Bloodborne', '01.09'))
            self.assertEqual(rows[0]['level'], 'ready')
            self.assertIn('verify decryption', rows[1]['detail'])
            self.assertEqual(rows[2]['level'], 'ready')

    def test_bad_pack_and_key_do_not_appear_ready(self):
        TEMP_PARENT.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            root = Path(temporary)
            game = root / 'CUSA03173'
            user = root / 'user'
            (game / 'sce_sys/trophy').mkdir(parents=True)
            (game / 'sce_sys/trophy/TROPHY.TRP').write_bytes(b'bad pack')
            user.mkdir()
            (user / 'keys.json').write_text('{"TrophyKeySet":{"ReleaseTrophyKey":"wrong"}}',
                                            encoding='utf-8')
            rows = check_readiness(game, user, lambda _: None)
            self.assertEqual(rows[1]['level'], 'error')
            self.assertEqual(rows[2]['level'], 'warning')

    def test_shadps4_savedata_folder_is_explained(self):
        # shadPS4's ...\home\1000\savedata as the Saves folder: <title>\SPRJ* lies directly in it.
        TEMP_PARENT.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            root = Path(temporary)
            game = root / 'CUSA03173'
            user = root / 'savedata'
            save = user / 'CUSA03173/SPRJ0005/userdata0000'
            save.parent.mkdir(parents=True)
            save.write_bytes(b'saved game')
            rows = check_readiness(game, user, lambda _: None)
            self.assertEqual(rows[2]['level'], 'warning')
            self.assertIn("shadPS4's savedata folder", rows[2]['detail'])
            # Its parent (home\1000), as the old "user folder" is chosen.
            rows = check_readiness(game, root, lambda _: None)
            self.assertIn("shadPS4's savedata folder", rows[2]['detail'])

    def test_save_id_comes_from_game_metadata(self):
        TEMP_PARENT.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            game = Path(temporary) / 'CUSA03173'
            (game / 'sce_sys').mkdir(parents=True)
            (game / 'sce_sys/param.sfo').write_bytes(b'metadata')
            with patch.dict(sys.modules, {'prepare': SimpleNamespace(sfo=lambda _: {
                'TITLE_ID': 'CUSA03173', 'INSTALL_DIR_SAVEDATA': 'CUSA00207'})}):
                self.assertEqual(save_title_id(game), 'CUSA00207')


if __name__ == '__main__':
    unittest.main()
