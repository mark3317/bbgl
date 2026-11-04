"""Russian text contracts; run with the Qt venv, no game/profile access."""
import json
import os
from pathlib import Path
import re
import string
import sys
import tempfile
import unittest
from collections import Counter
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'launcher'), str(ROOT / 'scripts'),
                str(ROOT / 'mods-src/BBSC/tools/gamedata')]
import bbport_qml_ru as ru
import gen_messages_ru as mod_ru
import menu_assets


class LocalizationTests(unittest.TestCase):
    def test_dynamic_errors_translate_and_preserve_paths(self):
        path = r'C:\Users\Hunter {2}\game'
        self.assertEqual(ru.tr('Could not open profile: ' + path),
                         ru.RU['Could not open profile: {}'].format(path))
        self.assertEqual(ru.tr('Player 3: the configured game folder is unavailable.'),
                         'Игрок 3: указанная папка игры недоступна.')
        self.assertEqual(ru.tr('Unsafe archive path: ' + path),
                         'Небезопасный путь внутри архива: ' + path)

    def test_format_arguments_survive_translation(self):
        def fields(text):
            automatic = 0
            result = []
            for _, name, spec, conversion in string.Formatter().parse(text):
                if name is not None:
                    if name == '':
                        name = str(automatic)
                        automatic += 1
                    result.append((name, spec, conversion))
            return Counter(result)
        for english, russian in list(ru.RU.items()) + ru.PATTERNS:
            with self.subTest(text=english):
                self.assertEqual(fields(english), fields(russian))

    def test_generated_mod_text_is_current_and_preserves_game_tokens(self):
        original = Path(mod_ru.OUT).read_text(encoding='utf-8')
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'messages.inc'
            with patch.object(mod_ru, 'OUT', str(target)):
                mod_ru.main()
            self.assertEqual(original, target.read_text(encoding='utf-8'))
        pattern = r'^\{(\d+), (\d+), u"((?:[^"\\]|\\.)*)"\},'
        english = re.findall(pattern, Path(mod_ru.SOURCE).read_text(encoding='utf-8'), re.M)
        russian = re.findall(pattern, original, re.M)
        self.assertEqual([row[:2] for row in english], [row[:2] for row in russian])
        for en, translated in zip(english, russian):
            self.assertEqual(Counter(re.findall(r'<\?.*?\?>', en[2])),
                             Counter(re.findall(r'<\?.*?\?>', translated[2])), en[:2])

    def test_native_menu_ids_and_concise_help(self):
        english = menu_assets.read_messages()
        russian = menu_assets.read_messages(ROOT / 'scripts/pc_menu_messages_ru.tsv')
        self.assertEqual(english.keys(), russian.keys())
        for mid, (text, hint) in russian.items():
            self.assertTrue(text, mid)
            # Editorial budget, not a substitute for measuring the game's font.
            self.assertLessEqual(len(hint), 52, (mid, hint))
        self.assertEqual(russian[14000351][0], 'Реванш: Людвиг Священный клинок')


class LocalizedLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
        from PySide6.QtGui import QGuiApplication
        cls.app = QGuiApplication.instance() or QGuiApplication([])

    def test_long_choice_wraps_in_closed_control_and_popup(self):
        from PySide6.QtCore import QObject, QUrl
        from PySide6.QtQml import QQmlApplicationEngine
        from PySide6.QtQuick import QQuickItem
        engine = QQmlApplicationEngine()
        label = ru.tr('Ultra Performance (×3)')
        qml = '''import QtQuick
import QtQuick.Controls
Window {
    width: 400; height: 400; visible: true
    GlassComboBox {
        objectName: "choice"; width: 160
        property QtObject testPopup: popup
        property Item testDelegate: popup.contentItem.currentItem
        model: [{text: LABEL, value: "3"}]; textRole: "text"
    }
    GlassButton {
        objectName: "button"; y: 220; width: 180; height: 48
        text: "Установить новую версию"
    }
}'''.replace('LABEL', json.dumps(label, ensure_ascii=False))
        engine.loadData(qml.encode(), QUrl.fromLocalFile(str(ROOT / 'launcher/qml/LocalizationTest.qml')))
        self.assertTrue(engine.rootObjects())
        window = engine.rootObjects()[0]
        try:
            for _ in range(5):
                self.app.processEvents()
            choice = window.findChild(QObject, 'choice')
            text = choice.property('contentItem')
            self.assertGreater(text.property('lineCount'), 1)
            self.assertGreaterEqual(text.height(), text.property('paintedHeight'))
            popup = choice.property('testPopup')
            popup.setProperty('visible', True)
            for _ in range(10):
                self.app.processEvents()
            delegate = choice.property('testDelegate')
            self.assertIsNotNone(delegate)
            popup_text = delegate.property('contentItem')
            self.assertGreater(popup_text.property('lineCount'), 1)
            self.assertGreaterEqual(popup_text.height(), popup_text.property('paintedHeight'))
            self.assertLessEqual(delegate.width(), popup.property('availableWidth'))
            button = window.findChild(QObject, 'button').property('contentItem')
            self.assertFalse(button.property('truncated'))
            self.assertGreaterEqual(button.height(), button.property('paintedHeight'))
        finally:
            window.close()
            engine.deleteLater()
            self.app.processEvents()


if __name__ == '__main__':
    unittest.main()
