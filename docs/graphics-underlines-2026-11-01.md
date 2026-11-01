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
