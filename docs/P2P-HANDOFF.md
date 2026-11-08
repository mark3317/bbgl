## 08.11.2026 — BBGL 1.4.0

Выпуск обновляет лаунчер, трофеи, оверлей и меню «Система».
BBSC-GL 1.4.0 сохраняет игровую логику кооператива и Party из 1.3.3.
Сборка DLL, порта и лаунчера прошла. Проверены состав обоих ZIP и
побайтовое совпадение 18 файлов отдельного ZIP мода с комплектом BBGL.
Лаунчер из архива прошёл проверку на русском и английском при двух
размерах окна, включая трофеи, уведомления, моды, мастер и списки FPS.
Проверка в запущенной игре из ZIP 1.4.0 остаётся открытой.
[Состав выпуска и границы проверки](release-1.4.0.md).

## 08.11.2026 — BBGL 1.3.3

Список частот кадров в лаунчере отсортирован, подписи сокращены.
Комплект для Windows содержит BBSC-GL 1.3.3 и локальный Party. В выпуск
вошли три исправления с подтверждением на тестовой DLL вдвоём: окно
награды у гостя, оба выхода из Лекционного корпуса и подсказка лампы
до победы. [Описание и границы проверок](release-1.3.3.md).
Целевые проверки трёх исправлений, сборка и проверка ZIP прошли.
Лаунчер из обновлённого ZIP запущен на русском и английском в
изолированных профилях. Порядок, подписи и предупреждения в списках FPS
проверены на обоих языках при двух размерах окна.
Архив содержит BBSC-GL `0a61ba4`, закреплённый в BBGL.
Игровой прогон из ZIP открыт.


## 05.11.2026 — итоги исправлений добычи и наград (ПК)

[Актуальная сводка мода](../mods-src/BBSC/docs/REWARDS.md): штатная добыча
врагов/охотников, скриптовые и боссовые награды; личные отметки подбора;
недостающие уникальные base/DLC награды и17 лотов чаш проверяются при готовности
загрузки к хосту без секундного опроса. Общий прогресс сохранён, предметы по
инвентарю хоста не рассылаются. Повторный «След когтя» исправлен общим путём
для107 лотов/86 глобальных флагов с учётом NG+.
Последний DLL-only build/deploy exit0, delta5; бэкап
`D:/Games/Bloodborne/coop-dev/backups/global-loot-receipts-20261105-20261105-062348`.
Два профиля стартовали06:24:17 МСК;34/34 hooks и native loot ready у обоих.
Сборка/установка/запуск подтверждены, игровые сценарии OPEN. Лаунчер повторно
не собирался в последней DLL-дельте. Подробности прогона:
`out/coop-dev/runs/global-loot-receipts-20261105/run.md`.
Исторические утверждения ниже не отменяют эту сводку.

## 05.11.2026 — отдельные GPU-логи и уменьшенный курсор установлены на ПК

В Система → расширенные настройки добавлен отдельный переключатель
«Подробные логи GPU», по умолчанию выключен. Предупреждение о сотнях мегабайт
и более за сеанс перенесено к нему. Включение задаёт BB_GPU_LOG=debug независимо
от общей диагностики; выключение сохраняет error/critical. Явные переменные
окружения по-прежнему имеют приоритет. Стрелка курсора уменьшена с максимальных
22×28 до 16×20 px; hotspot пересчитан по острию, HiDPI-вариант сохранён.
Целевые logging/settings/localization проверки, узкий русский Qt-предпросмотр,
проверка собранного лаунчера и SDL cursor smoke PASS. Пакет лаунчера и последующая
сборка порта завершились exit=0; полный быстрый деплой и дельта порта на ПК exit=0.
Мод не пересобирался. Бэкапы и журнал: out/coop-dev/runs/gpu-log-toggle-20261105.
Запрошен повторный запуск Player 1/2 с существующим cheat_one_hit_kill=1;
GPU debug по умолчанию выключен. Настройки/сейвы не менялись. Игровой контроль открыт.

## 04.11.2026 — настройки и мастер установлены ПК + ноут 19:06 МСК

Строка текущего профиля перенесена под три системные кнопки. Выбор подключения
недоступен до первой проверки и во время обновления списка. В мастер добавлено
приветствие. Пресеты закреплены только на вкладках «Экран» и «Эффекты изображения»;
«Баланс» убран, названия: «Производительность», «Качество», «Максимум», «Свои настройки».
Целевые проверки и Qt-предпросмотры PASS; быстрый пакет собран exit=0.
ПК и ноутбук установлены exit=0, по 5144 файлов, с резервными копиями.
Сейвы и настройки сохранены, игра/лаунчер не запускались. Подробности:
out/coop-dev/runs/profile-label-20261104/run.md.

## 04.11.2026 — папка профиля, установка ПК + ноут 18:53 МСК

В системных настройках после папки лаунчера добавлена «Папка профиля»:
открывает активный DATA_DIR в Проводнике. Из расширенных убраны старые
«Открыть профиль» (запуск тестового профиля) и «Открыть bbport.ini».
Целевые проверки 4 PASS, русский Qt-предпросмотр просмотрен.
DLL и полный быстрый пакет собраны exit=0; ПК и ноутбук установлены exit=0,
по 5146 файлов, с бэкапами. Включено завершённое исправление дверей лекционного
корпуса; игровой результат остаётся открытым. Игру/лаунчер не запускали,
сейвы и настройки не меняли. Подробности: fixes/2026-11-04-profile-folder-button.md,
out/coop-dev/runs/profile-folder-20261104/run.md.

## 04.11.2026 — built-in button images / false mod warning

Confirmed config difference: PC Xbox icons active, laptop icons disabled; laptop
Diamond Sword already active. Personal icons no longer participate in mod comparison.
Successful downloads update cached statuses immediately; pre-download polls cannot
restore obsolete missing/conflict results. Real mod mismatches still warn.

