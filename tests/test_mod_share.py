"""Isolated real TCP transfer and launcher polling; no installed files or profiles."""
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'launcher'), str(ROOT / 'scripts')]
import bbport_mod_share as share
import bbport_party as party


class ModShareTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.asset = self.source / 'Меч охотника/dvdroot_ps4/parts/sword.dcx'
        self.asset.parent.mkdir(parents=True)
        self.asset.write_bytes(b'asset' * 500000)
        self.share = share.Share(self.source)
        self.a = party.Discovery(self.root / 'a', '127.0.0.71', set(), 'HunterA', port=0)
        # Port 0 assigns independent UDP/TCP ports; requests use the TCP port.
        self.a.port = self.a.tcp.server_address[1]
        self.a.mod_share = self.share
        self.addCleanup(self.a.close)
        self.b = type('Client', (), dict(address='127.0.0.72', port=self.a.port))()

    def test_real_tcp_download_selection_and_no_overwrite(self):
        self.share.selection = (['Меч охотника'], {'Меч охотника'})
        row, = share.catalog(self.b, self.a.offer)
        self.assertTrue(row['enabled'])
        dest = self.root / 'dest'
        share.download(self.b, self.a.offer, row, dest)
        self.assertEqual((dest / self.asset.relative_to(self.source)).read_bytes(), self.asset.read_bytes())
        with self.assertRaisesRegex(ValueError, 'already installed'):
            share.download(self.b, self.a.offer, row, dest)
        self.assertEqual([p.name for p in dest.iterdir()], ['Меч охотника'])

    def test_changed_source_refused_and_catalog_updates(self):
        row, = self.share.catalog()
        self.asset.write_bytes(b'changed')
        updated, = self.share.catalog()
        self.assertNotEqual(row['digest'], updated['digest'])
        with self.assertRaisesRegex(ValueError, 'changed'):
            share.download(self.b, self.a.offer, row, self.root / 'dest')

    def test_legacy_peer_button_images_are_not_shared(self):
        from prompt_icons import PACKS
        gameplay = self.share.catalog()[0]
        legacy = [dict(gameplay, name=name.swapcase(), enabled=True)
                  for name in PACKS.values()]
        with patch.object(self.share, 'catalog', return_value=[*legacy, gameplay]):
            self.assertEqual(share.catalog(self.b, self.a.offer), [gameplay])
        with patch.object(self.share, 'catalog', return_value=legacy):
            self.assertEqual(share.catalog(self.b, self.a.offer), [])

    def test_unsafe_names_rejected(self):
        for name in ('../escape', 'C:evil', 'CON', 'a\\b', 'a.', '.hidden', '/abs', 'a/b'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                share.safe_name(name)

    def test_corrupt_traversal_and_truncated_download_cleanup(self):
        row, = self.share.catalog()
        for filename, truncated in [('../escape', False), ('dvdroot_ps4/parts/a', False),
                                    ('dvdroot_ps4/parts/a', True)]:
            archive = io.BytesIO()
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr(filename, b'wrong')
            raw = archive.getvalue()
            sock = type('Socket', (), {'close': lambda self: None})()
            with self.subTest(filename=filename, truncated=truncated), patch.object(
                    share, 'request', return_value=(sock, io.BytesIO(raw[:-3] if truncated else raw),
                                                   {'size': len(raw)})):
                dest = self.root / 'dest'
                with self.assertRaises((ValueError, zipfile.BadZipFile)):
                    share.download(self.b, self.a.offer, row, dest)
                self.assertEqual(list(dest.iterdir()), [])
                self.assertFalse((self.root / 'escape').exists())

    def test_hidden_staging_is_not_a_mod(self):
        import mods
        hidden = self.source / '.bbgl-download-test/content/dvdroot_ps4/parts'
        hidden.mkdir(parents=True)
        (hidden / 'partial').write_bytes(b'partial')
        self.assertEqual(mods.discover(self.source), ['Меч охотника'])

    def test_launcher_sync_applies_peer_order_and_enabled_set(self):
        from PySide6.QtWidgets import QApplication
        import bbport_launcher_win as core
        from bbport_launcher_backend import LauncherBackend
        app = QApplication.instance() or QApplication([])
        self.share.selection = (['Меч охотника'], {'Меч охотника'})
        root = self.root / 'launcher'
        root.mkdir()
        extra = root / 'mods/Extra/parts/extra.dcx'
        extra.parent.mkdir(parents=True)
        extra.write_bytes(b'extra')
        self.b.offers = lambda: [dict(self.a.offer)]
        self.b.offer = {'id': 'Client'}
        self.b.mod_share = None
        self.b.close = lambda: None
        with patch.object(core, 'PORT_DIR', root), patch.object(core, 'DATA_DIR', root), \
             patch.object(core, 'CONFIG_DIR', root), \
             patch.object(core, 'CONFIG_FILE', root / 'settings.json'), \
             patch.object(LauncherBackend, 'start_background_checks'), \
             patch.dict(os.environ, BB_CONFIG=str(root / 'bbport.ini')):
            backend = LauncherBackend()
            backend._party_timer.stop()
            backend._party_network_timer.stop()
            backend._addons_timer.stop()
            backend._party_discovery = self.b
            backend.setMod('Extra', False)
            remote_row = dict(self.share.catalog()[0], peer=self.a.offer['id'],
                              player='Hunter', status='missing')
            backend._network_mods = [remote_row]
            old_revision = backend._mod_catalog_revision
            # Keep the next periodic poll out of the immediate-after-download assertion.
            poll = patch.object(backend, '_poll_mods')
            poll.start()
            self.addCleanup(poll.stop)
            backend.downloadNetworkMod(self.a.offer['id'], 'Меч охотника')
            until = time.monotonic() + 5
            while backend.modsDownloading and time.monotonic() < until:
                app.processEvents()
                time.sleep(.01)
            self.assertFalse(backend.modsDownloading)
            self.assertIn('Меч охотника', json.loads((root / 'mods.json').read_text())['disabled'])
            self.assertEqual((root / 'mods' / self.asset.relative_to(self.source)).read_bytes(), self.asset.read_bytes())
            self.assertEqual(backend.networkMods[0]['status'], 'same')
            self.assertTrue(backend._mods_unsynchronized())  # Explicitly disabled download.
            backend.setMod('Меч охотника', True)
            self.assertFalse(backend._mods_unsynchronized())
            backend._receive_network_mods([remote_row], '', old_revision)
            self.assertEqual(backend.networkMods[0]['status'], 'same')
            # The two users may have different controls and different prompt assets.
            backend._mods.append(dict(name=core.KEYBOARD_PROMPTS, enabled=True))
            backend._network_mods.append(dict(name='Xbox Prompts (Dommo)', peer=self.a.offer['id'],
                                             status='conflict', enabled=True))
            self.assertFalse(backend._mods_unsynchronized())
            backend.app['play_mode'] = 'coop'
            warnings = []
            backend.modSyncWarning.connect(lambda: warnings.append(True))
            with patch.object(backend, 'coopPlay') as launch:
                for choice in ('Xbox', 'PlayStation', 'Keyboard'):
                    backend.setPrompt(choice)
                    self.assertFalse(backend._mods_unsynchronized())
                    backend.playSelected()
                self.assertEqual(launch.call_count, 3)
                self.assertEqual(warnings, [])
            backend._network_mods[0]['status'] = 'conflict'
            self.assertTrue(backend._mods_unsynchronized())
            backend._network_mods[0]['status'] = 'same'
            backend._network_mods[0]['enabled'] = False
            self.assertTrue(backend._mods_unsynchronized())
            backend._network_mods[0]['enabled'] = True
            backend.syncNetworkMods(self.a.offer['id'])
            until = time.monotonic() + 5
            while backend.modsDownloading and time.monotonic() < until:
                app.processEvents()
                time.sleep(.01)
            self.assertFalse(backend.modsDownloading)
            profile = json.loads((root / 'mods.json').read_text())
            self.assertEqual(profile['order'], ['Меч охотника', 'Extra'])
            self.assertEqual(profile['disabled'], ['Extra'])
            self.assertTrue(backend.app['mods_enabled'])
            self.assertEqual(extra.read_bytes(), b'extra')
            # A fresh catalog catches a conflict before changing settings or files.
            self.asset.write_bytes(b'other version')
            backend.syncNetworkMods(self.a.offer['id'])
            until = time.monotonic() + 5
            while backend.modsDownloading and time.monotonic() < until:
                app.processEvents()
                time.sleep(.01)
            self.assertIn('Меч охотника', backend.notice)
            self.assertEqual(json.loads((root / 'mods.json').read_text()), profile)
            self.a.mod_share = share.Share(self.root / 'empty')
            backend.syncNetworkMods(self.a.offer['id'])
            until = time.monotonic() + 5
            while backend.modsDownloading and time.monotonic() < until:
                app.processEvents()
                time.sleep(.01)
            profile = json.loads((root / 'mods.json').read_text())
            self.assertEqual(set(profile['disabled']), {'Меч охотника', 'Extra'})
            # Let any catalog worker finish before temporary directories disappear.
            until = time.monotonic() + 3
            while backend._mods_polling and time.monotonic() < until:
                app.processEvents()
                time.sleep(.01)
            backend.shutdown_coop()


class LauncherModPollingTests(unittest.TestCase):
    def test_timer_detects_new_deleted_mods_and_external_selection(self):
        from PySide6.QtWidgets import QApplication
        import bbport_launcher_win as core
        from bbport_launcher_backend import LauncherBackend
        app = QApplication.instance() or QApplication([])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(core, 'PORT_DIR', root), patch.object(core, 'DATA_DIR', root), \
                 patch.object(core, 'CONFIG_FILE', root / 'settings.json'), \
                 patch.object(LauncherBackend, 'start_background_checks'), \
                 patch.dict(os.environ, BB_CONFIG=str(root / 'bbport.ini')):
                backend = LauncherBackend()
                backend._party_timer.stop()
                backend._party_network_timer.stop()
                backend._addons_timer.setInterval(10)
                asset = root / 'mods/New/parts/a.dcx'
                asset.parent.mkdir(parents=True)
                asset.write_bytes(b'asset')
                def wait_for(predicate):
                    until = time.monotonic() + 2
                    while not predicate() and time.monotonic() < until:
                        app.processEvents()
                        time.sleep(.005)
                    self.assertTrue(predicate())
                wait_for(lambda: len(backend.contentMods) == 1)
                (root / 'mods.json').write_text(json.dumps({'disabled': ['New']}))
                wait_for(lambda: not backend.contentMods[0]['enabled'])
                asset.unlink()
                asset.parent.rmdir()
                wait_for(lambda: not backend.contentMods)
                backend.shutdown_coop()


if __name__ == '__main__':
    unittest.main()
