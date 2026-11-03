# Serverless data reduction: первый этап, 03.11.2026

BBSC7872819. Реализовано в экспериментальном подмодуле:

- Status содержит только sign. Native state остаётся локальным. Убраны remote
  placement/relay_id без потребителей; native connection binding сохранён.
- Publish идентичного sign не создаёт новую revision; отправка при изменении,
  epoch/generation change и каждые2s. При повторном подписанном status с той же
  incarnation/seq и тем же телом обновляется freshness.2s меньше3s control socket
  idle timeout; вариант3s отвергнут после проверки удаления объявления.
- Session-only BBSC types0x22..0x2d направляются owner+room members+pending+
  joined+departing. Discovery/follow/matching/placement и неизвестные типы
  сохраняют рассылку группе. Lite engine по умолчанию сохраняет прежнюю generic
  рассылку; adapter задаёт recipients для настоящих BBSC envelopes. Все части
  WorldFlags идут отдельно, выбранные адресаты участвуют в transport ACK.
- В party native sender default использует WorldFlags v5 (обычные карты) иv6
  (чаши с key+loader revision):30 групп/4 чанка вместо40/5.10 групп kind5 хоста
  нужны только diagnostic diff. BBSC_WORLD_DIAGNOSTICS=1 возвращает полный
  wire format; research logs сами по себе компактность не отключают.
- Приёмник читает старые v1/v2/v3/v4 и новые v5/v6 с проверкой точного числа
  частей/групп, карты и dungeon identity. Legacy launch отправляет прежний формат.
  Приглашённые party peers должны обновляться вместе: старый DLL v5/v6 не читает.
- Удалён неиспользуемый bbsc_world_ready; world_blocks остаётся canonical cache,
  Dream ready сохранён. Убраны два неиспользуемых Python поля.

Проверки: native compatibility contract и close/recreate2 PASS; новые независимые
клиенты: pending guest получает16/16 частей, idle peer0; routing test PASS;
status13s unchanged refresh/delete и отсутствие native fields PASS; faulted chunk
transport PASS; crash/partition restore PASS. Production C++ sender/receiver,
старые/новые shapes, incomplete/malformed chunks и dungeon revisions PASS через
расширенный tools/test_chalice_scope.py. Тест компилируется MSYS clang++, PATH
должен включать C:/msys64/clang64/bin для runtime DLL. Не полный suite.

Ожидаемая экономия: WorldFlags fixed1018B ×5→×4 =20% этого потока; одинаковый
status8.3/s→0.5/s (~94% периодических повторов), плюс публикации при изменении.
Не замер общего трафика/FPS. Для двух активных игроков адресация не уменьшает
число адресатов; выигрыш возникает при свободных игроках в большем roster.

Без изменений: native datagram boundaries/vports/signaling, unanimous durable
role protocol, personal loot/own-world/ledger/shared-progress, relay ingress
fsync и full snapshots1Hz. Delta snapshots, dirty journals, binary wire и
разделение durable control/relay persistence остаются следующими этапами.

Игровая проверка: новый вход ПК host/ноут guest, подтверждение compact marker
в host log и полного world load; menu leave/rejoin; cancel и смена хозяина.
Обычная игра/прогресс требуют пользовательского прогона.
