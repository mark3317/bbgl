# Serverless I/O: исправление выявленных расходов —03.11.2026

BBSC68035a2. Работа начата по просьбе «правки, после не собирай»: сначала только
исходники/Python проверки, без компиляции нативного кода. Позднее пользователь
явно разрешил «собери и установи после». После этого выполнены native fixtures
и запущена DLL build. Установка остаётся отдельным статусом ниже/HANDOFF.

## Что изменилось

- Private HTTP backlog128, HTTP/1.1 keepalive и ограниченное idle ожидание.
- PartyObserve guarded до вычисления аргументов: legacy не делает новых
  game-memory/SpEffect reads на tick. Обычные NPC/params/scaling guards сохранены.
- Один /party/tick вместо2–3 HTTP RPC. Native state, can_beckon и текущий
  awaiting-title ACK объединены. Leave predicate считается лишь для ожидающего
  выхода; Бланк сам не включает вечный polling. Native кеш отклоняет старый
  cancel_seq, HTTP ошибку/неполный ответ. WinHTTP session/connection переиспользуются
  per thread, response дочитывается полностью. Cancel title снимает ожидание.
- Сокетные connect/send в независимых bounded workers по peer; control priority,
  coalesce одинаковых ещё queued bytes. Медленный peer не держит Engine.lock.
- Disk writer вне Engine.lock, очередь256 и coalescing cumulative snapshots.
  Подтверждения отправляются лишь после durable ticket. Подтверждённость ревизии
  привязана к её final ticket, не к более поздней записи счётчика/ACK metadata.
  Disk error не разрешает роль/выход. Immutable copies снимаются под lock,
  fsync/replace выполняет worker. Native game thread I/O не добавлен.
- Relay watermarks выделены в party-relay-journal.json. Старые поля мигрируют
  до удаления из control journal. На каждый кадр больше не записывается весь
  state/proposal/results журнал. Durable ACK означает ingress, не native apply:
  прежнее ограничение exactly-once через crash между ingress/apply сохраняется.
- Window16 на peer, bounded backlog128, per-recipient sequence и stream
  (process incarnation, transport generation). Receiver reorder buffer16,
  cumulative ACK contiguous durable prefix. Parts individually ordered; никаких
  coalescing WorldFlags по типу. Адресные пропуски и новая connection не создают
  дыр в sequence. Старые stream/поколения не проходят. RTO по RTT/backoff вместо
  фиксированного80ms; expiry10s не освобождает owner.
- Отдельный event-driven relay dispatcher вместо shared monitor sleep50ms.
  Lifecycle monitor не ждёт command8s: poll async maintenance command. State
  deepcopy только при новой confirmed revision, routing читает immutable state
  под lock без полного snapshot. Бounded очереди и permission guards сохранены.

## Целевые проверки

Python, independent processes/isolated temp profiles: native contract; menu
leave/rejoin; close/recreate; concurrent bells; faulted multipart; coordinator
restart after durable commit; crash/partition restore; membership; wrong group/
sender/MAC/generation/coordinator; explicit close guest barrier; idle status
refresh/delete; pending recipient16/16 и idle0.

Новые Python fixtures: backlog128 даёт24/24 held-accept connects; HTTP1.1 одна
connection на несколько tick; current title ticket до/после partition/final leave;
64 ordered parts при delay/reorder/duplicates/loss; recipient gaps и новый stream;
blocked disk не блокирует snapshot и не выпускает ACK; coalesced durable receipts;
restart dedup; legacy receipt migration; final state/result не виден до durable
write; disk failure не подтверждается; slow peer не блокирует fast peer. PASS.

После нового разрешения на сборку: production tick gate (1000 disabled ticks0
reads), production menu/save fixture с party gate (60s не обходят ACK), actual
WinHTTP bridge+independent clients с partition и native process fence — PASS.
Python syntax/diff checks PASS. Полный discover/release audit не запускался.

## Ограничения

Все party peers обновлять вместе: новые stream/window поля требуют нового
engine у получателя и отправителя. Legacy запуск с прежним сервером не изменён.
Политики journal/role/native datagrams/vports и запрет menu load до ACK сохранены.
Фактическое использование Зовущего всё ещё ждёт unanimous role в callback
(до8500ms fail closed); async replay goods execution отдельно не вводился.
Это оптимизация source/data path, не измеренный FPS gain или WAN benchmark.
Полные→delta world snapshots и dirty native progress journals сюда не входят.
