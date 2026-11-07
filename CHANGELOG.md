# BBGL changelog

## 1.3.1

- Гость может запустить общие ролики у черепа Амелии и после Ром. Оба сценария подтверждены в игре, включая переход всей группы в Яаар’гул после Ром.
- Штатные триггеры Айлин и Хенрика продвигают личный квест гостя. Снимки карт и Сна исключают личные флаги и отметки подбора.
- В кооперативе сетевой пул игры увеличен с 14 до 16 МиБ. При пересоздании персонажа напарника старый получатель штатно отвязывается от очереди движения.
- Поля кооператива скрыты в офлайн-режиме, кнопка обновления перенесена на боковую панель, длинные уведомления прокручиваются под кнопкой запуска.

[Описание релиза и открытые проверки](docs/release-1.3.1.md).

## 1.3.0

- Каждый игрок может зажигать и использовать лампы, перемещаться независимо по лампам, надгробиям и алтарям и снова встречаться с группой. Сон охотника всегда личный.
- Штатная сетевая обработка NPC вместо полного сканирования памяти при подключении. Максимум HP пересчитывает игровой движок.
- У каждого свои чаши и алтари. Корневые подземелья генерируются случайно штатным способом, гости помогают проходить их и получают свои награды. Лампы общей чаши синхронизируются, прогресс первого слоя сохраняется в проверенном сценарии.
- Расширен самостоятельный доступ гостей к дверям, рычагам и лифтам, диалогам и личным подборам, магазинам, мастерской и сюжетным маршрутам.
- Сбор группы перед финалом, тихий выход в личные миры после общей концовки, штатная выдача наград боссов без дублирующей очереди.
- Исправления возрождения, пятна крови, выхода в главное меню и прыжка к Ром.
- Согласован шаг физики движущихся платформ с шагом персонажа. Исправлена гонка GPU в целевом тесте.
- Убрана настройка личного Сна. Явный уровень логов GPU заменяет унаследованные исключения классов.

[Описание релиза и открытые проверки](docs/release-1.3.0.md).

## 1.2.0, 05.11.2026

- Полное прохождение основной сюжетной игры в кооперативе и переход в NG+ подтверждены пользователем.
- Рабочие чаши в кооперативе; возвращена штатная случайная генерация корневых подземелий с общей раскладкой хоста и личными алтарями гостей.
- Двери Лекционного корпуса только для хоста, общая финальная фаза Сна, возврат погибших к лампе босса, очистка эффектов смерти, подтверждение предметов, внешний вид гостей и исключение участника без закрытия всей группы.

- P2P через LAN/VPN вместо отдельного сервера и приглашений; позднее подключение и последовательный приём гостей.
- Повторное подключение, роли колоколов, выход через меню и исключение выбранного гостя; переходы, чаши, смерть и возрождение.
- Штатная добыча и награды с личными условиями; ключи не копируются по инвентарю хоста; проверка недостающих уникальных наград и учёт одноразовых предметов/NG+.
- Обновлённые главный экран, мастер, выбор VPN и русские подписи; таблица и обмен модами, отдельные подсказки кнопок. Проверены английский и русский; исправлен перенос описаний разделов в узком окне.
- Необязательный «Алмазный меч» (выключен), открытие профиля, сохранение пресета при смене масштабирования.
- Компактный курсор с масштабом Windows, края затемнения, первый кадр и время жизни Vulkan-ресурсов FSR.
- Релизные логи Error/Critical по умолчанию, один журнал на запуск; исследовательская диагностика и читы выключены.

Подробное [описание релиза](docs/release-1.2.0.md). Новые игровые сценарии остаются частично неподтверждёнными; это подготовка релиза, не запись о публикации.

## 1.1.0, 02.11.2026

BBGL и BBSC-GL получают общий номер версии 1.1.0.

### Лаунчер
- Обновлён главный экран: расположение карточек, типографика и выбор графического пресета.
- Улучшены отмена запуска и диалог настройки брандмауэра.
- Добавлен индикатор подготовки шейдеров в окне игры.
- Исправлен повторный захват мыши после восстановления окна и возврата фокуса.
- Улучшена обработка сетевого рукопожатия и запоздавших сообщений предыдущего подключения.

