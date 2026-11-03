# Serverless: третий игровой прогон, 03.11.2026 06:31–06:38 МСК

Стабильный сбор: out/coop-dev/runs/serverless-review-20261103-0638, оба устройства,
ChangedDuringCopy=false, warnings=0. Версии BBGL 8d40a47 / BBSC c1632ed.

После исправления HTTP UserId native JoinRoom прошёл: ПК state6/phase4/type1,
own_world0 в06:33:18; ноут state3/phase4, удалённый chr1/slot_type1 в06:33:20.
ПК принял 17 частей WorldFlags в06:33:08–11. Это подтверждает native вход и
вставку персонажей по логам; качество боя/прохождения пользователь не описал.
В06:34:30 гость вышел; хост остановил native сессию. В06:34:31 пришёл host
LeaveRoom, затем повторный CreateRoom в06:34:51 отклонён Not sole owner,
следующий LeaveRoom с protobuf default0 вызвал KeyError. В06:36:15 room=null,
но owner остался MarkLaptop. Смена владельца в этом прогоне не подтверждена.

Исправление: закрывающаяся комната после подтверждённого выхода гостей
удаляется при idle native, даже если старый эффект колокола ещё активен.
Владение миром сохраняется до явного cancel; idle/EOF не освобождают роль.
LeaveRoom с отсутствующим proto3 room_id означает0 и ничего не удаляет.
Каждая новая комната получает новый сохраняемый serial внутри room ID,
в том числе при пересоздании в том же поколении мира. Поздний LeaveRoom
старой комнаты отклоняется. Журналы прежней версии принимаются без reset.

Целевые проверки: production socket close→guest ack→idle with bell→recreate,
zero/stale LeaveRoom; admission leave/rejoin; explicit close drain — PASS (3).
Полный compatibility contract после изменения room IDs — PASS. Игровая
проверка повторного подключения/смены хозяина новой версии ещё требуется.
