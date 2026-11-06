"""Collector/queue contracts against synthetic files; never opens real profiles."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


observer = module('log_observer', ROOT / 'tools/coop-dev/log_observer.py')
hook = module('start_log_observer', ROOT / 'scripts/start_log_observer.py')


class ObserverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = self.root / 'state'
        self.local = self.root / 'profiles'
        self.user = self.local / 'Bloodborne Game Launcher Player 1/user'
        self.user.mkdir(parents=True)
        self.collector = observer.Collector(self.state, self.local)
        self.since = time.time()

    def packets(self):
        return [json.loads(p.read_text(encoding='utf-8')) for p in (self.state / 'pending').glob('*.json')]

    def test_skips_old_logs_then_reads_only_new_bytes_and_complete_utf8_lines(self):
        path = self.user / 'run_old.log'
        path.write_bytes(b'historical ERROR\n')
        os.utime(path, (self.since - 60, self.since - 60))
        self.collector.scan([1], self.since)
        self.assertFalse(self.packets())
        with path.open('ab') as stream:
            stream.write('new ошибка\npartial'.encode())
        self.collector.scan([1], self.since)
        self.assertEqual([p['text'] for p in self.packets()], ['new ошибка\n'])
        self.collector.scan([1], self.since)
        self.assertEqual(len(self.packets()), 1)
        self.collector.scan([1], self.since, final=True)
        self.assertEqual(sorted(p['text'] for p in self.packets()), ['new ошибка\n', 'partial'])

    def test_rotation_restart_and_queue_crash_replay_do_not_lose_or_duplicate(self):
        path = self.user / 'last_run.log'
        path.write_text('first ERROR\n')
        self.collector.scan([1], self.since)
        # Simulate packet persisted but cursor checkpoint lost.
        (self.state / 'cursors.json').unlink()
        other = observer.Collector(self.state, self.local)
        other.scan([1], self.since)
        self.assertEqual(len(self.packets()), 1)
        path.rename(self.user / 'last_run.1.log')
        path.write_text('second ERROR\n')
        other.scan([1], self.since)
        # Rotated alias may repeat evidence: dispatcher groups it by semantic issue.
        self.assertIn('second ERROR\n', [p['text'] for p in self.packets()])
        final = observer.Collector(self.state, self.local)
        before = len(self.packets())
        final.scan([1], self.since)
        self.assertEqual(len(self.packets()), before)

    def test_user_dir_from_run_header_and_secrets_redacted(self):
        external = self.root / 'custom user'
        external.mkdir()
        (external / 'last_run.log').write_text('remote ERROR\n')
        header = json.dumps({'BB_USER_DIR': str(external), 'token': 'secret123'})
        (self.user / 'run_new.log').write_text(header + '\nBearer hidden.value\n')
        self.collector.scan([1], self.since)
        self.collector.scan([1], self.since)
        text = '\n'.join(p['text'] for p in self.packets())
        self.assertIn('remote ERROR', text)
        self.assertNotIn('secret123', text)
        self.assertNotIn('hidden.value', text)

    def test_ack_preserves_packets_arriving_during_analysis_and_rejects_traversal(self):
        (self.user / 'run_new.log').write_text('ERROR one\n')
        names = self.collector.scan([1], self.since)
        with (self.user / 'run_new.log').open('a') as stream:
            stream.write('ERROR two\n')
        self.collector.scan([1], self.since)
        command = [sys.executable, str(ROOT / 'tools/coop-dev/log_observer.py'), '--state', str(self.state), 'ack']
        subprocess.run(command + names, check=True, capture_output=True)
        self.assertEqual([p['text'] for p in self.packets()], ['ERROR two\n'])
        result = subprocess.run(command + ['../cursors.json'], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((self.state / 'cursors.json').exists())

    def test_singleton_released_on_exit(self):
        one = observer.Singleton(self.state / 'lock')
        self.assertTrue(one.acquire())
        two = observer.Singleton(self.state / 'lock')
        self.assertFalse(two.acquire())
        one.close()
        three = observer.Singleton(self.state / 'lock')
        self.assertTrue(three.acquire())
        three.close()

    def test_hook_optional_and_hidden_with_exact_player_and_parent(self):
        with patch.object(subprocess, 'Popen') as spawn:
            self.assertFalse(hook.start(self.root, 1))
            spawn.assert_not_called()
            observer.write_json(self.root / 'tools/log-observer.json',
                                {'enabled': True, 'pythonw': sys.executable,
                                 'script': str(ROOT / 'tools/coop-dev/log_observer.py')})
            for player in (1, 2, 3):
                self.assertTrue(hook.start(self.root, player, 12345))
                args, kwargs = spawn.call_args
                self.assertEqual(args[0][-4:], ['--player', str(player), '--parent-pid', '12345'])
                if os.name == 'nt':
                    self.assertTrue(kwargs['creationflags'] & subprocess.CREATE_NO_WINDOW)

    def test_real_profile_entry_dispatches_all_three_players_before_coordinator(self):
        import runpy
        import types
        from shutil import copyfile
        scripts = self.root / 'scripts'
        scripts.mkdir()
        copyfile(ROOT / 'scripts/start_log_observer.py', scripts / 'start_log_observer.py')
        observer.write_json(self.root / 'tools/log-observer.json',
                            {'enabled': True, 'pythonw': sys.executable,
                             'script': str(ROOT / 'tools/coop-dev/log_observer.py')})
        main = runpy.run_path(str(ROOT / 'scripts/local_party.py'))['main']
        local = types.SimpleNamespace(run_three=lambda port: 17)
        with patch.dict(sys.modules, {'bbport_local_test': local}), \
             patch.object(sys, 'frozen', True, create=True), \
             patch.object(sys, 'executable', str(self.root / 'Bloodborne.exe')), \
             patch.object(sys, 'argv', ['local_party.py', '--all']), \
             patch.object(subprocess, 'Popen') as spawn:
            self.assertEqual(main(None), 17)
        self.assertEqual([call.args[0][-3] for call in spawn.call_args_list], ['1', '2', '3'])


if __name__ == '__main__':
    unittest.main()
