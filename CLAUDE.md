## Цикличные обработки — только с разрешения пользователя, 06.11.2026

Любые новые цикличные обработки в моде (периодические опросы, таймеры,
ticks, фоновые проверки и повторы), в том числе внутри существующего
обработчика, добавлять только после явного разрешения пользователя
на конкретный механизм. Общая просьба исправить баг или добавить функцию
не считается таким разрешением. Обоснованная невозможность штатного решения
тоже не заменяет разрешения. До согласования описать назначение, период,
объём работы и ожидаемую стоимость; сначала искать штатный событийный путь.
Такие обработки не должны ухудшать общую оптимизацию: оценивать суммарную
нагрузку, включая простой и рост числа игроков/объектов, и проверять влияние
на производительность. При обнаружении регрессии устранить её до принятия
изменения; одно разрешение на механизм не означает согласия на ухудшение.

## Штатные обработки и оптимизация — предпочтение пользователя от 06.11.2026

При любых изменениях и новых доработках сначала искать и пробовать использовать
или корректировать штатные обработки игры/порта: существующие условия, команды
и обработчики. Предпочитать снятие конкретной блокировки сохранению её с новой
параллельной реализацией. Новые hooks/ticks, опросы, обходы памяти, очереди,
сетевые сообщения и повторы добавлять только при обоснованной невозможности
решить задачу штатным путём; объяснять ограничение и дополнительную стоимость.
Сохранять исходные ожидания, анимации, завершение событий и границы авторитета.
Перед такими работами читать и по новым результатам обновлять
[память по оптимизации](mods-src/BBSC/docs/OPTIMIZATION.md).

> Подтверждение пользователя 05.11.2026: основной сюжет полностью пройден и проверен в кооперативе, переход в NG+ работает. Чаши работают совместно, штатная случайная генерация корневых чаш возвращена. Прежние общие статусы финала ниже исторические; редкие сценарии наград/обрядов/составов группы учитываются отдельно.

> Подготовка BBGL 1.2.0 (05.11.2026): [описание релиза](docs/release-1.2.0.md). Текущий путь — LAN/VPN P2P с поздним подключением; отдельный сервер не нужен. Исторические версии/пути ниже не являются текущими инструкциями. Статусы сборки и игровых проверок см. в [отчёте подготовки](docs/fixes/2026-11-05-release-1.2.0-preparation.md).

> Награды/добыча, актуализация05.11: [сводка BBSC](mods-src/BBSC/docs/REWARDS.md).
> Она фиксирует итог чата и заменяет промежуточные описания очереди/drop fallback,
> home-only catch-up и секундного опроса наград. Последняя DLL установлена на ПК,
> два профиля стартовали06:24:17 МСК; игровой результат остаётся открытым.

> Сборка и установка очистки/локализации на этот ПК завершены 04.11 (exit=0),
> коммиты BBGL ec0ec22 / мод 7b464e0; детали в docs/P2P-HANDOFF.md.
> Игрового подтверждения нет. Правила русской локализации закреплены в AGENTS.md.

> Русская локализация 04.11: [отчёт](docs/fixes/2026-11-04-localization-review.md).
> Термины сверять с оригинальными msg/rusru; файлы игры только читать.
> Проверять длину текста в Qt и игровых рамках; 52 символа подсказки — лишь
> редакционный бюджет. Исходники исправлены, игровая проверка не выполнена.

> Аудит 04.11: [отчёт](docs/fixes/2026-11-04-full-project-audit.md). Каталог тестов — docs/TEST-CATALOG.md
> родительского проекта. Не запускать общий discover: некоторые native scripts
> выполняются при импорте; VPS/Blender/ELF — ручные. Файлы unittest без main
> запускать через unittest. Исторические save/profile skip не считать PASS.
> Отдельный экспериментальный party/launch.py и его prepare-скрипт удалены;
> текущий запуск — run.py / scripts/local_party.py.

# Актуальное состояние — 04.11.2026

