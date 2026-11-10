# SPDX-License-Identifier: GPL-2.0-or-later
"""Russian texts of the Qt Quick launcher (bbport_launcher_qml.py, launcher/qml).

The English text is the key: QML shows launcher.tr("English"), the backend passes its labels,
hints, notices and statuses through tr(). Texts made with values ("... {} ...") are matched by
PATTERNS; the values themselves are translated too when they are texts of this table.
The classic Tk launcher keeps its own table (bbport_i18n.py).
"""
import re

RU = {
    "Pick up the Notebook from the messengers in the Hunter's Dream to receive the co-op items automatically.": 'Заберите Блокнот у посланников в Сне охотника — предметы для совместной игры выдадутся автоматически.',
    'Download': 'Скачать',
    'Mod folders': 'Папки модов',
    'No installed mods': 'У игрока нет установленных модов',
    'Mods on the network': 'Моды в сети',
    'A mod with this name is already installed': 'Мод с таким именем уже установлен.',
    'Mod changed; wait for the list to update': 'Мод изменился. Дождитесь обновления списка.',
    'Mod sharing unavailable': 'У этого игрока обмен модами недоступен.',
    'Mod transfer busy': 'Игрок уже передаёт моды. Попробуйте ещё раз позже.',
    'Mod no longer available': 'Мод больше недоступен.',
    'Mod download interrupted': 'Соединение прервалось. Повторите скачивание.',
    'Downloaded mod does not match its catalog': 'Скачанные файлы не совпадают с заявленным содержимым мода.',
    'Mod is too large': 'Размер мода превышает ограничение в 8 ГБ.',
    'Mod archive is too large': 'Архив мода превышает допустимый размер или количество файлов.',
    'Invalid mod catalog': 'Игрок передал некорректный список модов.',
    'Invalid mod response': 'Игрок передал некорректный ответ.',
    'Invalid mod size': 'Игрок передал некорректный размер мода.',
    'Invalid mod name': 'Недопустимое имя мода или файла.',
    'Invalid archive path': 'В архиве обнаружен недопустимый путь.',
    'Invalid archive entry': 'В архиве обнаружены ссылки или повторяющиеся пути.',
    'The mod list updates automatically. Changes apply at the next game start. Lower mods override earlier ones.': 'Список обновляется автоматически. Изменения применятся при следующем запуске игры. Моды ниже в списке имеют приоритет.',
    'No mods yet. Put each mod in its own folder or download one from a player below.': 'Модов пока нет. Положите каждый мод в отдельную папку или скачайте его у игрока ниже.',
    'Mods from players on your selected co-op network': 'Моды игроков в выбранной сети кооператива',
    'Waiting for players with mod sharing. Open the updated launcher on both computers and select the same network in Co-op.': 'Ожидание игроков с обменом модами. Откройте обновлённый лаунчер на обоих компьютерах и выберите общую сеть в разделе «Кооператив».',
    'Downloading mods… Please wait.': 'Загружаем моды… Подождите.',
    'Not installed': 'Не установлен',
    'Different contents — existing files will be kept': 'Содержимое отличается — установленные файлы будут сохранены',
    'Installed, matching contents': 'Установлен, содержимое совпадает',
    'Download mod': 'Скачать мод',
    "Use this player's mod set": 'Применить набор этого игрока',
    'Mod synchronization complete.': 'Набор модов синхронизирован.',
    'Mod downloaded (disabled).': 'Мод скачан и пока выключен.',
    'Mod download failed:': 'Не удалось скачать мод:',
    'Different mod contents:': 'Содержимое мода отличается:',
    'Wait for mod synchronization to finish.': 'Дождитесь окончания синхронизации модов.',
    'Player name must be 3–16 Latin letters, numbers, - or _.': 'Имя игрока должно содержать от 3 до 16 латинских букв, цифр, знаков - или _.',
    'Players must use different names. Change the player name and refresh.': 'Имена игроков должны различаться. Измените имя игрока и обновите подключение.',
    'Detailed diagnostic logs': 'Подробные логи диагностики',
    'Detailed GPU logs': 'Подробные логи GPU',
    'Record co-op events, mod warnings and errors in the game log. GPU errors are included.': 'Записывает события коопа, предупреждения мода и ошибки, включая ошибки GPU.',
    'Current profile:': 'Текущий профиль:',
    'Open profile': 'Открыть профиль',
    'Profile folder': 'Папка профиля',
    'Open a separate launcher with settings and co-op data in this folder. New folders start with a fresh profile. The current window keeps its profile.': 'Открывает отдельный лаунчер с настройками и данными коопа в этой папке. В новой папке создаётся чистый профиль. Текущее окно сохраняет свой профиль.',
    'Choose an absolute profile folder path.': 'Укажите абсолютный путь к папке профиля.',
    'Could not open profile: {}': 'Не удалось открыть профиль: {}',
    'A separate launcher was opened with the selected profile.': 'Открыт отдельный лаунчер с выбранным профилем.',
    ' of 5': ' из 5',

    'Enter your co-op name, password and server invite code. You can skip this step for offline play and return to Settings → Co-op later.': 'Укажите ник, пароль и код приглашения сервера для совместной игры. Для офлайн-игры этот шаг можно пропустить и вернуться к нему позже в настройках коопа.',

    'Insert or L3+R3 opens the guide in game': 'Во время игры Insert или L3+R3 открывает меню.',
    'In the game, Insert or L3+R3 opens the guide. Setup can be run again from Game & Saves.': 'Во время игры Insert или L3+R3 открывает меню. Мастер настройки можно повторно открыть в разделе «Игра и сохранения».',
    'Game installed.': 'Игра установлена.',
    'The game folder already exists. Choose it using the folder button.': 'Папка game уже существует. Укажите её кнопкой выбора папки.',
    'Installation cancelled. Downloaded parts are kept for the next attempt.': 'Установка отменена. Скачанные части сохранены для следующей попытки.',
    'Another game installation is already running.': 'Установка игры уже выполняется другим лаунчером.',
    'Downloaded ZIP checksum does not match. Please retry.': 'Контрольная сумма ZIP не совпала. Повторите загрузку.',

    'Download game': 'Скачать игру',
    'Cancel download': 'Отменить загрузку',
    'Preparing download…': 'Подготовка загрузки…',
    'Downloads into the game folder beside the launcher. Verified ZIP parts are reused when you retry.': 'Игра будет установлена в папку game рядом с лаунчером. При повторной попытке проверенные ZIP-части используются повторно.',

    "Removes the summoned guest's 30% max HP cut": 'Убирает снижение максимального здоровья призванного гостя на 30%.',
    'A kept death still drops a bloodstain and echoes': 'После смерти отголоски крови остаются на месте гибели; их можно вернуть.',
    'The bell costs no Insight': 'Использование колокола не расходует озарение.',
    "Enemies and bosses get stronger for every guest (replaces the game's own boss buff)": 'Враги и боссы становятся сильнее за каждого гостя. Заменяет стандартное усиление боссов.',
    'Henryk, Djura and the other hostile hunters also get the enemy scaling (off = vanilla)': 'Усиление также применяется к Генрику, Джуре и другим враждебным охотникам.',
    'Extra health for normal enemies, per guest': 'Дополнительное здоровье обычных врагов за каждого гостя.',
    'Extra health for bosses, per guest': 'Дополнительное здоровье боссов за каждого гостя.',
    'Extra damage for enemies and bosses, per guest': 'Дополнительный урон врагов и боссов за каждого гостя.',
    'Harder to stagger normal enemies, per guest': 'Дополнительная устойчивость обычных врагов к ошеломлению за каждого гостя.',
    'Harder to stagger bosses, per guest': 'Дополнительная устойчивость боссов к ошеломлению за каждого гостя.',
    "When a guest goes home, bosses, shortcuts, doors and lamps the host has done are added to the guest's own world (adds only, never removes; NPC quests and your character are not touched; saves backed up first)": 'После возвращения гостя домой прогресс боссов, проходов и фонарей хоста добавляется к его миру. Открытые двери также переносятся. Прогресс только добавляется; квесты NPC и персонаж не меняются. Сначала создаётся копия сохранения.',
    'Extra logs for the developers (key item census, item hooks, every flag in a session). Off = faster': 'Подробные журналы для диагностики. По умолчанию выключены.',
    'Enter a whole number within the setting range.': 'Введите целое число в допустимом диапазоне.',
    'Which buttons the game shows, from the next start. Xbox (by Dommo) and Keyboard (PCBButtons by JinkiJinn) are bundled. Select your game folder, then choose the buttons; no separate download is needed. Keyboard also binds the keys its images show: E interact, Left Shift dodge, R blood vial, Q item, F transform, mouse buttons to attack.': 'Значки кнопок меняются после перезапуска игры. Xbox от Dommo и PCBButtons от JinkiJinn уже включены: выберите папку игры и нужный набор. Клавиатура также настраивает соответствующие клавиши: E — действие, Shift — уклонение, R — флакон, Q — предмет, F — трансформация, кнопки мыши — атаки.',
    'Experimental. This launcher includes the BBSC-GL fork: one session through deaths, lamps, areas and bosses, each hunter keeping their own character. Play on a co-op server (an invite code, or the one this launcher comes with), or host one on your PC for friends on Tailscale or your home network. BBSC-GL client and hosting files are included and ready to use. Your saves are backed up before every session. Normal play and online are unchanged.': 'Экспериментальный кооператив на основе форка BBSC-GL: одна сессия через смерти, фонари, области и боссов. Каждый сохраняет своего персонажа. Подключитесь по коду приглашения или создайте сервер на своём ПК. BBSC-GL включён в комплект и не требует отдельной загрузки. Перед каждой сессией создаётся копия сохранений.',

    'Prepare bundled BBSC': 'Подготовить встроенный BBSC',
    'Preparing bundled co-op…': 'Подготовка встроенного коопа…',
    'Co-op gameplay': 'Настройки кооператива',
    'No guest HP cut': 'Без снижения здоровья гостя',
    'Bloodstain on death': 'Пятно крови после смерти',
    'Free Beckoning Bell': 'Колокол без расхода озарения',
    'Enemy scaling': 'Усиление врагов',
    'Scale NPC hunters': 'Усиление NPC-охотников',
    'Enemy HP per guest (%)': 'Здоровье врагов за гостя (%)',
    'Boss HP per guest (%)': 'Здоровье боссов за гостя (%)',
    'Enemy damage per guest (%)': 'Урон врагов за гостя (%)',
    'Enemy stagger resistance per guest (%)': 'Устойчивость врагов за гостя (%)',
    'Boss stagger resistance per guest (%)': 'Устойчивость боссов за гостя (%)',
    'Shared progress': 'Общий прогресс',
    'Research logs': 'Подробные диагностические логи',
    'Bundled BBSC is ready to prepare. Play co-op installs it automatically.': 'BBSC-GL включён в комплект. При запуске коопа он будет подготовлен автоматически.',

    # --- Home, rail, splash -------------------------------------------------------------------
    'Default location': 'Папка по умолчанию',
    'Browse': 'Обзор',
    'The hunt is underway': 'Охота идёт',
    'Preparing game files': 'Подготовка файлов игры',
    'Game files needed': 'Нужны файлы игры',
    'Saves need attention': 'Сохранения требуют внимания',
    'Co-op needs setting up': 'Нужно настроить совместную игру',
    'Sign in to play online': 'Войдите, чтобы играть онлайн',
    'Ready to hunt': 'Готов к охоте',
    'Ready to hunt.': 'Готов к охоте.',
    'The saves folder cannot be written. Choose another one.':
        'В папку сохранений нельзя записывать. Выберите другую.',
    'LAUNCHER': 'ЛАУНЧЕР',
    'Running': 'Запущена',
    'Needs attention': 'Требует внимания',
    'Ready': 'Готово',
    'Game running': 'Игра запущена',
    'Installing…': 'Установка…',
    'Set up game files': 'Настроить файлы игры',
    'Choose a saves folder': 'Выбрать папку сохранений',
    'Set up co-op': 'Настроить совместную игру',
    'Play co-op': 'Играть вместе',
    'Play online': 'Играть онлайн',
    'Play offline': 'Играть офлайн',
    'Stop': 'Остановить',
    'Offline': 'Офлайн',
    'Online · Seamless co-op': 'Совместная игра',
    'A new version is ready': 'Готова новая версия',
    'Install': 'Установить',
    'Graphics': 'Графика',
    'Custom': 'Свой',
    ' preset': ' (пресет)',
    'Visuals': 'Изображение',
    'Controls': 'Управление',
    ' prompts': ' (подсказки)',
    'Button prompts': 'Подсказки кнопок',
    'Control icons': 'Иконки управления',
    'Game files & saves': 'Файлы игры и сохранения',
    'Game & Saves': 'Игра и сохранения',
    'Your data': 'Ваши данные',
    'Game files': 'Файлы игры',
    'Mods & patches': 'Моды и патчи',
    'None enabled': 'Не включены',
    ' mod enabled': ' мод включён',
    ' mods enabled': ' мод. включено',
    'Mods & Patches': 'Моды и патчи',
    'Installed mods': 'Установленные моды',
    'Home': 'Главная',
    'Game files need attention': 'Файлы игры требуют внимания',
    'Ready to play': 'Можно играть',
    'Bloodborne is running.': 'Bloodborne запущена.',
    'Installation is in progress.': 'Идёт установка.',
    'Choose a writable saves folder.': 'Выберите папку сохранений, доступную для записи.',
    'Everything required is ready.': 'Всё необходимое готово.',
    'Setup': 'Настройка',
    'Settings': 'Настройки',
    'Log': 'Журнал',
    'System': 'Система',
    'Logs': 'Журналы',
    'Game': 'Игра',
    'Play': 'Играть',
    'Bloodborne starts in ': 'Bloodborne запустится через ',
    'Launching Bloodborne…': 'Запуск Bloodborne…',
    'Bloodborne — Windows': 'Bloodborne — Windows',

    # --- Settings workspace -------------------------------------------------------------------
    'Graphics, display & frame rate': 'Графика, экран и FPS',
    'Prompts, mouse & keyboard': 'Подсказки, мышь и клавиатура',
    'Game files, saves & language': 'Файлы, сохранения, язык',
    'Online': 'Онлайн',
    'Co-op': 'Совместная игра',
    'Seamless co-op: host or join': 'Создать или присоединиться',
    'Mods, enhancements & tweaks': 'Моды, улучшения и настройки',
    'Startup, updates & diagnostics': 'Запуск, обновления, журнал',
    'SETTINGS': 'НАСТРОЙКИ',
    'Find a setting': 'Найти настройку',
    'Changes save as you make them. Some take effect the next time the game starts.':
        'Изменения сохраняются сразу. Некоторые вступят в силу при следующем запуске игры.',
    'Results': 'Результаты',
    'Nothing matches “': 'Ничего не найдено по запросу «',
    'Preset': 'Пресет',
    'Recommended': 'Рекомендуется',
    '  ★ Suggested for ': '  ★ Рекомендуется для ',
    'Keyboard': 'Клавиатура',
    'Which buttons the game shows, from the next start. Xbox (by Dommo) and Keyboard (PCBButtons by JinkiJinn) '
    'are mods from Nexus Mods, not part of the launcher: the first time you choose one, its Nexus page opens and '
    'you pick the file you downloaded (.zip, .7z or .rar). Keyboard also binds the keys its images show: E '
    'interact, Left Shift dodge, R blood vial, Q item, F transform, mouse buttons to attack.':
        'Какие кнопки показывает игра (со следующего запуска). Xbox (от Dommo) и Клавиатура (PCBButtons от '
        'JinkiJinn) — моды с Nexus Mods, они не входят в лаунчер: при первом выборе откроется их страница на '
        'Nexus, затем выберите скачанный файл (.zip, .7z или .rar). Клавиатура также назначает клавиши с её '
        'картинок: E — действие, Левый Shift — уклонение, R — флакон крови, Q — предмет, F — трансформация, '
        'кнопки мыши — атака.',
    'Upscaling': 'Масштабирование',
    'Download FSR 4 assets': 'Скачать ресурсы FSR 4',
    'Check again': 'Проверить снова',
    'Setup wizard': 'Мастер настройки',
    'Open saves folder': 'Открыть папку сохранений',
    'Copy code': 'Скопировать код',
    'Sign in again': 'Войти снова',
    'Cancel': 'Отмена',
    'Sign out': 'Выйти',
    'Test connection': 'Проверить соединение',
    'Seamless co-op': 'Бесшовная совместная игра',
    'Experimental. Seamless co-op is BBSC by CLS_AMG (Bloodborne Seamless Co-op): one session through deaths, '
    'lamps, areas and bosses, each hunter keeping their own character. Play on a co-op server (an invite code, '
    'or the one this launcher comes with), or host one on your PC for friends on Tailscale or your home network. '
    'Set up / update BBSC installs the newest BBSC release. Your saves are backed up before every session. '
    'Normal play and online are unchanged.':
        'Экспериментально. Бесшовная совместная игра — это BBSC от CLS_AMG (Bloodborne Seamless Co-op): одна '
        'сессия через смерти, лампы, локации и боссов, у каждого охотника свой персонаж. Играйте на сервере '
        'совместной игры (по коду приглашения или на сервере, который идёт с этим лаунчером) или создайте сервер '
        'на своём ПК для друзей в Tailscale или вашей домашней сети. «Установить / обновить BBSC» ставит новейший '
        'релиз BBSC. Перед каждой сессией делается копия сохранений. Обычная игра и онлайн не меняются.',
    'Host a session': 'Создать сессию',
    'Join a host': 'Присоединиться к хосту',
    'Set up / update BBSC': 'Установить / обновить BBSC',
    'BBSC from ZIP': 'BBSC из ZIP',
    'About BBSC': 'О BBSC',
    "Starts BBSC's two servers on this PC (the first time, Windows asks once to open the firewall for Tailscale "
    "and your home network only). After Play, the launcher window closes; the servers stay active until you exit the game.":
        'Запускает два сервера BBSC на этом ПК (в первый раз Windows один раз попросит открыть брандмауэр — '
        'только для Tailscale и вашей домашней сети). После запуска игры окно лаунчера закроется; серверы будут работать до выхода из игры.',
    'Restart hosting': 'Перезапустить сервер',
    'Start hosting': 'Запустить сервер',
    'Copy invite code': 'Скопировать код приглашения',
    'Stop hosting': 'Остановить сервер',
    'Paste the invite code from your host, then Play co-op. The host rings the Beckoning Bell; you ring the Small Resonant Bell.':
        'Вставьте код приглашения от хоста и нажмите «Играть вместе». Хост звонит в Зовущий Колокол, вы — в '
        'Малый звонкий колокол.',
    'Gameplay patches': 'Патчи геймплея',
    'Optional gameplay changes. All are off by default and apply the next time the game starts.':
        'Необязательные изменения геймплея. По умолчанию все выключены, применяются при следующем запуске игры.',
    'No mods in the mods folder yet. Put each mod in its own folder there, then refresh.':
        'В папке модов пока пусто. Положите каждый мод в отдельную папку и обновите список.',
    'Refresh': 'Обновить',
    'Open mods folder': 'Открыть папку модов',
    'External patches': 'Внешние патчи',
    'Launch': 'Запуск',
    'Close the launcher after Play': 'Закрывать лаунчер после запуска игры',
    'Desktop shortcut': 'Ярлык на рабочем столе',
    'Add to Steam': 'Добавить в Steam',
    'Updates': 'Обновления',
    'Check for updates': 'Проверять обновления',
    'Checks when the launcher opens and shows available updates here and on Home.':
        'Проверяет обновления при открытии лаунчера и показывает результат здесь и на главной странице.',
    'Install the new version': 'Установить новую версию',
    'Check now': 'Проверить сейчас',
    'Releases ↗': 'Релизы ↗',
    'Maintenance': 'Обслуживание',
    'Open port folder': 'Открыть папку порта',
    'Open bbport.ini': 'Открыть bbport.ini',
    'Clear shader cache': 'Очистить кэш шейдеров',
    'Copy log': 'Скопировать журнал',
    'Clear log': 'Очистить журнал',

    # --- Setup wizard -------------------------------------------------------------------------
    'Skip setup?': 'Пропустить настройку?',
    'Any missing game files or unwritable saves will still block Play. You can finish setup later in Game & '
    'Saves.\n\nSkip setup anyway?':
        'Без файлов игры или доступной для записи папки сохранений играть не получится. Закончить настройку '
        'можно позже в разделе «Игра и сохранения».\n\nВсё равно пропустить?',
    'FIRST-TIME SETUP': 'ПЕРВАЯ НАСТРОЙКА',
    'Step ': 'Шаг ',
    ' of 4': ' из 4',
    'Welcome to Yharnam': 'Добро пожаловать в Ярнам',
    'Performance': 'Производительность',
    'Quality': 'Качество',
    'Maximum': 'Максимум',
    'Custom settings': 'Свои настройки',
    'Your hunt begins here.': 'Здесь начинается ваша охота.',
    'This wizard will help you choose game and saves folders, set up co-op, and choose control icons and graphics settings.': 'Мастер поможет выбрать папки игры и сохранений, настроить совместную игру, иконки управления и графику.',
    'Co-op is optional. You can change all settings later in the launcher.': 'Совместную игру можно настроить позже. Все параметры доступны в настройках лаунчера.',
    'Add your game files': 'Добавьте файлы игры',
    'Welcome': 'Начало',
    'Finish': 'Готово',
    'This guide sets up your own copy of Bloodborne, checks the trophy pack and keeps your saves in the right '
    'place. It takes about two minutes.':
        'Этот мастер настроит вашу копию Bloodborne, проверит пакет трофеев и разместит сохранения в нужном '
        'месте. Это займёт около двух минут.',
    'The game files and trophy key are not included in this download. You can skip setup and use the launcher '
    'straight away.':
        'Файлы игры и ключ трофеев не входят в эту загрузку. Можно пропустить настройку и сразу пользоваться '
        'лаунчером.',
    'Choose how to add Bloodborne 1.09. The installer creates a new game folder and never replaces an existing one.':
        'Выберите, как добавить Bloodborne 1.09. Установщик создаёт новую папку игры и никогда не заменяет '
        'существующую.',
    'Choose a game folder': 'Выбрать папку игры',
    "A writable saves folder is required to play. Trophy keys are optional and add trophy names. Saves stay in the "
    "launcher's own user folder unless you choose another.":
        'Для игры нужна папка сохранений, доступная для записи. Ключи трофеев необязательны и добавляют названия '
        'трофеев. Сохранения лежат в папке user лаунчера, если вы не выберете другую.',
    'Trophies': 'Трофеи',
    'The launcher uses its built-in catalogue for trophy names and descriptions.':
        'Названия и описания трофеев загружены из встроенного каталога лаунчера.',
    '%1 of %2': '%1 из %2',
    '%1 earned': 'Получено: %1',
    'Progress unavailable': 'Прогресс недоступен',
    'Secret trophy': 'Скрытый трофей',
    'Trophy #%1': 'Трофей №%1',
    'Earned': 'Получен',
    'Not earned': 'Не получен',
    'Trophy notifications': 'Уведомления о трофеях',
    'Notification volume and appearance': 'Громкость и оформление уведомлений',
    'The launcher and in-game overlay share these settings for the current save profile.':
        'Лаунчер и игровой оверлей используют эти настройки для текущего профиля сохранений.',
    'Appearance': 'Оформление',
    'Notification style': 'Вид уведомления',
    'Card': 'Карточка',
    'Corner popup': 'В углу',
    'Platinum light': 'Свечение платины',
    'Animate the platinum': 'Анимация платины',
    'Write the grade': 'Показывать тип трофея',
    'Sound and timing': 'Звук и время',
    'Mute the sound': 'Без звука',
    'Volume': 'Громкость',
    'Time on screen': 'Время на экране',
    'Theme default': 'По умолчанию',
    '%1 s': '%1 с',
    'Preview': 'Предпросмотр',
    'Bronze': 'Бронза',
    'Silver': 'Серебро',
    'Gold': 'Золото',
    'Platinum': 'Платина',
    'Trophy unlocked!': 'Трофей получен!',
    "Hunter's trophy": 'Трофей охотника',
    'All four in a row': 'Все по очереди',
    'Three at once': 'Три сразу',
    'Visual preview. The game uses the selected sound and volume.':
        'Предпросмотр показывает оформление. Звук и громкость применяются в игре.',
    'Custom sounds and pictures': 'Пользовательские звуки и изображения',
    "Files in the save profile's custom_trophy folder are loaded by the game.":
        'Игра загружает файлы из папки custom_trophy выбранного профиля.',
    'No custom sound files found.': 'Пользовательские звуки не найдены.',
    'Refresh sound files': 'Обновить список звуков',
    'Close the game using this profile to edit trophy notifications.':
        'Закройте игру в этом профиле, чтобы изменить уведомления о трофеях.',
    'Could not read trophy notification settings.': 'Не удалось прочитать настройки уведомлений о трофеях.',
    'Could not save trophy notification settings.': 'Не удалось сохранить настройки уведомлений о трофеях.',
    'Names and descriptions are unavailable for this trophy pack.':
        'Названия и описания для этого набора трофеев недоступны.',
    'No trophies loaded yet. Launch the game to load the trophy list.':
        'Список трофеев пока пуст. Запустите игру, чтобы загрузить его.',
    'The name and requirement are revealed when this trophy is earned.':
        'Название и условие откроются после получения трофея.',
    'Description unavailable.': 'Описание недоступно.',
    'Optional': 'Необязательно',
    'Required': 'Обязательно',
    'Your game files and saves are ready. Choose a graphics preset, then start playing or open the launcher.':
        'Файлы игры и сохранения готовы. Выберите пресет графики, затем начните игру или откройте лаунчер.',
    'A required check needs attention. Go back to Game files or Your data to fix it.':
        'Обязательная проверка не пройдена. Вернитесь к шагу «Файлы игры» или «Ваши данные», чтобы исправить.',
    '  ★ Suggested for your graphics card.': '  ★ Рекомендуется для вашей видеокарты.',
    'Start setup': 'Начать настройку',
    'Skip for now': 'Пока пропустить',
    'Back': 'Назад',
    'Continue': 'Далее',
    'Open launcher': 'Открыть лаунчер',
    'Add valid game files to continue.': 'Добавьте правильные файлы игры, чтобы продолжить.',
    'Skip setup': 'Пропустить настройку',

    # --- Settings pages, sections, rows (backend FIELDS / SETTINGS_SECTIONS) -------------------
    'Display': 'Экран',
    'Display & frame rate': 'Экран и частота кадров',
    'Image effects': 'Эффекты изображения',
    'Video memory': 'Видеопамять',
    'Controller': 'Контроллер',
    'Mouse': 'Мышь',
    'Xbox and PlayStation prompts': 'Подсказки Xbox и PlayStation',
    'In-game preferences': 'Настройки в игре',
    'Cheats': 'Читы',
    'Mods': 'Моды',
    'Enhancements': 'Улучшения',
    'Built-in enhancements': 'Встроенные улучшения',
    'Advanced': 'Дополнительно',
    'Diagnostics': 'Диагностика',
    'Overlay': 'Overlay',
    'Engine': 'Движок',
    'Developer': 'Для разработчиков',
    'Online connection': 'Онлайн-подключение',
    'Upscaler': 'Масштабирование',
    'Renders below the output size and rebuilds a sharp image. DLSS needs an NVIDIA RTX card; FSR 3.1 works on any.':
        'Отрисовывает кадр в меньшем разрешении и восстанавливает чёткое изображение. DLSS требует видеокарту '
        'NVIDIA RTX, FSR 3.1 работает на любой.',
    'Upscaling preset': 'Пресет масштабирования',
    'How far below the output the game renders: higher factors are faster and softer.':
        'Чем сильнее снижено внутреннее разрешение, тем выше скорость и менее чёткое изображение.',
    'Output resolution': 'Выходное разрешение',
    "The final image size, usually your display's.": 'Итоговый размер изображения, обычно как у вашего экрана.',
    'Frame generation': 'Генерация кадров',
    "Makes frames between two of the game's: 60 FPS on screen becomes 120. Needs a display that fast; adds a "
    "little input latency. DLSS needs a GeForce RTX 40/50 and its frame generation files.":
        'Создаёт кадры между кадрами игры: 60 FPS на экране становятся 120. Нужен экран с такой частотой; '
        'немного увеличивает задержку ввода. DLSS требует GeForce RTX 40/50 и файлы генерации кадров.',
    'Frame generation multiplier': 'Множитель генерации кадров',
    '3× and 4× need DLSS on a GeForce RTX 50.': '3× и 4× требуют DLSS на GeForce RTX 50.',
    'Fit frame generation to the display': 'Подстраивать генерацию кадров под экран',
    "Generates only the frames your display's refresh rate can show.":
        'Создаёт только те кадры, которые может показать частота обновления экрана.',
    'HUD position (ultrawide)': 'Положение интерфейса (сверхширокий экран)',
    '21:9 and 32:9 outputs: health, items and Blood Echoes at the screen edges, or in the centred 16:9 area as on '
    'a 16:9 screen. Applies at the next start.':
        'Для 21:9 и 32:9: здоровье, предметы и Отголоски крови по краям экрана или в центральной области 16:9, '
        'как на экране 16:9. Применяется при следующем запуске.',
    'Live resolution changes': 'Смена разрешения на лету',
    'Lets the in-game menu change the upscaling preset without a restart, at some cost in speed.':
        'Позволяет менять пресет масштабирования в меню игры без перезапуска, ценой небольшой потери скорости.',
    'Model detail': 'Детализация моделей',
    'How soon distant models switch to simpler versions. Highest costs GPU time.':
        'Расстояние, на котором модели заменяются упрощёнными. «Максимальная» нагружает видеокарту.',
    'Video memory pressure target': 'Порог использования видеопамяти',
    'Starts clearing old textures and buffers before the chosen amount. This is not a hard VRAM cap; lower values '
    'may cause stutter. Restart the game to apply.':
        'Начинает выгружать старые текстуры и буферы до выбранного объёма. Это не жёсткий лимит видеопамяти; '
        'меньшие значения могут вызывать подтормаживания. Применяется после перезапуска игры.',
    'Chromatic aberration': 'Хром. аберрация',
    'Colour fringes at the screen edges. Look only.': 'Цветная кайма по краям экрана. Только внешний вид.',
    'Depth of field': 'Depth of Field (DoF)',
    'Blurs the background in cutscenes and close-ups. Look only.':
        'Размывает фон в катсценах и на крупных планах. Только внешний вид.',
    'Motion blur': 'Motion Blur',
    'Blur while turning the camera. Look only.': 'Размытие при повороте камеры. Только внешний вид.',
    'Ambient occlusion (SSAO)': 'SSAO',
    'Soft shadows in corners and creases. Costs GPU time.': 'Мягкие тени в углах и складках. Нагружает видеокарту.',
    "The game's own anti-aliasing": 'Сглаживание самой игры',
    "The game's own edge smoothing, under the upscaler. Look only.":
        'Штатное сглаживание контуров до обработки апскейлером. Влияет только на изображение.',
    'Shadows of dynamic lights': 'Тени от динамического света',
    'Shadows cast by lamps, torches and other moving lights. Costs GPU time.':
        'Тени от ламп, факелов и других подвижных источников света. Нагружает видеокарту.',
    'Screen-space reflections (not in the original)': 'SSR (отражения)',
    'Reflections on wet streets; not in the original game. Costs GPU time.':
        'Отражения на мокрых улицах; в оригинальной игре их нет. Нагружает видеокарту.',
    'Sharpening (RCAS)': 'RCAS',
    'Sharpens the upscaled image.': 'Делает масштабированное изображение резче.',
    'Sharpness (0.00–1.00)': 'Резкость (0.00–1.00)',
    'Object motion vectors': 'Векторы движения объектов',
    'Motion data for moving characters: fewer ghosting trails with an upscaler.':
        'Данные о движении персонажей: меньше шлейфов при масштабировании.',
    'Show FPS counter': 'Показывать счётчик FPS',
    'Frame rate': 'Частота кадров',
    'Frames ahead': 'Кадры в очереди',
    'Unlocked mode limit': 'Лимит FPS (без привязки к игре)',
    'Fullscreen': 'Полноэкранный режим',
    'Fullscreen type': 'Тип полноэкранного режима',
    'Exclusive switches the display to its own mode: notifications and other windows do not show over the game.':
        'Эксклюзивный переключает экран в собственный режим: уведомления и другие окна не появляются поверх игры.',
    'Monitor': 'Монитор',
    'The monitor the game window and fullscreen go to, in the order the game log lists them.':
        'Монитор для окна игры и полноэкранного режима, в порядке, как они перечислены в журнале игры.',
    'Primary monitor': 'Основной монитор',
    'Monitor 1': 'Монитор 1', 'Monitor 2': 'Монитор 2', 'Monitor 3': 'Монитор 3', 'Monitor 4': 'Монитор 4',
    'HDR output': 'Вывод HDR',
    'Presentation mode': 'Режим вывода кадров',
    'Draw pipeline': 'Конвейер отрисовки',
    'GPU readbacks': 'Чтение данных с видеокарты',
    'Frame statistics': 'Статистика кадров',
    'GPU profiling': 'Профилирование видеокарты',
    'Vulkan validation': 'Проверка Vulkan',
    'Extra environment variables': 'Дополнительные переменные окружения',
    'Game folder (contains eboot.bin)': 'Папка игры (с eboot.bin)',
    'DLC folder (base-game dumps only, e.g. SPEXPANSIONDLC03)':
        'Папка DLC (только для дампов базовой игры, например SPEXPANSIONDLC03)',
    'Saves folder': 'Папка сохранений',
    'Game language': 'Язык игры',
    'Voice language': 'Язык озвучки',
    'As in the game uses the original voice setting; other choices use available tracks.':
        '«Как в игре» оставляет исходную озвучку; другие варианты используют доступные дорожки.',
    'Hunter name': 'Имя охотника',
    'Skip the intro logos and movie': 'Пропускать логотипы и вступительный ролик',
    'Mouse camera (click the game window to use it)': 'Камера мышью (щёлкните по окну игры, чтобы включить)',
    'Mouse sensitivity': 'Чувствительность мыши',
    'Invert mouse Y': 'Инвертировать мышь по вертикали',
    "Mouse pointer in the game's menus (hover, click, right-click back)":
        'Указатель мыши в меню игры (наведение, щелчок, правый щелчок — назад)',
    'Hide the mouse cursor in the game (for mouse-to-controller tools)':
        'Скрывать курсор мыши в игре (для программ эмуляции контроллера)',
    'Keyboard movement smoothing (WASD direction changes)': 'Сглаживание движения с клавиатуры (смена направления WASD)',
    'Free camera': 'Свободная камера',
    'Debug menu': 'Меню отладки',
    'Never die (health stops at 1 HP)': 'Бессмертие (здоровье не опускается ниже 1)',
    'Enemies do not see you (unless attacked)': 'Враги не видят вас (пока вы не атакуете)',
    'Enemies do not hear you': 'Враги не слышат вас',
    'Rally never fades': 'Регенерация без убывания',
    'Control the targeted enemy (R3; L3 to go back; not with the free camera)':
        'Управлять выбранным врагом (R3; L3 — вернуться; не со свободной камерой)',
    'No stamina use': 'Выносливость не тратится',
    'No stamina use out of combat (8 s after your last attack or hit)':
        'Выносливость не тратится вне боя (через 8 с после последней атаки или удара)',
    'No Rally (hits do not give health back)': 'Без регенерации (удары не возвращают здоровье)',
    'Camera further from the character': 'Камера дальше от персонажа',
    'No camera auto-rotation while moving': 'Без автоповорота камеры при движении',
    'Run with less stick tilt (about 70%)': 'Бег при меньшем наклоне стика (около 70%)',
    'Japanese/Asian buttons: Circle confirms and interacts, Cross dodges':
        'Японская раскладка: Круг подтверждает и взаимодействует, Крест — уклонение',
    'Dark Souls-style ragdoll physics (corpses fly further)': 'Физика тел как в Dark Souls (тела отлетают дальше)',
    'UPnP': 'UPnP',
    'Opens a port on your router for summons. Turn it off on Tailscale or another VPN.':
        'Открывает порт на роутере для призывов. Выключите при Tailscale или другом VPN.',
    'Co-op name': 'Имя в совместной игре',
    'Your name in co-op, 3-16 letters, numbers, - or _.': 'Ваше имя в совместной игре: 3–16 букв, цифр, - или _.',
    'Co-op password': 'Пароль совместной игры',
    "For your co-op account on the host's server. Use one you use nowhere else.":
        'Для вашего аккаунта на сервере хоста. Используйте пароль, который больше нигде не используете.',
    'Host invite code': 'Код приглашения хоста',
    "Paste the BBCOOP- code your host sent you. Leave empty when you host, or to use this launcher's own co-op "
    "server (coop-server.json).":
        'Вставьте код BBCOOP-, присланный хостом. Оставьте пустым, если хост — вы, или чтобы играть на сервере '
        'этого лаунчера (coop-server.json).',
    'Co-op game program': 'Программа игры для совместной игры',
    "Which bb-probe.exe co-op runs. This launcher's has frame generation, the mouse settings and the rest; BBSC's "
    "is the one BBSC tests with.":
        'Какой bb-probe.exe запускать для совместной игры. У этого лаунчера есть генерация кадров, настройки мыши '
        'и остальное; эмулятор BBSC — тот, на котором BBSC тестируют.',
    "This launcher's (all its settings; BBSC relay built in)": 'Этого лаунчера (все настройки; relay BBSC встроен)',
    "BBSC's own BBport build (BBport 1.7.2 features only)": 'Собственная сборка BBport от BBSC (только возможности BBport 1.7.2)',
    'Enable mods': 'Включить моды',
    'Mods folder': 'Папка модов',
    'Refresh mods': 'Обновить список модов',
    'External patches folder': 'Папка внешних патчей',
    "Hunter's Dream mirror: change appearance": 'Зеркало во Сне Охотника: смена внешности',
    'Two invaders in the late areas (every player needs it)': 'Два захватчика в поздних локациях (нужно всем игрокам)',
    'Rebirth in the Nightmare at the Altar of Despair': 'Перерождение в Кошмаре у Алтаря отчаяния',
    'Lamps: Level Up and Storage at every lit lamp': 'Лампы: повышение уровня и хранилище у каждой зажжённой лампы',
    'Boss rematches at their lamps (experimental; back up your saves)':
        'Повторные бои с боссами у их ламп (экспериментально; сделайте копию сохранений)',
    'Hidden': 'Скрыты',
    'Launcher language': 'Язык лаунчера',
    'System default': 'Как в системе',

    # --- Graphics presets (core.GRAPHICS_PRESET_INFO), setup facts -----------------------------
    'Low': 'Низкий', 'Balanced': 'Баланс', 'High': 'Высокий', 'Ultra': 'Ультра',
    'Unlocked': 'Без ограничения', 'Windowed': 'В окне',
    'Performance upscaling (×2), lower model detail, no SSAO or dynamic-light shadows, 60 FPS. For integrated '
    'graphics, the Steam Deck and cards with under 4 GB.':
        'Режим апскейлера Performance (×2), упрощённые модели, без SSAO и теней от динамического '
        'света, 60 FPS. Для встроенной графики, Steam Deck и видеокарт с памятью меньше 4 ГБ.',
    "Balanced upscaling (×1.7) and the game's own detail, 120 FPS. The default; for cards with 4-8 GB.":
        'Режим апскейлера Balanced (×1.7) и исходная детализация игры, 120 FPS. По умолчанию; для видеокарт '
        'с 4–8 ГБ.',
    "Quality upscaling (×1.5) and the game's own detail, 120 FPS. For cards with 8-12 GB.":
        'Режим апскейлера Quality (×1.5) и исходная детализация игры, 120 FPS. Для видеокарт с 8–12 ГБ.',
    'Native resolution, highest model detail and screen-space reflections (not in the original game), 120 FPS. '
    'For cards with 12 GB or more.':
        'Исходное разрешение, максимальная детализация моделей и отражения в экранном пространстве (нет в '
        'оригинальной игре), 120 FPS. Для видеокарт с 12 ГБ и больше.',
    'Your own combination. Choosing a preset changes only upscaling, model detail, SSAO, dynamic-light shadows, '
    'reflections and the frame rate.':
        'Ваша собственная комбинация. Выбор пресета меняет только масштабирование, детализацию моделей, SSAO, '
        'тени от динамического света, отражения и частоту кадров.',

    # --- Option labels without a Russian label in the launcher core ----------------------------
    'Off': 'Выключено', 'On': 'Включено',
    'TAA (native resolution anti-aliasing)': 'TAA (сглаживание в родном разрешении)',
    'AMD FSR 3.1 Frame Generation (any GPU)': 'Генерация кадров AMD FSR 3.1 (любая видеокарта)',
    'NVIDIA DLSS Frame Generation (GeForce RTX 40/50)': 'Генерация кадров NVIDIA DLSS (GeForce RTX 40/50)',
    '2× (one generated frame)': '2× (один созданный кадр)',
    '3× (DLSS on GeForce RTX 50)': '3× (DLSS на GeForce RTX 50)',
    '4× (DLSS on GeForce RTX 50)': '4× (DLSS на GeForce RTX 50)',
    'Screen edges': 'По краям экрана', 'Halfway': 'Посередине', 'Centred (16:9)': 'В центре (16:9)',
    'Automatic (recommended)': 'Автоматически (рекомендуется)',
    'No limit  ⚠': 'Без ограничения  ⚠',
    '1 (default)': '1 (по умолчанию)',
    'Unbounded': 'Без ограничения',
    'Borderless (default)': 'Без рамки (по умолчанию)',
    'Exclusive': 'Эксклюзивный',
    'Mailbox (low latency, no tearing)': 'Mailbox (малая задержка, без разрывов)',
    'Immediate (tearing)': 'Immediate (с разрывами)',
    'Light': 'Слабое', 'Medium (default)': 'Среднее (по умолчанию)', 'Strong': 'Сильное',
    'Auto (8+ threads)': 'Авто (8+ потоков)',
    'Off (more stable)': 'Выключено (стабильнее)',
    'Relaxed (default)': 'Мягкий (по умолчанию)',
    'Precise': 'Точный',
    'shadNet server (address below)': 'Сервер shadNet (адрес ниже)',
    'Performance (×2)': 'Performance (×2)',
    'Balanced (×1.7)': 'Balanced (×1.7)',
    'Quality (×1.5)': 'Quality (×1.5)',
    'Native AA (×1.0)': 'Native AA (×1.0)',
    'Ultra Performance (×3)': 'Ultra Performance (×3)',
    'Russian': 'Русский', 'Japanese': 'Японский', 'French': 'Французский', 'Spanish': 'Испанский',
    'German': 'Немецкий', 'Italian': 'Итальянский', 'Portuguese (Brazil)': 'Португальский (Бразилия)',
    'Portuguese (Portugal)': 'Португальский (Португалия)', 'Spanish (Latin America)': 'Испанский (Латинская Америка)',
    'English (UK)': 'Английский (Великобритания)', 'Dutch': 'Нидерландский', 'Polish': 'Польский',
    'Turkish': 'Турецкий', 'Finnish': 'Финский', 'Swedish': 'Шведский', 'Danish': 'Датский',
    'Norwegian': 'Норвежский', 'Korean': 'Корейский', 'Chinese (Traditional)': 'Китайский (традиционный)',
    'Chinese (Simplified)': 'Китайский (упрощённый)',

    # --- Notices, statuses, errors (backend) --------------------------------------------------
    'Bloodborne was added to your Steam library.': 'Bloodborne добавлена в вашу библиотеку Steam.',
    'Bloodborne.exe is missing from the download': 'В загрузке нет Bloodborne.exe',
    'Checking BBSC releases…': 'Проверка релизов BBSC…',
    'Checking graphics card…': 'Проверка видеокарты…',
    'Choose a BBSC package (BBSC-<version>-BBport.zip)': 'Выберите пакет BBSC (BBSC-<версия>-BBport.zip)',
    'Choose a writable saves folder before playing.': 'Перед игрой выберите папку сохранений, доступную для записи.',
    'Choose the game folder containing eboot.bin first.': 'Сначала выберите папку игры с eboot.bin.',
    'Choose your game folder to begin': 'Выберите папку игры, чтобы начать',
    'Close the game before clearing its cache.': 'Закройте игру перед очисткой её кэша.',
    'Close the game before updating.': 'Закройте игру перед обновлением.',
    'Close the game or wait for the current setup to finish.': 'Закройте игру или дождитесь окончания текущей установки.',
    'Desktop and Start Menu shortcuts created.': 'Ярлыки на рабочем столе и в меню «Пуск» созданы.',
    'Entering original x86-64 code': 'Переход к исходному коду x86-64',
    'FSR 4 assets are already installed.': 'Ресурсы FSR 4 уже установлены.',
    'FSR 4 assets installed.': 'Ресурсы FSR 4 установлены.',
    'FSR 4 assets ready': 'Ресурсы FSR 4 готовы',
    'Fill in your co-op name and password first.': 'Сначала укажите имя и пароль для совместной игры.',
    'Fill in your co-op name and password first; they make your account on your server.':
        'Сначала укажите имя и пароль для совместной игры: с ними создаётся ваш аккаунт на вашем сервере.',
    'First time: say Yes to the Windows prompt (firewall and C++ runtime)…':
        'В первый раз: ответьте «Да» на запрос Windows (брандмауэр и библиотеки C++)…',
    'First time: say Yes to the Windows prompt (firewall)…': 'В первый раз: ответьте «Да» на запрос Windows (брандмауэр)…',
    'Game folder already exists': 'Папка игры уже существует',
    'Game installation could not finish': 'Не удалось завершить установку игры',
    'Game installed and version 1.09 verified. Press PLAY.': 'Игра установлена, версия 1.09 подтверждена. Нажмите «Играть».',
    'Game installed. Check that the launcher reports version 1.09 before playing.':
        'Игра установлена. Перед игрой проверьте, что лаунчер показывает версию 1.09.',
    'Getting co-op ready…': 'Подготовка совместной игры…',
    'Graphics card check unavailable': 'Проверка видеокарты недоступна',
    'Installing BBSC…': 'Установка BBSC…',
    'Invite code copied. Send it to your friend in a private message.':
        'Код приглашения скопирован. Отправьте его другу в личном сообщении.',
    'JSON files (*.json)': 'Файлы JSON (*.json)',
    'Last step: choose where to create the CUSA03173 game folder': 'Последний шаг: выберите, где создать папку игры CUSA03173',
    'Log copied to clipboard.': 'Журнал скопирован в буфер обмена.',
    'Mod change saved. Restart the game to apply it.': 'Изменение модов сохранено. Перезапустите игру, чтобы применить.',
    'No network found. Connect Tailscale, then try again.': 'Сеть не найдена. Подключите Tailscale и попробуйте снова.',
    'Not set up yet: Set up / update BBSC downloads the newest BBSC from its GitHub releases (about 100 MB), or '
    'Play co-op does it for you.':
        'Ещё не настроено: «Установить / обновить BBSC» скачает новейший BBSC из его релизов на GitHub (около '
        '100 МБ), или это сделает «Играть вместе».',
    'Offline: your own world, no servers.': 'Офлайн: ваш собственный мир, без серверов.',
    'Online ID must be your account name, not an email address.': 'Онлайн-ID — это имя аккаунта, а не адрес почты.',
    'Online connection test finished.': 'Проверка онлайн-подключения завершена.',
    'Preparing the game…': 'Подготовка игры…',
    'Preparing your game files. Keep the launcher open…': 'Подготовка файлов игры. Не закрывайте лаунчер…',
    'Prompt mod download (*.zip *.7z *.rar common.tpf.dcx);;All files (*)':
        'Загрузка мода подсказок (*.zip *.7z *.rar common.tpf.dcx);;Все файлы (*)',
    'ReleaseTrophyKey must be 32 hexadecimal characters': 'ReleaseTrophyKey должен состоять из 32 шестнадцатеричных символов',
    'Restarting with the new settings…': 'Перезапуск с новыми настройками…',
    'Seamless co-op: choose a co-op name and password first (Settings → Co-op).':
        'Бесшовная совместная игра: сначала укажите имя и пароль (Настройки → Совместная игра).',
    "Seamless co-op: joining your host's server from the invite code.":
        'Бесшовная совместная игра: подключение к серверу хоста по коду приглашения.',
    "Seamless co-op: start hosting, or paste a host's invite code (Settings → Co-op).":
        'Бесшовная совместная игра: запустите сервер или вставьте код приглашения хоста (Настройки → Совместная игра).',
    'Shader cache cleared. The next launch will rebuild it.': 'Кэш шейдеров очищен. Следующий запуск создаст его заново.',
    'Sign-in code copied.': 'Код входа скопирован.',
    'Starting the co-op servers…': 'Запуск серверов совместной игры…',
    'Starting the sign-in…': 'Начало входа…',
    'Steam did not close. Close it yourself and try again.': 'Steam не закрылся. Закройте его сами и попробуйте снова.',
    'Steam must close while the game is added. Close Steam now?': 'Пока игра добавляется, Steam нужно закрыть. Закрыть Steam сейчас?',
    'Steam was not found on this PC or no account has signed in.': 'Steam не найден на этом ПК, или в нём не выполнен вход.',
    'Stopped hosting.': 'Сервер остановлен.',
    'The game is running.': 'Игра запущена.',
    'Trophy keys copied to the new saves folder.': 'Ключи трофеев скопированы в новую папку сохранений.',
    'Vulkan graphics card not detected': 'Видеокарта с Vulkan не обнаружена',
    'Wait for the game files to finish installing.': 'Дождитесь окончания установки файлов игры.',
    'Game files not found': 'Файлы игры не найдены',
    'Saves folder is not writable': 'В папку сохранений нельзя записывать',
    # co-op (bbport_coop.py)
    'A co-op name is 3-16 letters, numbers, - or _.': 'Имя в совместной игре — 3–16 букв, цифр, - или _.',
    'Choose a password of at least 4 characters (one you use nowhere else).':
        'Выберите пароль не короче 4 символов (который больше нигде не используете).',

    'Set up co-op first (the BBSC package is missing).': 'Сначала настройте совместную игру (нет пакета BBSC).',
    'That invite code is damaged; ask the host to copy it again.':
        'Код приглашения повреждён; попросите хоста скопировать его ещё раз.',
    "The invite code does not match the host's server: it is from an older session or another host. Ask the host "
    "to copy the invite code again.":
        'Код приглашения не подходит к серверу хоста: он от прошлой сессии или другого хоста. Попросите хоста '
        'скопировать код ещё раз.',
    # pkg setup (bbport_pkg_setup.py)
    'Applying the update to the game folder…': 'Установка обновления в папку игры…',
    'Checking the base game and 1.09 update…': 'Проверка базовой игры и обновления 1.09…',
    'Choose an existing destination folder.': 'Выберите существующую папку назначения.',
    'Extracting the 1.09 update…': 'Распаковка обновления 1.09…',
    'Extracting the base game. This can take a while…': 'Распаковка базовой игры. Это может занять время…',
    'Game files installed. Ready to play.': 'Файлы игры установлены. Можно играть.',
    'The completed game folder is missing eboot.bin.': 'В готовой папке игры нет eboot.bin.',
    'Unpacking the 1.09 update from the ZIP…': 'Распаковка обновления 1.09 из ZIP…',
    # readiness (bbport_readiness.py)
    'Bloodborne 1.09 and required folders found.': 'Bloodborne 1.09 и нужные папки найдены.',
    'Missing: ': 'Не хватает: ',
    'No trophy pack found; achievements can show IDs only.': 'Пакет трофеев не найден; достижения будут показаны только номерами.',
    'Pack and key format found; launch the game to verify decryption.':
        'Пакет и формат ключа найдены; запустите игру, чтобы проверить расшифровку.',
    'Save folder is not writable.': 'В папку сохранений нельзя записывать.',
    'Save folder will be created on first launch.': 'Папка сохранений будет создана при первом запуске.',
    'Save path is a file, not a folder.': 'Путь сохранений указывает на файл, а не на папку.',
    'Trophy names have been loaded by the game.': 'Игра загрузила названия трофеев.',
    'Trophy pack cannot be read or has an invalid header.': 'Пакет трофеев не читается или у него неверный заголовок.',
}

