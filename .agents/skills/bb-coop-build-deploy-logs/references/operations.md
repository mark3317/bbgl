# Команды повторяющегося цикла

Команды PowerShell выполнять из корня текущего checkout. Один раз в сессии:

```powershell
$repoRoot = (Get-Location).Path
$skillRoot = Join-Path $repoRoot '.agents/skills/bb-coop-build-deploy-logs'
```

Проверить, что `$repoRoot` содержит AGENTS.md и mods-src/BBSC. Для установки
и запуска отдельно задать `$gameInstall` (существующая установка на текущем
устройстве) и `$deployRoot` (каталог для бэкапов и временной распаковки).
Значения получить из состояния устройства или запроса пользователя, без
подстановки путей другого ПК. Ниже эти переменные уже должны быть заданы.
Подготовка среды: [WORKSTATION.md](../../../../docs/WORKSTATION.md).

## Быстрая сборка и деплой — стандарт проекта

Только мод, при существующем staging, из корня checkout:

```powershell
& ./mods-src/BBSC/emulator/mod/build-mod-bbport.cmd
# Продолжать только после exit=0.
python "$skillRoot/scripts/prepare-mod-delta.py" --repo $repoRoot
$deltaFiles = @('coop/client/bbsc/bbsc.dll','coop/client/bbsc/bbsc-launch.exe','coop/client/bbsc/mod.json','coop/client/bundle.json','coop/SOURCE.json')
& "$skillRoot/scripts/deploy.ps1" -Source (Join-Path $repoRoot 'out/stage/Bloodborne Game Launcher') -Install $gameInstall -Root $deployRoot -Label 'latest-mod' -Files $deltaFiles
```

prepare-mod-delta.py обновляет runtime manifest только для трёх изменённых
файлов (расчёт обязательных полей, без проверки содержимого установки).
Одна установка ПК обслуживает все локальные профили. По указанию от 03.11.2026
режим ПК + ноутбук также разрешён для обычного сетевого прогона.
Source не должен быть пользовательской установкой. Скрипт создаёт бэкап.

Полный пакет — при новом staging или изменениях launcher/server/зависимостей:

Из корня того же checkout в **MSYS2 CLANG64**:

```bash
mkdir -p out
BB_FAST_DEPLOY=1 bash packaging/windows/build-coop-package.sh > out/build-deploy.log 2>&1
```

Добавить SKIP_BUILD=1, когда native код не менялся. BB_FAST_DEPLOY=1 отключает
verify-release и аудит файлов; одна архивация с быстрым сжатием, без SHA256 ZIP.
Полный пакет пересобирает все компоненты, поэтому для обычных правок DLL — delta.
Релизы для друзей относятся к bb-coop-release и отдельному запросу.
Staging: out/stage/Bloodborne Game Launcher;
ZIP: dist/bbgl-<версия>-windows-x64.zip (версию брать из текущей упаковки). Деплой полного пакета — без -Files.
-CheckOnly показывает выбор по метаданным без замены и чтения содержимого.
Следить за exit code; после ошибок зависимые шаги не выполнять.
Для SSH к VPS читать ssh-my-devices. Сложные команды передавать файлом/EncodedCommand,
задать $ProgressPreference='SilentlyContinue'. После установки выполнить
запрошенный запуск по разделу ниже.

## Ноутбук: один набор файлов, установка и видимый запуск

Сначала барьер связанных чатов из SKILL.md. Перед SSH прочитать ssh-my-devices;
использовать актуальный адрес и строгую проверку host key, BatchMode и timeout.
Путь установки, профиль и интерактивного пользователя определить из существующих
настроек/handoff и короткого чтения состояния ноутбука. Не копировать настройки,
учётные данные и сейвы ПК поверх ноутбука.

Собирать только на основном ПК. Для DLL передать out/mod-delta.zip и deploy.ps1
через scp в отдельный временный каталог ноутбука, распаковать delta в staging и
вызвать deploy.ps1 с пятью -Files из примера выше и фактическими -Install/-Root.
Delta ZIP содержит обёртку Bloodborne Game Launcher/: после распаковки указать
Source на этот вложенный каталог, содержащий coop/SOURCE.json. Передавать -Files
явно: в delta отсутствует Bloodborne.exe, поэтому это не полный пакет.
При полном пакете передать готовый ZIP и вызвать deploy.ps1 -Source <zip> без -Files.
Не собирать второй пакет, не передавать всю игровую папку. Перед копированием общих
файлов игра на каждом устройстве должна быть остановлена. Бэкапы остаются на том
устройстве, где заменены файлы. При ошибке ноутбука не объявлять оба устройства готовыми.

