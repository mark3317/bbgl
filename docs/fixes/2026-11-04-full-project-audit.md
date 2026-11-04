# Аудит архитектурных остатков и тестов — 04.11.2026

## Исходное состояние и границы

BBGL `fcd09c2`, BBSC `ef1d8ff`, gitlink совпадал с HEAD мода. Исходные
изменения стороннего `gpu/third_party/fsr-vulkan` и Python-кэши оставлены как были.
Коммиты, смена pin, сборка продукта, деплой и запуск игры в этом проходе не выполнялись.
Файлы игры, реальные сейвы и настройки не менялись.

В отличие от предыдущей очистки проверены основные области обоих проектов:
точки входа, связи сборки/упаковки, динамические UI-вызовы, генераторы, native
регистрация, инструменты и весь каталог тестовых файлов. Это статический аудит
достижимости и назначения с целевыми прогонами, а не доказательство отсутствия
любого мёртвого кода во всех путях исполнения. Построчная ревизия стороннего
renderer/emulator и всех вариантов условной компиляции не проводилась.

Полный каталог: [TEST-CATALOG.md](../TEST-CATALOG.md), 229 тестовых и
вспомогательных файлов. Он отражает статический просмотр, а не 229 успешных запусков.

## Карта действующего проекта

| Область | Точки входа и потребители | Решение / покрытие |
|---|---|---|
| Windows launcher | `bbport_launcher_win.main`, `bbport_startup`, `bbport_launcher_qml.run_ui`, QML → LauncherBackend | Qt — основной UI; `--classic-launcher` сохраняет Tk. Startup/setup/lifetime/UI tests различают эти задачи. |
| Linux launcher | `bb-launcher.sh`, install-desktop, GTK `bbport_launcher.py`, AppImage/Nix | Другой поддерживаемый способ запуска, не дубликат для удаления из Windows-ориентированного аудита. |
| Подготовка игры | `run.py`, prepare/link_libc/link_modules/patches/mods, content profile | Строковые `run_script` и `--script` учитываются как вызовы. CPU compatibility, shader catalog, rematches, prompts, language и game-check остаются. |
| Настройки и ресурсы | core defaults/env, backend FIELDS/SETTINGS_SECTIONS, QML и Tk, artwork/icons/fonts | Ключ профиля не равен UI-полю. `player_name` остаётся в данных, убрана только неотображаемая дублирующая строка Qt. Tk/Pillow/Tcl не удалены. |
| Кооп | `bbport_party`: сеть/discovery/mesh → конфигурация → `run.py` → `party/compat.py` | Текущий путь использует локальный Party, не старые Host/account/invite API. Проверки сети перенесены на реальный choose_network. |
| Party | engine + party_workers: согласование/запись; compat + protobuf/schema: loopback NP/HTTP/STUN | Native имена и durable identity различаются. Tests: identity, compat, rpc, processes, workers, pipeline — разные контракты, не дубликаты. |
| Native сеть | gpu/bbnet glue, guest_net, matching/signaling, transport/relay | Старая терминология не делает код мёртвым. Local compatibility использует native NP; UDP gameplay отделён от consensus. VPS fixtures помечены ручными. |
| DLL мода | build-mod-bbport.cmd → bbsc_mod Worker → byte patches/hooks, StartRelay/StartP2PChannel/InstallSessionRegister/PartyMaintain | `bloodborne_re.cpp`, patch tables, memscan и mod helpers входят в реальную DLL. Ничего не удалено по одному отсутствию обычного C++-вызова. |
| Port/runtime | build.sh + gpu/CMakeLists: probe, runtime*.c, engine/menu/input/graphics | `do_pwrite/do_rename/do_ftruncate/do_truncate/do_fsync` вызываются через `do_##name`; ложные кандидаты сохранены. Native tests и CMake targets остаются. |
| GPU | gpu/CMakeLists, shadps4/shim, shader recompiler, FSR/DLSS bridges | Проверены интеграционные зависимости и тестовые targets, без чистки сторонних внутренностей. Test stubs используются также shader-prebuild. |
| Генераторы | tools/gamedata gen_messages → bbsc_messages.inc; gen_messages_ru → RU table; quest_reward_rules → header; menu assets/prompts/shaders | Generated includes имеют потребителей; не редактировать как независимые исходники. Проверки с оригинальными данными — отдельный запуск. |
| Пакет | build-coop-package.sh → DLL/port → package.sh/PyInstaller → bundle-coop.py | DLL + 7 файлов Party + metadata/licenses. Отдельный server builder не вызывается. Дубли hidden imports удалены, уникальные зависимости сохранены. |
| Dev tools | coopdev.ps1/sh, scripts/local_party.py, bbport_local_test, profile launchers, pacing/perf tools | Действующие инструменты сохранены. Старый prepare-serverless-party вызывал отсутствующий launch.py — удалён. |
| Legacy server/emulator | server/gameserver, server patches/build_coop_server.sh, emulator tests/CMake | Отдельные инструменты совместимости/разработки и история исходного проекта; не входят в основной Party package. Сохранены, текущая инструкция server builder исправлена. |