# Texts with values: {} in the English template, {0}, {1}, ... in the Russian one.
PATTERNS = [

    ('Downloading {}/{} · {} / {} GiB', 'Загрузка {0}/{1} · {2} / {3} ГиБ'),
    ('Unpacking {}/{} · {}/{}', 'Распаковка {0}/{1} · {2}/{3}'),
    ('Not enough free space: need {} GiB', 'Недостаточно места: требуется {0} ГиБ'),

    ('A co-op server stopped at start; see {}.', 'Сервер совместной игры остановился при запуске; см. {0}.'),
    ('An invite code starts with {}', 'Код приглашения начинается с {0}'),
    ('No BBSC release has a {} package ({}).', 'Ни в одном релизе BBSC нет пакета {0} ({1}).'),
    ('No answer from the co-op server at {}. Is the host hosting, and are you both on Tailscale?',
     'Сервер совместной игры {0} не отвечает. Хост запустил сервер, и вы оба в Tailscale?'),
    ('No answer from the co-op server at {}. The host must be hosting (launcher open), and both of you on '
     'Tailscale or the same network.',
     'Сервер совместной игры {0} не отвечает. Хост должен запустить сервер (лаунчер открыт), а вы оба — быть '
     'в Tailscale или одной сети.'),

    ("The host's server did not create the account ({}).", 'Сервер хоста не создал аккаунт ({0}).'),
    ("The host's server does not accept the name {}; choose another.", 'Сервер хоста не принимает имя {0}; выберите другое.'),
    ('Unsafe path in the package: {}', 'Небезопасный путь в пакете: {0}'),
    ('Windows could not run the co-op setup: {}', 'Windows не смогла выполнить настройку совместной игры: {0}'),
    ('{} does not match the checksum BBSC published; not installed.',
     '{0} не совпадает с контрольной суммой, опубликованной BBSC; не установлено.'),
    ("{} is already taken on the host's server, with another password. Use the password you chose with this name "
     "before, or another co-op name.",
     'Имя {0} на сервере хоста уже занято с другим паролем. Введите пароль, который вы выбрали с этим именем, '
     'или другое имя.'),
    ("{} is signed in on the host's server right now. Every player needs their own co-op name; if it is yours, "
     "close the game that uses it first.",
     '{0} сейчас уже в сети на сервере хоста. У каждого игрока должно быть своё имя; если это ваше, сначала '
     'закройте игру, где оно используется.'),
    (' Saves backed up to {}.', ' Копия сохранений: {0}.'),
    ('BBSC {} ({}) installed from {}.', 'BBSC {0} ({1}) установлен из {2}.'),
    ('BBSC {} is the newest release.', 'BBSC {0} — новейший релиз.'),
    ('BBSC {} installed ({}).', 'BBSC {0} установлен ({1}).'),
    ('BBSC {}. Hosting on {}. Send your friend the invite code.', 'BBSC {0}. Сервер на {1}. Отправьте другу код приглашения.'),
    ("BBSC {}. Ready. Host a session, or paste a host's invite code and play.",
     'BBSC {0}. Готово. Создайте сессию или вставьте код приглашения хоста и играйте.'),
    ('BBSC {}. Ready: Play co-op joins {}.', 'BBSC {0}. Готово: «Играть вместе» подключит к серверу {1}.'),
    ('Choose your {} download (by {}, opened on Nexus Mods)', 'Выберите скачанный {0} (от {1}, открыт на Nexus Mods)'),
    ('Copy keys.json to the new saves folder yourself: {}', 'Скопируйте keys.json в новую папку сохранений сами: {0}'),
    ('Could not add the game to Steam: {}', 'Не удалось добавить игру в Steam: {0}'),
    ('Could not check for updates: {}', 'Не удалось проверить обновления: {0}'),
    ('Could not start: {}', 'Не удалось запустить: {0}'),
    ('Downloading version {}…', 'Загрузка версии {0}…'),
    ('Downloading version {}… {}%', 'Загрузка версии {0}… {1}%'),
    ('Downloading {}: {}%', 'Загрузка {0}: {1}%'),
    ('Installing BBSC {}…', 'Установка BBSC {0}…'),
    ('Installing {}…', 'Установка {0}…'),
    ('FSR 4 download failed: {}', 'Не удалось скачать FSR 4: {0}'),
    ('Game ready · version {}', 'Игра готова · версия {0}'),
    ('Hosting on {} ({}); your account is {}. Copy the invite code for your friend, then press Play co-op. The servers '
     'stay active until you exit the game.',
     'Сервер запущен: {0} ({1}); ваш аккаунт: {2}. Скопируйте код приглашения для друга и нажмите «Играть '
     'вместе». Серверы будут работать до выхода из игры.'),
    ('Install version {} now? Saves, settings and mods are kept.',
     'Установить версию {0} сейчас? Сохранения, настройки и моды останутся.'),
    ('Now: the game renders at the output size, {} × {}.', 'Сейчас: игра рисует в выходном разрешении, {0} × {1}.'),
    ('Now: the game renders at {} × {} and upscales it to {} × {}.',
     'Сейчас: игра рисует в {0} × {1} и масштабирует до {2} × {3}.'),
    ('Seamless co-op: you host on {}; send your friends the invite code.',
     'Бесшовная совместная игра: вы хост на {0}; отправьте друзьям код приглашения.'),
    ('Starting co-op with {}. Host: ring the Beckoning Bell. Guest: ring the Small Resonant Bell.{}',
     'Запуск совместной игры с {0}. Хост: звоните в Зовущий Колокол. Гость: в Малый звонкий колокол.{1}'),
    ('The game could not start (exit code {}). See the log for details.',
     'Игра не запустилась (код выхода {0}). Подробности — в журнале.'),
    ('Unexpected installer error: {}', 'Неожиданная ошибка установщика: {0}'),
    ('Update failed: {}', 'Обновление не удалось: {0}'),
    ('You have the latest version ({}).', 'У вас последняя версия ({0}).'),
    ('{} FSR 4 assets missing', 'Не хватает ресурсов FSR 4: {0}'),
    ('{} already exists. Choose another location so no game files are replaced.',
     '{0} уже существует. Выберите другое место, чтобы не заменить файлы игры.'),
    ('{} button prompts selected. Restart the game to apply them.',
     'Выбраны подсказки кнопок: {0}. Перезапустите игру, чтобы применить.'),
    ('{} preset chosen. It applies the next time the game starts.', 'Выбран пресет «{0}». Применится при следующем запуске игры.'),
    ('{} preset chosen. Restart the game to apply it.', 'Выбран пресет «{0}». Перезапустите игру, чтобы применить.'),
    ('{} prompts are a separate download: get {} by {} from {}, then choose {} again and pick the downloaded file.',
     'Подсказки {0} скачиваются отдельно: возьмите {1} от {2} с {3}, затем снова выберите {4} и укажите скачанный файл.'),
    ('{}. Or host a session yourself.', '{0}. Или создайте сессию сами.'),
    ('— The game exited (code {}) —', '— Игра завершилась (код {0}) —'),
    ('Could not load Qt Quick launcher: {}', 'Не удалось загрузить лаунчер Qt Quick: {0}'),
    ('Could not extract {}. {}', 'Не удалось распаковать {0}. {1}'),
    ('Could not inspect {}: {}', 'Не удалось проверить {0}: {1}'),
    ('Game installation failed: {}', 'Установка игры не удалась: {0}'),
    ('Not enough free space here. Allow about {} GB for setup.', 'Здесь мало места. Для установки нужно около {0} ГБ.'),
    ('The ZIP has more than one {}.', 'В ZIP больше одного {0}.'),
    ('{} You chose {} as the base game and {} as the update.', '{0} Вы выбрали {1} как базовую игру и {2} как обновление.'),
    ('{} already exists. Choose another destination so your game files stay safe.',
     '{0} уже существует. Выберите другое место, чтобы файлы игры не пострадали.'),
    ('{} appeared during setup. No files were replaced.', '{0} появилась во время установки. Файлы не заменены.'),
    (' {} local unlocks recorded.', ' Записано разблокировок: {0}.'),
    ('Save folder is writable; no {} save yet.', 'Папка сохранений доступна для записи; сохранения {0} пока нет.'),
    ('Save folder is writable; {} save data found.', 'Папка сохранений доступна для записи; найдены сохранения {0}.'),
    ('Extracting file {} of {}', 'Распаковка файла {0} из {1}'),
]

