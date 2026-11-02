"""Compare guest-flip performance windows from matched offline/co-op game logs.
Usage: python tools/coop-dev/compare-perf.py offline.log coop.log
Use --start-ms/--end-ms (Unix milliseconds) to exclude menus/loading/warmup.
"""
import argparse
import json
import re
from pathlib import Path


def summarize(path, start=0, end=float('inf')):
    windows = []
    stalls = []
    for line in Path(path).read_text(encoding='utf-8', errors='replace').splitlines():
        if 'Perf window:' not in line and 'Perf stall:' not in line:
            continue
        row = {k: float(v) for k, v in re.findall(r'(\w+)=([\d.]+)', line)}
        if not start <= row.get('epoch_ms', 0) <= end:
            continue
        if 'Perf window:' in line:
            # Require the entire window to lie within the selected gameplay segment.
            if row['epoch_ms'] - row['duration_ms'] >= start:
                windows.append(row)
        else:
            stalls.append(row)
    if not windows:
        raise ValueError(f'{path}: no complete performance windows in selected interval')
    seconds = sum(w['duration_ms'] for w in windows) / 1000
    frames = sum(w['frames'] for w in windows)
    # Event lists use only included windows, avoiding partial segment counts.
    stalls = [s for s in stalls if any(w['epoch_ms'] - w['duration_ms'] < s['epoch_ms'] <= w['epoch_ms'] for w in windows)]
    return dict(log=str(path), seconds=seconds, frames=frames, fps=frames / seconds,
                window_fps_min=min(w['fps'] for w in windows),
                window_fps_max=max(w['fps'] for w in windows),
                worst_frame_ms=max(w['worst_ms'] for w in windows),
                p99_window_ms_range=[min(w['p99_ms'] for w in windows), max(w['p99_ms'] for w in windows)],
                over33=sum(w['over33'] for w in windows),
                over50=sum(w['over50'] for w in windows),
                over100=sum(w['over100'] for w in windows),
                over50_per_min=sum(w['over50'] for w in windows) * 60 / seconds,
                stalls=stalls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('offline')
    parser.add_argument('coop')
    parser.add_argument('--start-ms', type=float, default=0)
    parser.add_argument('--end-ms', type=float, default=float('inf'))
    args = parser.parse_args()
    a, b = [summarize(p, args.start_ms, args.end_ms) for p in (args.offline, args.coop)]
    print(json.dumps(dict(offline=a, coop=b, fps_drop_percent=100 * (1 - b['fps'] / a['fps']),
                         note='Guest flips; p99 values are per-window 1 ms histogram upper bounds, capped at 2001 ms. Long frames include loading unless excluded.'), indent=2))


if __name__ == '__main__':
    main()
