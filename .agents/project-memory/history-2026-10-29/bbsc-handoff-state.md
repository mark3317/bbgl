---
name: bbsc-handoff-state
description: "Where BBSC work stopped on 2026-10-29 and machine state to undo (PC user_dir on testHost, moved journals)"
metadata:
  node_type: memory
  type: project
  originSessionId: 958cbc2f-060b-413d-bd28-1369b87765e0
  modified: 2026-10-29T08:52:18.481Z
---

BBSC session of 2026-10-29 ended with the rolling handoff in `C:\Users\markn\CLionProjects\BBSC\docs\HANDOFF.md` (read it first; it lists commits, what is deployed, open questions, the next test).

Machine state left behind (undo before normal play):
- PC launcher user_dir was switched from `D:\Games\Bloodborne\ddd` (friends' games) to `D:\Games\Bloodborne\testHost` for tests; switch back with coopdev.ps1 `-Action set-user-dir -Source D:\Games\Bloodborne\ddd` before the user plays with friends.
- Deployed mod on machines: the T4 test ran `3a095c2`; T4 stages 1-2 (`659b826`, `3081a08`), docs `3f3c15b` and own Dream `d90fe64` are built but not deployed; commits after `2d3e0c9` are not pushed.
- Hunter's Dream: the user chose option (a), guest sees its own Dream; done in `d90fe64` (switch `SHADPS4_BBSC_DREAM_OWN`, default on). Not tested; the old host-Dream code stays until the test passes, then delete it (`docs/fixes/DREAM.md` §5).
- New switch: research logs default off (`SHADPS4_BBSC_RESEARCH`, launcher "Research logs"); turn on for guest in tests that need the key item census / save writer log.
- Guest journals of earlier runs were renamed `*.bak-k2test` under `%LOCALAPPDATA%\bbport-coop\BBSC-0.0.1-BBport\bbsc\{guest-items,item-ledger}` (laptop and PC).

**Why:** test setup done during the K2 item work; easy to forget and it affects the user's real saves/launcher.
**How to apply:** mention the user_dir state when the user talks about playing with friends; update HANDOFF.md at the end of each work session. Related: [[bbsc-items-design-decisions]], [[bbsc-dev-on-mark-pc]].