_COMPILED = None

def _compiled():
    global _COMPILED
    if _COMPILED is None:
        _COMPILED = []
        explicit_patterns = {pattern for pattern, _ in PATTERNS}
        templates = PATTERNS + [(key, value) for key, value in RU.items()
                                if "{}" in key and key not in explicit_patterns]
        for english, russian in templates:
            regex = '^' + re.escape(english).replace(r'\{\}', '(.*?)') + '$'
            _COMPILED.append((re.compile(regex, re.S), russian))
    return _COMPILED

def tr(text):
    """The Russian text for an English launcher text, or the text itself."""
    if not text:
        return text
    found = RU.get(text)
    if found is not None:
        return found
    for regex, russian in _compiled():
        match = regex.match(text)
        if match:
            return russian.format(*(tr(value) for value in match.groups()))
    return text

# Player-focused launcher wording.
RU.update({
    'Player name': 'Имя игрока',
    '3–16 Latin letters, numbers, - or _. Also used in game.': '3–16 латинских букв, цифр, - или _. Также используется в игре.',
    'Save profile': 'Профиль сохранений',
    'Game folder': 'Папка игры',
    'DLC folder': 'Папка дополнения',
    'Advanced': 'Дополнительно',
    'Advanced settings': 'Расширенные настройки',
    'Mouse & keyboard': 'Мышь и клавиатура',
    'Display & frame rate': 'Экран',
    'In-game preferences': 'Язык игры',
    'Seamless co-op': 'Подключение',
    'Co-op gameplay': 'Правила игры',
    'Finish setup': 'Завершение настройки',
    'Finish': 'Завершить',
    'Game files & saves': 'Игра и сохранения',
    'Choose your game folder or download the game.': 'Укажите папку игры или скачайте игру.',
    'Choose your game folder or download the game. You can change both paths below.': 'Укажите папку игры или скачайте игру. Пути к игре и сохранениям можно изменить ниже.',
    'Optional. You can set up co-op later in Settings.': 'Необязательно. Кооператив можно настроить позже.',
    'Choose a graphics preset. You can change it later.': 'Выберите качество графики. Его можно изменить позже.',
    'Add desktop shortcut': 'Добавить ярлык на рабочий стол',
    'The shortcut will be named Bloodborne.': 'Название ярлыка — Bloodborne.',
    'Host on this PC': 'Создать сервер на этом ПК',
    'Send your invite code to friends.': 'Запустите сервер и отправьте код друзьям.',
    "Join a friend's server using their code.": 'Для подключения вставьте код друга.',
    'Paste the code from your host. Empty uses the default server.': 'Код друга. Без кода используется общий сервер.',
    'Download Tailscale': 'Скачать Tailscale',
    'No network found. Install or connect Tailscale: ': 'Сеть не найдена. Установите или подключите Tailscale: ',
    'Tailscale is not installed. Download: ': 'Tailscale не установлен. Скачать: ',
    'Downloads into the game folder beside the launcher.': 'Скачивание в папку игры рядом с лаунчером.',
    'Save data found.': 'Найдены сохранения.',
    'A new save will be created when you play.': 'При запуске игры будет создано новое сохранение.',
    'Graphics, display & frame rate': 'Качество и экран',
    'Prompts, mouse & keyboard': 'Кнопки, мышь и клавиатура',
    'Game files, saves & language': 'Папки и язык игры',
    'Seamless co-op: host or join': 'Играть с друзьями',
    'Mods, enhancements & tweaks': 'Дополнения и изменения',
    'Startup, updates & diagnostics': 'Лаунчер и обновления',
    'Changes save as you make them. Some take effect the next time the game starts.': 'Изменения сохраняются автоматически.',
    'Hunter name': 'Имя игрока',
    'Frame generation multiplier': 'Множитель кадров',
    'Fit frame generation to the display': 'По частоте монитора',
    'Video memory pressure target': 'Использование видеопамяти',
    'Fullscreen type': 'Режим полного экрана',
    'Mouse camera (click the game window to use it)': 'Камера мышью',
    "Mouse pointer in the game's menus (hover, click, right-click back)": 'Мышь в меню',
    'Keyboard movement smoothing (WASD direction changes)': 'Плавность движения',
    'HUD position (ultrawide)': 'Положение интерфейса',
    'Your name in co-op, 3-16 letters, numbers, - or _.': '3–16 латинских букв, цифр, - или _.',
    'Renders below the output size and rebuilds a sharp image. DLSS needs an NVIDIA RTX card; FSR 3.1 works on any.': 'Повышает FPS. DLSS — для RTX, FSR — для любых видеокарт.',
    'How far below the output the game renders: higher factors are faster and softer.': 'Баланс чёткости и производительности.',
    "Makes frames between two of the game's: 60 FPS on screen becomes 120. Needs a display that fast; adds a little input latency. DLSS needs a GeForce RTX 40/50 and its frame generation files.": 'Добавляет промежуточные кадры. DLSS требует RTX 40/50.',
    'Starts clearing old textures and buffers before the chosen amount. This is not a hard VRAM cap; lower values may cause stutter. Restart the game to apply.': 'Раньше освобождает видеопамять. Низкое значение может вызвать рывки.',
    '21:9 and 32:9 outputs: health, items and Blood Echoes at the screen edges, or in the centred 16:9 area as on a 16:9 screen. Applies at the next start.': 'Расположение HUD на широком экране.',
})

