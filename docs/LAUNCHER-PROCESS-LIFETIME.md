# Hidden launcher process exit — 1 November 2026

## Confirmed cause after the user's failed retest

The first deployment below did not fix the user's scenario. Live py-spy stacks
on both remaining GUI processes (PC 20884, laptop 16792) show the main thread in
`_receive_line -> _append_log`, with no game or runner processes remaining. The
PC main thread had accumulated over 14 minutes of CPU time. The reader and job
waiter had finished; game-exit notification was queued behind per-line UI signals.
The hidden Settings TextArea still bound its text to the 350,000-character log,
causing repeated text layout even when Logs was not displayed. This supersedes
the earlier unproven EOF/log-error explanation as the cause of this observed run.

The reader now keeps a bounded 64 KB UI tail with one outstanding wakeup. A
100 ms single-shot timer batches delivery, while startup/restart markers survive
tail eviction. Exit flushes the remaining tail directly. The complete disk log
is unchanged. The TextArea binds the log only while visible. Consequently output
volume cannot create an unbounded Qt event backlog ahead of game completion.

Validation: full QML source harness with an actual child producing 100,000 lines
passes in 0.66 seconds with seven UI updates; first and final lines remain in the
disk log. Two bounded-buffer/marker tests and nine existing process/window/exit
tests pass. Frozen staging flood passes in 0.81 seconds / eight UI updates.
User explicitly authorized stopping both verified hidden orphan launchers for
deployment after capturing their stacks; both were stopped, without game processes.

Rebuilt launcher/package from `8c4b7de`; unchanged native/mod artifacts from the
preceding successful full build were reused. Package verifier PASS. Installed on
both machines at 05:17–05:19 Moscow time; 5,263 files checked, five changed files
backed up and replaced per machine, both bundle manifests PASS. Launcher SHA256
`B3B97C51013E157FC43768B183F2EEB101DB806C85EE0BB81176503B53849120` matches both.
Installed full-QML 100,000-line flood: PC 0.71 s / seven updates; Windows 10 laptop
0.87 s / eight updates. Both exited with complete disk logs and no remaining
Bloodborne.exe. Backups: `launcher-lifetime-20261101-051705` (PC),
`launcher-lifetime-20261101-051719` (laptop), in each machine's existing
`Games/Bloodborne/coop-dev/backups`. No saves/settings/game files were changed.
Actual gameplay exit confirmation remains pending; the fake-child flood is a
reproduction of the log pressure, not an actual game session.

## Earlier investigation and first deployment (historical)

The launcher deliberately remains alive after its window closes, to drain the
game's output and host local servers. Previously `_read_output` was also the only
source of `_gameExited`: it waited for pipe EOF, then waited for run.py. A writer
retaining an inherited stdout handle prevents EOF even after the game exits. An
exception opening/writing last_run.log also kills that worker without reporting
exit; a full pipe can then stall the game itself. The hidden-window timer cannot
recover because `backend.running` remains true until `_receive_exit`.

Completion now has a separate waiter for run.py and its Windows job. Job accounting
keeps the launcher alive across Apply and restart successors; a parent-process-only
wait would prematurely stop their log reader and hosted servers. After the job is
empty, the reader gets up to two seconds to finish buffered output; a retained pipe
cannot hold the launcher indefinitely. Failed job assignment closes the unusable
handle and falls back to the direct process. Log open/write errors are reported
while output continues to drain.

Validation: three real Windows subprocess/job/pipe tests pass (retained unrelated
writer, log open failure, restart successor). The first two reproduce a hidden
launcher timeout with the previous reader implementation. Three existing Qt window
lifetime tests also pass. Tests use temporary files and helper processes, without
launching the game or touching saves. Ordinary source and previously installed
frozen launcher fake-child exits worked before the change; the exact trigger of
the user's reported Bloodborne.exe instance was not captured, so it is not proven
which of the two failure paths affected that run.

Three existing in-game settings/exit synchronization tests also pass. The built
frozen EXE passes all three process/job/pipe cases. Full QML lifecycle smoke with
an actual helper child also passes locally and in the installed Windows 10 laptop
build: window closes on the startup marker, final output is retained, the launcher
exits, and no Bloodborne.exe remains. This does not launch Bloodborne itself.

Full package build and its release verifier pass. Deployed on 1 November at 04:55–
04:57 Moscow time to both current installations. Each checked 5,263 payload files,
replaced 13 changed files with backups, and passed client/server bundle checksums.
Launcher SHA256: `6C300224CC0D26C1492A4DEEFAE6152E6BF441A7D64C9C6C8BFCB0B4D2C8880A`.
Bundled DLL SHA256: `F382B8E9B0925BF40EF9109C4CFF24A84BE11B7511DA09679BDB4657E259F033`.
Backups: PC `D:/Games/Bloodborne/coop-dev/backups/launcher-lifetime-20261101-045455`,
laptop `C:/Games/Bloodborne/coop-dev/backups/launcher-lifetime-20261101-045510`.
Saves, game files and user settings were not changed. User gameplay exit and
Apply and restart confirmation remain pending.
