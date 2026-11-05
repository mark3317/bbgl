# BBGL 1.2.0

**English** · [Русский](#русский)

## English

This release updates co-op, the interface and mod management since BBGL 1.1.0.

### Complete playthrough and Chalice Dungeons

**The entire main story has been tested as a co-op playthrough.** You can play the main campaign with friends through the finale and continue into **NG+**. A complete playthrough and the transition to the next cycle have been confirmed through gameplay by the user. Co-op covers story transitions, bosses and the finale, while each player's NPC quests, personal items and own world are tracked separately.

**Chalice Dungeons work in co-op, and random generation has been restored for Root Chalices.** The game itself generates the dungeon layout when a ritual is performed. Guests load the same generated chalice and explore it with the host. Support extends beyond fixed story dungeons: different rituals and layouts remain distinct even when they share an internal map number. Created dungeon data persists between launches, while guests retain their own altars and individual progress. Guests do not need to create a matching chalice before joining the host.

### Co-op

- Co-op runs over a LAN or VPN. Built-in P2P replaces the separate server and invite codes. Choose Local network, Tailscale or Radmin; the launcher shows available connections and helps install a missing VPN.
- Players can join an already running game. Everyone no longer needs to launch before the bells are used. Party discovery, sequential guest admission and player-name display have been improved.
- Reconnecting, switching bell roles, removing a selected player and ending a session have been improved. Area transitions, following the host and guest placement when entering a chalice have also been refined.
- Death, revival and the end of boss fights have been reworked, including guest status and poison cleanup, return lamps and Hunter's Dream transitions.
- Personal quest items, keys, badges and tools come from each player's own game interactions. Items are no longer granted by copying the host's inventory.
- Enemy loot, reviewed scripted items and boss rewards use the game's native delivery. Missing unique base-game, DLC and chalice rewards are checked after loading into the host's world; tracking of personal one-time rewards and NG+ has been improved.

### Smaller co-op fixes

- **Only the host can activate the Lecture Building's transition doors.** The exits to the Nightmare Frontier and Nightmare of Mensis no longer start a separate guest transition in response to the host's action. Guests travel with the party through host-following, addressing a cause of premature and repeated loading.
- **The final Hunter's Dream phase follows shared story progress.** After Mergo's Wet Nurse is defeated, guests see the corresponding Dream phase while keeping their personal workshop, shop and NPC services. The host retains control of the final choice in Gehrman's dialogue.
- **Return after a boss victory.** Fallen players are returned to the defeated boss's lamp when a usable return point exists. Bosses without a separate lamp and unresolved destinations keep the usual fallback.
- **Status cleanup after death.** Poison and other effects, status buildup and detection of subsequent deaths after revival without a map reload have been improved.
- **Item confirmation.** Fixed a blocker preventing the native confirmation button from appearing in reward and key-item notifications for a living guest.
- **Guest appearance.** Removed the persistent blue summon glow in the host's world while retaining search and arrival effects. Added correction for player models stuck invisible after transitions or death.
- **Removing one player keeps the rest of the party together.** Silencing Blank handling distinguishes a selected player's removal from closing the entire session and accounts for characters temporarily disappearing during loading.
- **A disconnected or crashed participant.** Improved isolation of a failing connection so it does not stop communication between the remaining players. Guests return to their own worlds if the host is lost; host migration is not implemented.
- **Chalice entry and guest placement.** Fixed ritual preparation when map numbers match and refined host-position delivery and placement order after loading.
- **Personal keys and NPC rewards.** Personal item prerequisites are preserved; the guest's Firing Hammer Badge award condition has been corrected. Previously obtained one-time items are tracked separately from shared story progress.
- **Co-op items in the Dream.** Removed duplicate original pickup locations for the co-op kit and outdated bell hints by the stairs. Receiving the kit through the Notebook is preserved.

### Launcher and visuals

- Updated the home screen, first-run wizard, network settings and Russian labels. Long mod names and category descriptions wrap, with rows adjusting their height, including English text at the minimum window width.
- Mods are shown in one table with load order, toggles, comparison against network participants and missing-mod downloads. A mismatch warning appears before launch.
- PlayStation, Xbox and keyboard prompts are selected separately from gameplay mods and no longer trigger false mod-mismatch warnings.
- Bundled the optional **Diamond Sword** mod, disabled by default. Its in-game purchase price is **10,000 Blood Echoes**. Files are reconstructed from the player's own game data; original game archives are not redistributed.
- Added a profile-folder button. Changing upscaling or frame generation preserves the selected graphics preset.
- Updated the in-game menu cursor with Windows scaling support. Fixed fade edges and window covering until the first game frame is ready.
- Included Vulkan resource-lifetime fixes for FSR frame generation.

### Defaults and logs

Detailed diagnostics, research logs, GPU profiling, Vulkan validation and cheats are disabled by default. Errors and crash output are saved in a separate `run_YYYYMMDD_HHMMSS.log` for each launch. Normal co-op does not enable detailed logging. Existing user settings are preserved.

### Installation and limitations

Extract `bbgl-1.2.0-windows-x64.zip`, run `Bloodborne.exe` and select your own CUSA03173 game with update 1.09. For co-op, update all participants to the same version and connect them to the same VPN or LAN. Preserve your profile and user mods when updating. Game files and saves are not included in the archive.

A complete main-story co-op playthrough and transition to NG+ have been confirmed by the user. This does not establish coverage of every additional rite, random chalice layout, party composition or reward edge case. Broader testing continues for groups of three or more, uncommon chalice transitions, loot when deaths occur simultaneously and duplicate rewards after reconnecting or changing NG cycles. The smaller fixes listed above have targeted checks; separate gameplay confirmation is not claimed for every individual fix. Host migration is not implemented.

Based on yharnam-pc / bbport and Bloodborne Seamless Co-op by CLS_AMG and contributors. Component credits and licences are preserved.

---

## Русский

[English](#english)

Обновление кооператива, интерфейса и работы с модами после BBGL 1.1.0.

### Полное прохождение и чаши

**Основная сюжетная игра полностью проверена на прохождение в кооперативе.** Можно пройти основную кампанию вместе с друзьями до финала и перейти в **NG+**: работоспособность полного прохождения и перехода в следующий цикл подтверждена пользователем. Совместная игра охватывает сюжетные переходы, боссов и финал; при этом личные квесты NPC, предметы и собственный мир каждого участника учитываются отдельно.

**Чаши работают в кооперативе, а корневым чашам возвращена случайная генерация.** При создании ритуала раскладку подземелья формирует сама игра. Гости загружают ту же сгенерированную чашу и исследуют её вместе с хостом. Поддержка не ограничивается фиксированными сюжетными подземельями: разные ритуалы и раскладки различаются даже при одинаковом внутреннем номере карты. Данные созданных чаш сохраняются между запусками, а личные алтари и прогресс гостей сохраняют самостоятельность. При входе в чашу хоста не требуется заранее создавать её копию у себя.

### Совместная игра

- Кооператив работает через локальную сеть или VPN: встроенный P2P заменяет отдельный сервер и коды приглашения. Выберите локальную сеть, Tailscale или Radmin; лаунчер показывает доступные подключения и помогает установить отсутствующий VPN.
- Добавлено подключение к уже запущенной игре. Больше не требуется запускать всех участников до использования колоколов. Доработаны поиск группы, последовательный приём гостей и отображение имён игроков.
- Улучшены повторное подключение, смена роли колоколов, исключение выбранного участника и завершение сессии. Доработаны переходы между картами, следование за хостом и размещение гостя при входе в чашу.
- Переработаны смерть, возрождение и завершение боя с боссом: очистка состояний, яда и эффектов гостей, возврат к лампе и переходы в Сне охотника.
- Личные квесты, ключи, значки и инструменты получают собственным игровым способом. Предметы больше не выдаются по инвентарю хоста.
- Добыча врагов, проверенные скриптовые предметы и награды боссов используют штатную выдачу игры. Добавлена проверка недостающих уникальных наград основной игры, DLC и чаш после загрузки к хосту; доработан учёт личных одноразовых наград и NG+.

### Небольшие исправления кооператива

- **Двери-переходы в Лекционном корпусе открывает только хост.** Выходы в Границу Кошмара и Кошмар Менсиса больше не запускают у гостя самостоятельный переход вслед за действием хоста. Гость переходит вместе с группой через следование за хостом; устранён источник преждевременной загрузки и повторного перехода.
- **Финальная стадия Сна охотника согласована с общим сюжетом.** После победы над Кормилицей Мерго гости видят соответствующую фазу Сна, сохраняя личные услуги мастерской, магазинов и NPC. Финальный выбор в разговоре с Германом остаётся за хостом.
- **Возвращение после победы над боссом.** Для погибшего участника приоритет отдаётся лампе побеждённого босса, если у него есть доступная точка возвращения. Для боссов без отдельной лампы и неразрешимых точек сохраняется обычный вариант возврата.
- **Состояния после смерти.** Доработаны очистка яда и других эффектов, сброс накопления состояний и повторная обработка смерти после возрождения без перезагрузки карты.
- **Подтверждение получения предметов.** Исправлена блокировка штатной кнопки подтверждения в уведомлениях о наградах и ключевых предметах у живого гостя.
- **Внешний вид гостей.** Убрано постоянное синее свечение призванного охотника в мире хоста; эффекты поиска и появления сохранены. Добавлена коррекция зависшей невидимости модели участника после переходов и смерти.
- **Исключение одного игрока сохраняет остальную группу.** Обработчик Бланка молчания отличает выбранное исключение от завершения всей сессии и учитывает временное отсутствие персонажей во время загрузки.
- **Отключение или сбой одного участника.** Доработана изоляция проблемного соединения, чтобы оно не останавливало обмен остальных игроков. При потере хоста гости возвращаются в собственный мир; передачи роли хоста другому игроку нет.
- **Вход в чашу и размещение гостя.** Исправлена подготовка ритуала при совпадающем номере карты, доработаны передача позиции хоста и порядок размещения после загрузки.
- **Личные ключи и награды NPC.** Сохранены личные условия получения предметов; исправлено условие выдачи значка Пылающего молота гостю. Уже полученные одноразовые предметы учитываются отдельно от общего сюжетного прогресса.
- **Кооперативные предметы в Сне.** Убраны дублирующие оригинальные места получения набора и устаревшие подсказки о колоколах у лестницы. Получение набора через Блокнот сохранено.

### Лаунчер и изображение

- Обновлены главный экран, мастер первого запуска, сетевые настройки и русские подписи. Длинные названия модов и описания разделов переносятся, строки подстраиваются по высоте — в том числе в английском интерфейсе при минимальной ширине окна.
- Моды представлены общей таблицей: порядок загрузки, включение, сравнение с участниками сети и загрузка недостающих модов. Перед запуском появляется предупреждение о несовпадениях.
- Значки PlayStation, Xbox и клавиатуры выбираются отдельно от игровых модов и не вызывают ложных предупреждений о разных наборах модификаций.
- Добавлен отключённый по умолчанию мод «Алмазный меч». Покупка в игре — 10 000 отголосков крови. Файлы восстанавливаются из собственных данных игры; оригинальные архивы не распространяются.
- Добавлена кнопка открытия папки профиля. Смена масштабирования и генерации кадров сохраняет выбранный графический пресет.
- Обновлён курсор игровых меню, учтён масштаб Windows. Исправлены края затемнения и прикрытие окна до готовности первого игрового кадра.
- Включены исправления времени жизни ресурсов Vulkan при генерации кадров FSR.

### Настройки и журналы

Подробная диагностика, исследовательские логи, GPU-профилирование, Vulkan validation и читы выключены по умолчанию. Ошибки и аварийный вывод сохраняются в отдельный журнал каждого запуска `run_YYYYMMDD_HHMMSS.log`. Обычный кооператив не включает расширенное логирование. Ранее сохранённые пользовательские настройки сохраняются.

### Установка и ограничения

Распакуйте `bbgl-1.2.0-windows-x64.zip`, запустите `Bloodborne.exe` и выберите свою игру CUSA03173 с обновлением 1.09. Для совместной игры обновите всех участников до одной версии и подключите их к одной VPN или локальной сети. При обновлении сохраняйте свой профиль и пользовательские моды. Файлы игры и сохранения в архив не входят.

Полное прохождение основной сюжетной игры в кооперативе и переход в NG+ подтверждены пользователем. Это не означает проверки всех дополнительных обрядов и вариантов случайных чаш, всех составов группы или каждого редкого случая выдачи наград. Расширенная проверка продолжается для групп из трёх и более игроков, редких переходов чаш, добычи при одновременной смерти и повторов наград после переподключения или смены NG-цикла. Для перечисленных небольших исправлений выполнены целевые проверки; отдельное игровое подтверждение каждого из них не заявляется. Миграция хоста не реализована.

Основа проекта — yharnam-pc / bbport и Bloodborne Seamless Co-op от CLS_AMG и участников проекта. Авторство и лицензии компонентов сохранены.
