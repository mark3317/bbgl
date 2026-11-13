# shadPS4, статус Sony и проекты вокруг эмуляции

## Что официально доступно и какие проекты существуют

### Takeaway

На 7 ноября 2026 года Sony по-прежнему перечисляет Bloodborne как игру PS4. Оригинальную игру запускает, в частности, shadPS4, экспериментальный эмулятор PS4 для Windows, Linux и macOS, а проекты вроде BB PC Remaster и BB Launcher добавляют функции вокруг него.

### Cited Findings

- [Карточка PlayStation](https://www.playstation.com/en-us/games/bloodborne/) указывает PS4. У Sony ещё в сентябре 2018 был официальный облачный стриминг PS4-версии через PlayStation Now с ПК, описанный в [PlayStation Blog](https://blog.playstation.com/2018/09/04/playstation-now-bloodborne-and-more-join-the-lineup/). Это запуск на стороне сервиса, а не Windows-релиз. В интервью PC Gamer от июня 2024 Миядзаки говорил о личной поддержке идеи расширить доступ и желании других разработчиков FromSoftware, без анонса [интервью](https://www.pcgamer.com/games/action/hidetaka-miyazaki-knows-for-a-fact-other-fromsoftware-devs-want-a-bloodborne-pc-port-if-i-say-i-want-one-ill-get-in-trouble-but-its-nothing-im-opposed-to/). Даже GamesRadar 6 ноября 2026 всё ещё пишет об отсутствии ПК-порта, ремастера и сиквела [материал](https://www.gamesradar.com/games/action-rpg/former-playstation-boss-says-we-dont-have-bloodborne-2-yet-because-the-biggest-challenge-is-getting-fromsoftware-its-owner-and-everyone-else-to-agree-on-it/).
- В феврале 2026 Bloomberg сообщил о предложении Bluepoint сделать ремейк и об отказе FromSoftware. Предложение о ремейке нельзя трактовать как анонс ПК-версии [публикация автора Jason Schreier со ссылкой на Bloomberg](https://bsky.app/profile/jasonschreier.bsky.social/post/3mfuj367ur22a).
- shadPS4 — эмулятор общего назначения. На 07.11 проверенная актуальная стабильная сборка v0.21.0 вышла 30.10.2026, есть pre-release 05.11. [Репозиторий](https://github.com/shadps4-emu/shadPS4) и [страница релизов](https://github.com/shadps4-emu/shadPS4/releases).
- shadPS4 v0.20.0 14.10.2026 объявил поддержку сетевых функций Bloodborne через собственный shadNet 0.1.0. Это обычные сетевые функции игры, термин «официально» относится к команде эмулятора. Бесшовная игра BBSC — отдельный мод. [Релиз shadPS4](https://github.com/shadps4-emu/shadPS4/releases/tag/v.0.20.0), [документация BBSC в bbport](https://github.com/deadinside28/bloodborne_pc/blob/master/docs/BBSC.md).
- BB PC Remaster от fromsoftserve — графический мод (динамические тени, источники света, текстуры), публиковавшийся также под названием Shadows of the Hunt. Nexus Original upload 03.09.2024 21:02; разные отображения часового пояса могут показать 4 сентября. Один из подтверждённых роликов автора от 04.10.2024. Digital Foundry показывал моды в январе 2025 и отдельно Shadows of the Hunt в январе 2026. [Nexus, метаданные оригинальной загрузки](https://www.nexusmods.com/bloodborne/mods/45?show_file=393&tab=files), [Nexus, список файлов](https://www.nexusmods.com/bloodborne/mods/45?tab=files), [видео автора](https://www.youtube.com/watch?v=6beXWLRYJd8), [Digital Foundry](https://www.youtube.com/watch?v=fqOs2chL3NQ).
- BB Launcher от rainmakerv2/v3 — лаунчер и менеджер модов shadPS4, отличный от проекта пользователя BBGL. Nexus фиксирует первую загрузку 04.01.2025. Затем YouTube-гайды, например Keyvan 06.07.2025, и материал PC Gamer 24.09.2026, автор которого использовал руководство Retro Renew и этот лаунчер. [Nexus](https://www.nexusmods.com/bloodborne/mods/194?tab=files), [GitHub](https://github.com/rainmakerv3/BB_Launcher), [гайд Keyvan](https://www.youtube.com/watch?v=ovAzulKegrw), [PC Gamer](https://www.pcgamer.com/games/after-mainlining-30-hours-of-1440p-bloodborne-i-know-in-my-heart-it-belongs-on-pc/).
- Опционально упомянуть Night of the Hunt VR как отдельный мод со своим VR-форком shadPS4, который распространялся через Reddit 17.10.2026 и GitHub. Есть также отдельный эксперимент laughtt/bloodborne-vr на базе ветки нативного порта с OpenXR, его нельзя смешивать с Night of the Hunt VR. [GitHub Night of the Hunt](https://github.com/bldbrne-vr/bldbrne-vr), [анонс Reddit](https://www.reddit.com/r/PCVR/comments/1x7wtey/bloodborne_vr_is_out_now/), [GitHub laughtt](https://github.com/laughtt/bloodborne-vr).
- Bloodborne PSX от Lilith Walther — самостоятельное переосмысление пролога в стиле PS1, выпущенное для Windows 31.01.2022. Аудитория знакомилась через дневники автора в Twitter/YouTube, ролик с датой релиза и Reddit. На itch.io файлы сейчас приостановлены по заявлению правообладателя. [Game Informer о дневниках и прологе](https://gameinformer.com/2021/10/22/bloodborne-psx-faithfully-de-makes-the-games-memorable-prologue), [релизный трейлер автора](https://www.youtube.com/watch?v=9Pz_T6Kog6k), [Reddit на дату релиза](https://www.reddit.com/r/bloodborne/comments/sh64a4/the_fanmade_bloodborne_psx_demake_has_just/), [itch.io](https://b0tster.itch.io/bbpsx), [публичное уведомление](https://itch.io/takedowns/1370201).

### Inferences

- Роль Sony в PS Now и слово «официально» в changelog shadPS4 могут создать ложное впечатление релиза для Windows. Официальный релиз игры на ПК по открытым источникам не подтверждается.

### Gaps

- Нет оснований назвать RPCSX/fpPS4 сопоставимым вариантом полноценного прохождения Bloodborne по проверенным публичным источникам. Не включал в карту рабочих проектов.
- Нет статистики атрибуции трафика отдельных модов. Первые документируемые публикации и известные каналы охвата не показывают, сколько людей пришло из каждого.

## Как люди узнали о shadPS4

### Takeaway

Первые публичные доказательства шли от разработчиков и тестеров через блог, YouTube, Discord и GitHub. Игровая пресса и Reddit подхватили эти материалы, а Digital Foundry позднее проверила уже практически играбельную версию.

### Cited Findings

- **5.07.2024:** блог shadPS4 и видео ведущего разработчика George Moralis показали загрузку до экрана создания персонажа. В интервью Wes Fenlon от 14.07 Moralis объяснил предысторию: внутренний запуск уже был, часть нужного кода временно отсутствовала в публичном исходнике, пользователь обнаружил способ, после чего разработчик продемонстрировал результат. Первую волну в русскоязычном сегменте фиксируют DTF и GameGPU. [Блог shadPS4](https://shadps4.net/blog/blooborne/), [ролик Moralis](https://www.youtube.com/watch?v=FWX0ziJNyew), [интервью Read Only Memo](https://readonlymemo.com/shadps4-bloodborne-interview-pcsx2-0-new-features/), [DTF](https://dtf.ru/hard/2790747-bloodborne-zapustili-na-pk-cherez-emulyator-poka-rabotaet-tolko-menyu), [GameGPU](https://gamegpu.com/news/igry/entuziasty-zapustili-bloodborne-na-pk-s-pomoshchyu-emulyatora-shadps4).
- **18.08.2024:** блог эмулятора показывает выход в игру благодаря временному PR TheTurtle. DSOGaming в тот же день описал, что взял раннее игровое видео из Discord shadPS4, а Dexerto позже сослался на ролик fromsoftserve от 18 августа. Параллельно клипы обсуждали на Reddit. [Блог](https://shadps4.net/blog/even-more-bloodborne-progress/), [GitHub PR](https://github.com/shadps4-emu/shadPS4/pull/465), [DSOGaming](https://www.dsogaming.com/videotrailer-news/heres-your-first-look-of-bloodborne-running-on-pc-via-shadps4/), [Dexerto](https://www.dexerto.com/gaming/bloodborne-finally-works-on-pc-thanks-to-modders-but-its-not-great-2867617/), [Reddit](https://www.reddit.com/r/BloodbornePC/comments/1evijij/).
- **22.09.2024:** TheTurtle рассказал Read Only Memo, что загрузка из основной ветки стала возможна без ранних специальных обходов, а в Discord уже были тысячи участников. Издание ссылалось на многочисленные ролики сообщества и показывало видео боя с боссом от Moralis. [Интервью](https://readonlymemo.com/bloodborne-emulation-improved-so-fast/), [ролик Moralis](https://www.youtube.com/watch?v=gidwmgrkI_c).
- **21.01.2025** Digital Foundry проверил, что игру можно пройти от начала до конца, и протестировал 60 FPS и графические моды. **17.01.2026** команда выпустила повторный тест 4K/60 на ПК и тест на ROG Xbox Ally X. По снимку поисковой выдачи первое видео порядка 484 тыс. просмотров, второе порядка 421 тыс., цифры меняются. [Видео 2025](https://www.youtube.com/watch?v=-zjzBbdl7hk), [видео 2026](https://www.youtube.com/watch?v=fqOs2chL3NQ), [тест на сайте Digital Foundry](https://digitalfoundry.net/news/2026/01/bloodborne-pc-emulation-can-now-exceed-4k-at-60fps-and-its-brilliant).

### Inferences

- Самая наглядная цепочка охвата подтверждена здесь: предварительный результат команды в Discord -> ролик, который процитировала пресса -> более поздний независимый замер для широкой аудитории. Июльская история немного другая: пользователь раньше авторского показа разобрался с недостающим кодом, а затем появился публичный ролик команды.

### Gaps

- Точная дата, авторство и ссылка на первоначальный пользовательский эксперимент, упомянутый Moralis, из интервью не устанавливаются. 5 июля — дата официального публичного показа, а не доказанная дата первого запуска в мире.
- В августе и начале сентября распространялись заявления о первом полном прохождении. Один ранний Reddit-тред сам исправляет первоначальный приоритет. Без необходимости безопаснее говорить о публичных демонстрациях прохождения, а не присуждать первенство. [Тред от 04.09.2024](https://www.reddit.com/r/bloodborne/comments/1f8swzi/).
