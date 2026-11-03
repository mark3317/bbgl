# 03.11.2026 — host rotation: failed admission retry and joining guest exit

## Evidence / cause

Source parent e4f57cb, bundled d8c8e08 plus inherited working changes. Prior run
review-20261103-local-three: all3 final journals show owner P2 released at rev8,
then owner P1 acquired at rev9. Thus role consensus itself succeeded. P3 native
pre-room negotiation expires 14:33:57.254 (phase11, exchange ready=false).
All recorded encoded vport40 sends before failure match receiver I hashes:
P1->P3 8/8, P3->P1 7/7 for 14:33:51.3–14:33:57.2. This excludes loss of
these15 observed datagrams, not all conceivable transport/application failures.
Why the native exchange did not set ready on this first attempt is NOT proven.

The subsequent non-recovery IS explained by code and journals: claim remains
pending rev11 until owner cancellation at14:34:47. Old compatibility delete only
cleared sign advertisement; it did not withdraw pending. Therefore the sign was
excluded from host search and create kept returning the SAME failed claim (mod
serials2/3/4), without a new native activation. The original public broker's Force
withdrawal semantics had been lost in the private adapter.

Second attempt reaches native state4. P3 confirms title14:34:58.852, active native
queue head is kind8 (Join); Stop merely appends task C and sets state7. Join's
CC51F0/CC52D0 phases keep waiting for members, so LeaveRoom cannot execute. All3
journals stay rev18 ownerP1 members[P3] closing=true. This is a queued Stop,
not a completed leave or failed owner-election transaction.

## Changes

- A Force withdrawal of a DELIVERED pending claim, with fresh native idle and no
  load, now submits unanimous admission_cancel. Ordinary deletion, undelivered
  claims, state4/state6 and loading do not withdraw. No owner release is inferred.
- Pending admissions carry revision tickets. Withdrawals validate that ticket at
  transition time; a late old withdrawal cannot cancel a replacement admission.
  Legacy pending records without tickets use0 for compatible startup recovery.
- Explicit guest cancel plus observed native idle can finish room_leave even when
  owner has not marked room closing. Previously release_intent was tested outside
  but omitted from the joined-member branch, stranding a genuine guest leave.
- Native C9C6AB deadline-read observer acts only for the actual CSMultiPlayMan
  controller, active Join kind8 and an already-issued Stop/state7. It substitutes
  an expired deadline for this ONE read. Original CMP/SETB and virtual failure
  continuation CC6610 -> C9C500 select normal join cleanup, followed by queued
  Stop/LeaveRoom. It does not write task deadline/session state, free/pop tasks,
  fake JoinRoom completion, release owner on timeout or bypass final title ACK.
- Stop diagnostics now include joining states; party events log delivered ticket
  and explicit failed-admission withdrawal (no claim payload/secret).

## Validation

PASS actual3-process socket scenario: P2-equivalent owner exit, new P1-equivalent
owner, failed delivered claim withdrawal, fresh claim, stale-ticket rejection,
joined guest quit/idle drain without closing owner room, final owner release.
Negative cases: ordinary delete, undelivered claim, loading/state4 and state7.
PASS existing menu rejoin cancellation retirement; title current-ticket/keepalive,
retained-bell host drain and stale-room leave fixtures (4 named cases).
First run of cancellation-retirement fixture caught a missing kwargs parameter
in maintain_command; corrected, affected two process scenarios rerun PASS.
PASS exact native C9C6A0 predicate + production hook/trampoline AND actual CC51F0
join-wait instruction body, controller/task/state exclusion, ordinary timeouts.
PASS production menu quit and native-leave release fixtures.
DLL build exit0,3 existing warnings. Native port/launcher rebuild unnecessary.

Installed7 files on stopped PC via fast delta: DLL/launch/mod.json/bundle/SOURCE
and coop/party/{engine,compat}.py. Copy exit0, file verification disabled.
Backup D:/Games/Bloodborne/coop-dev/backups/p2p-host-rotation-20261103-20261103-145849.
Main installation D:/Games/Bloodborne/Bloodborne Game Launcher. VPS not involved
in private local runtime; VPS/laptop unchanged. No settings/save/journal deletion,
restore, real-save hashing or game-data writes. No broad commit/pin/push; inherited
native working changes retained. out/mod-delta.zip is DLL-only, installed runtime
Python files were copied separately; it is not a complete release artifact.

## New game run

Explicit user request authorizes game launch. Coordinator PID28988:
out/coop-dev/runs/host-rotation-fix-20261103-1459/run.json records actual UTC/MSK.
Existing3 Player profiles, per-launch60FPS/window1280x720/Skip Intro retained.
Scenario: P2 host/P3 guest; P2 menu exit; P1 host/P3 guest; if native negotiation
fails, watch fresh retry; P3 menu exit during joining; then normal rejoin/three
players if desired. Full game outcome remains PENDING; fixture/build/copy are
not gameplay proof. Old distributed journal is recovered normally, never erased.
Startup confirmed 15:00 MSK: native P1=33516/P2=36244/P3=20616; all3 mod ready,
DLL built Nov3 14:56:31, no hook-install ERROR in their new mod logs. Games left
running. Persistent distributed journal retained for ordinary recovery.