User requested icons out of mods: packaged resources now under
launcher/assets/button-prompts, separate selection with read-only legacy fallback.
run.py maps chosen built-in layer even with user mods off. Legacy icon names excluded
from discovery/sharing; old directories moved to device backup during installation.
10 targeted checks PASS plus 3 direct mods PASS / 1 POSIX-only skip. Fast launcher
build and PC/laptop copy exit=0; both launchers opened with responding titled
windows. Legacy icon directories moved into device backups. Details recorded in
out/coop-dev/runs/builtin-icons-20261104/run.md. Game visual confirmation OPEN.
No original game/save writes, BBSC source/pin or protocol/VPS change for this task.

## 04.11.2026 — mod table and co-op launch warning

Missing peer mods now appear inactive in the shared table with an inline Install
button; matching mods have no marker. Removed the per-player set button/separate
catalog UI. Co-op Play warns on catalog/content/active-order differences and offers
accented Mod settings or Launch game. Download stays disabled until selected.
Seven sharing checks and actual Qt workspace/Main dialog check PASS; RU previews
reviewed at narrow width. Fast launcher build and laptop copy exit=0 (5142 files);
backup C:/Games/Bloodborne/coop-dev/backups/mod-table-20261104-160233.
Launcher/game not started. Laptop build/deploy record:
`out/coop-dev/runs/mod-table-20261104/run.md`. Physical transfer/gameplay OPEN.
No BBSC source/pin, protocol, save/settings changes for this task.

## 04.11.2026 — current package installed laptop; launcher opened15:49MSK

New explicit request supersedes earlier PC-only scope. Same successful15:38package
transferred by strict SSH to DESKTOP-73Q9JB7; source input metadata unchanged and
no other active related chat. Remote copy exit0,5149files; backup:
C:/Games/Bloodborne/coop-dev/backups/settings-cleanup-laptop-20261104-154907.
Install C:/Games/Bloodborne/Bloodborne Game Launcher. User settings/saves/game data
preserved. Launcher started in interactive markn/session1; direct interactive
snapshot confirms window Bloodborne Game Launcher, PID19168, Responding=true.
Temporary launch/check tasks removed; no game start or VPS update. Details:
out/coop-dev/runs/settings-cleanup-20261104-1538/run.md.

## 04.11.2026 — settings cleanup built/installed PC15:39MSK

Removed firewall button/dialog/script generator/elevation helper and obsolete
firewall-only test/doc. Existing Windows rules unchanged. Installed mods now has
its own table and both folder settings showing configured/effective runtime paths;
removed separate folder tab. Short co-op description and online-count label.
All preset identities retain independent upscaling/frame-generation choices through
real settings calls. Targeted tests and1280/1024 Qt previews PASS; frozen executable
Qt smoke in isolated profile PASS. Fast launcher/package build and PC copy exit0,
5142files. Existing current DLL/port reused; mod input metadata unchanged since
successful15:18build. Backup:
D:/Games/Bloodborne/coop-dev/backups/settings-cleanup-20261104-153924.
User narrowed scope to PC only: laptop not modified; no VPS update applicable.
No game launch, real save/settings/game-data changes, commit/pin/push. Record:
out/coop-dev/runs/settings-cleanup-20261104-1538/run.md.
See fixes/2026-11-04-settings-cleanup.md. Installed package also includes completed
home/VPN/mod-sharing source changes; earlier source-only install status historical.

## 04.11.2026 — launcher home spacing and VPN dropdown, SOURCE ONLY

Home summary/fields share padding and alignment, without card backplates at user
request; launch footer follows wrapped
content, with scrolling on short windows. Missing VPNs appear after inventory
checks, with a Download button on the right of their dropdown row; installed VPNs
remain selectable. Download preserves the selected connection. Qt preview reviewed;
VPN6 and localization5 checks PASS. No build/deploy, live profile/save/game writes,
commit/pin/push. See fixes/2026-11-04-launcher-home-spacing.md.

## 04.11.2026 — current fixes built/installed; three PC profiles launched13:40MSK

Supersedes SOURCE ONLY deployment status below for native world retirement,
repeat-death native handlers, guest aura and recipient crash isolation. Related
chats read and complete, including launcher mod sharing and VPN settings.
DLL build exit0; fast package build exit0. New VPN work began during first build;
waited for completion and rebuilt only launcher/package, retaining unchanged DLL.
Source size/mtime unchanged during final rebuild. Native port reused; no VPS
component/protocol update needed. Parent HEAD1987812, BBSC HEAD/gitlink0ddb1d4
plus recorded local changes; no commit/pin/push.

PC deploy exit0, copied5147; backup:
D:/Games/Bloodborne/coop-dev/backups/native-retirement-20261104-133925.
Existing Player1/2/3 CMD scripts started distinct profiles/ports3658/3659/3660;
three native windows present/responding (PID32276/31192/27620), fresh13:40 logs.
Existing60FPS/no-DLSS settings retained. Party-only process diagnostics enabled
for this test; parent environment restored. No manual save/settings/live-journal
edits, game-data changes or process termination. Laptop not updated/launched.
Gameplay recovery, native death reset and guest appearance remain OPEN.
Record: parent out/coop-dev/runs/native-retirement-deploy-20261104-1328/run.md.

## 04.11.2026 — VPN connection settings, SOURCE ONLY

Default LAN; no automatic/custom mode in UI. Installed Radmin VPN/Tailscale
detected independently of active adapters; only installed providers enter the list.
Settings/wizard share download-and-open-installer buttons for missing programs,
background progress and periodic post-install detection. Removed manual IP fields,
local-three test UI and empty Connection tab. Targeted VPN/UI6, network6+8,
firewall3, localization5 PASS. Official installer endpoints HTTP200/MZ checked;
actual installers not launched. No build/deploy/gameplay, live profile/save edits,
BBSC/pin changes or commit/push. Details: [VPN settings](fixes/2026-11-04-vpn-connection-settings.md).

