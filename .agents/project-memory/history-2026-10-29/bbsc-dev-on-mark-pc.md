---
name: bbsc-dev-on-mark-pc
description: How to run the BBSC build/deploy/test loop when Claude runs directly on mark-pc (not the Linux VM)
metadata:
  node_type: memory
  type: reference
  originSessionId: 958cbc2f-060b-413d-bd28-1369b87765e0
  modified: 2026-10-29T08:52:25.318Z
---

When Claude Code runs on mark-pc itself (desktop app, Git Bash + PowerShell), the `bloodborne_pc/tools/coop-dev/coopdev.sh` wrapper does not fit (it ssh-es to `mark_pc` from a VM). Working recipe used on 2026-10-29:
- Build: `emulator\mod\build-mod-bbport.cmd` from `C:\Users\markn\CLionProjects\BBSC` (PowerShell `cmd /c`), check `build\mod-build.log` ends with `exit=0` (~3-5 min).
- PC: `powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\markn\CLionProjects\bloodborne_pc\tools\coop-dev\coopdev.ps1 -Action status|deploy-mod|save-snap|save-restore|set-user-dir|collect -Install D:\Games\Bloodborne\bbport-coop ...`.
- Laptop: `scp` coopdev.ps1 and `build/mod/*` to `local_pc:C:/Games/Bloodborne/coop-dev/`, then `ssh local_pc 'powershell ... coopdev.ps1 -Action ...'` (ssh alias `local_pc` works from Git Bash).
- Test start / logs: write `bloodborne_pc/out/coop-dev/runs/<id>/run.txt` (start epoch + VPS gameserver log offset via `ssh remote_server`), collect with `-Action collect -Since <epoch> -RunId <id>` on both machines and copy into `runs/<id>/{pc,laptop,vps}`.
- Analysis helpers: `BBSC/tools/eboot-disasm.sh <hex offset>`, `BBSC/tools/gamedata/item_lots.py`, `eboot_imports.py`; guest saves can be scanned for item keys (`0xB0000000|goods`, LE bytes) to see what really got saved.

Related: [[bbsc-handoff-state]].