RU.update({
    'Start hosting before playing co-op.': 'Сначала запустите сервер.',
    'Connection help': 'Помощь с подключением',
    'Advanced settings': 'Тонкие настройки',
    'Co-op password': 'Пароль',
    "For your co-op account on the host's server. Use one you use nowhere else.": 'Отдельный пароль для кооператива.',
    'Exclusive switches the display to its own mode: notifications and other windows do not show over the game.': 'Эксклюзивный режим скрывает уведомления и другие окна.',
    'The monitor the game window and fullscreen go to, in the order the game log lists them.': 'На каком экране запускать игру.',

})

RU['Downloads into the game folder selected above.'] = 'Скачивание в указанную выше папку игры.'

RU.update({
    'Server is running. Send the invite code to friends.': 'Сервер запущен. Отправьте код друзьям.',
    'Start hosting to invite friends.': 'Запустите сервер, чтобы пригласить друзей.',
    'Enter your details and play co-op.': 'Укажите имя, пароль и код друга, затем нажмите «Играть вместе».',
    'Bundled BBSC-GL files are missing. Re-extract the launcher release.': 'Файлы кооператива не найдены. Переустановите лаунчер.',
    'Copy invite code': 'Копировать код',
    'Co-op name': 'Имя игрока',
})

RU.update({'Play mode': 'Режим игры', 'Advanced system': 'Расширенные настройки системы'})