## 04.11.2026 — launcher file-mod list and LAN exchange, SOURCE ONLY

Automatic folder/profile polling replaces manual Refresh. Installed file mods
have switches and compact priority controls; folder settings moved to their own
tab. Existing selected-interface discovery TCP serves catalogs and verified mod
downloads, without new ports. Download one missing mod disabled, or explicitly
apply another player's order/enabled set after fetching missing files. Conflicting
same-name contents never overwritten. Temporary download folders ignored by loader.
7 isolated polling/real-TCP tests,1 rendered Russian Qt workspace,8 Party checks,
20 mod-loader tests PASS (6 existing skips); localization5 PASS. Old setup suite
has2 pre-existing expectation errors. No build/deploy/physical LAN/gameplay check,
real profile/save edits, BBSC source/pin changes, commit or push by this task.
Details: [mod exchange](fixes/2026-11-04-launcher-mod-sharing.md).

## 04.11.2026 — late joining built and installed PC + laptop

Supersedes SOURCE ONLY deployment status below. All related chats completed before
build (late joining, sword integration, cursor, FPS, Player1 menu, cleanup).
Launcher package.sh BB_FAST_DEPLOY=1/SKIP_BUILD=1 exit0; current native cursor port
and BBSC DLL reused. Frozen launcher smoke loaded dynamic-worlds-v1, discovery2
and acquired an isolated temporary world successfully. Source input metadata
unchanged during build. Build contents/run status: parent
out/coop-dev/runs/late-join-pc-laptop-20261104-112427/run.md.
Parent HEAD1987812, BBSC HEAD/gitlink0ddb1d4, with recorded local source changes;
no commit, pin update or push performed by this build/deploy task.

PC deploy exit0, copied5143; laptop deploy exit0, copied5146 (metadata selection,
no file/hash audit). Backups:
- D:/Games/Bloodborne/coop-dev/backups/late-join-20261104-112904
- C:/Games/Bloodborne/coop-dev/backups/late-join-20261104-112932

Updated Diamond Sword already installed on PC by its authoring chat; copied its
current asset package to laptop mods/Diamond Sword. Laptop existing mods_enabled
and default new-mod selection enable it without editing settings/mod profiles.
Both launchers opened in interactive sessions (PC2 / laptop1), visible/responding
confirmed. Laptop direct task attempt did not confirm a window; recovered with
an interactive hidden helper, confirmed visible UI, removed our one-shot tasks.
Fresh automatic discovery on both devices lists twin and test. This confirms
launcher presence, not native room join/world arrival or any gameplay fix.
No game launched by this task. Real settings/saves/journals unchanged.
Late-join gameplay and native menu-exit confirmation remain OPEN.

## 04.11.2026 — late joining implemented, SOURCE ONLY

Regular launcher co-op now uses per-player durable home sessions and live peer
lookup (discovery BBGL-P2P-2). A player may start alone; a host can reserve a guest
whose launcher/game starts later, without rebuilding a roster or restarting either
game. Discovery feeds a live directory, never a voting list. Bells keep their roles.
DynamicEngine uses one durable writer/authority per hosted world. Admission first
persists a provisional guest binding, then commits on the host; only a confirmed
host snapshot exposes a native admission. Competing hosts/guest acquire serialize
at the guest. Separate unbound players may host independent worlds. Explicit
native leave/cancel is still required; partitions never promote or release guests.
Guest identity/login and NP/HTTP/relay sockets survive attaching/detaching. Native
room IDs are random63-bit, fencing callbacks across independent hosts. Relay keeps
16 outstanding frames/peer, ordered buffering, bounded queues and durable receipts.
Legacy static/local-three invitations retain their unanimous Engine path.

Checks:14 new real-socket/crash/race/native integration tests PASS;8 launcher
connection tests and3 explicit-firewall tests PASS;4 targeted legacy NP/RPC tests
PASS. All data/profiles temporary; no game launched, no product build, installation,
settings/save changes, pin update or push. Gameplay remains UNCONFIRMED.
All participants need the new runtime/discovery version for a later game test.
Details: mods-src/BBSC/docs/fixes/2026-11-04-late-join.md.

## 04.11.2026 — co-op frame rate follows launcher settings (installed on PC)

Removed forced BB_FPS=60 / BB_FPS_LIMIT=60 from regular Party launch and
local-three launch. Each local player retains its own profile FPS mode/cap;
run metadata records these per player instead of claiming a shared 60 FPS.
Selected launch-environment tests PASS (2 tests, fixed/unlocked/custom-cap cases);
git diff --check PASS. Launcher package.sh BB_FAST_DEPLOY=1 build exit0;
PC deploy exit0 (5141 files, metadata selection), native port/mod reused.
Backup: D:/Games/Bloodborne/coop-dev/backups/fps-settings-20261104-102240.
Build inputs unchanged; related chats completed. No game launch or real
settings/save changes; gameplay confirmation pending.
Above-60 platform/elevator reports in TickBbscFrameRate remain a hypothesis,
not a confirmed consequence of this change. Prefer matching rates across peers.

## 04.11.2026 — launcher presence UI installed on this PC

Co-op PLAY no longer depends on discovery readiness or mesh preflight. Removed
manual connection-check button. Presence updates every 3s without coopBusy;
adapters refresh every 15s, discovery remains alive in the hidden launcher while
its game runs. Network/name edits serialize against discovery work.
Launch permits a singleton; a known group retains missing peers instead of
silently becoming a different group. Live journal replacement protection remains.
Party roster remains fixed: first-time late joining into a singleton world is not
implemented here; detect the intended group before its first launch.
Build package.sh BB_FAST_DEPLOY=1 exit0; PC deploy exit0 (5141 files by metadata).
Backup: D:/Games/Bloodborne/coop-dev/backups/launcher-presence-20261104-100216.
No game launched; live UI/network confirmation pending.
Targeted tests: discovery 8, firewall 3, localization 5 PASS. No real settings,
saves or journals changed by development checks. Build/deploy/gameplay separate.

