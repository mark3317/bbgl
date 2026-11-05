"""Render the current QML launcher using an isolated example profile, without network or game access."""
import os
import argparse
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'launcher'), str(ROOT / 'scripts')]
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from PySide6.QtCore import QObject, QUrl, QPointF
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
import bbport_launcher_win as core
from bbport_launcher_backend import LauncherBackend


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language', choices=('en', 'ru'), default='en')
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/screenshots')
    parser.add_argument('--review', action='store_true', help='Capture all sections and setup steps at normal/minimum size')
    args = parser.parse_args()
    QQuickStyle.setStyle('Basic')
    app = QApplication([])
    with tempfile.TemporaryDirectory(prefix='bbgl-screenshots-') as folder:
        profile = Path(folder)
        names = {'CONFIG_DIR': profile, 'DATA_DIR': profile,
                 'CONFIG_FILE': profile / 'settings.json', 'INI_FILE': profile / 'bbport.ini',
                 'MODS_FILE': profile / 'mods.json', 'PATCHES_FILE': profile / 'patches.json'}
        with patch.multiple(core, create=True, **names), \
             patch.dict(core.APP_DEFAULTS, ui_language=args.language, check_updates=False,
                        game_dir=str(profile / 'game'), user_dir=str(profile / 'user')), \
             patch.object(LauncherBackend, 'start_background_checks'), \
             patch.dict(os.environ, BB_CONFIG=str(profile / 'bbport.ini')):
            backend = LauncherBackend()
            # Example display paths only; no reads/writes or discovery at these paths.
            backend.app.update(player_name='Hunter', mods_dir='C:/Games/BBGL/mods',
                               patches_dir='C:/Games/BBGL/profile/patches')
            backend._mods = [dict(name='Diamond Sword', enabled=False)]
            backend._coop_inventory_ready = True
            for timer in (backend._party_timer, backend._party_network_timer, backend._addons_timer):
                timer.stop()
            engine = QQmlApplicationEngine()
            engine.rootContext().setContextProperty('launcher', backend)
            warnings = []
            engine.warnings.connect(lambda rows: warnings.extend(row.toString() for row in rows))
            engine.load(QUrl.fromLocalFile(str(ROOT / 'launcher/qml/Main.qml')))
            assert engine.rootObjects(), warnings
            window = engine.rootObjects()[0]
            window.setWidth(1290)
            window.setHeight(900)
            workspace = window.findChild(QObject, 'settingsWorkspace')
            output = args.output.resolve()
            output.mkdir(parents=True, exist_ok=True)
            shots = [('home', None, None), ('graphics', 'Visuals', 'Display & frame rate'),
                     ('coop', 'Co-op', 'Seamless co-op'),
                     ('mods', 'Mods & Patches', 'Installed mods')]
            if args.review:
                import bbport_launcher_backend as model
                shots = [('home', None, None)]
                shots += [(f'section-{i}-{j}', category, section)
                          for i, (category, sections) in enumerate(model.SETTINGS_SECTIONS.items())
                          for j, (section, _) in enumerate(sections)]
                shots += [(f'setup-{step}', 'Setup', step) for step in range(4)]
            sizes = [(1290, 900), (1050, 650)] if args.review else [(1290, 900)]
            metrics = []
            def inspect(item, screen):
                if item.isVisible() and item.metaObject().className().startswith('QQuickText'):
                    names = {item.metaObject().property(i).name() for i in range(item.metaObject().propertyCount())}
                    if 'truncated' in names:
                        pos = item.mapToScene(QPointF(0, 0))
                        if (0 <= pos.x() < window.width() and 0 <= pos.y() < window.height()
                                and (item.property('truncated') or item.property('paintedHeight') > item.height() + 1)):
                            metrics.append(dict(screen=screen, text=item.property('text'),
                                                truncated=item.property('truncated'),
                                                height=item.height(), painted=item.property('paintedHeight')))
                for child in item.childItems():
                    inspect(child, screen)
            try:
                for width, height in sizes:
                    window.setWidth(width)
                    window.setHeight(height)
                    for name, category, section in shots:
                        window.setProperty('page', 'Setup' if category == 'Setup' else 'Settings' if category else 'Home')
                        if category == 'Setup':
                            window.findChild(QObject, 'setupWizard').setProperty('step', section)
                        elif category:
                            workspace.openAt(category, section, '')
                        QTest.qWait(220 if args.review else 700)
                        suffix = f'-{width}' if args.review else ''
                        target = output / f'launcher-{name}{suffix}.png'
                        assert window.grabWindow().save(str(target)), target
                        if args.review:
                            inspect(window.contentItem(), target.name)
                        else:
                            print(target.name)
                assert not warnings, '\n'.join(warnings)
                if args.review:
                    (output / 'layout-review.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
                    print(f'{args.language}: {len(shots) * len(sizes)} screens; {len(metrics)} text metrics to review')
            finally:
                window.close()
                backend.shutdown_coop()
                engine.deleteLater()
                app.processEvents()
    print('Current QML screenshots: PASS (temporary profile, no game or network)')


if __name__ == '__main__':
    main()
