from paths import ROOT
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(ROOT / 'scripts'))
import menu_assets as m  # noqa: E402
from fromsoft import Bnd4, dcx_decompress  # noqa: E402

# BB_TEST_GAME_DIR=<CUSA03173>: also edit the real 1.09 movie and message bundles.
GAME = Path(os.environ['BB_TEST_GAME_DIR']) / 'dvdroot_ps4' if os.environ.get('BB_TEST_GAME_DIR') else None


def placed_names(movie, codes=(m.PLACE2, m.PLACE3)):
    out = []
    for code, _head, s, _e in m.tags(movie, m.body_start(movie), len(movie)):
        if code in codes:
            name = m.placement(movie, code, s)[3]
            if name:
                out.append(name)
    return out


class FormatTests(unittest.TestCase):
    def test_fmg_round_trip(self):
        ids = {5: 'five'.encode('utf-16-le'), 6: None, 7: 'seven'.encode('utf-16-le'),
               20: 'five'.encode('utf-16-le')}
        self.assertEqual(m.fmg_read(m.fmg_write(ids)), ids)

    def test_matrix_round_trip(self):
        matrix = m.Matrix()
        matrix.has_scale, matrix.sn, matrix.sa, matrix.sc = True, 17, 65536, 70000
        matrix.tx, matrix.ty = -1234, 5678
        again, _end = m.read_matrix(m.write_matrix(matrix), 0)
        self.assertEqual((again.sa, again.sc, again.tx, again.ty), (65536, 70000, -1234, 5678))

    def test_messages_are_menu_or_event_text(self):
        rows = m.read_messages()
        for mid in (110006, 110013, 116020, 124020, 125000, 116004, 124001, 124003):
            self.assertTrue(rows[mid][0], mid)
        events = [mid for mid in rows if m.message_kind(mid) == 'event']
        # Rebirth; the 19 boss rematches (14000337 Cleric Beast to 14000355 Orphan of Kos)
        self.assertEqual(events, [14000332, 14000333, 14000334, 14000335, 14000336, *range(14000337, 14000356)])
        self.assertEqual([mid for mid in rows if m.message_kind(mid) == 'dialog'], [920001, 920002])
        self.assertEqual(rows[122000][0], 'Quit Game')

    def test_runtime_and_movie_agree_on_sections_rows_and_strings(self):
        import re
        runtime = (ROOT / 'src/pc_menu.c').read_text(encoding='utf-8')
        rows = m.read_messages()
        self.assertEqual(m.SECTION_ROWS, [('PCGraphics', 117020, 6), ('PCAchieve', 128020, 6)])
        self.assertEqual(m.NATIVE_SECTIONS, m.SECTION_ROWS)
        self.assertIn('MAX_ROWS = 16', runtime)
        self.assertIn('bbgpu_output_live_supported', runtime)
        self.assertNotIn('add_command(builder, ROW_RESTART', runtime)
        template = re.search(r'g_graphics_template\[\] = \{(.*?)\n\};', runtime, re.S).group(1)
        ids = [int(i) for i in re.findall(r'_ROW\("\w+", (\d+)', template)]
        self.assertEqual(len(ids), 15)
        self.assertNotIn('effect_ssr', template)
        self.assertNotIn('live_resolution', template)
        ru = m.read_messages(m.MESSAGES.with_name('pc_menu_messages_ru.tsv'))
        self.assertEqual(ru.keys(), rows.keys())
        self.assertEqual(ru[110007][0], 'Графика')
        self.assertEqual(ru[110018][0], 'Достижения')
        for mid in ids:
            self.assertTrue(ru[mid][1], mid)