## 04.11.2026 — Player 1 menu fix installed on this PC

BBSC d893098 built successfully (exit0); six-file delta installed (copy exit0)
into D:/Games/Bloodborne/Bloodborne Game Launcher, including coop/party/compat.py.
Backup: D:/Games/Bloodborne/coop-dev/backups/player1-menu-fix-20261104-095340.
No game launch, real saves/settings/journals unchanged. Gameplay confirmation
remains OPEN; do not equate native fixture PASS with title arrival in game.
Source diagnosis and checks follow below.

## 04.11.2026 — Player 1 menu exit fix, BBSC d893098

Latest solo Player1 run retained Party ownerPlayer3/joinedPlayer1 at rev239.
Permit local title unload after fresh native Stop/idle and explicit current ticket,
without waiting forever for absent peers. Shared ownership/leave consensus unchanged.
Restore confirmed native System-exit latch after save/Stop and CloseMenus;
actual StageFlow branch test proves task+150 is otherwise omitted by request2.
Targeted native/production/RPC/WinHTTP checks PASS. Build/deploy in progress;
actual title arrival still unconfirmed. No saves/settings/journals changed.
See ../mods-src/BBSC/docs/fixes/2026-11-04-player1-menu-exit.md.

## 04.11.2026 — cleanup/localization installed on this PC

Built BBSC DLL and launcher package with BB_FAST_DEPLOY=1, SKIP_BUILD=1;
build and deploy exited 0. BBSC revision: 7b464e056aebddad71c3dc48f148815602f033ec.
Installed to D:/Games/Bloodborne/Bloodborne Game Launcher; 5145 files copied.
Backup: D:/Games/Bloodborne/coop-dev/backups/localization-cleanup-20261104-031341.
Build log: out/coop-dev/runs/20261104-localization-deploy/build.log.
No game launch or gameplay confirmation, no game/save/profile changes.
Existing quest/name fixes are included in the newly built mod; open gameplay
issues remain open. Third-party submodule and Python caches excluded from commits.

## 04.11.2026 — architecture/test cleanup, no product build

Reviewed main entrypoints/build dependencies and catalogued229 test/support files.
Removed unreachable launcher helpers, orphan QML and obsolete experiment launcher
setup; adapted network/UI/version tests to Party. Legacy save/profile contracts
retained with explicit skips. Targeted checks:48 PASS,1 FAIL,1 skipped.
Local-three lifetime fixture hit WinError5 replacing exit-status JSON; worker
failed and coordinator timed out. Retained as OPEN, exact file-lock cause unknown.
No game/save/settings/deploy/pin changes; second guest and host exit still OPEN.
See [audit](fixes/2026-11-04-full-project-audit.md) and parent docs/TEST-CATALOG.md.

## 04.11.2026 — current architecture and cleanup review

Mainline uses embedded Party; external server/VPS is not required. Removed
unreachable launcher ZIP/vendor installation helpers, retained native compatibility
and save paths. Targeted cleanup checks PASS; no product build/deploy/gameplay.
Second guest admission and host menu exit remain OPEN. Names/claim recheck/quest
guards retain their source-only status below. Full state committed at user request.
Review: [fixes/2026-11-04-project-cleanup.md](fixes/2026-11-04-project-cleanup.md).

## 03.11.2026 — all-current changes built/deployed; three local games launched

User requested waiting for current parallel fixes, then build/install/launch3.
Related chats completed before build; source input size/mtime and HEAD stable
through build. Parent d588b23 / BBSC ac5e70b plus inherited working changes.
Includes second-guest cooldown consumption fix, host title reload correction,
host quit input wait, accelerated initial guest placement and precise vblank tail.
DLL build0 + native incremental build0; explicit6-file delta copy0, no repeated
tests/file verification/full package. Backup:
D:/Games/Bloodborne/coop-dev/backups/all-current-three-20261103-20261103-162312.
Run out/coop-dev/runs/all-current-three-20261103-162200; coordinator27708,
local20261103-132331, UTC13:23:31. Three native PIDs12068/30784/26556 observed.
Existing local-three group/profiles and service-lifetime coordinator retained;
no save/settings/journal resets. Latest changes are client DLL/native pacing;
no VPS/server protocol change in this batch, laptop unchanged. Games left running.
Gameplay pending: second guest joins, host reaches title without reload and
input lock retains camera, guest teleport visibility and FPS/stutters. Build and
startup do not close these bugs. Earlier source-only statuses describe pre-build.

## 03.11.2026 — source-only second-guest cooldown consumption fix

Native018732DD marks pending.state1 BEFORE SummonBuild's enabled/positive role
cooldown guard can returnnull. Same-generation node stays consumed forever.
Production ApplyBbscSummonRoleDelayMask at signature-checked Scan01873269 defers
roles7/21/22/23/24 before consumption, preserving node/timer/counters/native
capacity/identity/readiness. Hook selected with research off; change-only mask
log. Exact native scan+builder-guard/production trampoline fixture reproduces
baseline and fixes delayed retry/renewed nodes; existing matchmaking fixture PASS.
Historical node/countdown not logged: causal fit, not proof of every live failure.
User no build: source only; only temporary regression harness compiled, no product
build/deploy/launch/save/settings/journal changes. Gameplay pending. See
 mods-src/BBSC/docs/fixes/2026-11-03-second-guest-cooldown.md.

## 03.11.2026 — host title reload corrected in source, build deferred

