"""Exercise real native entry points against a stand-in child, without starting the game."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
COMPILER = Path('C:/msys64/clang64/bin/clang.exe')
PROBE = r'''
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <wchar.h>
int wmain(int argc, wchar_t **argv) {
    if (argc != 3) return 2;
    FILE *out = _wfopen(argv[1], L"wb");
    if (!out) return 3;
    const wchar_t *names[] = {L"BBGL_PROFILE_DIR", L"BB_P2P_PORT", L"BB_CONFIG",
                             L"BB_DATA_DIR", L"BB_USER_DIR", L"BBSC_DATA_DIR"};
    for (unsigned i = 0; i < sizeof(names) / sizeof(names[0]); ++i) {
        wchar_t value[32768] = L"";
        GetEnvironmentVariableW(names[i], value, 32768);
        fwrite(value, sizeof(wchar_t), wcslen(value), out);
        fwrite(L"\n", sizeof(wchar_t), 1, out);
    }
    fwrite(argv[2], sizeof(wchar_t), wcslen(argv[2]), out);
    fclose(out);
    return 17;
}
'''


@unittest.skipUnless(os.name == 'nt' and COMPILER.is_file(), 'Windows clang required')
class ProfileEntrypointTests(unittest.TestCase):
    def test_three_concurrent_children_have_distinct_profiles_and_ports(self):
        with tempfile.TemporaryDirectory(prefix='profile entrypoints ') as temp:
            folder = Path(temp)
            source = folder / 'probe.c'
            source.write_text(PROBE)
            subprocess.run([str(COMPILER), '-static', '-municode', str(source),
                            '-o', str(folder / 'Bloodborne.exe')], check=True,
                           capture_output=True)
            env = dict(os.environ, BBGL_PROFILE_DIR='inherited', BB_P2P_PORT='9999',
                       BB_CONFIG='old.ini', BB_DATA_DIR='old', BB_USER_DIR='old', BBSC_DATA_DIR='old')
            children = []
            for number in range(1, 4):
                name = f'Bloodborne Player {number}.exe'
                shutil.copy2(REPO / 'out/profile-launchers' / name, folder / name)
                output = folder / f'player {number}.txt'
                child = subprocess.Popen([str(folder / name), str(output), 'space argument'], env=env,
                                         creationflags=subprocess.CREATE_NO_WINDOW)
                children.append((number, child, output))
            profiles, ports = set(), set()
            for number, child, output in children:
                self.assertEqual(child.wait(timeout=15), 17)
                profile, port, *remaining = output.read_text(encoding='utf-16-le').splitlines()
                self.assertTrue(Path(profile).is_absolute())
                self.assertEqual(Path(profile).name, f'Bloodborne Game Launcher Player {number}')
                self.assertEqual(port, str(3657 + number))
                self.assertEqual(remaining, ['', '', '', '', 'space argument'])
                profiles.add(profile)
                ports.add(port)
            self.assertEqual(len(profiles), 3)
            self.assertEqual(len(ports), 3)


if __name__ == '__main__':
    unittest.main()