### Кооперативный мод
- Подключение к хосту на другой карте использует одну загрузку; убраны дополнительные экраны подключения и устаревшие оверлеи загрузки.
- Возвращено плавное затемнение при кооперативном возрождении без перезагрузки карты — в открытом мире и после победы над боссом в режиме наблюдения. Уведомления появляются после завершения затемнения.
- Улучшены завершение сессии через игровое меню, блокировка движения при выходе и защита от лишней перезагрузки босса.
- Доработаны повторный призыв, очистка старых записей сессии и переходы в чашах.
- Обновлены оригинальные колокола и их русские/английские подсказки; устранены повторные выдачи кооперативных предметов.
- Доработаны учёт PvP-убийств, награды Blood Dreg и локальный рейтинг Vileblood.
- Уменьшена фоновая работа синхронизации прогресса и масштабирования врагов; оптимизирован поиск квестовых событий.
- Добавлена логика совместного финала в Сне охотника и перехода в следующий NG-цикл хоста с журналом восстановления прерванного финала.

### Статус проверки
Плавное затемнение при возрождении проверено C++ fixture-тестом; сборка DLL выполнена; игровая проверка этой последней правки ещё не выполнена. Совместный финал/NG+ и восстановление после прерывания требуют игрового подтверждения. Редкий отказ подключения до входа в комнату остаётся в расследовании. Покрытие больших групп и редких сценариев чаш/прогрессии продолжается. Эта запись не объявляет их исправленными.

Релизные метаданные BBGL и BBSC-GL синхронизированы на версии 1.1.0.


## Live-resolution defaults, 2026-10-31

- Hide DLSS options on non-NVIDIA RTX adapters in both launcher and game; fall back from unsupported saved selections.

- Enable live resolution by default and preserve it at 16:9 outputs above 1080p.
- Expose resolution and upscaling controls when live resolution is enabled and supported by the current session.
- Remove restart actions from the native System menu and the overlay.


## Graphics menu update, 2026-10-31

- Merge PC Graphics, Display and Effects into one native Graphics screen with scrolling.
- Remove PC Settings, PC Gameplay and Restart to Apply from the native menu; show only settings that can apply live.
- Apply LOD, chromatic aberration, DoF, motion blur, SSAO, game AA, dynamic shadows and object motion without restarting. SSR remains a startup setting in the launcher.
- Keep stable value controls when scrolling and retain the native option-screen frame.
- Add Russian menu labels, choices, help and achievement UI selected by the game language.
- Fit the System frame to seven commands and dropdown backgrounds to their choice counts.


## 1.0.0 — refreshed release, 2026-10-31

- Rename the launcher to Bloodborne Game Launcher (BBGL), repository to `bbgl`, and bundled mod fork to BBSC-GL (`bbsc-gl`).
- Extract into `Bloodborne Game Launcher`; store the writable profile in `%LOCALAPPDATA%\bbgl`, importing previous Local/Roaming profiles without overwriting existing files.
- Include the latest pinned client and server, profile storage changes and ready-to-use button packs.
- Replace the initial test 1.0.0 package. This is still version 1.0.0; existing 1.0.0 installs need a manual download.
- Rewrite player documentation and explain upstream attribution and fork architecture. Gameplay limitations remain tracked in BBSC-GL.


## 1.0.0

- First version of the mark3317 launcher distribution.
- BBSC fork pinned as a Git submodule and bundled with its matching client and server.
- Removed the official BBSC download / DLL override installation sequence.
- Built-in Xbox and PCBButtons texture patches.
- BBSC gameplay settings alongside existing one-hit kill and other gameplay patches.
- Updates use mark3317/bbgl stable releases.
- Removed optional Discord Rich Presence packaging and Hunter's Atlas distribution.
- English / Russian getting-started documentation, release checks and development branch.

Gameplay validation of this packaging change is separate from the existing BBSC test history; see the release notes for the actual checks performed.
