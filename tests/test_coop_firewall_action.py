"""Launching never elevates; firewall setup is an explicit user action."""
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
import bbport_coop as coop
from bbport_launcher_backend import LauncherBackend


class FirewallActionTests(unittest.TestCase):
    def backend(self):
        backend = SimpleNamespace(
            process=None, _coop_busy=False,
            app={'coop_invite': 'invite', 'user_dir': 'test-saves'},
            _coop_host=SimpleNamespace(running=False, start=Mock()),
            _coop_account=lambda: ('hunter', 'password'), _write=Mock(),
            _coop_ensure_packages=Mock(), _coop_probe=lambda: Path('game.exe'),
            _coop_game_exe=lambda: Path('game.exe'))
        backend._coop_run = lambda message, work: work()
        return backend

    def test_join_does_not_check_or_configure_firewall(self):
        backend = self.backend()
        with patch.object(coop, 'setup_done', side_effect=AssertionError('automatic check')), \
                patch.object(coop, 'run_setup', side_effect=AssertionError('automatic elevation')), \
                patch.object(coop, 'read_invite', return_value=('server', 'key')), \
                patch.object(coop, 'create_account'), patch.object(coop, 'backup_saves'), \
                patch.object(coop, 'co_op_environment', return_value={'TEST': '1'}), \
                patch('bbport_launcher_backend.core.game_environment', return_value={}):
            LauncherBackend.coopPlay(backend)
        self.assertEqual(backend._coop_launch_env, {'TEST': '1'})

    def test_host_does_not_check_or_configure_firewall(self):
        backend = self.backend()
        with patch.object(coop, 'setup_done', side_effect=AssertionError('automatic check')), \
                patch.object(coop, 'run_setup', side_effect=AssertionError('automatic elevation')), \
                patch.object(coop, 'host_address', return_value=('address', 'LAN')), \
                patch.object(coop, 'registration_key', return_value='key'), \
                patch.object(coop, 'create_account'), patch.object(coop, 'make_invite'):
            LauncherBackend.coopStartHosting(backend)
        backend._coop_host.start.assert_called_once_with('address')

    def test_only_explicit_action_configures_firewall(self):
        backend = self.backend()
        with patch.object(coop, 'run_setup') as setup:
            LauncherBackend.coopConfigureFirewall(backend)
        setup.assert_called_once_with(Path('game.exe'))

    def test_cannot_configure_while_running_or_busy(self):
        backend = self.backend()
        with patch.object(coop, 'run_setup') as setup:
            backend._coop_busy = True
            LauncherBackend.coopConfigureFirewall(backend)
            backend._coop_busy, backend.process = False, object()
            LauncherBackend.coopConfigureFirewall(backend)
        setup.assert_not_called()
