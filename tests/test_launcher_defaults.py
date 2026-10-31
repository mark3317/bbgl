import base64
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'launcher'), str(ROOT / 'scripts')]
import bbport_launcher_win as core
import bbport_startup as startup
import bbsc_information


class LauncherDefaultsTests(unittest.TestCase):
    def test_language_is_resolved_at_launch_and_manual_override_survives(self):
        settings = core.app_settings({'language': '1', 'launchDirectly': True})
        self.assertEqual(settings['language'], 'auto')
        self.assertNotIn('launchDirectly', settings)
        for system, expected in [('ru', '8'), ('en', '1'), ('ja', '0')]:
            with patch.object(core, 'windows_language', return_value=system):
                self.assertEqual(core.game_environment(settings)['BB_LANGUAGE'], expected)
        manual = core.app_settings(dict(settings, language='2'))
        self.assertEqual(core.game_language(manual), '2')

    def test_default_fullscreen_and_old_bypass_flag_open_launcher(self):
        self.assertTrue(core.APP_DEFAULTS['fullscreen'])
        settings = dict(core.APP_DEFAULTS, setupCompleted=True, launchDirectly=True)
        for args in ([], ['--play'], ['--launcher']):
            self.assertEqual(startup.choose_route(settings, args, False, True, True)['mode'], 'launcher')

    def test_information_has_localized_text_and_stable_notice_identity(self):
        for language, phrase in [('8', 'Колокол охоты'), ('1', 'Hunt Bell')]:
            with tempfile.TemporaryDirectory() as folder:
                path = bbsc_information.prepare(folder, language)
                data = json.loads(Path(path).read_text())
            notice = data['NoticeList'][0]
            self.assertIn(phrase, base64.b64decode(notice['Notice']).decode('utf-8'))
            self.assertIn('BBSC-GL', base64.b64decode(notice['Title']).decode('utf-8'))
            self.assertEqual(notice, bbsc_information.response(language)['NoticeList'][0])