## Подтверждённые удаления и основания

Поиск включал Python/QML/scripts/run/packaging/tests, а не только Python AST.
Одиночное упоминание имени использовалось как кандидат, не как доказательство.

| Элемент | Доказательство и последствия | Проверка |
|---|---|---|
| `bbport_coop.installed_version`, `host_address` | Нет потребителей в рабочих entrypoints. Текущий discovery выбирает сеть через Party. | Сеть/launch tests |
| `select_host_address` | Вызывали только старые tests/test_host_connections; UI использует `party.choose_network`. | Перенесены ambiguity/multi-address/absent-provider/custom-local сценарии; 6 PASS |
| Backend `_coop_ensure_packages`, `_coop_probe`, `_coop_progress`, `_coop_show_progress`, signal/connect | Внутренний замкнутый остаток старой установки пакетов; coopPlay проверяет installed и вызывает party.launch_environment. | Firewall action, Party, UI |
| Backend `scene_size_text`, `_mods_dir`, `_choose_prompt_download` | Нет вызовов из QML/кода/строковых действий. Текущие prompt packs выбираются setPrompt. | Settings/UI tests |
| `openShadNetRegistration` | Не подключён к текущему QML; публичная регистрация не является частью Party launch. | Поиск UI-вызовов |
| `CoopFirewall.qml` | Не включён в qmldir и нигде не создаётся/не загружается; действующий firewall UI в CoopConnection. Сам coopConfigureFirewall сохранён. | Firewall action 3 PASS |
| Дублирующее `FIELDS.player_name`, search hint online_npid | Строка отсутствовала в SETTINGS_SECTIONS, второй edit имени заменён coop_name. Данные player_name и синхронизация сохранены. | Settings navigation 2 PASS; redesign 4 PASS |
| `run.py started=[]` и пустой terminate-loop | Список не заполнялся после удаления отдельных серверных процессов. Party/game cleanup сохранён. | Реальный runner log fixture 2 PASS; run_scripts 3 PASS |
| `prepare-serverless-party.ps1` | Создавал команду на `coop/party/launch.py`, которого нет ни в подмодуле, ни в packaged manifest. | Поиск путей; исторический эксперимент помечен |
| Неиспользуемые `http.client`, `sys`, `datetime` | Нет обращений в соответствующих launcher_win/local_test/compat. Future annotations сохранены. | Python syntax, локальные/identity/logging tests |
| Повторные hidden imports | socketserver/http.server/hmac/uuid уже присутствуют в той же строке package.sh. | Shell syntax; упаковка продукта не запускалась |

Справка `scripts/bbsc_information.py` больше не обещает резервную копию
лаунчером перед каждой кооп-сессией: текущий Party launch не вызывает сохранённый
backup_saves. Это исправление текста, не изменение логики сейвов. Native механизмы
резервирования не оценивались как эквивалент этой старой гарантии.

## Тесты: удаление, адаптация, сохранение

- Удалены 8 тестов старых invite/account/Host/environment/end_tree API из test_coop
  и helper account_server: соответствующих API уже не было до этого аудита.
