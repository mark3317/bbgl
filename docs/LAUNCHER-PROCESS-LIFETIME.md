# Hidden launcher process exit — 1 November 2026

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

Build/deployment and a user gameplay exit check are recorded separately in HANDOFF.