RU.update({'Single player': 'Одиночная', 'Multiplayer': 'Совместная', 'Desktop shortcut': 'Создать ярлык', 'Add desktop shortcut': 'Создать ярлык'})

RU.update({
'Performance upscaling, reduced effects, 60 FPS.': 'Приоритет FPS, упрощённые эффекты, 60 FPS.',
'Balanced upscaling, standard effects, 120 FPS.': 'Баланс чёткости и скорости, обычные эффекты, 120 FPS.',
'Quality upscaling, standard effects, 120 FPS.': 'Приоритет чёткости, обычные эффекты, 120 FPS.',
'Native resolution, maximum detail and reflections, 120 FPS.': 'Полное разрешение, максимум деталей и отражений, 120 FPS.',
'Custom graphics settings.': 'Собственные настройки графики.'
})

RU.update({'Start server': 'Запустить сервер', 'Stop server': 'Остановить сервер',
})

RU.update({'Cheats': 'Читы', 'Advanced system': 'Расширенные настройки'})

RU.update({'Logs': 'Журнал', 'Open launcher folder': 'Открыть папку лаунчера'})

RU.update({'Remove FSR 4 assets': 'Удалить ресурсы FSR 4', 'FSR 4 assets removed.': 'Ресурсы FSR 4 удалены.',
'Reduced effects, 60 FPS.': 'Упрощённые эффекты, 60 FPS. Апскейлер выключен.',
'Standard effects, 120 FPS.': 'Обычные эффекты, 120 FPS. Апскейлер выключен.',
'High quality, 120 FPS.': 'Высокое качество, 120 FPS. Апскейлер выключен.'})