Основной кооп использует локальный Party внутри run.py, private-network discovery
и native UDP; отдельный VPS/shadNet/gameserver для этого пути не нужен.
Старые серверные инструкции ниже — история, не текущая схема запуска.
Имена игроков, повтор ожидания того же claim и квестовые guards добавлены в исходники;
их игровое подтверждение ещё требуется. Второй гость и выход хоста остаются открыты.
Overlap-admission эксперимент отменён, используется последовательный native admission.
Для обычного деплоя — BB_FAST_DEPLOY=1, delta изменённых компонентов, без повторного
verify-release/хэширования. Код, сборка, установка и игровой результат различаются.
Текущее состояние см. в HANDOFF и отчёте docs/fixes/2026-11-04-project-cleanup.md
родительского репозитория; исторические пути/версии ниже не применять автоматически.

> **Правила проверок:** [docs/TESTING.md](docs/TESTING.md). Тестировать затронутое поведение; проверки сейвов/восстановления не являются стандартным обязательным прогоном.

# Актуальные рабочие правила — 01.11.2026

При расхождении со старыми разделами ниже приоритет у этой записи и
[BBSC HANDOFF](mods-src/BBSC/docs/HANDOFF.md).
Работаем локально в Windows/PowerShell; VM/device_bash не требуются.
Единственный источник и место сборки мода — подмодуль `mods-src/BBSC`.
Staging `out/stage/Bloodborne Game Launcher`, ZIP `dist/bbgl-1.0.0-windows-x64.zip`.
Установка: D:/Games/Bloodborne/Bloodborne Game Launcher (ноут C:/Games/Bloodborne/Bloodborne Game Launcher).
Профиль: %LOCALAPPDATA%/Bloodborne Game Launcher, данные BBSC: profile/coop;
бинарники: install/coop/client/bbsc. Старые bbgl/bbport-coop — история.
coopdev.ps1 исправлен: текущий профиль имеет приоритет; status показывает пути данных и логов.
T26 отменён; Офлайн / Совместно выбираются при запуске.
Native menu save/disconnect подтверждён для гостя в группе из двух.
T22/T23/T24 закрыты пользователем; T25 в целом решён, осталось покрытие.
Локальные GPU-вылеты этого ПК отложены пользователем, не считать блокером мода.
Не откатывать сейвы без отдельной просьбы. Не менять файлы игры; не включать их в пакет.


# Current naming (2026-10-31)

BBGL = Bloodborne Game Launcher; GitHub: mark3317/bbgl. Mod: BBSC-GL, mark3317/bbsc-gl. Release folder: `Bloodborne Game Launcher`; profile: `%LOCALAPPDATA%\bbgl`. Source checkout folder names below remain local paths. Historical test paths refer to the installation at the time.

# bloodborne_pc / bbport (форк mark3317) — заметки для Claude

Windows-порт Bloodborne (bbport) + Qt/QML-лаунчер на Python, в нашем форке — сборка «bbport-coop»
с кооперативом BBSC. Цель: релизный кооп (см. CLAUDE.md в `mods-src/BBSC`) и лаунчер с минимумом настроек:
запустил → указал игру/сейвы/графику → играешь; моды, сервер, BBSC настраиваются автоматически и скрыто.

Общайся по-русски. Пользователь — Android/Kotlin-разработчик, Linux/macOS знает.

## Рабочие папки (mark-pc, Windows)
| Путь | Что |
|---|---|
| `C:\Users\markn\CLionProjects\bloodborne_pc` | этот репо |
| `C:\Users\markn\CLionProjects\bloodborne_pc\mods-src\BBSC` | форк мода BBSC; его `build\mod` кладётся в пакет |
| `D:\Games\Bloodborne\bbport-coop` | установленный лаунчер на этом ПК (сюда деплоим) |
| `D:\Games\Bloodborne\game` | файлы игры CUSA03173 v1.09 (только чтение!) |

Тестовые машины: этот ПК, ноутбук `local_pc` (192.168.88.233, Windows 10, ssh `markn`),
VPS `remote_server` (77.73.67.175, Ubuntu 24, ssh `root`) — co-op сервер (shadNet/BBSC gameserver).

