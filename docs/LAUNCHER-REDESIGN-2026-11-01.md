# Редизайн лаунчера — 01.11.2026

Код: `cb583ea`. Сборка и установка на этом ПК завершены в 06:23 МСК.

- Главная: Bloodborne Game Launcher, два запуска, имя и профиль сохранений.
  Фоны пользователя для главной/настроек; прежняя цветовая гамма сохранена.
- Мастер: игра и сохранения с редактируемыми путями → необязательный кооператив →
  графика и ярлык Bloodborne → Завершить (без запуска игры).
- Настройки: FPS в Экран, одиночные/технические параметры объединены и скрыты
  за тонкими настройками, подписи переносятся, русские описания сокращены.
- Кооператив: переключатель клиент/хост; единое поле имени при редактировании
  записывает coop_name и player_name. Старые разные имена автоматически не меняются.
  Ошибка старта хоста при отсутствии Tailscale содержит ссылку скачивания.
- Удалены локальный ZIP/PKG-установщик, его тесты и упаковка extractor.
  Скачивание игры сохранено, использует выбранную папку и не заменяет существующую.

Проверки: 29 целевых unittest PASS (setup/startup/defaults/redesign/download).
Русский QML в 1290×830 и 1050×650 визуально проверен, предупреждений 0.
Полная build-coop-package.sh, verify-release и проверка состава ZIP PASS.
Frozen smoke staging и установленной копии PASS: экраны, роль хоста, завершение
мастера без запуска игры. Использованы отдельные временные профили.
Реальный игровой запуск и соединение двух игроков в этой задаче не выполнялись.

Установка: `D:/Games/Bloodborne/Bloodborne Game Launcher`.
Проверено 5219 файлов, заменено 19, bundle manifests PASS.
Бэкап: `D:/Games/Bloodborne/coop-dev/backups/launcher-lifetime-20261101-062339`.
Старый extractor и кеш его ZIP перенесены в
`D:/Games/Bloodborne/coop-dev/backups/ui-redesign-retired-20261101`.
Пользовательские настройки, сейвы и файлы игры не заменялись. Ноутбук не обновлялся.
Launcher SHA256: `81A8B9195E7D7D6D8A80688EADA9E5A07E1739EDBEEE5C58688E68A0538D9CCA`.
BBSC SHA256: `149004471A5B7C00D611B0FB5DDBA890C30BA5C02D3A1E06EDDB7D04E8136636`.

Артефакты: `out/redesign-build.log`, `out/redesign-preview/`,
`out/redesign-preview-small/`, `out/redesign-installed-smoke/result.json`.


## FSR и начальная настройка — 08:07 МСК

Код `3623f51`: FSR 4.1.1 удалён из Windows-лаунчера и обоих игровых списков
(числовые ID других апскейлеров сохранены). FSR 4 доступен только при полном наборе
непустых v07 assets; native дополнительно проверяет поддержку GPU. Старое значение
fsr411 нормализуется в off. По умолчанию и во всех пресетах upscaler=off.
Последний этап мастера включает масштабирование с зависимыми полями и общей
кнопкой загрузки/удаления FSR 4. Удаление касается только manifest-файлов;
выбранный FSR 4 предварительно выключается. Посторонние файлы остаются.

Целевые проверки defaults/presets/полноты assets/удаления PASS, QML warnings=0.
Полная сборка порта и пакета/verify PASS. Установлено только на ПК, 5220 файлов
проверены, 12 заменены с бэкапом, bundle manifests PASS. Installed QML smoke PASS.
Реальное игровое меню и качество масштабирования в игре не проверялись.
Бэкап: D:/Games/Bloodborne/coop-dev/backups/launcher-lifetime-20261101-080702.
Лог: out/fsr-availability-build.log.


## Итоговая сверка и установка на ноутбук — 09:12 МСК

Последний коммит программных изменений: `596f213af82fd87acca037d5c06fdfd0fbf23be4`.
Все доработки интерфейса в этом чате закоммичены; последующие изменения этого
отчёта относятся только к документации. Существующие сторонние/пользовательские
изменения рабочих деревьев не включались в коммиты.

Проверка актуальности выполнена без повторной пересборки:
- 15 Python-модулей внутри замороженного Bloodborne.exe и его main-code совпали
  с текущими исходниками (сравнение code objects, игнорируются только пути файлов).
- Все 21 QML/служебный файл каталога launcher/qml побайтно совпали с исходниками.
- 5220 программных файлов staging, dist/bbgl-windows.zip и установленного ПК
  совпали по SHA256. Профиль, сейвы и пользовательские моды исключены из замены.
