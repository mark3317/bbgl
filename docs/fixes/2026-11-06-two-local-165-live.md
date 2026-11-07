# Два локальных профиля, 165 FPS: живая просадка 06.11.2026

Запрошены два существующих профиля без штатного ограничения 60 FPS,
с пределом 165. Запуск 21:06:48 МСК, native процессы стартовали 21:07:12:
Player 1 PID10540, Player 2 PID35580. Оба окна responding;
VideoOut подтверждает frame limit 165 FPS. Процессные overrides:
BB_FPS=uncap, BB_FPS_LIMIT=165, BB_VBLANK_HZ=0. Settings и сейвы не менялись.
Профильные EXE отсутствовали в установленной папке; запущен установленный
Bloodborne.exe --script с явными отдельными BBGL_PROFILE_DIR и портами
3658/3659, через существующий scripts/local_party.py / individual_party.

## Подключение и FPS

Player 2 стал хостом 21:08:31.769. Player 1 начал join 21:08:34.778,
перешёл state4→6 в 21:08:38.091; два охотника отмечены к 21:08:45.
До подключения, уже в мире: гость ~98–108 FPS, хост ~95–112 FPS.
После: гость сначала ~80–83, затем 21:09:32–57 ~48–61 FPS;
хост ~68–90 FPS. Ранние 165 FPS до загрузки мира не брать за базу.
Худший кадр гостя в окне 21:09:57 — 141.830 мс.

В этом запуске не задан BBSC_NATIVE_NPC_SYNC_TEST=1: обычные NPC hooks
активны. Настройки обоих профилей: BB_DIAGNOSTICS=1, TIMELINE=1,
PERF/frame/pacing=1, RESEARCH=0, net/Party diagnostics=0.
Поэтому это не повтор прежнего native NPC sync / diagnostic-OFF теста.

## Наблюдения и границы вывода

- Гость: рабочий набор 3605→12986→13052 MiB в последовательных минутных
  Memory reports; private committed 5625→5835→5851 MiB.
- Хост: рабочий набор 3595→3677→3696 MiB; committed 5695→5799→5813 MiB.
- VRAM обоих ~2.7–2.9 GiB. На ПК ~32 GiB RAM, снимок свободной памяти
  ~4.36 GiB. Нет данных hard faults/residency для доказательства paging.
- Гость: BBSC scopes ~2.7 ms/frame до join →4.4 сразу после →7.7–8.6
  позднее. SetFlag hook ~0.9→3.3 ms/frame, ~10 calls/frame;
  IsValidSos.Update ~2.1–2.3→3.1–3.4 ms/frame;
  NPC pass ~0.22→0.6–0.8 ms/frame. Хост BBSC ~3.7–4.6 ms/frame.
- Замеры scopes — elapsed time, включают ожидания/вытеснение и вложенную
  функциональную работу; сумма не является доказанным чистым CPU overhead.
  Название ResearchSetFlagHook не означает включённый research: RESEARCH=0,
  но хук обслуживает также личные флаги, разговоры, чаши и перемещения.
- В relay queue bytes=0, oldest_ms=0, dropped=0; сетевой backlog не виден.
- Сильная асимметрия памяти/замедления локализована на госте, похожа на
  предыдущий ноутбук-гость. Корень роста working set и затрат пока OPEN;
  не объявлять утечкой private heap или единственной причиной весь SetFlag.

## Сохранённые данные

out/coop-dev/runs/two-local-165-20261106-210648:
launch-165.py, run.json, player-*-runner/error.log.
live-snapshot-2111: collection.json и два player-*-native-live.log.
Снимок сделан во время работающих игр; он не окончательный сбор прогона.
Helper collection exit0/warnings0; native logs добавлены явно, поскольку
их метаданные времени записи при открытом файле могут отставать.
Никакой сборки/деплоя/остановки игр/изменения настроек или сейвов при анализе.