P2 character creation16:02:49.548 was automatic after menu exit, per user;
the older Continue interpretation below is superseded. Removed StageTransition
after OnReturnTitle: actual native command execution confirms this second call
arms a separate world reload despite pending title request2. Production menu
regression FAIL before/PASS after; native command regression PASS. No production
build/deploy/launch for this fix. Gameplay confirmation pending; details in
mods-src/BBSC/docs/fixes/2026-11-03-host-title-world-reload.md.

## 03.11.2026 — 16:03 run: signs returned, second guest never claimed; clean final79

Collected9 stable logs/warnings0 +3 party events +coordinator metadata:
parent out/coop-dev/runs/review-20261103-1603/pc. P1->P3, P1->P2, P3->P2 native
state6/two hunters confirmed. P3 native host->guest works after role termination,
not menu/Continue. At P3+P1, P2 sign returned but no claim. At P2+P1, P3 returned
but only claimed after P1 leaves and room recreated. P1 after guest menu/Continue
returned to P2+P3 but never claimed. Thus second-guest blocker narrowed to native
candidate/request path; exact predicate unknown, no proven UDP/capacity cause.
No3-player session, no crossed responder icon. P1 guest title0.673s/P2host3.045s.
Final79 unanimous owner/roomnull, joined/pendingempty, tx/acceptedabsent;
all native exits0, coordinatorparty_drainedtrue. Owner released BEFORE native
processes closed: missing-ACK early-close reproduction not exercised. No code,
build/deploy/launch/save/settings edits. See parent
 docs/fixes/2026-11-03-second-guest-run-1603.md.

## 03.11.2026 — 15:56 user-authorized all-current build and local-three launch

After the initial no-build request, user explicitly requested launch with all
latest changes. BBSC5351ecd / parentd588b23 plus inherited working changes:
full fast build0 (DLL/native/launcher), PC copy0/5145 files, backup
local-party-lifetime-20261103-20261103-155517. Coordinator22972;
run local-party-lifetime-20261103-155615, local20261103-125615. No journal reset,
save/settings changes or VPS update. Gameplay pending. The service lifetime
fix is implemented/tested; former-host native admission remains open.

## 03.11.2026 — source-only local exit lifetime fix; former-host admission remains open

P1/P2 native exits previously immediately closed their consensus nodes before
P3 final release. Local-three coordinator now keeps early-exit services alive
until all native games exit and unanimous idle is durable; missing coordinator
or 30s unresolved drain stops services without forced ACK/release/journal reset.
Real 3-peer lifetime regression and former-host sign/admission socket fixture
PASS; timeout/profile checks PASS. Compatibility sign_search diagnostics expose
returned/excluded/missing peers without payloads/secrets. No native search bypass;
actual P1 guest recovery remains open. User said no build: source only, no build,
deploy, game launch or save/settings edits. See parent
 docs/fixes/2026-11-03-local-party-service-lifetime.md.

## 03.11.2026 — 15:38 run: P2->P1 works; former-host P1 publishes but is never claimed

Collected9 stable mod/native logs +3 event logs, warnings0; parent
out/coop-dev/runs/review-20261103-responder-area/pc. DLL15:28:11. P2 publishes in
Cathedral240000 and joins P1 state6/two hunters. P1 active title exit2.662s and
Continue observed. P3 later becomes native host (room created); P2 joins state6.
P1 after Continue has normal responder icon, publishes sign15:35:17, but NO claim/
JoinRoom/state4/6. Crossed-area gate/publication improved; former-host guest entry
NOT confirmed/fixed. P3 earlier pre-room attempt toP1 phase11 ready=false times
out15:34:31; exact cause open. No3-player session or quit-during-Join exercised.
P2 guest menu/title1.110s+Continue works. Final all3 rev56 retains ownerP3 with
room=null/joined/pending empty. Last P3 title waits for release: persistent tx
prepare release seq18 ACK onlyP3; P1/P2 processes closed BEFORE P3 quit request.
No unilateral release/journal reset performed. P1 last idle title transition
also unconfirmed. Analysis only; no build/deploy/settings/save changes. See
parent docs/fixes/2026-11-03-responder-area-run-1538.md.
## 03.11.2026 — crossed responder bell area gate fixed, P1/P2 guest validation pending

User clarifies P1/P2 could not join one another after hosting; bell HUD crossed.
Prior P1->P2 success covered P3 as guest only. Native0191A750 still retained
!area_disable_flag in AL (Cathedral240000->flag2405) after goods/SosStatus allowed
the area. 0191A8C3 signed patch copiedAL; now MOV CL,1 lifts this geographical
veto while native common-player eligibility/range/null checks remain. Exact
native function fixture reproduces old rejection and fixes positive/negative
areas; guest-bell/matchmaking fixtures PASS. Runtime2405/common values absent
from old logs, so historical cause is consistent, not proven for every attempt.
Read-only change-only bell icon/area/publication diagnostics added. Bundled
c1d3cfd / parent1469079, inherited working changes retained. DLL build0 (3 old
warnings),5-file PC copy0, backup responder-area-crossed-bell-20261103-20261103-152859.
User-authorized coordinator20692, run responder-area-fix-20261103-152919.
P1<->P2 actual former-host guest gameplay pending; no claim of completed fix in
game. Journals/settings/saves/VPS/laptop unchanged. See parent
 docs/fixes/2026-11-03-responder-crossed-bell.md.
## 03.11.2026 — 15:07 host rotation run reviewed, P3 grant without native room remains open

Collected9 stable PC logs +3 party event logs, warnings0:
parent out/coop-dev/runs/review-20261103-host-rotation/pc. DLL14:56:31 present.
Old closing rev18 recovered normally. P1+P3 state6/two hunters; P1 addressed kick
returns P3 home. P1 role drains, P2 acquires and P3 joins state6/two hunters.
P2 active title exit completes in2.493s, guest returns home, Continue observed.
P3 next acquire unanimously final rev38 at15:06:26, BUT native remainsstate0:
no CreateJoinRoom/state1/state3 until menu15:06:59. Exact post-item/native-start
cause unknown; third hosting NOT confirmed. P3 menu releases owner rev39; all3
journals end idle. No native negotiation failure/slow-disconnect ERROR; failed
admission retry and quit-during-Join hook NOT exercised. No3-player gameplay.
All runner exit0; P2 last idle exit only reaches final-leave log before shutdown,
not a separately confirmed title transition. Analysis only; no runtime changes.
See parent docs/fixes/2026-11-03-host-rotation-run-1507.md.
## 03.11.2026 — host rotation retry/guest join exit fixed and installed, game pending

