"""Summarize new Perf pacing windows, independently per process and configuration.

python tools/coop-dev/summarize-pacing.py log1 log2 log3 --start-ms N --end-ms N
Only complete windows are included. No scheduler/GPU/limiter cause is inferred.
"""
import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path


def read_windows(path, start=0, end=math.inf):
    rows, malformed = [], 0
    required = {'epoch_ms', 'pid', 'duration_ms', 'frames', 'limit', 'strict', 'grid',
                'ready_by_deadline', 'cpu_valid'}
    for line in Path(path).read_text(encoding='utf-8', errors='replace').splitlines():
        if 'Perf pacing: ' not in line:
            continue
        payload = line.split('Perf pacing: ', 1)[1]
        # Interleaved native output is rejected rather than silently repaired.
        if not re.fullmatch(r'(?:\w+=-?\d+(?:\.\d+)?\s*)+', payload):
            malformed += 1
            continue
        row = {k: float(v) for k, v in re.findall(r'(\w+)=(-?\d+(?:\.\d+)?)', payload)}
        if (not required <= row.keys() or row['duration_ms'] <= 0 or row['frames'] <= 0
                or not 0 <= row['ready_by_deadline'] <= row['frames']):
            malformed += 1
            continue
        if row['epoch_ms'] - row['duration_ms'] >= start and row['epoch_ms'] <= end:
            rows.append(row)
    return rows, malformed


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(int(row[k]) for k in ('pid', 'limit', 'strict', 'grid'))].append(row)
    result = []
    for (pid, limit, strict, grid), windows in sorted(groups.items()):
        windows.sort(key=lambda r: r['epoch_ms'])
        for prev, current in zip(windows, windows[1:]):
            # 1ms tolerance for millisecond wall-clock rounding.
            if current['epoch_ms'] - current['duration_ms'] < prev['epoch_ms'] - 1:
                raise ValueError(f'Overlapping/duplicate pacing windows for pid {pid}')
        duration = sum(w['duration_ms'] for w in windows)
        frames = sum(w['frames'] for w in windows)
        out = dict(pid=pid, limit=limit, strict=strict, grid=grid, windows=len(windows),
                   seconds=duration / 1000, fps=frames * 1000 / duration,
                   ready_by_deadline_pct=(100 * sum(w['ready_by_deadline'] for w in windows)
                                          / frames) if limit else None)
        for key in ('ready_late_ms', 'dispatch_ms', 'queue_ms', 'prepare_ms', 'flip_ms'):
            present = [w for w in windows if key in w]
            out[key] = (sum(w[key] * w['frames'] for w in present)
                        / sum(w['frames'] for w in present)) if present else None
        for key in ('ready_late_max_ms', 'dispatch_max_ms', 'queue_max_ms',
                    'prepare_max_ms', 'flip_max_ms', 'cap_wake_max_ms', 'tail_wake_max_ms'):
            out[key] = max((w[key] for w in windows if key in w), default=None)
        for mean, count in (('cap_wake_ms', 'cap_waits'), ('tail_wake_ms', 'tail_waits')):
            samples = [w for w in windows if mean in w and w.get(count, 0) > 0]
            out[mean] = (sum(w[mean] * w[count] for w in samples)
                         / sum(w[count] for w in samples)) if samples else None
        for key in ('process_cores', 'present_cores', 'system_busy_pct'):
            valid = [w for w in windows if w['cpu_valid'] and w.get(key, -1) >= 0]
            out[key] = (sum(w[key] * w['duration_ms'] for w in valid)
                        / sum(w['duration_ms'] for w in valid)) if valid else None
        # System CPU is a machine-wide observation; do not sum it across PIDs.
        result.append(out)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('logs', nargs='+')
    parser.add_argument('--start-ms', type=float, default=0)
    parser.add_argument('--end-ms', type=float, default=math.inf)
    args = parser.parse_args()
    rows, malformed = [], 0
    for log in args.logs:
        found, bad = read_windows(log, args.start_ms, args.end_ms)
        rows.extend(found)
        malformed += bad
    print(json.dumps(dict(processes=summarize(rows), malformed_windows=malformed,
                          note='CPU cores = CPU time / wall time. Dispatch includes scheduling, '
                               'locks and vblank handling. No causal attribution.'), indent=2))


if __name__ == '__main__':
    main()
