"""Real runtime mapping of built-in icons, independent of user mod selection."""
import json
import subprocess
import sys
import tempfile
import unittest
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import mods
import prompt_icons


class BuiltinPromptTests(unittest.TestCase):
    @staticmethod
    def archive(glyph, atlas, item):
        from fromsoft import dcx_compress
        textures = {'KG_OK': glyph, 'MENU_Common_00091': atlas, 'MENU_Icon_01001': item}
        data = bytearray(16 + 36 * len(textures))
        data[:4] = b'TPF\0'
        struct.pack_into('<I', data, 8, len(textures))
        data[12:15] = bytes((4, 3, 1))
        for i, name in enumerate(textures):
            struct.pack_into('<I', data, 16 + i * 36 + 24, len(data))
            data.extend(name.encode('utf-16-le') + b'\0\0')
        data.extend(b'\0' * (-len(data) % 16))
        start = len(data)
        for i, payload in enumerate(textures.values()):
            data.extend(b'\0' * (-len(data) % 16))
            struct.pack_into('<II', data, 16 + i * 36, len(data), len(payload))
            data.extend(payload)
        struct.pack_into('<I', data, 4, len(data) - start)
        return dcx_compress(data)

    def test_selected_buttons_survive_multiple_mods_and_repeated_switches(self):
        from fromsoft import dcx_decompress
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            game = root / 'game'
            original = game / prompt_icons.COMMON
            original.parent.mkdir(parents=True)
            original.write_bytes(self.archive(b'PS', b'PS-atlas', b'original-item'))
            layers = []
            for i in range(12):
                folder = root / f'mod-{i}'
                path = folder / prompt_icons.COMMON
                path.parent.mkdir(parents=True)
                path.write_bytes(self.archive(b'Xbox', b'Xbox-atlas', f'item-{i}'.encode()))
                layers.append((folder.name, folder))
            for glyph in (b'Keyboard', b'Xbox', b'PS', b'Keyboard'):
                source = root / 'selected.dcx'
                source.write_bytes(self.archive(glyph, glyph * 300, b'unused-item'))
                merged = prompt_icons.apply(layers, game, source, root / 'out')
                mods.build_manifest(game, root / 'out', merged)
                mapping = dict(line.split('\t') for line in
                               (root / 'out/mod-files.tsv').read_text().splitlines()[1:])
                result = dcx_decompress(Path(mapping[prompt_icons.COMMON]).read_bytes())
                textures = prompt_icons._textures(result)
                self.assertEqual(textures['KG_OK'][1], glyph)
                self.assertEqual(textures['MENU_Common_00091'][1], glyph * 300)
                self.assertEqual(textures['MENU_Icon_01001'][1], b'item-11')
            # Disabling user mods and returning to native PlayStation uses the original.
            self.assertEqual(prompt_icons.apply([], game, original, root / 'out'), [])
            self.assertEqual(dcx_decompress(original.read_bytes()),
                             dcx_decompress(self.archive(b'PS', b'PS-atlas', b'original-item')))
            for enabled in ('1', '0'):
                # Exercise the actual startup CLI, including native PlayStation restoration.
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/mods.py'),
                    str(game), '--out', str(root / 'cli'), '--mods-dir', str(root),
                    '--enabled', enabled, '--button-icons', str(original)],
                    capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                mapping = dict(line.split('\t') for line in
                               (root / 'cli/mod-files.tsv').read_text().splitlines()[1:])
                archive = Path(mapping.get(prompt_icons.COMMON, original)).read_bytes()
                self.assertEqual(prompt_icons._textures(dcx_decompress(archive))['KG_OK'][1], b'PS')

    def test_builtin_mapping_with_mods_off_and_legacy_migration(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            game = root / 'game'
            game.mkdir()
            (game / 'eboot.bin').write_bytes(b'original')
            profile = root / 'profile'
            profile.mkdir()
            config = profile / 'mods.json'
            config.write_text(json.dumps({'order': [prompt_icons.PACKS['Keyboard']]}))
            self.assertEqual(prompt_icons.choice(profile), 'Keyboard')
            for name in prompt_icons.PACKS.values():
                old = root / 'mods' / name / 'menu/common.tpf.dcx'
                old.parent.mkdir(parents=True)
                old.write_bytes(b'old-icons')
                ready = root / 'launcher/assets/button-prompts' / name / 'menu/common.tpf.dcx'
                ready.parent.mkdir(parents=True)
                ready.write_bytes(b'builtin-icons')
            self.assertEqual(mods.discover(root / 'mods'), [])
            for value in ('Keyboard', 'Xbox'):
                folder = prompt_icons.layer(root, value)
                out = root / ('out-' + value)
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/mods.py'),
                    str(game), '--out', str(out), '--mods-dir', str(root / 'mods'),
                    '--enabled', '0', '--generated', str(folder)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                mapping = (out / 'mod-files.tsv').read_text()
                self.assertIn((folder / 'menu/common.tpf.dcx').resolve().as_posix(), mapping)
                self.assertFalse((game / 'dvdroot_ps4').exists())
            self.assertEqual((game / 'eboot.bin').read_bytes(), b'original')
            (profile / 'button-prompts.json').write_text('{"choice":"PlayStation"}')
            self.assertEqual(prompt_icons.choice(profile), 'PlayStation')
            self.assertIsNone(prompt_icons.layer(root, 'PlayStation'))


if __name__ == '__main__':
    unittest.main()
