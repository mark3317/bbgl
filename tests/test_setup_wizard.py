import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
import bbport_launcher_win as core
import bbport_startup
from bbport_launcher_backend import LauncherBackend


class FirstRunWizardTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).resolve().parents[1] / 'out'
        parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=parent)
        self.root = Path(self.temporary.name)
        self.patches = [patch.object(core, 'CONFIG_DIR', self.root),
                        patch.object(core, 'CONFIG_FILE', self.root / 'settings.json'),
                        patch.object(core, 'DATA_DIR', self.root),
                        patch.object(core, 'PORT_DIR', self.root),
                        patch.dict(os.environ, {'BB_CONFIG': str(self.root / 'bbport.ini')}),
                        patch.dict(core.APP_DEFAULTS, {'check_updates': False,
                                                       'game_dir': str(self.root / 'missing')}),
                        patch.object(LauncherBackend, '_detect_gpu', lambda self: None)]
        for active in self.patches:
            active.start()

    def tearDown(self):
        for active in reversed(self.patches):
            active.stop()
        self.temporary.cleanup()

    def settings(self):
        return {**core.APP_DEFAULTS, **json.loads((self.root / 'settings.json').read_text(encoding='utf-8'))}

    def route(self, args=()):
        return bbport_startup.route(self.settings(), list(args), self.root, False)

    def test_wizard_survives_partial_setup_and_stops_after_finish(self):
        first = LauncherBackend()
        first.setValue('game_dir', str(self.root / 'game'))
        self.assertEqual(self.route()['page'], 'Setup')
        first.completeSetup()
        saved = self.settings()
        self.assertTrue(saved['setupCompleted'])
        self.assertEqual(saved['setupVersion'], bbport_startup.SETUP_VERSION)
        self.assertNotEqual(self.route()['page'], 'Setup')

    def test_finished_setup_with_game_opens_home(self):
        game = self.root / 'CUSA03173'
        game.mkdir()
        (game / 'eboot.bin').write_bytes(b'\0')
        backend = LauncherBackend()
        backend.setValue('game_dir', str(game))
        backend.completeSetup()
        self.assertEqual((self.route()['mode'], self.route()['page']), ('launcher', 'Home'))
        self.assertEqual(self.route(['--launcher'])['page'], 'Home')
        self.assertEqual(self.route(['--setup'])['page'], 'Setup')
        backend.setValue('launchDirectly', True)  # obsolete saved preference is ignored
        self.assertEqual(self.route()['mode'], 'launcher')

    def test_skip_opens_game_page_with_fix_banner(self):
        backend = LauncherBackend()
        backend.skipSetup()
        self.assertTrue(self.settings()['setupSkipped'])
        self.assertTrue(backend.startupProblem)
        self.assertTrue(backend._problem_active())
        route = self.route()
        self.assertEqual((route['page'], route['problem'], route['step']), ('Game', 'game', 1))
        backend.dismissProblem()
        self.assertEqual(backend.startupProblem, '')

    def test_fix_banner_clears_once_game_folder_is_valid(self):
        backend = LauncherBackend({'mode': 'launcher', 'page': 'Game', 'step': 1, 'problem': 'game'})
        self.assertEqual(backend.startPage, 'Game')
        self.assertEqual(backend.fixStep, 1)
        self.assertTrue(backend.startupProblem)
        self.assertTrue(backend._problem_active())
        game = self.root / 'game'
        game.mkdir()
        (game / 'eboot.bin').write_bytes(b'\0')
        backend.setValue('game_dir', str(game))
        self.assertEqual(backend.startupProblem, '')

    def test_bundled_prompts_switch_without_download_and_follow_ingame_choice(self):
        from prompt_icons import layer
        for name in (core.KEYBOARD_PROMPTS, core.XBOX_PROMPTS):
            texture = self.root / 'launcher/assets/button-prompts' / name / 'menu/common.tpf.dcx'
            texture.parent.mkdir(parents=True)
            texture.write_bytes(b'DCX\0fixture')
        profile_file = self.root / 'mods.json'
        original = {'order': ['User mod', core.XBOX_PROMPTS], 'disabled': [core.KEYBOARD_PROMPTS]}
        profile_file.write_text(json.dumps(original))
        backend = LauncherBackend()
        self.addCleanup(backend.shutdown_coop)
        self.assertEqual(backend.promptChoice, 'Xbox')
        backend.setPrompt('Keyboard')
        self.assertEqual(backend.promptChoice, 'Keyboard')
        ini = (self.root / 'bbport.ini').read_text(encoding='utf-8')
        self.assertIn('key_roll=Left Shift', ini)
        self.assertIn('key_lock_on=Mouse3', ini)
        self.assertEqual(layer(self.root, backend.promptChoice).name, core.KEYBOARD_PROMPTS)
        backend.app['mods_enabled'] = False
        self.assertEqual(backend.promptChoice, 'Keyboard')
        backend.setPrompt('Xbox')
        self.assertEqual(backend.promptChoice, 'Xbox')
        backend.setPrompt('PlayStation')
        self.assertEqual(backend.promptChoice, 'PlayStation')
        self.assertIsNone(layer(self.root, backend.promptChoice))
        self.assertEqual(json.loads(profile_file.read_text()), original)
        self.assertFalse((self.root / 'mods' / core.KEYBOARD_PROMPTS).exists())
        self.assertFalse((self.root / 'mods' / core.XBOX_PROMPTS).exists())

    def test_launch_options_moved_out_of_advanced(self):
        backend = LauncherBackend()
        keys = {field['key'] for page in ('Advanced', 'Diagnostics') for field in backend.fields(page)}
        self.assertFalse(keys & {'close_on_play', 'launchDirectly', 'check_updates'})
        self.assertEqual([f['key'] for f in backend.fields('Diagnostics')],
                         ['diagnostic_logs', 'gpu_logs', 'frame_stats', 'gpu_profile', 'vk_validation'])
        pages = ('Graphics', 'Display', 'Game', 'Controller', 'Cheats', 'Online', 'Mods', 'Advanced', 'Diagnostics')
        every = [field['key'] for page in pages for field in backend.fields(page)]
        self.assertEqual(len(every), len(set(every)), 'a setting appears on two pages')


if __name__ == '__main__':
    unittest.main()
