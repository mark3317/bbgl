import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
from bbport_launcher_backend import PendingGameOutput


class OutputBufferTests(unittest.TestCase):
    def test_flood_has_one_wakeup_bounded_tail_and_preserves_start(self):
        output = PendingGameOutput()
        wakes = int(output.append('Entering original x86-64 code\n'))
        for i in range(100000):
            wakes += output.append(f'P2P diagnostic sample {i}: ' + 'x' * 100 + '\n')
        tail, started, restarting = output.drain()
        self.assertEqual(wakes, 1)
        self.assertLessEqual(len(tail), 64000)
        self.assertTrue(started)
        self.assertFalse(restarting)
        self.assertIn('sample 99999:', tail)
        self.assertTrue(output.append('next run\n'))
        self.assertEqual(output.drain(), ('next run\n', False, False))

    def test_oversized_line_and_restart_marker(self):
        output = PendingGameOutput()
        output.append('restarting through run.py\n')
        output.append('x' * 100000)
        tail, started, restarting = output.drain()
        self.assertEqual(len(tail), 64000)
        self.assertFalse(started)
        self.assertTrue(restarting)