from bbport_setting_hints import HINTS as _SETTING_HINTS
RU.update({en: ru for en, ru in _SETTING_HINTS.values()})
RU.update({'Image effects': 'Графика', 'Seamless co-op: host or join': 'Игра с друзьями'})

RU.update({'Sets the button icons shown in game menus. Keyboard also applies matching key bindings.': 'Вид значков кнопок в меню игры. Для клавиатуры также назначаются соответствующие клавиши.',
'Checks for new launcher versions at startup.': 'Проверяет новые версии лаунчера при запуске.'})


RU.update({'Open saves folder': 'Папка сохранений', 'Open mods folder': 'Папка модов', 'Open launcher folder': 'Папка лаунчера', 'Open port folder': 'Папка лаунчера'})

RU.update({'Reduced effects, 60 FPS.': 'Упрощённые эффекты, 60 FPS.',
'Standard effects, 120 FPS.': 'Обычные эффекты, 120 FPS.',
'High quality, 120 FPS.': 'Высокое качество, 120 FPS.',
'Maximum detail and reflections, 120 FPS.': 'Максимум деталей и отражений, 120 FPS.'})

RU.update({'Single-player': 'Одиночный', 'Cooperative': 'Совместный'})

RU.update({'Resolution': 'Разрешение', 'Window mode': 'Режим окна', 'Generation': 'Генерация', 'Disabled': 'Выключено', 'Exclusive fullscreen': 'Эксклюзивный', 'Borderless fullscreen': 'Без рамки'})

