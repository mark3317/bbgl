import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
import bbport_launcher_win as core


class OverlayLanguageTests(unittest.TestCase):
    def test_interface_language_is_independent_of_game_language(self):
        for ui, game, system, expected in [
            ('ru', '1', 'en', 'ru'),
            ('en', '8', 'ru', 'en'),
            ('', '1', 'ru', 'ru'),
            ('', '8', 'en', 'en'),
        ]:
            with self.subTest(ui=ui, game=game, system=system):
                settings = core.app_settings(dict(ui_language=ui, language=game))
                with patch.object(core, 'windows_language', return_value=system):
                    env = core.game_environment(settings)
                self.assertEqual(env['BB_UI_LANGUAGE'], expected)
                self.assertEqual(env['BB_LANGUAGE'], game)


if __name__ == '__main__':
    unittest.main()
