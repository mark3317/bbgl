# 03.11.2026 — local three-player P2P mode

User requested three local games with the existing profiles, build and launch.
Source75411e7 adds a local-test button to the co-op page and scripts/local_party.py.
No native port or DLL changes. Launcher-only freeze exit0, 4-file delta installed
on stopped PC, backup local-three-20261103-20261103-142456. Standard package Qt
VC-runtime/ICU normalization applied to the raw PyInstaller output before smoke.
Installed frozen imports/profile checks and QML page PASS. No save/settings reset.

Existing profiles: Bloodborne Game Launcher Player1/2/3 (actual folder names have
spaces before the number); names MarkTest1/MarkTest2/MarkTest3, separate user dirs.
A persistent loopback group uses LocalPlayer1/2/3; control37610/37611/37612 and
native UDP3658/3659/3660, all127.0.0.1. Guard37609 prevents a second coordinator.
Validate all3 existing settings/game/user folders and distinct saves before any
child starts. Each frozen child receives its own BBGL_PROFILE_DIR before module
initialization; a mismatched child refuses to use the wrong profile. Parent paths
and save backup overrides are cleared. Existing profile configs are read only.
Per-run overrides: windowed1280x720, FPS60, Skip Intro. No VPN, LAN discovery,
separate game server, restoration of test saves or automatic role assignment.
The shared local-test config/log metadata lives under main profile/coop/local-test;
each game retains its own durable group journal and ordinary native/mod logs.

Four targeted tests PASS:3 actual embedded compatibility clients and all6 UDP
peer directions through the native wildcard-bind pattern, occupied port rejection,
existing-profile/environment isolation, duplicate saves/missing profile rejection,
stable group config. No production saves used by these fixture tests.

Run out/coop-dev/runs/local-three-20261103-142526 (UTC11:25:26), source75411e7,
bundled d8c8e08 plus retained inherited working fixes. Three native PIDs:
Player1=28640,Player2=19400,Player3=36528. All3 NP login/context/world replies and
UDP ports observed. Player1 initial startup hit existing compatibility NP-TCP+1
UDP pair allocation exhaustion before native launch. That failed runner had no
child; only its error-dialog helper was stopped. The same profile/group was
started again successfully; Player2/3 were never stopped. This allocator issue is
not claimed fixed; retry recorded in authoritative run.json. No live shared
runtime files replaced after games started. All games left running for the user.

Gameplay pending: P1 Beckoning, P2/P3 Small Resonant; movement/combat, one guest
menu exit and same-host rejoin with the other guest remaining, host menu exit.
The mode is a lifecycle/sync test, not a provider VPN/NAT/latency test.
