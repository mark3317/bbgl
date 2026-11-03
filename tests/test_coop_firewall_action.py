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
            process=None, _coop_busy=False, coopConnection='auto', app={},
            _party_discovery=object(), _write=Mock(), _coop_networks=[],
            _coop_game_exe=lambda: Path('game.exe'))
        backend._coop_run = lambda message, work: work()
        return backend

    def test_party_launch_does_not_check_or_configure_firewall(self):
        backend = self.backend()
        with patch.object(coop, 'setup_done', side_effect=AssertionError('automatic check')), \
                patch.object(coop, 'run_setup', side_effect=AssertionError('automatic elevation')), \
                patch.object(coop, 'installed', return_value=True), \
                patch('bbport_launcher_backend.party.launch_environment', return_value={'TEST': '1'}), \
                patch('bbport_launcher_backend.core.game_environment', return_value={}):
            LauncherBackend.coopPlay(backend)
        self.assertEqual(backend._coop_launch_env, {'TEST': '1'})

    def test_only_explicit_action_configures_firewall(self):
        backend = self.backend()
        with patch.object(coop, 'run_setup') as setup, \
                patch('bbport_launcher_backend.party.choose_network', return_value=('26.1.2.3', {'ranges': ['26.0.0.0/8']})):
            LauncherBackend.coopConfigureFirewall(backend)
        setup.assert_called_once_with(Path('game.exe'), remote_ranges=('26.0.0.0/8', 'LocalSubnet'))

    def test_cannot_configure_while_running_or_busy(self):
        backend = self.backend()
        with patch.object(coop, 'run_setup') as setup:
            backend._coop_busy = True
            LauncherBackend.coopConfigureFirewall(backend)
            backend._coop_busy, backend.process = False, object()
            LauncherBackend.coopConfigureFirewall(backend)
        setup.assert_not_called()