RU.update({
    'Cancel launch': 'Отменить',
    'Launch cancelled.': 'Запуск отменён.',
    'Confirm': 'Подтвердить',
    'Allow incoming game and co-op server connections on local and Tailscale networks. Windows will ask for administrator permission.': 'Будут разрешены входящие подключения для игры и серверов кооператива в локальной сети и Tailscale. Windows запросит права администратора.'
})

RU.update({
    'Automatically': 'Автоматически',
    'Custom IPv4 address': 'Свой IPv4-адрес',
    'Connection': 'Подключение',
    'Address': 'Адрес',
    'Choose an address': 'Выберите адрес',
    'Choose a connection': 'Выберите подключение',
    'Your external or VPN IPv4': 'Ваш внешний или VPN IPv4',
    'Finding connections…': 'Поиск подключений…',
    'Refresh': 'Обновить',
    'For a public IP, forward the server ports on your router. Remote access is not verified.': 'Для белого IP нужен проброс портов сервера на роутере. Доступ извне не проверен.',
    'VPN: friends need the same network. Active adapters are shown; remote access is not verified.': 'Для VPN друзья должны быть в той же сети. Доступ со стороны друзей не проверен.',
    'Enter a valid IPv4 address for friends.': 'Введите корректный IPv4-адрес для друзей.',
    'Several VPN connections found. Choose the network your friends use.': 'Найдено несколько VPN. Выберите сеть, которой пользуются друзья.',
    'No active IPv4 connection found. Refresh the connection list.': 'Активных подключений с IPv4 нет. Обновите список подключений.',
    'Several connections found. Choose the network your friends use.': 'Найдено несколько подключений. Выберите сеть для друзей.',
    'The selected connection is unavailable. Refresh the connection list.': 'Выбранное подключение недоступно. Обновите список.',
    'Choose an address for the selected connection.': 'Выберите адрес для этого подключения.',
})


