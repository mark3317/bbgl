# 03.11.2026 — P2P promoted to develop and installed on PC

User accepts the P2P implementation and requests replacement of the old hosting/
invite-code launcher flow, mainline integration, PC build/install and test cleanup.

Parent develop fast-forwarded572e066 ->1650f48, then launcher3f4b56a and docs079fa3b.
Bundled mod develop151e24c ->94b53b3 ->5868376/d8c8e08 (runtime promotion and
retired experimental startup test). Inherited working changes preserved; original
patches and differing experimental untracked sources retained under
out/p2p-migration-safety. No push. Experimental source worktrees removed through
Git, including fmt/xbyak; automated regression tests retained in the main tree.

Launcher: no host/client switch, server start/stop, account password or invite code.
Automatic/Tailscale/Radmin/Custom network picker, active local adapter selection.
Tailscale CLI status --json supplies online peer addresses; LAN/Radmin directed
broadcast discovery. Custom also accepts explicit peer IPv4s. Multiple ambiguous
adapters require explicit selection. Stable private profile identity, selected-
interface TCP/UDP discovery37601. All players must see the same group and each
peer checks TCP/UDP against every other member before launch (2–5 participants).
A failed fresh check blocks launch even if the UI had previously been ready.
Bootstrap trusts the selected private VPN/LAN, as a LAN game; it does not implement
public-internet NAT traversal. Native gameplay remains UDP37658; distributed role
control37600 is unchanged. Preflight validates discovery TCP/UDP paths, not frame
rate/gameplay or native UDP37658 delivery across a provider VPN.

No user-entered invite secret, separate game server or permanent coordinator.
Initial group configuration derives from stable peer offers exchanged on that
private network. An active old owner/room prevents replacing its saved group.
Game adapter stays embedded in run.py; journals are isolated under
profile/coop/party/groups/<group>. Old local server/account binaries and default
server file moved to the deployment backup. No VPS update: its legacy services
are not used/changed. No router/VPN/firewall changes performed.

Targeted checks:5 real-socket discovery/mesh/negative tests PASS; QML page source
load PASS; production menu transition fixture and explicit-host-return fixture
PASS. Native port incremental build exit0. DLL exit0,3 existing unused warnings.
Fast package exit0, no archive/binary hashing or verify-release. PyInstaller warns
about an unused Qt labs assetdownloader plugin; installed actual page load PASS.
Installed frozen Python3.14.6 booted two embedded compatibility clients, loaded
schema.json and ss_info_template.xml, and kept native relay off: PASS. Installed
QML page loaded with all4 options and no old server/invite actions: PASS. The
first GUI smoke depended on unittest.mock unavailable in the freeze; that smoke
helper was stopped and rewritten without test-only imports, then passed.
No game launched; new discovery UI has not been played across two physical PCs.

PC install: D:/Games/Bloodborne/Bloodborne Game Launcher. Deployment copied5151
selected files, exit0, no file verification. Backup:
D:/Games/Bloodborne/coop-dev/backups/p2p-main-20261103-20261103-095153.
FPS60 and Skip Intro set for co-op launch; existing saves/settings left intact.

Automatic approval review rejected permanent test install/temp deletion with
"blocked by policy" (no further reason supplied). Reversible cleanup used:
old experimental install moved to
D:/Games/Bloodborne/coop-dev/backups/retired-serverless-party-20261103;
experimental PC profile including test saves moved to
%LOCALAPPDATA%/Bloodborne Game Launcher/backups/serverless-party-PC-20261103.
They are absent from their former active paths; they were archived, not erased.
The experimental source checkout itself was removed successfully by git worktree.
Laptop install/profile untouched per PC-only deployment request.
