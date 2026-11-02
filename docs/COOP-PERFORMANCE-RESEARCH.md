# FPS / stutter research build — 2026-11-02

Prepared guest-flip telemetry (offline and co-op; default enabled, BB_PERF_CAPTURE=0 disables).
Each five-second window records weighted FPS, best/worst frame, p50/p95/p99 (1 ms histogram upper bounds; last bin >=2000 ms), counts >33.333/>50/>100 ms.
Every >50 ms interval records Unix epoch milliseconds. These are guest flips, not generated frames or GPU execution times. Menus, loading, focus loss and startup are included until excluded during analysis. Final partial windows are not summarized.
BBSC now reports all scopes with calls >8/>16/>50 ms every ten seconds, including rare holds outside top ten by total. Nested scopes overlap; never sum nested and parent costs. Scope wall time includes waiting/preemption and is not proof of a mutex hold. Existing SHADPS4_BBSC_PERF=0 disables mod profiling.

## Matched run

On each machine keep resolution, graphics, frame generation, FPS cap and background programs unchanged. Keep role/device results separate.
1. Offline: warm the same location/route once, then stand 60 s and run/fight along the same route for 3 minutes. Record wall-clock start/end of measured sections.
2. Co-op enabled alone: repeat the same route. This separates mod/session-search overhead from having a peer.
3. Co-op with peer: repeat as host and guest. Then separately exercise join, map transition, death/revive and disconnect. Record their times; exclude these transitions from steady gameplay FPS comparisons.
4. Repeat offline after co-op to detect cache/thermal drift. Do not clear shader caches. Do not restore saves automatically.
After completion collect both machines' rotated game/mod/timeline logs; an offline launch rotates the previous game log.

## Analysis

`python tools/coop-dev/compare-perf.py offline.log coop.log`
Optional --start-ms/--end-ms restrict both logs to absolute epochs; for different run segments call summarize separately with each run's bounds. Reports duration-weighted FPS, percent drop, five-second FPS range, worst frame, window p99 range, >50 ms frames/min and event timestamps. The p99 range is not a whole-run p99 or 1% low. Repeated slow frames are counted separately, not merged into stutter episodes.
Correlate each stall with timeline/loading, shader compiles, and the overlapping ten-second BBSC scope report. More detailed BB_FRAME_STATS=1 exists but its diagnostics add overhead: keep it equal across modes if used.

## Optimization audit / limits

Historical laptop report in T10-performance.md: 4.306 ms/frame BBSC before earlier optimizations; not evidence for current build. Current baseline must be measured.
BbscTimeline serializes and flushes each timeline event under a mutex; durable journals also flush at lifecycle boundaries. These are candidates for measured I/O delays, not proven current causes. Reinsert's 250 ms sleep is on a detached timer thread, not evidence of game-thread sleep. Game-memory operations must remain on the owning game thread; do not move them wholesale to workers. If measurements identify diagnostic I/O, move non-durable log writes to a bounded writer queue; preserve durable journal ordering. If one tick dominates, bound work per frame only after identifying ordering/load constraints.
No optimization gain or stutter cause is claimed before the matched game run.

## Build result

Native build.sh exit=0; bundled mod build exit=0 (two existing unused-symbol warnings). Analysis fixture passed weighted aggregation, interval exclusion and empty-capture failure. No game launched or installations changed. Staging updated; out/perf-research-delta.zip contains native loader and mod delta. DLL commits standalone 666a03a / bundled d5a2322.
