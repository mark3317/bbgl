from paths import ROOT
import hashlib
import json
import os
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import bsdiff4
import bundled_deltas
import mods
from fromsoft import dcx_compress, dcx_decompress

sys.path.insert(0, str(ROOT / 'launcher'))


class BundledDeltaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.game = self.root / 'game'
        self.mod = self.root / 'mods/Diamond Sword'
        self.mod.mkdir(parents=True)
        self.relative = 'dvdroot_ps4/parts/sword.dcx'
        self.base = self.game / self.relative
        self.base.parent.mkdir(parents=True)
        self.base.write_bytes(dcx_compress(b'original weapon'))
        self.original = self.base.read_bytes()
        self.result = b'new sword, price 10000'
        (self.mod / '0.bsdiff').write_bytes(bsdiff4.diff(b'original weapon', self.result))
        self.manifest = dict(format=1, files=[dict(target=self.relative, base=self.relative,
            patch='0.bsdiff', base_sha256=hashlib.sha256(b'original weapon').hexdigest(),
            sha256=hashlib.sha256(self.result).hexdigest())])
        self.write_recipe()

    def write_recipe(self):
        (self.mod / 'bbgl-delta.json').write_text(json.dumps(self.manifest))

    def test_default_off_and_explicit_selection(self):
        self.assertEqual(mods.discover(self.mod.parent), ['Diamond Sword'])
        self.assertEqual(mods.selected(self.mod.parent, None), [])
        config = self.root / 'mods.json'
        config.write_text('{}')
        self.assertEqual(mods.selected(self.mod.parent, config), [])
        config.write_text(json.dumps(dict(order=['Diamond Sword'], disabled=[])))
        self.assertEqual(mods.selected(self.mod.parent, config), ['Diamond Sword'])
        config.write_text(json.dumps(dict(order=['Diamond Sword'], disabled=['Diamond Sword'])))
        self.assertEqual(mods.selected(self.mod.parent, config), [])

    def test_materialization_and_runtime_manifest_preserve_game(self):
        destination = self.root / 'generated'
        layer = bundled_deltas.materialize(self.mod, self.game, destination)
        self.assertEqual(dcx_decompress((layer / self.relative).read_bytes()), self.result)
        mods.build_manifest(self.game, self.root / 'out', [('Diamond Sword', layer)])
        self.assertIn(self.relative, (self.root / 'out/mod-files.tsv').read_text())
        self.assertEqual(self.base.read_bytes(), self.original)
        self.assertFalse((self.mod / 'dvdroot_ps4').exists())

    def test_wrong_original_rejected(self):
        self.base.write_bytes(dcx_compress(b'other game version'))
        with self.assertRaisesRegex(ValueError, 'original Bloodborne'):
            bundled_deltas.materialize(self.mod, self.game, self.root / 'generated')

    def test_path_escape_rejected(self):
        self.manifest['files'][0]['target'] = 'dvdroot_ps4/../../outside.dcx'
        self.write_recipe()
        with self.assertRaisesRegex(ValueError, 'Invalid bundled mod path'):
            bundled_deltas.materialize(self.mod, self.game, self.root / 'generated')
        self.assertFalse((self.root / 'outside.dcx').exists())

    def test_ordinary_mod_unchanged(self):
        ordinary = self.root / 'ordinary'
        self.assertEqual(bundled_deltas.materialize(ordinary, self.game, self.root / 'generated'), ordinary)

    def test_launcher_toggle_and_unrelated_reorder_preserve_selection(self):
        os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
        from PySide6.QtWidgets import QApplication
        import bbport_launcher_win as core
        from bbport_launcher_backend import LauncherBackend
        app = QApplication.instance() or QApplication([])
        extra = self.mod.parent / 'Extra/parts'
        extra.mkdir(parents=True)
        (extra / 'extra.dcx').write_bytes(b'extra')
        with patch.object(core, 'PORT_DIR', self.root), patch.object(core, 'DATA_DIR', self.root), \
             patch.object(core, 'CONFIG_FILE', self.root / 'settings.json'), \
             patch.object(LauncherBackend, 'start_background_checks'), \
             patch.dict(core.APP_DEFAULTS, mods_dir=str(self.mod.parent)), \
             patch.dict(os.environ, BB_CONFIG=str(self.root / 'bbport.ini')):
            backend = LauncherBackend()
            backend._party_timer.stop()
            backend._party_network_timer.stop()
            backend._addons_timer.stop()
            self.addCleanup(backend.shutdown_coop)
            def enabled():
                return next(m['enabled'] for m in backend._mods if m['name'] == 'Diamond Sword')
            self.assertFalse(enabled())
            backend.moveMod('Extra', -1)
            self.assertFalse(enabled())
            backend.setMod('Extra', False)
            self.assertFalse(enabled())
            backend.setMod('Diamond Sword', True)
            self.assertTrue(enabled())
            self.assertIn('Diamond Sword', mods.selected(self.mod.parent, self.root / 'mods.json'))
            backend.setMod('Diamond Sword', False)
            self.assertFalse(enabled())
            self.assertNotIn('Diamond Sword', mods.selected(self.mod.parent, self.root / 'mods.json'))


if __name__ == '__main__':
    unittest.main()
