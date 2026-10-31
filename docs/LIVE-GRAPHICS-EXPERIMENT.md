# Live graphics experiment (2026-10-31)

Opt-in: `BB_LIVE_GRAPHICS=1` inherited by run.py, patches.py and bb-probe.
Normal launches retain the existing startup patches. CUSA03173 1.09 only.

The startup patch selector omits CA, DoF, blur, SSAO, game AA, dynamic-shadow and LOD patches;
it always prepares the existing SSR patch set. All 20 engine hook sites are hash-checked before
installation; a mismatch aborts the experimental launch. Engine hooks must be enabled.
Mid-after hooks execute the original comparison before masking its flags; disabled means the
comparison observes zero, enabled preserves the game's own decision. CA masks its output store;
LOD overrides the base bias before the original per-object adjustment and clamp.

Object motion preallocates resources even when initially off; GPU compatibility exclusions remain.
Turning it off selects ordinary shader pipelines and stops exposing object vectors. Turning it
back on reuses resources and invalidates object history. Buffers remain allocated while off.
The hooks' full register preservation and shader variant changes can affect timings: this build
is for functional testing, not an FPS benchmark.

SSR OFF suppresses its render/use checks, but its startup infrastructure (including the existing
patch set's other changes) remains in place. Therefore SSR OFF is not byte-identical to a normal
non-SSR launch. A final implementation must revisit this before enabling the feature by default.
Live resolution, aspect changes, cheats and gameplay patches retain their current behavior.

## Automated validation

- Existing engine hook checks plus new post-instruction register/flags tests.
- Startup patch selection tests: normal path unchanged; disabled effects retain resources;
  SSR prepared even with an absent setting.
- Fingerprint/whole-instruction checks against the user's own executable, including overlap
  with startup SSR writes. No game bytes are stored in the repository.
- Build of bb-probe. These checks do not establish visual correctness in game.

## Player test

Use an isolated copy of the selected save and configuration. Do not use co-op for this test.
Check LOD, CA, DoF, game AA (external upscaler OFF), motion blur, SSAO, dynamic shadows, SSR,
then object motion (temporal upscaler ON). For each: ON/OFF/ON, close menu, move camera/attack,
then travel to another area. Repeat a second launch with the initial effects disabled to test
OFF/ON/OFF. Inspect the Live graphics and PC menu lines in last_run logs.

Labels that still say restart describe the normal build; this opt-in overrides only the nine
settings listed above. Unsupported object-motion hardware still cannot enable that path.

Validation: engine hooks, output-settings C++ checks, 3 new Python tests and 7 graphics-preset tests PASS.
All 20 fingerprints and whole-instruction boundaries verified against the installed 1.09 executable
after 189 normal startup/SSR patch writes; none need RIP/branch relocation.
The unrelated run.sh restart tests cannot run in the Windows Python environment (WSL bash and
symlink privileges); this experiment uses run.py. Player validation pending.

## Native menu scrolling failure (player log 20261031-214200)

8dc52cb still crashed after rebinding viewport 8..13. The selected row lookup in
sub_1f1a9a4 returned a null widget, then GetMember dereferenced wrapper+0x30.
Retaining old widgets did not fix this. The stock dialog includes a seventh Defaults
cell, while the Graphics movie and value-widget viewport have six cells. Set the
native list dimensions explicitly to one cell per line and six visible lines before
layout. The native cursor must remain inside the rebound window. Log cursor and
capacity with each rebind for the next player run. Build only; no tests or game launch
per the user's instruction. This fix remains unconfirmed until the player checks it.

## Follow-up 20261031-214532: viewport capacity was insufficient

405ed8d still failed, including on wrap from the first row to the last. Values also
shifted independently from captions. Remove temporary record vectors, null widgets
and retirement lists. Each logical row now owns its persistent movie clip and widget;
only its Widgets child's Y and visibility are updated through GFx DisplayInfo.
Native captions use six visible cells. Extra clip labels and cursors are hidden.
This is a replacement implementation, not a confirmed runtime fix. Build only;
player must check scrolling in both directions, wrap, dropdowns and reopening.

## Player confirmation and layout refinement

Player confirmed persistent controls, scrolling and dropdowns work in 658890d.
Reduce System capacity to seven commands and shorten the frame/footer by one
67.65-pixel row. Normalize popup row pitch to 56.2 pixels. Name popup background
and arrow clips, size its background to the actual choice count, and hide unused
scroll arrows/bar when all choices fit. Only popup artwork is scaled; text rows
keep their native size and pitch. Build only; visual refinement awaits player check.
