# Crossed responder bell / former-host guest search — 03.11.2026

## User clarification and correction to the earlier run review

User reports P1 and P2 could not join one another, especially after a host's
menu exit/Continue, and the blocked players' bell effects had a cross on the HUD.
The earlier P1->P2 role-rotation result only meant that P3 joined both hosts.
It did NOT validate either former host as a guest. Keep that distinction.

Prior mod logs show no native sign /create/own-user announcement for P1/P2;
P3 publishes and joins from Hunter's Dream, while P1/P2 are in Cathedral Ward.
The absence of a guest sign puts this failure before room admission/UDP joining.

## Reproduced source defect

Read-only CUSA03173 1.09 native 0191A750 computes responder geographical
eligibility. It chooses PlayerIns+278/+27C via native virtual+628, takes the
absolute area and looks up a map event flag at table047301B0. Area240000 uses
flag2405; area210000 uses2105. It reads that flag via01399BF0 and leaves
AL=!flag. The map m24 constructor can set2405; later script paths clear it
(including events around12400160/12401800). No live save flag was read or changed.

The existing patch at0191A8C3 only changed the unsigned range check to signed:
7D04 88C1 EB02, i.e. JGE reject; MOV CL,AL; JMP return. Thus it still rejected
an otherwise valid responder area with its disable flag set. The goods-use
patch and SosStatus geographical patch already allowed the bell, so activation
and ongoing sign publication used inconsistent area eligibility.

Native1506A2C ANDs this area result with the separate common player predicate
018C96D0. With the Small Resonant effect9005, a false result adds effect9009
(icon8814); true adds9008(icon8802). The same geographical helper participates
in responder search. Game parameters read from the installation confirm these
IDs; no game/param files were modified. The crossed-icon symptom and locations
are consistent with this reproduced gate. Prior logs do not contain the live
2405/common-predicate values, so do not claim every reported case's exact
runtime cause is proven, or that a persistent former-host latch was observed.

## Fix

Replace only MOV CL,AL with MOV CL,1 at the existing checked site:
7D04 B101 EB02. Keep the signed upper bound, null-player failure, area-source
selection, and independent player/common validity. This completes the existing
private co-op geographical override; no session state/owner/ACK/signaling success
is fabricated and no event flag/save is rewritten. The real native sign create
and admission must still run and complete.

Add read-only once-per-second, change-only bell-search diagnostics: native
state, primary/alternate area, active host/responder effect, normal/crossed icon
effects, native HTTP request count, claim pending and publication armed. This
also covers a search that never sent its first /create.

## Validation, source and installation

PASS new tools/test_responder_area_gate.py: execute the exact0191A750 native
instruction body, real map->flag lookup and original virtual area selection.
Old patch rejects flag-set210000/240000/-240000; fixed patch accepts them;
normal flags, signed areas, out-of-range rejection and null-player checks pass.
PASS tools/test_guest_bells.py (native/anywhere/local/remote/role constraints)
and tools/test_matchmaking_native.py (intervals/guards/counts/search lifecycle).
These fixtures do not run the live game or modify real saves.

Bundled commit c1d3cfd; parent pin1469079. Only this change/new test committed;
pre-existing dirty source changes retained and still included in the working
DLL build. No push. DLL build exit0,3 pre-existing warnings. Fast delta5-file
PC copy exit0; file verification disabled per user preference. Backup:
D:/Games/Bloodborne/coop-dev/backups/responder-area-crossed-bell-20261103-20261103-152859.
Main installation D:/Games/Bloodborne/Bloodborne Game Launcher. No Python/native
transport/server changes, so VPS/laptop unchanged. Settings, persistent party
journals and saves retained. No reset/restore/hash of live save data.

User explicitly requested launch. Coordinator20692 launched existing3 profiles:
out/coop-dev/runs/responder-area-fix-20261103-152919/run.json records start/scenario.
Per-launch60FPS/window1280x720/Skip Intro retained. Gameplay PENDING:
P1 host/P2 guest; P1 menu+Continue, then guest toP2; reverse and check crossed
icon/sign publication. P3 available as third participant. Successful source test,
build/install/start do not establish full former-host guest gameplay recovery.
The separate P3 granted Beckoning/no native room episode also remains unconfirmed.
Startup confirmed15:29 MSK: P1=23948/P2=21056/P3=25572; all3 new mod logs
report DLL built15:28:11 and mod ready, no signature/hook-install errors. Games
left running, actual gameplay pending.