RU.update({'Connection unavailable': 'Подключение недоступно', })

RU.update({
    'Custom network': 'Своё подключение',
    'Check connection': 'Проверить подключение',
    'Local IPv4 of your network adapter': 'Локальный IPv4 выбранного сетевого адаптера',
    'Player IPv4 addresses, separated by commas (optional)': 'IPv4 участников через запятую (если не найдены автоматически)',
    'Open the launcher on every PC in the same VPN or local network. Roles are chosen with bells in the game.': 'Откройте лаунчер на всех ПК в одной VPN или локальной сети. Роли выбираются колоколами в игре.',
    'Choose a connection and check the players in your network.': 'Выберите подключение и проверьте связь с участниками.',
    'Finding players and checking the connection…': 'Поиск игроков и проверка связи…',
    'Connection checked: TCP and UDP between all players.': 'Связь проверена: TCP и UDP между всеми участниками.',
    'Checking the connection before launch…': 'Проверка связи перед запуском…',
    'Starting P2P co-op. Host: Beckoning Bell. Guest: Small Resonant Bell.': 'Запуск P2P. Хозяин: Зовущий колокол. Гость: Малый звонкий колокол.',
    'Open the launcher on 2–5 players in the same network.': 'Откройте лаунчер у 2–5 участников в одной сети.',
    'Selected network is not connected. Check the VPN and refresh.': 'Выбранная сеть недоступна. Проверьте VPN и обновите подключение.',
    'Several networks found. Choose Tailscale, Radmin or a custom local IPv4.': 'Найдено несколько сетей. Выберите Tailscale, Radmin или локальный IPv4 своего подключения.',
    'P2P co-op over your network': 'Кооператив P2P через вашу сеть',
    'Players see different groups. Refresh all launchers.': 'Участники видят разный состав группы. Обновите подключение на всех ПК.',
    'UDP connection failed. Check the VPN and firewall on every PC.': 'Нет связи по UDP. Проверьте VPN и брандмауэр на каждом ПК.',
})

RU.update({
    'Local test: 3 players on this PC': 'Локальный тест: 3 игрока на этом ПК',
    'Local test is running': 'Локальный тест запущен',
    'Starting three local players…': 'Запуск трёх локальных игроков…',
    'Starting three local players with existing profiles. No VPN is needed.': 'Запускаются три игры с существующими профилями. VPN не нужна.',
    'Uses the existing Player 1, 2 and 3 profiles and their saves. Close each game normally after the test.': 'Используются существующие профили Player 1, 2 и 3 и их сейвы. После теста закройте каждую игру штатным способом.',
})

# Current Party errors and graphics choices (Russian localization audit).
RU.update({
    'Native AA (×1.0)': 'Сглаживание (×1.0)',
    'Quality (×1.5)': 'Качество (×1.5)',
    'Balanced (×1.7)': 'Баланс (×1.7)',
    'Performance (×2)': 'Производительность (×2)',
    'Ultra Performance (×3)': 'Макс. производительность (×3)',
    '2560 x 1080 (Ultrawide)': '2560 x 1080 (сверхширокий)',
    '3440 x 1440 (Ultrawide)': '3440 x 1440 (сверхширокий)',
    '5120 x 2160 (Ultrawide)': '5120 x 2160 (сверхширокий)',
    '3840 x 1600 (Ultrawide)': '3840 x 1600 (сверхширокий)',
    '1080 x 1920 (Portrait)': '1080 x 1920 (вертикальный)',
    'Each player needs a separate network address.': 'Каждому игроку нужен отдельный сетевой адрес.',
    'Tailscale is not connected.': 'Нет подключения к Tailscale.',
    'The running game uses another group. Finish that session first.': 'Запущенная игра использует другую группу. Сначала завершите ту сессию.',
    'Invalid peer response': 'Некорректный ответ другого участника',
    'Peer identity changed. Refresh the connection.': 'Идентификатор участника изменился. Обновите подключение.',
    'The previous group has not finished its session. Reconnect those players first.': 'Предыдущая группа ещё не завершила сессию. Сначала подключите её участников повторно.',
    'Local players must use three separate saves folders.': 'Для трёх локальных игроков нужны отдельные папки сохранений.',
    'The local player process has the wrong profile.': 'Локальный игрок запущен с неверным профилем.',
    'Player {}: existing profile settings.json is missing.': 'Игрок {}: в профиле отсутствует settings.json.',
    'Player {}: the existing saves folder is unavailable.': 'Игрок {}: папка сохранений недоступна.',
    'Player {}: the configured game folder is unavailable.': 'Игрок {}: указанная папка игры недоступна.',
    'Local test configuration is invalid; it was preserved.': 'Конфигурация локального теста некорректна. Она сохранена без изменений.',
    'A local player port is already in use. Close the previous test games first.': 'Порт локального игрока уже занят. Сначала закройте игры предыдущего теста.',
    'A three-player local test is already running.': 'Локальный тест на трёх игроков уже запущен.',
    'Bundled co-op files are damaged. Re-extract the launcher release: {}': 'Встроенные файлы кооператива повреждены. Распакуйте лаунчер заново: {}',
    'Unsafe archive path: {}': 'Небезопасный путь внутри архива: {}',
    'Download URL must use HTTPS': 'Адрес загрузки должен использовать HTTPS',
    'Unsupported game manifest': 'Неподдерживаемый формат описания файлов игры',
    'Invalid or duplicate asset name': 'Некорректное или повторяющееся имя файла',
    'Invalid game manifest sizes or checksum': 'В описании файлов игры указаны некорректные размеры или контрольная сумма',
    'Installation folders cannot be symbolic links': 'Папки установки не могут быть символическими ссылками',
    'Incomplete game archive': 'Архив игры неполон',
    'Download cache cannot contain symbolic links': 'Кэш загрузки не может содержать символические ссылки',
    'Archive size does not match manifest': 'Размер архива не совпадает с указанным в описании файлов',
    'Duplicate or unsupported ZIP entry': 'Повторяющийся или неподдерживаемый элемент ZIP-архива',
    'Download exceeds declared size': 'Объём загрузки превышает заявленный размер',
    'bb-probe.exe is missing from this install.': 'В папке установки отсутствует bb-probe.exe.',
    'an update is still being installed; try again in a minute': 'обновление ещё устанавливается; повторите попытку через минуту',
    'Image effects': 'Эффекты изображения',
    'Starting P2P co-op. Host: Beckoning Bell. Guest: Small Resonant Bell.': 'Запуск совместной игры. Хост: Зовущий Колокол. Гость: Малый звонкий колокол.',
})

RU.update({
    'Finding players automatically…': 'Автоматический поиск игроков…',
    'Enter a player name to play co-op.': 'Введите имя игрока, чтобы начать совместную игру.',
    'Players online:': 'В сети:',
    'Player search unavailable:': 'Поиск игроков недоступен:',
    'Starting co-op…': 'Запуск совместной игры…',
    'A group supports 1–5 players in the same network.': 'Группа поддерживает от 1 до 5 игроков в одной сети.',

    'Players with an open launcher or game are found automatically in the selected network. Roles are chosen with bells in the game.': 'Игроки с открытым лаунчером или игрой находятся автоматически в выбранной сети. Роли выбираются колоколами в игре.',
})

RU.update({
    'Local network': 'Локальная сеть',
    'Unknown connection type.': 'Неизвестный способ подключения.',
    'Selected network is not connected. Check the network connection.': 'Выбранная сеть недоступна. Проверьте подключение к сети.',
    'Several VPN addresses found. Check the selected VPN network.': 'Найдено несколько VPN-адресов. Проверьте выбранную VPN-сеть.',
    'Download and install {}…': 'Скачать и установить {}…',
    'Downloading {}…': 'Загрузка {}…',
    'Installer opened. Complete installation, then connect to your VPN network.': 'Установщик открыт. Завершите установку и подключитесь к вашей VPN-сети.',
    'For Internet play, install a VPN and join the same network as your friends.': 'Для игры через интернет установите VPN и подключитесь к одной сети с друзьями.',
    'VPN installation failed:': 'Не удалось установить VPN:',
    'Could not find the VPN installer on the official website.': 'Не удалось найти установщик VPN на официальном сайте.',
    'VPN installer is too large.': 'Установщик VPN превышает допустимый размер.',
    'VPN installer download is incomplete.': 'Установщик VPN загружен не полностью.',
    'The VPN download is not a Windows installer.': 'Загруженный файл не является установщиком Windows.',
})

RU.update({
    'Play with friends': 'Игра с друзьями',
    'Mod': 'Мод',
    'Order': 'Порядок',
    'Move mod up': 'Переместить мод выше',
    'Move mod down': 'Переместить мод ниже',
    'Enabled': 'Включён',
    'Inactive — installation required': 'Неактивен — требуется установка',
    'Put each mod in its own folder. Mods shared by players appear in this table automatically.': 'Поместите каждый мод в отдельную папку. Моды других игроков появятся в таблице автоматически.',
    'Mods are not synchronized': 'Моды не синхронизированы',
    'Not all player mods are installed or synchronized. Check the mod list before starting co-op, or launch the game anyway.': 'Не все моды игроков установлены или синхронизированы. Проверьте список модов перед совместной игрой или запустите игру без синхронизации.',
    'Mod settings': 'Настройки модов',
    'View mods': 'Открыть список модов',
    'Launch game': 'Запустить игру',
})
