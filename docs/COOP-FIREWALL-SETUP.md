# Optional co-op firewall setup — 1 November 2026

Co-op joining and local hosting no longer check or configure Windows firewall
rules automatically. They run without requesting elevation. Existing rules remain.

Settings → Co-op → Seamless co-op has a Configure firewall action. Only this
action invokes the elevated setup script (including the existing conditional VC++
runtime installation). Cancelling or failing setup leaves the launcher usable.
Without appropriate inbound rules, multiplayer connections may still be blocked.

First-run setup now has five steps: Welcome, Game files, Your data, Co-op, Finish.
The Co-op step shares the existing name/password/invite fields and the same firewall
action with Settings. It is optional for offline play. Existing completed profiles
are not forced through setup again; the wizard can be reopened in Settings.

Validation: 4 explicit-action/launch regression tests, 16 co-op tests and 10 startup
routing tests pass. The full QML window and new step load without warnings; Russian
layout rendered and inspected. The existing wizard suite retains its four previously
documented failures (direct launch, translated notices, old prompt download behavior).
No network rules, saves or game files were changed by validation.

## Hidden launcher lifetime

An orphan Bloodborne.exe (PID 13820, no window, no game/server processes) was
observed and terminated on 1 November. Its exact original hang cause is unproven.
Window lifetime now explicitly quits a hidden idle launcher, connects game-exit
handling before launching, and periodically rechecks hidden idle state. The reader
still survives while a game is running. Three isolated real Qt event-loop tests
pass: close while idle, hidden during a game then exit, and game exit while visible.
