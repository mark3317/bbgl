# Graphics caption underlines — 2026-11-01

`e0fc144` names the native row underline in optionsetting.gfx and hides it
alongside Text_0/Cursor for logical graphics rows 6 and above. The six native
caption cells and persistent value controls keep their existing behavior.
The underline was an unnamed PlaceObject3 child, so hiding the label alone
left extra rules below the window. Its filter and other fields are preserved.

Validation: native port build PASS; one targeted real-game asset check
(test_graphics_has_persistent_widget_slots_and_native_scrollbar) PASS.
Inspected generated row: Underline names character 40 at depth 2; other
children and placements preserved. No broad tests or game launch performed.

Deployment payload: out/graphics-underlines (bin/bb-probe.exe and
scripts/menu_assets.py). Guarded deployment script:
out/deploy-graphics-underlines.ps1. Pending: both launchers are running;
installation requires them to exit. In-game visual confirmation pending.

Deployment completed 2026-11-01 04:15 MSK on PC and laptop after the user
authorized terminating the leftover windowless launcher processes. No game
process was running. Both updated files match the payload by SHA256:
- bin/bb-probe.exe: 56EAEED575E5761E0874196E76D09CC40A48A34CB22F6DE2A11480058419F21E
- scripts/menu_assets.py: 8A0949361D7C4D6AADE71E456428A4DFEE2B70CD2B19E692133354BABBB88A56
Backups: PC D:/Games/Bloodborne/coop-dev/backups/graphics-underlines-20261101-041506;
laptop C:/Games/Bloodborne/coop-dev/backups/graphics-underlines-20261101-041516.
This supersedes the pending deployment status above. Visual confirmation pending.
