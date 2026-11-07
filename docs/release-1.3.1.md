# BBGL 1.3.1

This update includes BBSC-GL 1.3.1 and focuses on co-op story events, personal NPC quests, and stability when players travel independently.

- The party can trigger the cutscene at Amelia’s skull from a guest’s interaction. Players on the same map enter the cutscene, while players elsewhere receive the world phase. A three-profile run confirmed this behavior with the third hunter in the Hunter’s Dream.
- The post-Rom cutscene uses the same native continuation. Targeted tests covered both roles and the transition to Yahar’gul after the cutscene.
- Guests can advance personal NPC quests through the game’s triggers. In the tested Eileen quest, the guest advanced their own quest after using the stairs and received credit for the party’s victory over Henryk. Map and Dream snapshots exclude personal quest flags, pickup receipts, and personal shop data.
- The port increases the game’s 14 MiB network heap profiles to 16 MiB in co-op. In the retest, the third player visited the Dream and returned to Cathedral Ward in the same session. The mod also detaches an old remote character from the game’s movement queue before recreating it. The two-player transition and a three-player reunion were tested.
- Offline mode hides co-op connection fields. The update button now sits in the side rail, and longer notices can scroll below the launch controls.

### Install or update

Extract `bbgl-1.3.1-windows-x64.zip` and run **Bloodborne.exe**. Use Windows x64, a Vulkan-capable driver, and Bloodborne **CUSA03173 with update 1.09**. Keep your profile, saves, and custom mods when updating. All co-op players need the same BBGL version and a shared LAN or VPN. The archive includes the mod and runtime. The setup wizard handles the game folder separately.

### Open checks

The shared post-Rom cutscene still needs an in-game retest on the updated DLL. The original three-player crash route with hunters on three different maps also remains open. The repeated NG+ counter and a missing Mergo reward in NG+ are still under investigation.

---

## Русский

В BBGL 1.3.1 входит BBSC-GL 1.3.1. В обновлении доработаны сюжетные сцены, личные квесты NPC и устойчивость сессии при самостоятельных перемещениях.

- Гость может запустить общий ролик у черепа Амелии. Игроки на той же карте видят ролик, а игроки в других локациях получают смену фазы мира. Это проверили на трёх профилях, один из которых находился в Сне охотника.
- После Ром общий ролик продолжает штатное событие игры. На стенде проверили обе роли и переход в Яаар’гул после ролика.
- Штатные триггеры продвигают личные квесты гостей. В проверенном сценарии гость прошёл лестницу, продвинул свой квест Айлин и получил зачёт общей победы над Хенриком. Из сетевых снимков карт и Сна исключены личные флаги квестов, отметки подбора предметов и данные личного ассортимента.
- В кооперативе сетевой пул игры увеличен с 14 до 16 МиБ для профилей, использующих меньший объём. При повторной проверке третий игрок посетил Сон и вернулся в Соборный округ в той же сессии. Перед пересозданием персонажа напарника мод отвязывает его старую модель от очереди движения. Проверили переход вдвоём и повторную встречу втроём.
- В офлайн-режиме скрыты поля подключения. Кнопка обновления перенесена на боковую панель. Длинные уведомления можно прокручивать под кнопкой запуска.

### Установка и обновление

Распакуйте `bbgl-1.3.1-windows-x64.zip` и запустите **Bloodborne.exe**. Нужны Windows x64, драйвер Vulkan и Bloodborne **CUSA03173 с обновлением 1.09**. При обновлении сохраните профиль, сохранения и пользовательские моды. Для кооператива установите одинаковую версию BBGL на все ПК и подключитесь к одной локальной сети или VPN. Мод и библиотеки входят в архив. Папку игры можно выбрать в мастере.

### Открытые проверки

Общий ролик после Ром ещё предстоит повторить в игре на обновлённой DLL. Открыт точный повтор вылета при переходе, когда трое охотников находятся на разных картах. Также остаются открытыми номер повторного цикла NG+ у гостя и случай пропажи пуповины Кормилицы в NG+.
