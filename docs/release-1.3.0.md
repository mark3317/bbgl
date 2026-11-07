# BBGL 1.3.0

BBGL 1.3.0 includes BBSC-GL 1.3.0. Hunters in the same party can travel independently, meet again and continue playing together.

## Co-op

- Use lamps, Hunter’s Dream headstones and Chalice altars independently during a session. The game handles travel and recreates the other hunters when their paths cross again. Lit lamps are shared. Each hunter uses their own Hunter’s Dream, including their workshop and shops.
- NPC activity, movement and damage use the game’s network handling. The mod no longer scans the entire game memory after joining to rebuild enemy state. Enemy and boss HP scaling uses the game’s existing stat update.
- In the host’s Chalice Dungeon, the party sees the same lamp destinations. Lamps lit by a guest reach the host’s altar menu even while the host is elsewhere. First-layer progress persists when the party returns to the dungeon in the tested scenario.
- The party can gather in the Hunter’s Dream for the finale. After a shared ending, each hunter starts in their own Central Yharnam. The game closes the party during loading without the connection-loss banner in the tested transition.
- The game now delivers main-game and DLC boss rewards without a second shared reward queue. Also included are corrections for lamp selection after death, Blood Echo stains when a guest dies alone, returning to the title menu, and the guest’s jump to Rom.

## Launcher and port

- The launcher removes the old personal Dream switch because the Dream is always personal in a co-op session.
- Moving platforms use the same simulation step as character physics on the affected 1.09 frame-rate presets. The port also fixes a GPU submission race reproduced in a targeted test.
- Setting a GPU log level in the profile clears inherited class exceptions unless the profile explicitly lists its own. Fresh profiles keep detailed logs, research, profiling, Vulkan validation and cheats off.

## Install or update

Extract `bbgl-1.3.0-windows-x64.zip`, open **Bloodborne Game Launcher** and run **Bloodborne.exe**. Requires Windows x64, a Vulkan-capable driver and Bloodborne **CUSA03173, update 1.09**. In the setup wizard, point to your existing game folder or use the built-in downloader. Keep your profile, custom save folder and user mods when updating.

Use the same BBGL version on every PC. Connect to one LAN or VPN (such as Tailscale or Radmin), check connectivity in the launcher and summon with the game’s bells. The P2P path works without a separate server, account or invite code. The ZIP includes the mod and runtime. Game files are obtained separately.

## Known limits

The two-player tests confirmed reunion visibility, the tested NPC movement and combat scenarios, Chalice lamps and first-layer progress, and the return to separate worlds after Gehrman’s ending. The guest’s NG+ counter on a repeated transition and a missing Mergo’s cord in NG+ are still open. Other endings, rare reward cases, larger parties and the GPU fix’s effect on the reported in-game crash need further coverage.

---

## Русский

В BBGL 1.3.0 входит BBSC-GL 1.3.0. Охотники в одной группе могут перемещаться по отдельности, снова встретиться и продолжить игру вместе.

### Совместная игра

- В общей сессии можно по отдельности пользоваться лампами, надгробиями и алтарями чаш. Переходы выполняет игра, а при новой встрече она снова создаёт персонажей напарников. Зажжённые лампы общие. У каждого охотника свой Сон с личной мастерской и магазинами.
- ИИ, движение и урон NPC используют сетевую логику игры. Убран полный обход памяти при подключении для восстановления состояния врагов. Масштабирование HP врагов и боссов использует штатный пересчёт характеристик.
- В подземелье хоста у группы общий список ламп. Лампа, зажжённая гостем, появляется у алтаря хоста, даже когда хост находится в другой локации. В проверенном сценарии прогресс первого слоя сохраняется при возвращении в чашу.
- Перед финалом группу можно собрать в Сне охотника. После общей концовки каждый начинает в своём Центральном Ярнаме. В проверенном переходе игра закрыла общую сессию во время загрузки без сообщения о потере связи.
- Награды боссов основной игры и DLC выдаёт сама игра. Убрана вторая общая очередь наград. Также уточнён выбор лампы возрождения, исправлены проверенные сценарии пятна крови при смерти гостя в одиночку, выхода в главное меню и прыжка гостя к Ром.

### Лаунчер и порт

- Переключатель «Собственный Сон охотника» убран из настроек. В кооперативе Сон всегда личный.
- На затронутых пресетах частоты кадров для версии игры 1.09 движущиеся платформы и персонаж используют один шаг физики. В порте также исправлена гонка при отправке команд GPU, воспроизведённая в целевой проверке.
- Уровень журналирования GPU, заданный в профиле, сбрасывает унаследованные исключения для отдельных классов, если профиль явно их не задаёт. В новом профиле подробные логи, исследовательский режим, профилирование, Vulkan validation и читы выключены.

### Установка и обновление

Распакуйте `bbgl-1.3.0-windows-x64.zip`, откройте папку **Bloodborne Game Launcher** и запустите **Bloodborne.exe**. Нужны Windows x64, драйвер Vulkan и Bloodborne **CUSA03173 с обновлением 1.09**. В мастере укажите готовую папку игры или воспользуйтесь встроенной загрузкой. При обновлении сохраните профиль, свою папку сохранений и пользовательские моды.

Установите одинаковую версию BBGL на все ПК. Подключитесь к одной локальной сети или VPN, например Tailscale или Radmin, проверьте связь в лаунчере и используйте игровые колокола. Для P2P не нужны отдельный сервер, аккаунт или код приглашения. Мод и библиотеки входят в ZIP. Файлы игры загружаются отдельно.

### Открытые проверки

На двух игроках подтверждены видимость при повторной встрече, проверенные сценарии движения и боя NPC, лампы и прогресс первого слоя чаши, а также переход в отдельные миры после концовки с Германом. Остаются открытыми номер цикла гостя при повторном переходе в NG+ и пропажа пуповины Мерго в NG+. Другие концовки, редкие случаи с наградами, большие группы и связь исправления GPU с зарегистрированным вылетом требуют дополнительной проверки.