- Из redesign удалены 2 сценария старого hosting UI; проверка выбранного имени
  использует текущий app state вместо отсутствующего `_coop_account`.
- Из Party identity удалён тест отсутствующего экспериментального launch.py;
  оба теста int32 identity/collision сохранены и прошли.
- test_host_connections теперь проверяет действующий choose_network. Custom IP
  должен принадлежать активному локальному интерфейсу; старое разрешение любого
  advertised IP не переносилось как требование к новой архитектуре.
- Settings navigation приведён к реальным QML-секциям (Game files; Steam/Launch
  больше нет). Неотображаемое поле исправлено в production, а не исключено из
  проверки полноты таблицы. Тест полноты по-прежнему требует один destination.
- Тест stable updates фиксирует VERSION внутри fixture; он больше не становится
  ложным при выпуске новой версии продукта. Preview/старые теги по-прежнему отвергаются.
- Старые save/profile contracts не удалены: два метода получили явный skip с
  причиной отсутствующего API. Это сохранённый технический долг, не PASS и не
  актуальное покрытие Party. Остальные сейвовые и миграционные тесты не тронуты.
- Header/stubs, Python/native пары и исследования не удалялись как «дубли»:
  Python часто компилирует или управляет native fixture, а stubs дают link support.
  Признаков безопасного массового объединения остальных тестов не найдено.
- String-based проверки и извлечение production функций имеют ограниченную
  устойчивость к рефакторингу; они сохранены как дополнительные guards. Socket/
  process/native tests остаются отдельным доказательством поведения.

## Проверки и обнаруженные проблемы

Финальные целевые наборы (повторялись только после соответствующих изменений):

| Набор | Результат |
|---|---|
| redesign | 4 PASS |
| host/network selection | 6 PASS |
| coop helpers | 6 PASS, 1 исторический skip |
| party log ownership | 2 PASS |
| Party identity | 2 PASS |
| firewall action | 3 PASS |
| settings navigation | 2 PASS |
| bundled release: version/settings, без save test | 2 PASS |
| DLSS startup/UI categories | 2 PASS |
| Party connection | 6 PASS |
| launcher defaults/information | 3 PASS |
| Party logging | 1 PASS |
| run scripts | 3 PASS |
| local_party | 6 PASS, 1 FAIL |

**Открытый дефект, P2:** test_closed_native_games_keep_real_consensus_peers_until_owner_releases
получил PermissionError/WinError 5 в bbport_party.write_json при os.replace
LocalPlayer1-exited.tmp → LocalPlayer1-exited.json. Worker завершился с исключением,
coordinator не завершился за 8 секунд. Проверка поймала реальную ошибку I/O в
процессе теста; причина конкретной блокировки файла не доказана. Удаление одного
неиспользуемого импорта sys не меняет эту логику. Тест сохранён, состояние не
выдаётся за исправленное. Собственный незавершившийся тест остановлен; игры не трогались.

Другой долг: смешанные старые save/profile contracts надо мигрировать отдельно;
каталог не даёт оснований запускать/удалять их автоматически. Native fixtures,
которые извлекают код по `.index`, могут требовать адаптации после будущих изменений.

## Сохранённые спорные элементы

- bbport_bundle.install/verify и coop.download/setup_done/backup_saves: сейчас
  не часть основного Party launch, но связаны с сохранёнными проверками установки,
  профилей и данных. Не вырезаны вместе с сохранительными контрактами.
- Сторонний shadPS4/emulator, legacy server, Linux/Tk, shaders/FSR tools:
  отдельные build/tool entrypoints, а не доказанно мёртвые копии.
- Qt Property/Slot без прямого Python-вызова: Qt и QML используют динамические
  связи; удалены лишь конкретные подтверждённые остатки, не весь список кандидатов.
- Native hooks/stubs/ABI и generated tables: публичная или макросная регистрация
  важнее числа текстовых ссылок.
- Старые исследования/логи в документации: сохранены как исторические свидетельства.

Сборка, установка, запуск, полное прохождение тестов и исправление игровых багов
этим аудитом не подтверждены. Второй гость и выход хоста остаются открытыми.
