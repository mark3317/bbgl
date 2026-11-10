#!/usr/bin/env bash
# Builds dist/Bloodborne Game Launcher/ (and dist/bbgl-windows.zip): Bloodborne.exe (the launcher, frozen
# with PyInstaller so players need no Python), bb-probe.exe with the MSYS2 CLANG64 DLLs it needs,
# the preparation scripts and run.py. Run from an MSYS2 CLANG64 shell after `bash build.sh`.
# Freezing uses a Windows Python 3.10+ (python.org; WINPYTHON overrides) and a private venv with
# PyInstaller and PySide6 Essentials. FSR 4 assets are included when present.
set -euo pipefail
cd -- "$(dirname -- "$0")/../.."
source ./msys2-env.sh
[[ -f out/bb-probe.exe && -f out/bb-gpu-capabilities.exe && -f out/bb-play.exe ]] || { echo 'Build first: bash build.sh' >&2; exit 1; }

# A Windows Python (not MSYS2's) for PyInstaller.
python=${WINPYTHON:-}
if [[ -z $python ]]; then
    for candidate in /c/Python3*/python.exe "${LOCALAPPDATA:-/c/Users/$USER/AppData/Local}"/Programs/Python/Python3*/python.exe; do
        [[ -x $candidate ]] && python=$candidate
    done
fi
[[ -n $python ]] || { echo 'Need a Windows Python 3 (python.org) or WINPYTHON=path\to\python.exe' >&2; exit 1; }
# A venv outside Python's install tree may not find Tcl/Tk itself. Point PyInstaller's
# tkinter hook at the base interpreter's data so the frozen launcher keeps its UI.
for library in "$(dirname "$python")"/tcl/tcl*; do
    if [[ -d $library && -z ${TCL_LIBRARY:-} ]]; then export TCL_LIBRARY=$(cygpath -w "$library"); break; fi
done
for library in "$(dirname "$python")"/tcl/tk*; do
    if [[ -d $library && -z ${TK_LIBRARY:-} ]]; then export TK_LIBRARY=$(cygpath -w "$library"); break; fi
done
# Windows Python needs USERPROFILE (some MSYS2 shells start without it).
export USERPROFILE=${USERPROFILE:-$(cygpath -w "/c/Users/$(id -un)")}
venv=${BB_LAUNCHER_VENV:-out/qt-venv}
if [[ ! -x $venv/Scripts/python.exe ]]; then
    "$python" -m venv "$venv"
fi
# Qt Quick uses real translucent surfaces over full-window artwork. Pillow remains for the
# classic Tk fallback. Essentials avoids the unrelated, very large Qt Addons wheel.
"$venv/Scripts/python.exe" -m pip install -q --disable-pip-version-check pyinstaller pillow certifi bsdiff4==1.2.6 PySide6_Essentials==6.12.0
# The scripts run inside Bloodborne.exe (--script): the standard modules they import come along.
hidden=()
for module in socketserver hmac uuid queue random select http.server bsdiff4 argparse base64 bisect collections contextlib hashlib json re shutil struct tempfile               xml.etree.ElementTree urllib.request ctypes.wintypes certifi secrets; do
    hidden+=(--hidden-import "$module")
done
"$venv/Scripts/python.exe" -m PyInstaller --noconfirm --clean --log-level WARN --windowed \
    --name Bloodborne --icon "$(cygpath -w "$PWD/launcher/assets/hunter-icon.ico")" --distpath out/pyi-dist \
    --workpath out/pyi-work --specpath out/pyi-work --paths "$(cygpath -w "$PWD/scripts")" "${hidden[@]}" \
    "$(cygpath -w "$PWD/launcher/bbport_launcher_win.py")"
# Qt Quick needs the VC runtime shipped with the PySide6 wheel. PyInstaller can pick an older
# root copy from Windows Python. It can also collect an unrelated ICU from the build host's PATH;
# that DLL shadows Windows' ICU and prevents Qt6Core from loading in the packaged launcher.
pyi_internal=out/pyi-dist/Bloodborne/_internal
for dll in VCRUNTIME140.dll VCRUNTIME140_1.dll; do
    cp "$pyi_internal/PySide6/$dll" "$pyi_internal/$dll"
done
rm -f "$pyi_internal/icuuc.dll" "$pyi_internal/icudt78.dll"

# The package is assembled in a fresh staging folder and zipped from there; dist/Bloodborne Game Launcher
# (a playable copy that may hold saves and settings) is only refreshed afterwards.
dest="out/stage/Bloodborne Game Launcher"
rm -rf -- out/stage
mkdir -p "$dest/bin" "$dest/launcher"
cp -r out/pyi-dist/Bloodborne/. "$dest/"
llvm-strip -o "$dest/bin/Play Bloodborne.exe" out/bb-play.exe
cp launcher/bloodborne.ico launcher/bloodborne.png "$dest/launcher/"
cp -r launcher/art "$dest/launcher/"
cp -r launcher/qml "$dest/launcher/"
mkdir -p "$dest/launcher/assets"
cp launcher/assets/hunter-icon.ico "$dest/launcher/assets/"
cp -r launcher/assets/ui "$dest/launcher/assets/"
# The executables without debug information (out/ keeps the symbols for crash reports).
for exe in bb-probe.exe bb-gpu-capabilities.exe; do
    llvm-strip --strip-debug -o "$dest/bin/$exe" "out/$exe"
