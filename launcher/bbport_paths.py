"""One writable profile for the Windows launcher; installed files stay immutable."""
import os
from pathlib import Path
import shutil
import json


PROFILE_NAME = 'Bloodborne Game Launcher'


def _copy_missing(source, target):
    """Merge old data without replacing any files in the new profile."""
    if not source.is_dir():
        return
    for item in source.rglob('*'):
        destination = target / item.relative_to(source)
        if item.is_file() and not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)


def _migrate_paths(root, legacy):
    config = root / 'settings.json'
    if not config.is_file():
        return
    try:
        settings = json.loads(config.read_text(encoding='utf-8'))
    except (ValueError, OSError):
        return
    if not isinstance(settings, dict):
        return
    for key in ('user_dir', 'mods_dir', 'patches_dir', 'coop_user_dir'):
        value = settings.get(key)
        if value:
            try:
                settings[key] = str(root / Path(value).relative_to(legacy))
            except ValueError:
                pass
    for key in tuple(settings):
        if key.startswith('thd_') or key in ('online_pool', 'online_community'):
            del settings[key]
    if settings.get('play_mode') not in ('offline', 'coop'):
        settings['play_mode'] = 'offline'
    settings['online'] = False
    config.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding='utf-8')


def profile_dir():
    local = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
    roaming = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
    root = local / PROFILE_NAME
    # Rename on the same volume: saves and large shader caches need no duplicate copy.
    legacy_bbgl = local / 'bbgl'
    marker = root / '.migrated-from-bbgl-v1'
    if legacy_bbgl.is_dir() and not marker.exists():
        if not root.exists():
            legacy_bbgl.rename(root)
        else:
            _copy_missing(legacy_bbgl, root)
        _migrate_paths(root, legacy_bbgl)
        marker.write_text('1\n', encoding='utf-8')
    # GPU cache belongs to the shared profile, independent of the selected save folder.
    config = root / 'settings.json'
    selected_user = ''
    if config.is_file():
        try:
            settings = json.loads(config.read_text(encoding='utf-8'))
            if isinstance(settings, dict):
                selected_user = settings.get('user_dir', '')
        except (ValueError, OSError):
            pass
    caches = [root / 'user' / 'cache']
    if selected_user and Path(selected_user).is_relative_to(root):
        caches.append(Path(selected_user) / 'cache')
    for cache in dict.fromkeys(caches):
        if cache.is_dir():
            if not (root / 'cache').exists():
                cache.rename(root / 'cache')
            else:
                cache_marker = root / ('.migrated-cache-' + '-'.join(cache.relative_to(root).parts) + '-v1')
                if not cache_marker.exists():
                    _copy_missing(cache, root / 'cache')
                    cache_marker.write_text('1\n', encoding='utf-8')
    # Prefer the most recent Local profile, then fill gaps from the older Roaming one.
    # A new marker makes this independent of the previous Roaming-to-Local migration.
    for label, legacy in (('local', local / 'bbport-launcher'),
                          ('roaming', roaming / 'bbport-launcher')):
        marker = root / f'.migrated-from-{label}-bbport-v1'
        if legacy.is_dir() and not marker.exists():
            root.mkdir(parents=True, exist_ok=True)
            for source in legacy.rglob('*'):
                target = root / source.relative_to(legacy)
                if source.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                elif source.is_file() and not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
            marker.write_text('1\n', encoding='utf-8')

    return root


def initialize(port):
    root = profile_dir()
    root.mkdir(parents=True, exist_ok=True)
    port = Path(port)
    # Import existing portable data once, without overwriting the user's profile.
    # Old installations remain untouched until the user retires that installation.
    marker = root / 'profile-layout-v2'
    if not marker.exists():
        for name in ('bbport.ini', 'mods.json', 'patches.json', 'input.ini', 'user'):
            source, target = port / name, root / name
            if source.exists() and not target.exists():
                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    shutil.copy2(source, target)
        legacy = Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'bbport-coop'
        # Mutable BBSC journals and the host database are independent of installed binaries.
        for old, new in (('bbsc-client/bbsc', 'bbsc'),
                         ('BBSC-0.0.2-BBport/bbsc', 'bbsc'),
                         ('shadnet-bbport', 'server'), ('bbsc-server/server', 'server')):
            source = legacy / old
            for item in source.rglob('*'):
                if (not item.is_file() or item.suffix.lower() in ('.exe', '.dll')
                        or item.name in ('mod.json', 'SOURCE.txt', 'LICENSE.txt')):
                    continue
                target = root / 'coop' / new / item.relative_to(source)
                if not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target)
        marker.write_text('2\n', encoding='utf-8')
    # Ship patch definitions with the application, keep user additions in the profile.
    for source in (port / 'patches').rglob('*'):
        if source.is_file():
            target = root / 'patches' / source.relative_to(Path(port) / 'patches')
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
    # Ready-made icon mods live in the installation; selection stays in AppData.
    import json
    mods_marker = root / 'ready-mods-layout-v1'
    if not mods_marker.exists():
        config = root / 'mods.json'
        profile = json.loads(config.read_text(encoding='utf-8')) if config.exists() else {}
        disabled = set(profile.get('disabled', []))
        known = set(profile.get('enabled', [])) | set(profile.get('order', []))
        for name in ('Xbox Prompts (Dommo)', 'Keyboard Prompts (PCBButtons)'):
            if name not in known:
                disabled.add(name)
        profile['disabled'] = sorted(disabled)
        config.write_text(json.dumps(profile, indent=2), encoding='utf-8')
        for source in (root / 'mods').iterdir() if (root / 'mods').is_dir() else ():
            target = port / 'mods' / source.name
            if source.is_dir() and not target.exists():
                shutil.copytree(source, target)
        mods_marker.write_text('1\n', encoding='utf-8')
    return root