Prior local3 consensus DID rotate P2->P1 (rev8 release/rev9 acquire). P3 initial
native phase11 timeout had15/15 recorded UDP frames delivered; inner ready=false
cause remains unproven. Proven recovery bug: private Force delete retained pending
rev11, replayed failed claim and prevented fresh admission. Delivered-pending Force
withdrawal now requires native idle/no load and revision ticket (stale rejected).
Guest explicit cancel+idle now retires joined membership even without owner close.
Native stopped Join task8 selects ordinary deadline/failure cleanup via C9C6AB
read hook; no state/task writes or title ACK bypass. Real3-process rotation/failure/
retry/quit scenario + exact native predicate/CC51F0/trampoline + menu/leave fixtures
PASS. DLL build0,7-file fast PC copy0, backup p2p-host-rotation-20261103-20261103-145849.
User explicitly requested launch: coordinator28988, parent run
out/coop-dev/runs/host-rotation-fix-20261103-1459. All3 native games running15:00 (P1=33516,P2=36244,P3=20616), new DLL14:56:31 ready; gameplay pending. Saves/settings/
journals/VPS/laptop unchanged; inherited working changes kept, no pin/push.
See parent docs/fixes/2026-11-03-host-rotation-retry-exit.md.
# Переход на P2P — памятка для дальнейших исправлений

Состояние на **03.11.2026**, после запуска трёх локальных игр. Этот файл —
точка входа для продолжения работы, а не подтверждение отсутствия багов.
Обновлять при новых исправлениях и результатах игровых прогонов.

## Текущее состояние

- Рабочий репозиторий: `C:/Users/markn/CLionProjects/bloodborne_pc`, ветка `develop`.
- Мод: `mods-src/BBSC`, также `develop`; закреплённый коммит `d8c8e08`.
- Основная установка ПК: `D:/Games/Bloodborne/Bloodborne Game Launcher`.
- Пользователь принял экспериментальную P2P-реализацию как основу основной ветки.
- Старый сценарий запуска сервера и подключения по коду заменён новым интерфейсом.
- Собран и установлен лаунчер с локальным тестом на три существующих профиля.
- На момент записи три native-процесса работали; результат игрового прогона
  пользователь ещё не сообщил. Не завершать их ради обновления.
- Ноутбук и VPS при переносе в основную ветку **не обновлялись**: запрос был на этот ПК.
- Push не выполнялся. В обоих репозиториях остались унаследованные незакоммиченные
  изменения. Не включать их автоматически в свои коммиты и не делать reset/clean.

Установленные файлы собраны из рабочей копии, включая сохранённые унаследованные
правки. Один номер HEAD не описывает всю эту копию.

## Опорные коммиты

| Репозиторий | Коммит | Изменение |
|---|---|---|
| BBGL | `1650f48` | Конец истории экспериментальной ветки перед переносом |
| BBGL | `3631ee3` | Пакетная запись native-логов вместо множества мелких `fprintf` |
| BBGL | `3f4b56a` | Новый P2P-интерфейс, обнаружение и проверка связи |
| BBGL | `5360210` | Зафиксированы установка P2P и очистка экспериментальной рабочей папки |
| BBGL | `75411e7` | Локальный режим на три экземпляра |
| BBGL | `0df67d6` | Зафиксированы сборка и фактический запуск трёх игр |
| BBSC | `68035a2` | Ограниченные очереди, асинхронный диск/отправка, сокращение I/O |
| BBSC | `f56a960` | Выход хоста при оставшемся эффекте колокола; ускоренный явный возврат гостя |
| BBSC | `dd47b2c` | Неудачная попытка блокировать движение через native movement gate; FPS60 |
| BBSC | `94b53b3` | Убраны ручные ограничения; выход через native `StageTransition` |
| BBSC | `5868376` | Runtime перенесён из `experimental/party` в `party`, журналы разделены по группе |
| BBSC | `d8c8e08` | Удалён тест старого экспериментального запуска через приглашение |

Временный фильтр ввода `c5333ce` отменён в `8bdba88` по прямому требованию
пользователя и на игровые устройства не устанавливался. Не возвращать его.

## Архитектура и ограничения, которые нужно сохранить

Это распределённая сессия с временным координатором каждой ревизии,
а не постоянным выделенным сервером. Игровой хозяин мира и координатор
протокола — разные роли. Роль хозяина получается через фактическое применение
Зовущего колокола; выбор доступности пункта меню сам роль не захватывает.

В каждом процессе `run.py` работают `Engine` и `Compatibility`. Последний
предоставляет игре локальные NP/HTTP/STUN/BBSC API на loopback. Старые
`shadnet.exe` и `BBSC-GameServer.exe` для этого не запускаются.

Реплицируются ревизия, состав группы, эпоха, поколение мира, owner, room,
joined/pending/departing и результаты команд. Подтверждение изменений —
единогласное, с durable prepare/commit/final. **Нет таймаута, который сам
переназначает хозяина или разрешает загрузку меню.**

Различать ID участника, поколение TCP-соединения, поколение мира, native room
и роль хозяина. EOF/закрытие старого сокета не означает уход игрока; позднее
событие старого соединения не должно закрывать новую сессию.

Два разных потока данных:

- Native игровые пакеты остаются **UDP-датаграммами** с исходными границами,
  виртуальными портами и привязкой к участнику. Их нельзя целиком перевести
  в надёжный упорядоченный поток.