done
# Every DLL the executables load from the CLANG64 tree (SDL3, FFmpeg, Vulkan loader, ...).
ldd "$dest/bin/bb-probe.exe" "$dest/bin/bb-gpu-capabilities.exe" |
    awk '/\/clang64\/bin\// {print $3}' | sort -u | while read -r dll; do
        cp -u "$dll" "$dest/bin/"
    done
cp -r scripts patches "$dest/"
"$venv/Scripts/python.exe" packaging/windows/bundle-prompts.py "$dest"
"$venv/Scripts/python.exe" packaging/windows/bundle-diamond-sword.py "$dest"
# Legacy CPU (Intel 3rd generation and older): the translation plan scripts/cpu_compat.py applies.
mkdir -p "$dest/tools" && cp tools/legacy-cpu-plan.json "$dest/tools/"
cp run.py LICENSE README.md README.ru.md CHANGELOG.md THIRD_PARTY.md packaging/windows/README-Windows.txt "$dest/"
mkdir -p "$dest/docs"
cp -r docs/screenshots "$dest/docs/"
cp docs/release-1.5.8.md "$dest/docs/"
if [[ -d fsr4_shaders ]]; then cp -r fsr4_shaders "$dest/"; fi
# Shader pre-build catalog (scripts/shader_catalog.py): records only, no game code or SPIR-V.
if [[ -d shader_catalog ]]; then cp -r shader_catalog "$dest/"; fi
# DLSS (NVIDIA RTX): the MSVC-built bridge and NVIDIA's runtime, next to bb-probe.exe
# (packaging/windows/build_dlss.sh). Without them the DLSS option stays unavailable.
if [[ -f out/bbport_dlss.dll && -f out/nvngx_dlss.dll ]]; then
    cp out/bbport_dlss.dll out/nvngx_dlss.dll "$dest/bin/"
    if [[ -f out/nvngx_dlssg.dll ]]; then cp out/nvngx_dlssg.dll "$dest/bin/"; fi
    mkdir -p "$dest/licenses" && cp out/NVIDIA-DLSS-LICENSE.txt "$dest/licenses/"
    cp gpu/dlss_bridge/LICENSE.txt "$dest/licenses/bbport_dlss-LICENSE.txt"
else
    echo "DLSS bridge not built (packaging/windows/build_dlss.sh): no DLSS in this package" >&2
fi
# Online co-op: the libraries compiled in (wepoll, cpp-httplib) and the MSYS2 DLLs it loads.
mkdir -p "$dest/licenses"
cp gpu/third_party/wepoll/LICENSE "$dest/licenses/wepoll-LICENSE.txt"
cp gpu/third_party/httplib/LICENSE "$dest/licenses/cpp-httplib-LICENSE.txt"
cp packaging/windows/licenses/*.txt "$dest/licenses/"
# Where The Hunter's Dream backend comes from (Awaken's port of bbhost's network code, GPL-3.0).
cp gpu/bbnet/THD-PORT.md "$dest/licenses/online-code-NOTICE.md"
cp gpu/bbnet/SHADNET-PORT.md "$dest/licenses/shadps4-network-NOTICE.md"
for package in protobuf abseil-cpp openssl miniupnpc zlib; do
    license=/clang64/share/licenses/$package/LICENSE
    if [[ -f $license ]]; then cp "$license" "$dest/licenses/$package-LICENSE.txt"; fi
done
"$venv/Scripts/python.exe" packaging/windows/bundle-coop.py
find "$dest" -name __pycache__ -prune -exec rm -r {} +
if [[ ${BB_FAST_DEPLOY:-0} != 1 ]]; then
"$venv/Scripts/python.exe" packaging/windows/verify-release.py "$dest"
# Nothing from the game itself may ship: its archives (.dcx and what they hold) and executables.
game_files=$(find "$dest" -type f ! -path "$dest/launcher/assets/button-prompts/*/menu/common.tpf.dcx" \( -iname '*.dcx' -o -iname '*.tpf' -o -iname '*bnd' -o -iname '*.bdt' \
    -o -iname '*.bhd' -o -iname '*.prx' -o -iname '*.sprx' -o -iname 'eboot.bin' -o -iname 'param.sfo' \))
if [[ -n $game_files ]]; then
    echo "Game files in the package (players supply their own):" >&2
    echo "$game_files" >&2
    exit 1
fi
fi
mkdir -p dist
rm -f dist/bbgl-windows.zip
# Zip entries need forward slashes: Windows PowerShell's Compress-Archive writes backslashes,
# which other unzip tools (Linux, Proton) turn into flat files named "Bloodborne Game Launcher\_internal\..."
# (issue #75).
"$venv/Scripts/python.exe" - out/stage dist/bbgl-windows.zip <<'PY'
from pathlib import Path
import sys, zipfile

stage, archive = Path(sys.argv[1]), Path(sys.argv[2])
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as package:
    for path in sorted((stage / 'Bloodborne Game Launcher').rglob('*')):
        if path.is_file():
            package.write(path, path.relative_to(stage).as_posix())
PY

du -sh "$dest" dist/bbgl-windows.zip