## Git
- Remotes: `mark` = github.com/mark3317/bbgl (push сюда), `origin` = Jgamrot/bloodborne_pc (апстрим, только fetch).
- Рабочая ветка: `mark/coop-relay`. Не пушить в `origin`, без force-push без явной просьбы.
- Стиль коммитов: `<область>: <что сделано>` (например `bbnet event filter: ...`).

## Структура
- `src/` — C-код порта/хуков (probe.c — загрузчик, engine_hooks, pc_menu, mouse_camera, ...).
- `gpu/` — видеоядро shadPS4 (CMake), там же `gpu/shadps4` и сеть/bbnet.
- `launcher/` — лаунчер: `bbport_launcher*.py`, `bbport_coop.py` (кооп, сервер, invite), `bbport_pkg_setup.py` (мастер установки), `qml/`.
- `packaging/windows/` — `package.sh`, `build-coop-package.sh`, `build_coop_server.sh` (shadnet-p2p + патчи), `play.c`.
- `tests/` — pytest + C-тесты. `docs/` — ROADMAP, CHANGELOG, DEVELOPMENT_LOG.ru.md.

## Сборка (только MSYS2 CLANG64: `C:\msys64\msys2_shell.cmd -clang64` или `bash` с `source msys2-env.sh`)
- Порт: `bash build.sh` → `out/bb-probe.exe`, `bb-play.exe`, `bb-gpu-capabilities.exe` (лог `out/gpu-build.log`).
- Полный кооп-пакет: `bash packaging/windows/build-coop-package.sh`
  (`SKIP_BUILD=1` — без пересборки exe; `COOP_BBSC_BUILD` по умолчанию `mods-src/BBSC/build/mod`;
  `COOP_INVITE`/`COOP_NAME` — сервер по умолчанию). Результат: `out/stage/bbport-windows/` и `dist/bbport-coop-windows.zip`.
- Co-op сервер (shadnet) для Windows-хоста: `bash packaging/windows/build_coop_server.sh`.

## Деплой на этот ПК / ноут
- Источник — `out/stage/bbport-windows/`. Копировать поверх установки, НЕ затирая пользовательское:
  `user/`, `mods/`, `bbport.ini`, `input.ini`, `mods.json`, `patches.json`, `coop-server.json` (если там свой сервер).
- Перед заменой — бэкап заменяемых exe/dll (`*.bak-YYYYMMDD`, как `bin/bb-probe.exe.bak-20261027`).
- Ноут: `scp`/`ssh local_pc` (Windows, cmd/PowerShell), путь установки на ноуте уточнить у пользователя, если не записан.

## Цикл разработки и теста (tools/coop-dev в bloodborne_pc)
`bloodborne_pc/tools/coop-dev/coopdev.sh` (из Linux-VM Claude, по ssh) + `coopdev.ps1` (Windows-сторона):
status · commit bbsc|port · build mod|port|package · job · deploy mod|launcher pc|laptop|all · deploy server ·
save list|snap|restore pc|laptop · test begin|collect. Логи прогонов: `bloodborne_pc/out/coop-dev/runs/<id>/{pc,laptop,vps}`.
Снимки сейвов: `<D:|C:>\Games\Bloodborne\coop-dev\saves\<имя>` (SPRJ0005 + BBSC own-world/bell-pending).
На ноуте: установка `C:\Games\Bloodborne\bbport-coop`, user_dir `C:\Games\Bloodborne\test`. На ПК user_dir `D:\Games\Bloodborne\ddd`.
Логи BBSC: `%LOCALAPPDATA%\bbport-coop\BBSC-0.0.1-BBport\bbsc\logs` (+ captures), лог игры `<user_dir>\last_run*.log`.
VPS: `/opt/bbsc/{gameserver,shadnet,logs,data,backups}`, сервисы `bbsc-gameserver`, `bbsc-shadnet` (пользователь bbsc).

## Правила
- Сейвы — только копии. Файлы игры не изменять.
- Лаунчер: любую новую настройку мода/кооператива по возможности делать автоматической, а не ещё одним полем для пользователя.
