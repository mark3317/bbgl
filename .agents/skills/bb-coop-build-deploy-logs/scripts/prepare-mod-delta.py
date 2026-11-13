"""Refresh an existing development stage and create a small mod-only deployment ZIP."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()
stage = repo / 'out/stage/Bloodborne Game Launcher'
fork = repo / 'mods-src/BBSC'
manifest_path = stage / 'coop/client/bundle.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
source_path = stage / 'coop/SOURCE.json'
source = json.loads(source_path.read_text(encoding='utf-8'))
revision = subprocess.check_output(['git', '-C', str(fork), 'rev-parse', 'HEAD'], text=True).strip()
version = json.loads((fork / 'build/mod/mod.json').read_text(encoding='utf-8'))['version']
files = []
for name in ('bbsc.dll', 'bbsc-launch.exe', 'mod.json'):
    relative = 'coop/client/bbsc/' + name
    target = stage / relative
    shutil.copy2(fork / 'build/mod' / name, target)
    # Runtime manifest data, not a verification pass. Unchanged entries are reused.
    manifest['files']['bbsc/' + name] = hashlib.sha256(target.read_bytes()).hexdigest()
    files.append(relative)
manifest.update(version=version, source=f'https://github.com/mark3317/bbsc-gl/tree/{revision}')
source.update(bbsc_commit=revision, version=version)
for path, data in ((manifest_path, manifest), (source_path, source)):
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    files.append(path.relative_to(stage).as_posix())
archive = repo / 'out/mod-delta.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as package:
    for relative in files:
        package.write(stage / relative, 'Bloodborne Game Launcher/' + relative)
print(archive)
print('files=' + ','.join(files))