- Распределённые команды и непрозрачные BBSC frames идут через ограниченные
  очереди контроля/relay. Native UDP и эти очереди не смешивать.

WorldFlags — части снимка. Нельзя объединять всё по одному типу сообщения:
это теряет куски. Компактные party v5/v6 используют 30 групп/4 части;
старые форматы принимаются. Диагностический полный снимок включается отдельно.

HMAC подтверждает протокольные сообщения группы. Bootstrap нового лаунчера
доверяет выбранной частной VPN/LAN: предложения участников обмениваются
через неё. Это не новый защищённый discovery для публичного интернета.
Свой NAT traversal/интернет-relay здесь не реализован. Результаты relay-тестов
GNS ничего не доказывают о преимуществах/недостатках прямого P2P.

## Где искать код

| Область | Файл относительно репозитория |
|---|---|
| Выбор сети, объявления, all-peer TCP/UDP preflight | `launcher/bbport_party.py` |
| UI-слоты и запуск | `launcher/bbport_launcher_backend.py` |
| Страница подключения | `launcher/qml/CoopConnection.qml` |
| Локальные профили, порты, координатор запуска | `launcher/bbport_local_test.py` |
| Запуск локального прогона | `scripts/local_party.py` |
| Встроенный runtime перед native-запуском | `run.py` |
| Протокол состояния и opaque relay | `mods-src/BBSC/party/engine.py` |
| Локальные API, signaling, native bindings | `mods-src/BBSC/party/compat.py` |
| Disk/per-peer workers | `mods-src/BBSC/party/party_workers.py` |
| Wire schema и server-info | `mods-src/BBSC/party/schema.json`, `ss_info_template.xml` |
| Native bridge и текущий билет выхода | `mods-src/BBSC/emulator/mod/bbsc_party.cpp` |
| Native SessionLeave | `mods-src/BBSC/emulator/mod/bbsc_relay.cpp` |
| Жизненный цикл, колокола, меню, возврат домой | `mods-src/BBSC/emulator/src/core/bloodborne_re.cpp` |
| Native UDP transport | `gpu/bbnet/vendor/shadps4/core/net/p2p_transport.cpp` |
| Native logging sink | `gpu/shim/common/logging/log.cpp` |

В `party/PROTOCOL.md` остались исторические формулировки про эксперимент,
фиксированное приглашение и отсутствие broadcast. Для **текущего bootstrap**
приоритет имеют этот файл и `launcher/bbport_party.py`; ядро протокола сохранено.

## Новый сценарий лаунчера

«Автоматически», Tailscale, Radmin, своё подключение. Tailscale использует
список online peers из `tailscale status --json`; LAN/Radmin — directed broadcast.
Для своего подключения доступны локальный IPv4 адаптера и явные адреса участников.
При неоднозначном выборе сети требуется явный выбор, не случайный адаптер.

Перед запуском участники должны видеть одинаковый состав группы из 2–5 игроков.
Каждый проверяет TCP/UDP до каждого. Перед самим запуском проверка повторяется:
старый статус «готово» не разрешает старт после потери связи. Изменение группы
запрещено при незавершённой роли/комнате прежней группы.

Обычные порты: discovery TCP+UDP `37601`, control TCP `37600`, native UDP `37658`.
Preflight проверяет discovery-путь TCP/UDP; **не доказывает** доставку native
UDP37658, прохождение конкретного VPN или игровую плавность.
Все участники запускают игру до использования колоколов.

Основные данные каждого профиля:

- `coop/party/identity.json` — постоянная локальная идентичность;
- `coop/party/config.json` — согласованная группа;
- `coop/party/groups/<group>/party-journal.json` — durable control;
- рядом `party-relay-journal.json` и `party-events.jsonl`;
- `coop/bbsc/` — собственные данные/логи мода;
- `<фактический user_dir>/last_run.log` и ротации — native stdout.

Не копировать в эту памятку secret, token, приглашения, пароли или полные settings.
Нельзя удалять журнал как способ «лечения» занятой роли.

## Выход хоста/гостя: что меняли

Ранее выход гостя и повторное подключение мешал старый cancel latch. Затем
хост застревал: native idle и room=null уже наступали, но сохранённый эффект
колокола мешал освобождению owner. Title ждать owner, owner ждать исчезновения
эффекта — цикл. Добавлен текущий положительный cancel ticket и доказательство
сохранённого/остановленного выхода. Loading, живые участники и неподтверждённая
ревизия по-прежнему не разрешают раннюю загрузку меню.

Движение хоста во время выхода **не было устранено** попыткой `DisableMove`/
movement hook/r14. Пользователь явно потребовал нативный переход без ручной
блокировки. В `94b53b3` эти вмешательства удалены:

1. Сохраняется штатное System-меню во время save → Stop → final group ACK.
2. Выбирается title через `OnReturnTitle`.
3. Вызывается штатный `StageTransition`, затем закрывается старое меню.

Нет принудительного выбора домашних координат хоста или записи loading/session
вручную. Целевые fixture-тесты прошли; новый переход в игре ещё не подтверждён.
Принятие P2P пользователем не означает автоматического закрытия этого бага.

Проверено по оригинальному Lua/native: `OnBeKickOut` показывает уведомление,
назначает через 5с `OnLeave_Limit`, поднимает 4047 и вызывает `SetLoadWait`.
`OnLeave_Limit` вызывает `WarpNextStageKick`, а тот — `StageTransition`.
`SendPhantomHome` тоже использует `StageTransition`. Отдельного `DisableMove`
в этих Lua-цепочках нет. Флаг4047 прежде всего защищает от повторного ухода;
не приписывать ему одному доказанную блокировку движения.
`EventMenuBrake` = CloseMenu → SetMenuBrake, но непосредственно из
`OnBeKickOut` не вызывается. Точный потребитель ранних ограничений ещё не разобран.

