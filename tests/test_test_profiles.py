"""Independent launcher profiles using a shared, read-only installation."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
import bbport_paths as paths
import bbport_launcher_win as core
from bbport_launcher_backend import LauncherBackend
import test_setup_wizard as wizard_tests


class TestProfileUITests(unittest.TestCase):
    setUp = wizard_tests.FirstRunWizardTests.setUp
    tearDown = wizard_tests.FirstRunWizardTests.tearDown

    def test_open_uses_selected_profile_without_switching_parent(self):
        backend = LauncherBackend()
        self.assertEqual(backend.value('test_profile_dir'), str(self.root))
        selected = self.root / 'other profile'
        backend.setValue('test_profile_dir', str(selected))
        with patch.object(subprocess, 'Popen') as spawn:
            backend.action('openTestProfile')
        args, kwargs = spawn.call_args
        self.assertEqual(kwargs['env']['BBGL_PROFILE_DIR'], str(selected))
        self.assertNotIn('BB_CONFIG', kwargs['env'])
        self.assertEqual(core.DATA_DIR, self.root)
        self.assertEqual(core.CONFIG_FILE, self.root / 'settings.json')
        self.assertEqual(args[0][0], sys.executable)
        self.assertEqual(LauncherBackend().value('test_profile_dir'), str(selected))

    def test_relative_path_and_file_are_rejected_without_launching(self):
        backend = LauncherBackend()
        for value in ('relative/profile', str(core.CONFIG_FILE)):
            backend.setValue('test_profile_dir', value)
            with patch.object(subprocess, 'Popen') as spawn:
                backend.action('openTestProfile')
            spawn.assert_not_called()

    def test_child_profile_replaces_parent_port(self):
        backend = LauncherBackend()
        for name, expected in (('Bloodborne Game Launcher Player 2', '3659'), ('custom', None)):
            backend.setValue('test_profile_dir', str(self.root / name))
            with patch.dict(os.environ, {'BB_P2P_PORT': '3658'}):
                with patch.object(subprocess, 'Popen') as spawn:
                    backend.open_test_profile()
            self.assertEqual(spawn.call_args.kwargs['env'].get('BB_P2P_PORT'), expected)


class ProfileSelectionTests(unittest.TestCase):
    def test_numbered_profiles_have_stable_ports(self):
        for player in range(1, 4):
            self.assertEqual(paths.profile_p2p_port(Path('root') / f'Bloodborne Game Launcher Player {player}'),
                             str(3657 + player))
        self.assertIsNone(paths.profile_p2p_port(Path('root') / 'other profile'))

    def test_game_environment_selects_profile_port_and_respects_override(self):
        with patch.object(core, 'DATA_DIR', Path('Bloodborne Game Launcher Player 3')):
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(core.game_environment(core.app_settings({}))['BB_P2P_PORT'], '3660')
            with patch.dict(os.environ, {'BB_P2P_PORT': '3900'}, clear=True):
                self.assertEqual(core.game_environment(core.app_settings({}))['BB_P2P_PORT'], '3900')

    def test_explicit_profile_skips_legacy_import_and_routes_all_data(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            port = base / 'install'
            port.mkdir()
            (port / 'bbport.ini').write_text('preset=3')
            legacy = base / 'bbgl'
            legacy.mkdir()
            (legacy / 'settings.json').write_text('{"coop_name":"Original"}')
            selected = base / 'test profile'
            env = {**os.environ, 'LOCALAPPDATA': temp, 'APPDATA': temp,
                   'BBGL_PROFILE_DIR': str(selected)}
            with patch.dict(os.environ, env):
                self.assertEqual(paths.initialize(port), selected)
            self.assertFalse((selected / 'settings.json').exists())
            self.assertFalse((selected / 'bbport.ini').exists())
            self.assertTrue((legacy / 'settings.json').exists())
            # Fresh process matters: DATA_DIR and CONFIG_FILE are import-time constants.
            script = """
import json
import bbport_launcher_win as core
import bbport_coop as coop
env = core.game_environment(core.app_settings({}))
print(json.dumps([str(core.CONFIG_FILE), str(coop.coop_dir()),
                  env['BB_DATA_DIR'], env['BB_USER_DIR']]))
"""
            result = subprocess.run([sys.executable, '-c', script], env=env,
                                    cwd=str(Path(core.__file__).parent),
                                    capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(result.stdout),
                             [str(selected / 'settings.json'), str(selected / 'coop'),
                              str(selected), str(selected / 'user')])


if __name__ == '__main__':
    unittest.main()
