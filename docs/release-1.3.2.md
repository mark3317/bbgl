# BBGL 1.3.2

This update includes BBSC-GL 1.3.2 and improves co-op lifts, personal quest isolation, and boss rewards in Chalice Dungeons.

- Lifts use the current area's owner position when another player loads in. Once loaded, the game controls platform movement and lever interlocks. The Forbidden Woods lift was tested with two players, including the host arriving after the guest.
- The game's join snapshot and event messages preserve each hunter's personal quest state. The mod now records 17 personal flags when the game writes them, reducing the work done by two existing flag checks. The two ItemLot receipts still use the existing checks.
- Guests can earn Vermin from Chalice Dungeon bosses through the game's original League eligibility rules. Ordinary boss rewards were observed in co-op. Vermin eligibility and delivery were exercised in a test harness.

### Install or update

Extract `bbgl-1.3.2-windows-x64.zip` and run **Bloodborne.exe**. You need Windows x64, a Vulkan-capable driver, and Bloodborne **CUSA03173 with update 1.09**. The setup wizard lets you choose your game folder. Keep your profile, saves, and custom mods when updating. Every co-op player needs BBGL 1.3.2 and access to the same LAN or VPN. Party and the mod are bundled.

### Open checks

Guest interaction prompts may disappear after an in-place respawn. Rejoining restored lamp use in the observed run. In-game coverage of Vermin with the Impurity rune, personal flags across all maps, and the added in-game UI in both languages is pending. The effect on frame rate has yet to be measured in the same scene before and after the change. The three-player crash route and NG+ cases listed for 1.3.1 remain open.

---

## Русский

В BBGL 1.3.2 входит BBSC-GL 1.3.2. В обновлении доработаны лифты в кооперативе, личные квесты и награды боссов чаш.

- При загрузке карты лифт принимает положение из актуального снимка владельца локации, если он доступен. После загрузки движением платформы и блокировками рычагов управляет игра. Лифт в Запретном лесу проверили вдвоём, в том числе при прибытии хоста к гостю.
- Штатные снимки при подключении и сетевые сообщения событий сохраняют личный прогресс каждого охотника. Мод теперь учитывает 17 личных флагов в момент их записи игрой. В двух существующих проверках стало меньше работы. Две отметки выдачи предметов по-прежнему проходят через прежние проверки.
- Для гостя в чашах игра выдаёт «Паразита» за боссов по исходным условиям Лиги. Обычные награды наблюдали в кооперативе. Условия и выдачу «Паразита» проверили на стенде.

### Установка и обновление

Распакуйте `bbgl-1.3.2-windows-x64.zip` и запустите **Bloodborne.exe**. Нужны Windows x64, драйвер Vulkan и Bloodborne **CUSA03173 с обновлением 1.09**. Папку игры можно выбрать в мастере. При обновлении сохраните профиль, сохранения и пользовательские моды. Всем участникам кооператива нужны BBGL 1.3.2 и общая локальная сеть или VPN. Party и мод уже в архиве.

### Открытые проверки

У гостя после возрождения на месте могут пропасть подсказки взаимодействия. В наблюдавшемся прогоне повторный вход восстановил доступ к лампе. Открыты игровые проверки выдачи «Паразита» с руной «Нечистота», личных флагов на всех картах и добавленного игрового интерфейса на двух языках. Влияние на FPS ещё предстоит измерить в одинаковой сцене. Сценарий вылета при игре втроём и случаи NG+ из описания 1.3.1 остаются открытыми.
