# Local party service lifetime after native exit — 03.11.2026

## Confirmed defect and change

The 15:38 run closed P1/P2 runners before P3 requested release. run.py closed
Compatibility immediately after game_proc.wait(), removing the peers required
by the unanimous prepare/commit/final protocol. The final P3 release had only
its own ACK. Native game exit and party-service exit were incorrectly coupled.

For an explicit local-three run, the coordinator now gives each runner a unique
run directory. After its native game exits, a runner withdraws its sign but keeps
its existing Compatibility/Engine alive. All services stop together after all
native games exit and all three report an ownerless, roomless, finalized state
with no pending command/transaction/acceptance. The coordinator heartbeat keeps
the earlier runners alive while the last game remains open. Ordinary launches
without BB_LOCAL_PARTY_RUN retain their original shutdown behavior.

If the coordinator disappears, the runner stops after a stale heartbeat. If all
games have exited but consensus still cannot drain within 30 seconds, services
stop with party_drained=false and coordinator exit=1. These are process-lifetime
deadlines only: they never grant release, fabricate a native ACK, mutate native
state, change membership or erase journals. A crash without native leave remains
an unresolved lifecycle case, not a successful release.

## Former host sign: still open

An actual-socket fixture reproduces A hosting, releasing, C acquiring, B joining,
then A publishing from area230010. C receives A's sign and a real /request reaches
A. Thus this fixture does not reproduce a Compatibility admission failure; it
does not prove that the live native search received/accepted the same sign.

Added change-only sign_search party events: owner/finalization, each known peer's
exclusion reason or returned area, decoded size and bytes78..7A (generation,
available count, role). Missing statuses are explicitly not_received. No opaque
payload, session token or secret is logged. No candidate predicate or invitation
is bypassed. Native rejection/HTTP delivery in the historical run is still
unobserved; the former-host guest-entry problem is NOT claimed fixed.

## Checks and delivery status

- Real three-Engine/Compatibility socket test: the first two native exits keep
  their services alive; the last owner can still get unanimous release; all
  services then finish drained. PASS.
- Former-host discovery and explicit admission with another guest: PASS.
- Shutdown deadline preserves unresolved state; profile environment and inherited
  path isolation: PASS (3 tests).
- Changed Python files compile through Python compile() and diff --check: PASS.

User explicitly requested no build. No compilation of DLL/launcher/package,
deploy, game launch, save/settings/game-file modification or journal reset.
Source changes are uncommitted; existing unrelated working changes retained.


## Later user authorization: build, install and launch at 15:56 MSK

The user subsequently requested launch with all current changes, superseding the
initial no-build constraint. BBSC diagnostics commit5351ecd, BBGLd588b23; other
pre-existing local source changes were preserved and included in the build,
not staged as unrelated commits. Full BB_FAST_DEPLOY=1 build completed exit0:
DLL3 existing warnings; native port exit0; launcher packaging exit0 (Qt optional
assetdownloader plugin warning). No release audit or file/hash verification.
Full PC copy exit0,5145 files, backup
D:/Games/Bloodborne/coop-dev/backups/local-party-lifetime-20261103-20261103-155517.
Existing Player EXEs/settings/saves retained. Local client/service changes do not
require updating the running VPS services.

User-authorized local-three launch15:56:15 MSK (12:56:15 UTC), coordinator22972;
parent out/coop-dev/runs/local-party-lifetime-20261103-155615/run.json.
Local coordinator run20261103-125615. Gameplay validation remains pending;
former-host native guest entry is still not claimed fixed.