- Архив передан на ноутбук; SHA256 архива проверен до распаковки.
- На ноутбуке проверены все 5220 программных файлов и четыре файла встроенных
  модов подсказок кнопок. Client/server bundle manifests PASS.
- Installed frozen QML smoke на Windows 10 PASS, warnings=0, завершение мастера
  не запускает игру; после smoke процессов игры/лаунчера нет.

Установка: C:/Games/Bloodborne/Bloodborne Game Launcher (DESKTOP-73Q9JB7).
Проверено 5220 программных файлов, заменено 25.
Бэкап: C:/Games/Bloodborne/coop-dev/backups/launcher-lifetime-20261101-091058.
Старый PKG extractor перенесён в
C:/Games/Bloodborne/coop-dev/backups/retired-pkg-extractor-20261101-091232.
Smoke: C:/Games/Bloodborne/coop-dev/runs/latest-ui-20261101-091232.
Launcher SHA256 обеих машин:
`BC83E4373F62C0DF3DFC079E03EFD55C88B9F5873FED5942359B26245AA53A6D`.
BBSC SHA256 обеих машин:
`76B8A66D4353E3C476CE424156F937B4546F076E2E6054F6FC543C97CB5BBD53`.

Сохранены все последние изменения: графическая сводка списком; вкладки режима
над запуском; имя игрока всегда на главной и автозаполнение из папки сейва в
мастере; независимые от масштабирования/генерации названия пресетов; проверка
DLSS до создания первого окна; FSR 4 по наличию полного набора ресурсов,
удаление ресурсов и отсутствие FSR 4.1.1 в меню; компактный кооператив и действия
сервера/брандмауэра; перегруппированные настройки и новые описания.
Игровой прогон и реальное сетевое подключение этим smoke не подтверждаются.

Локальные доказательства: out/latest-build-audit.json,
out/latest-program-manifest.json, out/home-facts-build.log.


## Кнопка отмены и брандмауэр — 01.11.2026 16:30 МСК

BBGL b8fb563: Играть заменяется контурной Отменить на время подготовки;
отмена подавляет отложенный запуск кооператива или завершает job подготовки.
Кнопка брандмауэра сохранена только в настройках, скрыта на главной и в мастере.
При ошибке брандмауэра открывается модальный диалог с описанием и подтверждением.
13 целевых defaults/startup tests PASS; QML source/staging/installed smoke PASS,
warnings=0. Состояния подготовки и ошибки в smoke моделировались; реальную игру
и изменение правил брандмауэра не запускали.
package.sh / verify-release PASS; установлено на ПК, 16 замен, 5223 файла,
client/server manifests PASS. Бэкап launcher-lifetime-20261101-162948.
Скриншоты: bloodborne_pc/out/launch-ui-installed-smoke/{cancel,firewall,home,settings}.png.
Ноутбук не обновлялся, настройки и сейвы не менялись.


## 2026-11-02 — home typography and preset selector installed on PC

Launcher code d1a0b7c: EB Garamond bundled with OFL, compact home summary,
connection panel background removed, player-name divider always visible;
serif home labels, Custom preset preserves current values, transparent preset
selector with active underline. Nine targeted graphics-preset tests passed.
package.sh BB_FAST_DEPLOY=1 completed exit=0, log out/launcher-ui-build.log.
Launcher-only deployment on PC completed: 2964 files, no file-content audit.
Backup: D:/Games/Bloodborne/coop-dev/backups/launcher-ui-polish-20261102-041137.
Installed frozen UI smoke PASS on isolated temporary profile, QML warnings=0;
host/client/offline fit at 1290x830; Custom retains graphics values.
Results: out/launcher-ui-installed-smoke. No game launch or real profile/save
changes; native game/mod files and laptop were not updated by this deployment.

## 2026-11-02 — same launcher UI installed on laptop

Transferred launcher-only archive from the successful d1a0b7c build, no rebuild.
DESKTOP-73Q9JB7 stopped; launcher-only copy exit=0, 2964 files replaced.
Backup: C:/Games/Bloodborne/coop-dev/backups/launcher-ui-polish-20261102-042411.
Installed frozen UI smoke PASS on isolated temporary profile: host/client/offline
fit at 1290x830, Custom preserves current graphics values, no QML warnings.
Laptop results: C:/Games/Bloodborne/coop-dev/runs/launcher-ui-smoke-20261102-042402.
No file-content audit, native mod/game replacement, real profile/save changes,
or game launch. Both PC and laptop now have this launcher UI revision.
