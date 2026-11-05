"""Settings behavior in isolated profiles: effective folders and independent presets."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'launcher'), str(ROOT/'scripts')]
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtWidgets import QApplication
import bbport_coop as coop
import bbport_launcher_win as core
from bbport_launcher_backend import LauncherBackend, SETTINGS_SECTIONS
import bbport_qml_ru as ru


class SettingsCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qt = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for context in [patch.object(core, 'PORT_DIR', self.root/'install'),
                        patch.object(core, 'DATA_DIR', self.root/'profile'),
                        patch.object(core, 'CONFIG_FILE', self.root/'settings.json'),
                        patch.object(LauncherBackend, 'start_background_checks'),
                        patch.dict(os.environ, BB_CONFIG=str(self.root/'bbport.ini'))]:
            context.start()
            self.addCleanup(context.stop)
        self.backend = LauncherBackend()
        for timer in (self.backend._party_timer, self.backend._party_network_timer, self.backend._addons_timer):
            timer.stop()
        self.addCleanup(self.backend.shutdown_coop)

    def test_folders_show_the_effective_runtime_paths(self):
        b = self.backend
        for key, expected in [('mods_dir', core.PORT_DIR/'mods'), ('patches_dir', core.DATA_DIR/'patches')]:
            b.app[key] = ''
            self.assertEqual(b.value(key), str(expected))
            self.assertEqual(b.app[key], '')  # showing a default never rewrites the setting
            b.app[key] = str(self.root/'custom'/key)
            self.assertEqual(b.value(key), b.app[key])
        sections = dict(SETTINGS_SECTIONS['Mods & Patches'])
        self.assertNotIn('Mod folders', sections)
        self.assertTrue({'mods_enabled', 'mods_dir', 'patches_dir'} <= set(sections['Installed mods']))

    def test_open_profile_uses_active_profile_without_launching_test_profile(self):
        self.backend.app['test_profile_dir'] = str(self.root/'other-profile')
        with patch('os.startfile') as open_folder, \
             patch.object(self.backend, 'open_test_profile') as launch_profile:
            self.backend.action('openProfile')
        open_folder.assert_called_once_with(str(core.DATA_DIR))
        launch_profile.assert_not_called()

    def test_upscaling_and_generation_do_not_change_quality_selection(self):
        b = self.backend
        b._dlss_supported = True
        for preset in ('low', 'high', 'ultra', 'custom'):
            b.applyGraphicsPreset(preset)
            for key, values in [('upscaler', ('fsr3', 'off', 'dlss', 'off')),
                                ('frame_gen', ('fsr3', 'off', 'dlss', 'off')),
                                ('preset', ('0', '3', '1'))]:
                for value in values:
                    b.setValue(key, value)
                    self.assertEqual(b.graphicsPreset, preset, (preset, key, value))
                    self.assertEqual(b.app['graphics_preset'], preset)
        b.applyGraphicsPreset('ultra')
        b.setValue('model_lod', '1')
        self.assertEqual(b.graphicsPreset, 'custom')

    def test_firewall_action_and_script_generation_are_removed(self):
        self.assertFalse(hasattr(LauncherBackend, 'coopConfigureFirewall'))
        self.assertFalse(hasattr(LauncherBackend, 'coopFirewallError'))
        for name in ('_firewall_script', 'setup_done', 'run_setup', 'run_as_administrator'):
            self.assertFalse(hasattr(coop, name))
        for name in ('Main.qml', 'CoopConnection.qml', 'SettingsWorkspace.qml'):
            text = (ROOT/'launcher/qml'/name).read_text(encoding='utf-8')
            self.assertNotIn('firewall', text.lower())
        self.assertEqual(ru.RU['Players online:'], 'В сети:')
        self.assertNotIn('P2P', ru.RU['Play with friends'])


if __name__ == '__main__':
    unittest.main()