## Локальный режим на одном ПК

Кнопка «Локальный тест: 3 игрока на этом ПК» запускает три игры с существующими
профилями `%LOCALAPPDATA%/Bloodborne Game Launcher Player 1`, `Player 2`, `Player 3`.
Имя папки каждого профиля содержит полный префикс. Имена: MarkTest1/2/3.
Фактический user_dir проверять по настройкам и свежим native-логам.

| Игрок | ID группы | Control TCP | Native UDP |
|---|---|---|---|
| Player 1 | LocalPlayer1 | 37610 | 3658 |
| Player 2 | LocalPlayer2 | 37611 | 3659 |
| Player 3 | LocalPlayer3 | 37612 | 3660 |

Все адреса — `127.0.0.1`. Guard TCP37609 предотвращает второй координатор запуска.
Общая конфигурация: основной профиль `coop/local-test/config.json`; metadata и
runner logs — `coop/local-test/runs/<UTC stamp>/`. Журналы игр остаются раздельными.

До старта проверяются наличие всех профилей, игры, трёх разных папок сейвов и
свободные порты. Каждый child получает BBGL_PROFILE_DIR **до** загрузки лаунчера.
Переменные путей другого игрока очищаются. Профили и сейвы не пересоздаются.
Оконный режим1280×720 и Skip Intro задаются на запуск, без записи settings.
Обновление 04.11 (исходники): FPS и лимит берутся из профиля каждого игрока.
При выходе/ошибке одного игрока остальные игры не завершаются автоматически.

Последний запуск:

- `out/coop-dev/runs/local-three-20261103-142526/run.json`, старт11:25:26 UTC /14:25:26 МСК;
- P1 native PID28640, P2 PID19400, P3 PID36528 — **исторические**, не использовать
  для последующих действий без свежей проверки;
- у всех наблюдались NP login/context/world replies и свои native UDP-порты;
- роли ещё не назначались: предложен P1 Зовущий, P2/P3 Малый;
- движение/бой, выход одного гостя при остающемся втором, повторный вход и
  выход хоста требуют ответа пользователя.

## Открытая проблема запуска: выделение портов Compatibility

Первый запуск P1 закончился **до native игры** ошибкой
`OSError: Cannot reserve native compatibility ports` в `Compatibility.__init__`.
TCP выбирается через bind(port=0), UDP должен занять соседний NP-port+1;
после 16 неудач конструктор сдаётся. Точная причина исчерпания не доказана
(конфликт/исключённый диапазон/повторный выбор ОС — пока гипотезы).

У ошибочного runner не было native-потомка. Завершён только его диалоговый helper,
P1 повторно запущен с тем же профилем и группой — успешно. P2/P3 не завершались.
Ошибка **не исправлена**. Повтор не выдавать за исправление allocator.
При разборе проверить выделение пар TCP/UDP и закрытие частично созданного Engine,
повторение одного кандидата ОС, Windows excluded ranges, одновременный старт.
Общие установленныe файлы при уже работающих играх не заменять.

## Проверки и пределы подтверждения

- 5 проверок discovery/full mesh/негативных случаев — PASS.
- 4 проверки локального режима: 3 настоящих embedded clients, все 6 направлений
  UDP с native-подобным wildcard bind, занятые порты, изоляция путей — PASS.
- Installed frozen runtime: схема JSON, XML server-info, embedded API — PASS.
- Installed QML: четыре подключения, отсутствие server/invite actions,
  наличие локального режима — PASS.
- Production menu state-machine и explicit-host-return fixtures — PASS.
- Сборка native/DLL/package при mainline-переносе — exit0, DLL3 прежних warning.
- Последний локальный режим: пересобирался только лаунчер, exit0; установлены
  EXE, base_library.zip, QML и `scripts/local_party.py`.
- Не утверждать по этому списку подтверждение VPN/NAT, FPS или игрового выхода.

Полезные целевые тесты: `tests/test_party_connection.py`, `tests/test_local_party.py`,
`mods-src/BBSC/tools/test_menu_quit.py`, `test_explicit_host_return.py`,
`mods-src/BBSC/party/test_rpc.py`, `test_menu_rejoin.py`, `test_io_workers.py`.
Запускать только затронутые сценарии. Не запускать автоматически восстановление
сейвов/полные наборы. Реальные сейвы не хэшировать и не откатывать без просьбы.

## Где остались резервные данные и материалы

- Mainline backup: `D:/Games/Bloodborne/coop-dev/backups/p2p-main-20261103-20261103-095153`.
- Local-three backup: `D:/Games/Bloodborne/coop-dev/backups/local-three-20261103-20261103-142456`.
- Старые server/account binaries и default server file перемещены в mainline backup.
- Экспериментальная Git working tree удалена штатно через Git; ветки сохранены.
- Безвозвратное удаление тестовой установки заблокировано автоматической проверкой.
  Она архивирована в `D:/Games/Bloodborne/coop-dev/backups/retired-serverless-party-20261103`.
- Тестовый профиль ПК с сейвами архивирован в основном профиле
  `backups/serverless-party-PC-20261103`. Это архивирование, не стирание данных.
- Исходные dirty patches/отличающиеся untracked sources: `out/p2p-migration-safety`.
- Исторические подробности: `docs/fixes/2026-11-03-p2p-mainline.md`,
  `2026-11-03-local-three-p2p.md`, `2026-11-03-serverless-host-menu-exit.md`;
  в моде `docs/fixes/2026-11-03-native-title-transition.md`.

При новом «готово» сначала собрать логи **всех трёх профилей** и их ротации,
сопоставить реальные роли/PID/время. Начало текущего прогона брать из run.json,
а не из старого PC+ноут-прогона. Сначала установить точку отказа: discovery,
подтверждение группы, NP/signaling, native JoinRoom, UDP или переход мира.
