# Выход активного хоста через меню —03.11.2026

Прогон08:26–08:37 МСК, BBGLc743e19/BBSC68035a2.
Сбор out/coop-dev/runs/serverless-review-20261103-083725: оба устройства,
warnings0/ChangedDuringCopyfalse, native runner exit0. Это не доказательство
успешного menu exit хоста: пользователь сообщил потерю управления/зависание,
и финального permitting title load в проблемном интервале нет.

## Подтверждено

Три JoinRoom ноутбука к ПК rev80/86/94, каждый дошёл до state6/phase4.
Два menu leave гостя08:31:43 и08:33:43 дали final leave ACK и title через~2s;
после первого тот же клиент вошёл снова. Ошибка старого cancel не повторилась.

При menu exit активного ПК08:35:25: native save completed, Stop, members drain,
Native state0 к08:35:26.189; group closing95→guest removed96→roomnull97.
Далее waiting for final party leave, ownerMarkPC остался; title не запущен.
Host explicit SessionLeave клиент получил08:35:24.534 (часы устройств имеют
сдвиг, абсолютный causal порядок подтверждается пакетами/ревизиями, не ms).
Клиент остановил matching, native state0 к08:35:26.492; native send-home
произошёл08:35:39.882, cleanup дома08:35:42.136 (~17s после SessionLeave).

## Причина/исправление

Adapter release и leave_ready требуют !bell. Native при menu exit может
сохранить Beckoning SpEffect до title unload, а title теперь ждёт release:
получается цикл. Фактический bridge body старый лог не сохраняет; это вывод
из согласованного state0/roomnull/owner-held и воспроизводимого code path,
не прямой замер значения SpEffect в логе.

Введён native_leave_idle: native свежий, loading=false, state0/2/5; старый bell
не мешает ТОЛЬКО для await_title и текущего положительного cancel_seq. Pending,
joined/members/departing, final revision/durable ACK и no-owner барьеры прежние.
Idle/ringing без явного текущего menu ticket не освобождает роль. Отмена после
полного drain погашается, и ready продолжает признавать тот же title ticket.

Для клиента старый15s резерв ожидал native send-home, который в прогоне был
поздним. Явный проверенный SHAD SessionLeave от текущего host теперь отмечается
отдельно от generic peer-left/EOF. После native teardown (state0 вне своего
мира, loading=false) fallback начинает возврат через1s вместо15s. Общая потеря
связи сохраняет15s, active/rejoin/menu/death/finale safeguards прежние. Вызовы
нативного возврата и его claim тот же; поздний native callback не делает второй
load. Метка сбрасывается дома/в новой сессии, старый leave не ускоряет новый.

## Проверки

Независимые native NP/HTTP clients: idle+bell не release; loading+current title
не ACK; host menu при живом госте не ACK; после guest LeaveRoom полный drain,
release owner и current title ACK несмотря на retained bell. PASS. Combined
RPC/partition/current ticket и menu/rejoin regressions PASS (3).
Production C++ fallback/hook: explicit host fast1s, generic loss15s, loading/
menu guards, поздний native callback не делает двойной load, новая поездка не
наследует старую метку PASS. Resident guest protection PASS. Return-order checks
PASS4 (существующий source-only check был untracked baseline, обновлена только
ожидаемая строка grace, в коммит целиком не включался).

BBSCf56a960. Actual game verification новой правки pending; скорость загрузки
самой карты не равна1s, это только grace до запроса native transition.
