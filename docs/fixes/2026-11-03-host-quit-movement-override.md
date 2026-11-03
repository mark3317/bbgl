# 03.11.2026 — host menu movement override and party 60 FPS

User reports that the host can still move forward during confirmed menu exit.
Review: out/coop-dev/runs/quit-move-review-20261103-090252, PC/laptop mod logs.
PC save/stop09:00:31.474–.520, final party/title09:00:33.567. Thus the previous
host-exit lifecycle completed; movement itself has no flag readback in logs.
Observed frame counters105/66 both exceed60.

Read-only exit-study.elf disassembly: DisableMove at0132F770 writes control+111.
The hooked CMP01513EB5 disables r15b/bl, but TEST r14b at01513EE5 lets a
frame-local override force both permissions back to1. During a confirmed
pending/title quit, clear only its low byte for the exact current local
world/character/control. Existing DisableMove, save and group-confirmation
ordering remain. This makes host and guest follow the disabled native branch.
The override's value in the reported game run is inferred, not logged.

Production callback + real Windows trampoline test reproduces old override
and covers pending/title, both flag values, native reset, remote, replacement
control, changed world and ordinary play. PASS. Existing menu save/Stop and
cancellation fixture PASS. Prior fixture did not model the post-CMP override.
Party launch sets fps_mode/frame_cap and BB_FPS/BB_FPS_LIMIT to60 on both
experimental clients; Skip Intro remains. Main profiles untouched.

BBSC dd47b2c. Build/deployment/gameplay status recorded after build below.