@unittest.skipUnless(GAME, 'BB_TEST_GAME_DIR not set')
class RealGameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = m.make(GAME, log=lambda line: None)

    def test_movie_gains_sections_and_system_rows_without_scrolling(self):
        source = (GAME / m.MOVIE).read_bytes()
        movie = self.files[m.MOVIE]
        self.assertEqual(int.from_bytes(movie[4:8], 'little'), len(movie))
        names = placed_names(movie)
        for name, title, *_ in m.SECTIONS:
            self.assertEqual(names.count(name), 1)
            self.assertIn(f'StaticText_{title}'.encode(), movie)
        sprites = [s for code, _h, s, _e in m.tags(movie, m.body_start(movie), len(movie)) if code == m.DEFINE_SPRITE]
        before = [s for code, _h, s, _e in m.tags(source, m.body_start(source), len(source)) if code == m.DEFINE_SPRITE]
        self.assertEqual(len(sprites), len(before) + 2 * len(m.SECTIONS))  # each: the section and its title
        self.assertEqual(len(m.symbol_classes(movie)), len(m.symbol_classes(source)) + len(m.SECTIONS))
        # The System list has room for every command; a scrollbar is unnecessary.
        top = next(m.placement(movie, code, s) for code, _h, s, _e in m.tags(movie, m.body_start(movie), len(movie))
                   if code in (m.PLACE2, m.PLACE3) and m.placement(movie, code, s)[3] == 'Top')
        head, s, e = m.find_sprite(movie, top[1])
        inside = [m.placement(movie, code, s2)[3] for code, _h, s2, _e in m.tags(movie, s + 4, e)
                  if code in (m.PLACE2, m.PLACE3)]
        self.assertNotIn('ScrollBarV', inside)
        self.assertEqual({name for name in inside if name and name.startswith('Item_')},
                         {f'Item_{i}_0' for i in range(m.SYSTEM_VISIBLE_ROWS)})
        self.assert_row_animation(movie, top[1], m.SYSTEM_VISIBLE_ROWS, m.SYSTEM_ROW_PITCH * 20)

    def test_graphics_has_persistent_widget_slots_and_native_scrollbar(self):
        movie = self.files[m.MOVIE]
        item = next(m.placement(movie,c,a) for c,_,a,_ in m.tags(movie,m.body_start(movie),len(movie))
                    if c in (m.PLACE2,m.PLACE3) and m.placement(movie,c,a)[3] == 'PCGraphics')
        _, a, z = m.find_sprite(movie,item[1])
        names = [m.placement(movie,c,a)[3] for c,_,a,_ in m.tags(movie,a+4,z) if c in (m.PLACE2,m.PLACE3)]
        self.assertIn('ScrollBarV',names)
        self.assertEqual({n for n in names if n and n.startswith('Item_')}, {f'Item_{i}_0' for i in range(15)})
        self.assertNotIn('PCDisplay', placed_names(movie))
        self.assertNotIn('PCSetting', placed_names(movie))

    def test_system_frame_and_footer_enclose_all_thirteen_rows(self):
        movie = self.files[m.MOVIE]
        source = (GAME / m.MOVIE).read_bytes()
        def frames(data, cid):
            _h, a, z = m.find_sprite(data, cid)
            current, result = {}, []
            for code, _h, s, e in m.tags(data, a + 4, z):
                if code in (m.PLACE2, m.PLACE3):
                    depth, _char, mat, _name = m.placement(data, code, s)
                    if mat:
                        current[depth] = mat
                if code == m.SHOW_FRAME:
                    result.append(current.copy())
            return result
        self.assertEqual(m.SYSTEM_VISIBLE_ROWS, 8)  # six native in-world, six PC, Restart
        for before, after in zip(frames(source, 145), frames(movie, 145), strict=True):
            for depth, shift in ((11, m.SYSTEM_FRAME_TOP), (17, m.SYSTEM_FRAME_BOTTOM), (23, m.SYSTEM_FRAME_TOP), (27, m.SYSTEM_FRAME_BOTTOM)):
                self.assertEqual(after[depth][5] - before[depth][5], shift * 20)
                self.assertEqual(after[depth][:4], before[depth][:4])  # ornaments keep their shape
        for frame in frames(movie, 150):
            # Row text baseline comes 50.7 px below its placement. The header and
            # divider/footer must leave at least 40 px after the last row text.
            first_y = frame[31][5] / 20 + 50.7
            last_y = first_y + (m.SYSTEM_VISIBLE_ROWS - 1) * m.SYSTEM_ROW_PITCH
            self.assertGreater(first_y, frame[69][5] / 20 + 40)
            divider = frame[3][5] / 20 + (15799 / 20 + m.SYSTEM_FRAME_BOTTOM)
            help_y = frame[66][5] / 20 + 4662 / 20
            self.assertLess(last_y + 40, divider)
            self.assertGreater(help_y, divider)
        # Other sections share StatusBar/backdrop art: those sprites stay byte-identical.
        for cid in (19, 37, 107, 115, 126, 134, 138):
            _h, a, z = m.find_sprite(source, cid)
            _h2, a2, z2 = m.find_sprite(movie, cid)
            self.assertEqual(source[a:z], movie[a2:z2])

    def test_title_lists_fit_all_commands_in_available_regions(self):
        movies = [*m.TITLE_MOVIES, *(p for p in m.OPTIONAL_TITLE_MOVIES if (GAME / p).is_file())]
        for relative in movies:
            source, movie = (GAME / relative).read_bytes(), self.files[relative]
            self.assertEqual(int.from_bytes(movie[4:8], 'little'), len(movie))
            self.assertNotIn('Item_5_0', placed_names(source, (m.PLACE2,)) + self.list_rows(source))
            for i in range(m.TITLE_VISIBLE_ROWS):
                self.assertIn(f'Item_{i}_0', self.list_rows(movie))
            cid = next(m.u16(movie, s) for code, _h, s, e in m.tags(movie, m.body_start(movie), len(movie))
                       if code == m.DEFINE_SPRITE and any(
                           c == m.PLACE2 and m.Place2(movie, s2, e2).name == 'Item_0_0'
                           for c, _h2, s2, e2 in m.tags(movie, s + 4, e)))
            self.assert_row_animation(movie, cid, m.TITLE_VISIBLE_ROWS, 797)

    def test_missing_optional_eu_title_keeps_standard_title_support(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for relative in [m.MOVIE, *m.TITLE_MOVIES,
                             Path('msg/engus') / m.MESSAGE_FILE]:
                (root / relative).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(GAME / relative, root / relative)
            result = m.make(root, log=lambda line: None)
            self.assertTrue(all(p in result for p in m.TITLE_MOVIES))
            self.assertNotIn(Path('menu/title_dlc_eu.gfx'), result)

    def assert_row_animation(self, movie, cid, count, pitch):
        """Every opening/closing frame retains capacity, pitch and relative motion."""
        _h, s, e = m.find_sprite(movie, cid)
        depths, positions, frames = {}, {}, 0
        for code, _h, s2, e2 in m.tags(movie, s + 4, e):
            if code == m.PLACE2:
                p = m.Place2(movie, s2, e2)
                if p.name and p.name.startswith('Item_') and p.name.endswith('_0'):
                    depths[p.depth] = int(p.name[5:-2])
                if p.depth in depths and p.mat:
                    positions[depths[p.depth]] = p.mat.ty
            if code == m.SHOW_FRAME:
                self.assertEqual(sorted(positions), list(range(count)))
                self.assertEqual([positions[i] - positions[0] for i in range(count)],
                                 [i * pitch for i in range(count)])
                frames += 1
        self.assertGreaterEqual(frames, 1)

    @staticmethod
    def list_rows(movie):
        rows = []
        for code, _h, s, e in m.tags(movie, m.body_start(movie), len(movie)):
            if code == m.DEFINE_SPRITE:
                rows += [m.placement(movie, c, s2)[3] for c, _h2, s2, _e2 in m.tags(movie, s + 4, e)
                         if c in (m.PLACE2, m.PLACE3)]
        return [r for r in rows if r]

    def test_every_language_gains_the_strings_and_keeps_its_own(self):
        rows = m.read_messages()
        languages = [k for k in self.files if k.name == m.MESSAGE_FILE]
        self.assertGreater(len(languages), 1)
        for relative in languages:
            before = Bnd4(dcx_decompress((GAME / relative).read_bytes()))
            after = Bnd4(dcx_decompress(self.files[relative]))
            self.assertEqual(after.names, before.names)
            for group in m.GROUP_KIND:
                old = m.fmg_read(before.files[before.ids.index(group)])
                new = m.fmg_read(after.files[after.ids.index(group)])
                self.assertEqual({k: v for k, v in new.items() if k in old}, old)  # nothing changed
            rows = m.read_messages(m.MESSAGES.with_name("pc_menu_messages_ru.tsv")) if relative.parts[1] == "rusru" else m.read_messages()
            menu = m.fmg_read(after.files[after.ids.index(m.MENU_TEXT)])
            self.assertEqual(menu[110006].decode('utf-16-le'), rows[110006][0])
            events = m.fmg_read(after.files[after.ids.index(m.EVENT_TEXT)])
            self.assertEqual(events[14000335].decode('utf-16-le'), rows[14000335][0])
            for group in (m.DIALOG_TEXT, m.SCREEN_DIALOG_TEXT):
                dialog = m.fmg_read(after.files[after.ids.index(group)])
                self.assertEqual(dialog[920001].decode('utf-16-le'), rows[920001][0])

    def test_a_damaged_message_bundle_turns_the_menu_off(self):
        # Issue #8: a cut-short menu.msgbnd.dcx stopped the game instead.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / m.MOVIE).parent.mkdir(parents=True)
            shutil.copyfile(GAME / m.MOVIE, root / m.MOVIE)
            relative = Path('msg') / 'engus' / m.MESSAGE_FILE
            (root / relative).parent.mkdir(parents=True)
            (root / relative).write_bytes((GAME / relative).read_bytes()[:-100])
            lines = []
            self.assertEqual(m.make(root, log=lines.append), {})
            self.assertEqual(len(lines), 1)
            self.assertIn('PC menu: off - msg/engus/menu.msgbnd.dcx: DCX file is truncated', lines[0])


if __name__ == '__main__':
    unittest.main()
