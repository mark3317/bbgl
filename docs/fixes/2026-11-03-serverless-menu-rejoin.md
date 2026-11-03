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
