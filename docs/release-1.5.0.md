# BBGL 1.5.0

Includes [BBSC-GL 1.5.0](https://github.com/mark3317/bbsc-gl/releases/tag/v1.5.0) and its matching Party runtime.

- **Boss retries.** After a team wipe, players in the same encounter wait for the last death sequence before reloading. Amelia’s temporary attempt flags are cleared during the normal load, and the fog gate uses the game’s role checks and collision.
- **Chalice Dungeons.** A guest can join an open room after its boss is defeated. When a team reloads after a wipe, the fallback lamp selection stays within the current layer.
- **Guest travel and departures.** The mod preserves each guest’s own lamp for the return home and can select a lit lamp on the current map if the shared checkpoint belongs to another map. The Silencing Blank can list eligible guests on other maps and still supports the game’s original confirmation flow.
- **Co-op notifications and personal progress.** Party forwards confirmed Beckoning Bell uses through its existing presence exchange. Introductory Insight receipts for Amelia and Rom stay personal when world flags are shared.
- **Trophies.** Choose Card or Corner in the launcher and the in-game overlay. Profiles using the old banner or basic card move to Card. The card supports the platinum animation and adjustable intensity.
- **Diagnostics.** The port can report the Scaleform pool state on a matching crash during a Chalice ritual. The cause of the reported crash is still under investigation.

### Install or update

Close the game and launcher, extract `bbgl-1.5.0-windows-x64.zip` and run **Bloodborne.exe**. Keep your profile, saves and custom mods. Use Windows x64, a Vulkan-capable driver and **Bloodborne CUSA03173 with update 1.09**. Install BBGL 1.5.0 on every PC in the group and connect to the same LAN or VPN.

### Gameplay coverage

Development builds were tested in game with three local profiles. The runs covered Amelia’s team wipe and spectator view, the return to a personal lamp, a departure using the Silencing Blank and a late summon into a cleared Chalice Dungeon. The final ZIP still needs a live co-op run and an in-game visual check of trophy notifications in both languages. A Rom wipe with a previous checkpoint on another map and the display of repeated bell notices still need confirmation.

## Русский

В комплекте [BBSC-GL 1.5.0](https://github.com/mark3317/bbsc-gl/releases/tag/v1.5.0) и совместимая версия Party.

- **Повторные попытки у боссов.** После общей гибели участники одного боя ждут завершения последней анимации смерти перед загрузкой. Временные флаги попытки Амелии сбрасываются при штатной загрузке, а у тумана действуют штатные проверки роли и коллизия.
- **Подземелья чаш.** Гость может присоединиться к открытой комнате после победы над боссом. Если после общей гибели нужна резервная лампа, игра выбирает её в пределах текущего слоя.
- **Переходы и выход гостей.** Мод сохраняет личную лампу гостя для возвращения домой. Если общая точка относится к другой карте, при возрождении доступна местная зажжённая лампа. Бланк молчания может показать доступных гостей с других карт и сохраняет штатное подтверждение.
- **Уведомления и личный прогресс.** Party передаёт подтверждённые звонки Зовущего колокола через существующий обмен данными о присутствии. Отметки о выдаче озарения при первой встрече с Амелией и Ром остаются личными при обмене флагами мира.
- **Трофеи.** В лаунчере и игровом оверлее доступны «Карточка» и «В углу». Старый баннер и обычная карточка переходят на «Карточку». Для неё доступны анимация платины и настройка интенсивности.
- **Диагностика.** Порт записывает состояние пула Scaleform при совпадении с известной сигнатурой вылета во время ритуала чаши. Причина вылета ещё выясняется.

### Установка и обновление

Закройте игру и лаунчер, распакуйте `bbgl-1.5.0-windows-x64.zip` и запустите **Bloodborne.exe**. Сохраните профиль, сохранения и пользовательские моды. Нужны Windows x64, драйвер с Vulkan и **Bloodborne CUSA03173 с обновлением 1.09**. Для кооператива установите BBGL 1.5.0 на всех ПК и подключитесь к одной локальной сети или VPN.

### Игровые проверки

На промежуточных сборках с тремя локальными профилями проверены общая гибель на Амелии и наблюдение за напарником, восстановление личной лампы, выход через Бланк и поздний призыв в зачищенную чашу. Игровой прогон итогового ZIP и визуальная проверка уведомлений о трофеях на обоих языках ещё впереди. Общая гибель на Ром при предыдущей точке с другой карты и показ уведомлений о повторном звоне требуют подтверждения.