Для видимого запуска по SSH использовать существующий механизм интерактивного
запуска, если он есть. Иначе создать разовую задачу Windows Task Scheduler для
уже вошедшего пользователя с LogonType Interactive, без пароля и повышения прав:
New-ScheduledTaskAction (профильный EXE и WorkingDirectory установки),
New-ScheduledTaskPrincipal -UserId <пользователь> -LogonType Interactive -RunLevel Limited,
Register-ScheduledTask с уникальным именем BBGL-Test-<RUN_ID>, Start-ScheduledTask.
Не добавлять автозагрузку или постоянный триггер; удалить только созданную нами
задачу после старта. Разовую задачу с видимым игровым окном не запускать от SYSTEM.
Если интерактивной сессии нет или профильного запуска нет, сообщить конкретный
блокер; не менять вход в Windows, аккаунты и не создавать профиль с чужими сейвами.

## Запуск трёх экземпляров на ПК

После успешной установки, из локальной интерактивной сессии:

```powershell
# $gameInstall уже определён для текущего устройства.
foreach ($playerNumber in 1..3) {
    Start-Process -FilePath (Join-Path $gameInstall "Bloodborne Player $playerNumber.exe") -WorkingDirectory $gameInstall
}
```

Этот пример для трёх ещё не запущенных профилей. В сетевом режиме локально запустить
только один существующий профильный EXE; на ноутбуке — его собственный профильный EXE.
Не задавать глобально BBGL_PROFILE_DIR, который смешает профили. Не пересоздавать
профильные EXE, если они уже актуальны. Если они изменились — собрать существующим
packaging/windows/build-profile-launchers.ps1 и включить в деплой.

Минимум между сборкой и игрой: exit=0 сборки → бэкап заменяемых файлов → копирование
нужной delta → запуск → один короткий снимок процессов/свежего стартового лога.
Не запускать CheckOnly перед обычным деплоем, тестовые suites, smoke-прогоны,
verify-release, аудит архива, повторную упаковку, хэши или сравнение всех файлов.
Не ждать установленных таймеров «на всякий случай». При необходимости запуска
компонента VPS выполнить только требуемое обновление и краткую проверку сервиса.
Сообщить режим, завершение доработок, собранные компоненты, устройства установки,
сколько экземпляров действительно стартовало и куда сохранены бэкапы.

## Сбор логов

```powershell
$testProfiles = @(1..3 | ForEach-Object { Join-Path $env:LOCALAPPDATA "Bloodborne Game Launcher Player $_" })
& "$skillRoot/scripts/collect-logs.ps1" -Destination (Join-Path $repoRoot 'out/coop-dev/runs/RUN_ID/pc') -SinceUtc '2026-11-02T19:00:00Z' -ProfileRoots $testProfiles -Install $gameInstall
```

RUN_ID и SinceUtc заменить реальным прогоном. Собрать каждого локального участника,
а в режиме ПК + ноут — также ноутбук за тот же интервал; проверить exit code и collection.json.
На ноутбуке передать и запустить collect-logs.ps1 с его фактическими профилями и
установкой, затем забрать каталог результата через scp в RUN_ID/laptop.
Добавить основной/другой профиль в -ProfileRoots, если он участвовал, и при
необходимости явные -GameDirs. Профиль/роль/PID сопоставлять по логам, не по
предположению, что Player 1 обязательно хост. Без -ProfileRoots скрипт уже находит
основной профиль и папки Bloodborne Game Launcher * в LocalAppData.
Сбор включает все подходящие ротации за интервал, а не только самый новый файл.

Сервер при необходимости:

```text
journalctl -u bbsc-shadnet --since 'YYYY-MM-DD HH:MM:SS UTC' --until 'YYYY-MM-DD HH:MM:SS UTC' --no-pager
journalctl -u bbsc-gameserver --since 'YYYY-MM-DD HH:MM:SS UTC' --until 'YYYY-MM-DD HH:MM:SS UTC' --no-pager
```

Зафиксировать точные интервалы: МСК = UTC+3. Ошибку SSH/доступа к журналу
отразить как отсутствующий источник. Не путать локальный час в mod log с UTC
серверного журнала. После сбора сохранять все raw logs локально, в ответе
давать короткую хронологию, доказанную причину/неопределённость и статус установки.
