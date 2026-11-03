"""Analysis checks only: does not invoke a compiler or start the game."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    'pacing_summary', Path(__file__).resolve().parents[1] / 'tools/coop-dev/summarize-pacing.py')
pacing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pacing)


def window(**kw):
    return dict(epoch_ms=10000, duration_ms=5000, frames=300, pid=1, limit=60,
                strict=1, grid=0, ready_by_deadline=300, cpu_valid=1,
                process_cores=2, system_busy_pct=50, **kw)


class PacingSummaryTests(unittest.TestCase):
    def test_complete_windows_and_corruption(self):
        a = window()
        line = 'Perf pacing: ' + ' '.join(f'{k}={v}' for k, v in a.items())
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'log'
            p.write_text(line + '\nPerf pacing slow: frame_ms=70\n'
                         + line + 'interleaved garbage\n', encoding='utf-8')
            rows, bad = pacing.read_windows(p, 5000, 10000)
            self.assertEqual((len(rows), bad), (1, 1))
            self.assertEqual(pacing.read_windows(p, 5001, 10000)[0], [])

    def test_weights_and_missing_fields(self):
        a = window(dispatch_ms=1, cap_wake_ms=2, cap_waits=10)
        b = dict(a, epoch_ms=20000, duration_ms=10000, frames=100,
                 ready_by_deadline=0, process_cores=5, dispatch_ms=5,
                 cap_wake_ms=4, cap_waits=30)
        out = pacing.summarize([a, b])[0]
        self.assertAlmostEqual(out['dispatch_ms'], 2)
        self.assertAlmostEqual(out['cap_wake_ms'], 3.5)
        self.assertAlmostEqual(out['process_cores'], 4)
        self.assertEqual(out['ready_by_deadline_pct'], 75)
        self.assertIsNone(out['prepare_ms'])

    def test_processes_and_modes_separate(self):
        rows = [window(), dict(window(), pid=2), dict(window(), grid=1)]
        result = pacing.summarize(rows)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(w['system_busy_pct'] == 50 for w in result))
        uncapped = pacing.summarize([dict(window(), limit=0, cpu_valid=0)])[0]
        self.assertIsNone(uncapped['ready_by_deadline_pct'])
        self.assertIsNone(uncapped['process_cores'])

    def test_duplicate_windows_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            pacing.summarize([window(), window()])


if __name__ == '__main__':
    unittest.main()
