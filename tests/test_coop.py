import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
import bbport_coop as coop


class CoopTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        patcher = mock.patch.dict(os.environ, {'LOCALAPPDATA': self.folder.name, 'APPDATA': self.folder.name})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.folder.cleanup)
        port_patch = mock.patch.object(coop, 'port_dir', return_value=Path(self.folder.name) / 'port')
        port_patch.start()
        self.addCleanup(port_patch.stop)

    @unittest.skip("Historical server save contract retained; migrate separately to Party before running")
    def test_bbsc_is_told_where_the_saves_are(self):
        # BBSC gives its co-op kit (Hunt Bell, Kin Bell) only after backing up the save it finds.
        user = Path(self.folder.name) / 'saves'
        older = user / 'savedata' / '2' / 'CUSA00207' / 'SPRJ0005'
        newer = user / 'savedata' / '1' / 'CUSA00207' / 'SPRJ0005'
        for folder, when in ((older, 1000), (newer, 2000)):
            folder.mkdir(parents=True)
            (folder / 'userdata0000').write_bytes(b'save')
            os.utime(folder / 'userdata0000', (when, when))
        port = Path(self.folder.name) / 'Bloodborne Game Launcher'
        env = coop.co_op_environment({'BB_USER_DIR': str(user)}, '100.65.141.9', 'hunter', 'secret',
                                     port / 'bin' / 'bb-probe.exe')
        self.assertEqual(Path(env['BBSC_SAVE_DIR']), newer)
        # With the copy made before the session, BBSC backs that up instead: copying the save the
        # running game has open failed, and the kit was never given.
        copy = coop.backup_saves(user)
        env = coop.co_op_environment({'BB_USER_DIR': str(user)}, '100.65.141.9', 'hunter', 'secret',
                                     port / 'bin' / 'bb-probe.exe', save_copy=copy)
        self.assertEqual(Path(env['BBSC_SAVE_DIR']),
                         copy / 'savedata' / '1' / 'CUSA00207' / 'SPRJ0005')
        self.assertTrue((Path(env['BBSC_SAVE_DIR']) / 'userdata0000').is_file())

    def test_firewall_rules_stay_on_tailscale_and_the_home_network(self):
        script = coop._firewall_script(r'C:\Games\bbport\bin\bb-probe.exe')
        self.assertIn("@('100.64.0.0/10','LocalSubnet')", script)
        self.assertNotIn('Any', script)
        self.assertEqual(script.count('New-NetFirewallRule'), len(coop.FIREWALL_PORTS) + 1)

    def test_firewall_script_quotes_an_apostrophe_in_the_path(self):
        script = coop._firewall_script(r"C:\Users\O'Neil\bbport\bin\bb-probe.exe")
        self.assertIn(r"-Program 'C:\Users\O''Neil\bbport\bin\bb-probe.exe'", script)

    def test_tailscale_addresses(self):
        self.assertTrue(coop.is_tailscale('100.65.141.9'))
        self.assertFalse(coop.is_tailscale('100.128.0.1'))
        self.assertFalse(coop.is_tailscale('192.168.1.5'))

    def test_tailscale_is_found_on_path_outside_program_files(self):
        # Ask which() for the full 'tailscale.exe', not bare 'tailscale': the bare
        # name is only ever resolved by appending a PATHEXT entry, so what comes back
        # is 'tailscale' + whatever extension matched; the full name makes the result
        # unambiguously the file handed to subprocess.run. Also check that exact file
        # is the one run.
        exe = r'D:\Apps\Tailscale\tailscale.exe'
        ran = mock.Mock(stdout='100.65.141.9\n')
        with mock.patch.object(coop.shutil, 'which', return_value=exe) as which, \
                mock.patch.object(coop.subprocess, 'run', return_value=ran) as run:
            self.assertEqual(coop.tailscale_ip(), '100.65.141.9')
        which.assert_called_once_with('tailscale.exe')
        self.assertEqual(run.call_args[0][0][0], str(Path(exe)))

    def test_tailscale_found_in_program_files_when_not_on_path(self):
        # Not on PATH, so which() misses; it must fall back to the install folder,
        # ProgramW6432 before ProgramFiles, and only when the file is there. Both
        # env vars point at our own temp dirs so the real C:\Program Files on the
        # test machine is never consulted. A distinct exe in each proves the order.
        with tempfile.TemporaryDirectory() as w6432, tempfile.TemporaryDirectory() as pf:
            exe_w6432 = Path(w6432) / 'Tailscale' / 'tailscale.exe'
            exe_pf = Path(pf) / 'Tailscale' / 'tailscale.exe'
            exe_w6432.parent.mkdir()
            exe_pf.parent.mkdir()
            exe_w6432.write_bytes(b'')
            exe_pf.write_bytes(b'')
            env = {'ProgramW6432': w6432, 'ProgramFiles': pf}
            with mock.patch.object(coop.shutil, 'which', return_value=None), \
                    mock.patch.dict(coop.os.environ, env, clear=False):
                # ProgramW6432 wins over ProgramFiles when both hold the exe.
                self.assertEqual(coop.tailscale_exe(), exe_w6432)
            # ProgramW6432 empty, ProgramFiles has it: fall through to ProgramFiles.
            exe_w6432.unlink()
            with mock.patch.object(coop.shutil, 'which', return_value=None), \
                    mock.patch.dict(coop.os.environ, env, clear=False):
                self.assertEqual(coop.tailscale_exe(), exe_pf)
            # Neither folder has it: no exe is reported.
            exe_pf.unlink()
            with mock.patch.object(coop.shutil, 'which', return_value=None), \
                    mock.patch.dict(coop.os.environ, env, clear=False):
                self.assertIsNone(coop.tailscale_exe())

    def test_tailscale_address_from_the_route_when_the_cli_is_missing(self):
        probe = mock.MagicMock()
        probe.__enter__.return_value.getsockname.return_value = ('100.65.141.9', 50000)
        with mock.patch.object(coop, 'tailscale_exe', return_value=None), \
                mock.patch.object(coop.socket, 'socket', return_value=probe):
            self.assertEqual(coop.tailscale_ip(), '100.65.141.9')
        probe.__enter__.return_value.getsockname.return_value = ('192.168.1.5', 50000)
        with mock.patch.object(coop, 'tailscale_exe', return_value=None), \
                mock.patch.object(coop.socket, 'socket', return_value=probe):
            self.assertIsNone(coop.tailscale_ip())

if __name__ == '__main__':
    unittest.main()
