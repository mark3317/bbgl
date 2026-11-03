# Serverless: menu leave → rejoin same guest, 03.11.2026

Последний прогон BBGL354675c/BBSC7872819,07:21–07:32 МСК.
Сбор out/coop-dev/runs/serverless-review-20261103-073431: оба процесса закрыты,
оба exit0, warnings0, ChangedDuringCopy=false. Сейвы/приглашения не собирались.
Первый вход к ПК состоялся, compact30/4 marker есть. После смены хозяина
ноутбук также отправлял compact; ПК дошёл до state6/phase4. Первый этап
уменьшения WorldFlags подтверждён в игре по обоим направлениям, не по FPS.

## Сбой

07:28:51 гость выходит через native menu. Хост уже получил explicit SessionLeave,
NP LeaveRoom/room_close/drain прошли: rev43 closing,44 guest removed,45 roomnull.
Дублировать Бланк перед меню не требуется: сообщение явного выхода было.

07:29:21 новая комната100663302, rev47 pendingMarkLaptop. JoinRoom отклонён
One outstanding command per member, затемrev48 pending удалён. В07:30:21
повторилось с room100663303/rev51→52. При смене хоста вход ПК прошёл rev58.

Причина в adapter: release_intent/observed и cancel_floor гостя не завершали
жизненный цикл после final LeaveRoom. Новый claim при idle native и старом
cancel запускал admission_cancel из monitor параллельно JoinRoom. Получалась
коллизия локальных операций, а не недостающий SessionLeave или потеря WorldFlags.
Owner acquire/release уже сбрасывал этот latch, поэтому смена роли помогала.

## Исправление

После final выхода, отсутствия guest в pending/joined/members/departing,
отсутствия локальной незавершённой команды и свежего native idle без loading/bell
снимается гостевой release_intent, observed=false, cancel_floor=latest_cancel.
Операция не освобождает owner и не меняет журнал группы. Номер cancel остаётся
монотонным. Новая отмена pending admission проверяется даже если observed=false
после старой поездки. Loading/active membership/recovery не позволяют ранний reset.
Обновления native/cancel и retirement согласованы gate_lock.

## Проверки

Независимые процессы, настоящие private NP/HTTP: join→menu cancel while loading→
LeaveRoom→idle→новая комната того же хоста→новый claim остаётся pending→JoinRoom
успешен→второй cancel/leave→новая pending отменяется новым cancel после loading.
PASS. Два прямых contract сценария (полный compatibility и close/recreate) PASS.
Итого3 tests/18.2s. Только Python adapter; DLL7872819 актуальна, rebuild не нужен.
Живой menu/rejoin после исправления требует повторного прогона.

## Уточнение пользователя: подтверждение до загрузки меню

Пользователь потребовал подтверждать выход гостя до загрузки главного меню.
Дополнение BBSCeab2dc2 после первой Python-правкиa58870b:

- После успешного native save и Stop меню остаётся в pending.stopping; native
  idle теперь недостаточен для OnReturnTitle. Переход проходит PartyTitleReady.
- Подтверждение запрашивается worker через local /party/leave_ready, game tick
  читает только атомарный cache. Body содержит текущий cancel_seq; API проверяет
  свежий native idle, совпадение sequence, final group revision, отсутствие
  pending_local и самого игрока в owner/pending/joined/members/departing.
- Каждый выход вооружает новый cancel_seq даже при уже idle native. ACK от
  прошлого Бланка/меню не подходит; просроченный cache и HTTP ошибки запрещают
  переход. Таймаут ожидания не заменяет подтверждение. Legacy bypass сохранён.
- В логе появляются waiting for final party leave / final party leave confirmed
  перед permitting title load. Меню/движение удерживаются штатным quit guard.

Production menu fixture с BBSC_MOD gate PASS: save→disconnect→idle без group ACK
не вызывает title, даже через60s; после ACK вызывает. Existing save failure,
role/slot guards и menu movement ограничения также PASS в этом fixture.
Реальный WinHTTP bridge +2 независимых клиента PASS: guest joined, native idle,
leave при network partition не разрешает title; после reconnect и final leave
ready появляется; следующий cancel мгновенно инвалидирует старый ACK.
Повторный guest menu/rejoin lifecycle PASS. Это не игровой результат.
DLL пересобирается для этого дополнения; первый Python delta уже был установлен
до уточнения пользователя. Пользователь закрыл обе игры для установки новой DLL.
