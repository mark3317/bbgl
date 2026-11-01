# Player-facing descriptions shared by the launcher languages.
HINTS = {}
_DATA = '''upscaler|Reconstructs a higher-resolution image from fewer rendered pixels to improve performance.|Восстанавливает изображение высокого разрешения из меньшего числа пикселей для повышения FPS.
preset|Sets the internal rendering resolution. Higher quality gives a sharper image.|Задаёт внутреннее разрешение рендеринга. Чем выше качество, тем чётче изображение.
output_res|Sets the resolution of the image displayed on your screen.|Разрешение изображения, выводимого на экран.
frame_gen|Creates intermediate frames for smoother motion. May increase input latency.|Создаёт промежуточные кадры для более плавного движения. Может увеличить задержку управления.
frame_gen_multiplier|Sets how many frames are displayed for each rendered frame.|Число отображаемых кадров на один отрисованный кадр.
frame_gen_fit_display|Limits generated frames to your monitor's refresh rate.|Ограничивает генерацию кадров частотой обновления монитора.
hud_position|Places the HUD at the screen edges or inside a centred 16:9 area.|Размещает интерфейс у краёв экрана или в центральной области 16:9.
live_resolution|Allows internal resolution changes while playing.|Позволяет менять внутреннее разрешение во время игры.
sharpen|Enhances fine details and edges after upscaling.|Повышает чёткость деталей и контуров после масштабирования.
sharpness|Sets sharpening strength. High values may create bright edges.|Сила повышения резкости. Высокие значения могут создавать ореолы.
object_motion|Reduces ghosting around moving characters when upscaling.|Уменьшает шлейфы за движущимися персонажами при масштабировании.
model_lod|Sets the level of detail of distant objects.|Уровень детализации удалённых объектов.
vram_budget_mb|Sets when unused graphics resources are cleared. Low values may cause stutter.|Порог очистки неиспользуемых ресурсов видеопамяти. Низкие значения могут вызвать рывки.
show_fps|Displays the current frame rate during gameplay.|Показывает текущую частоту кадров во время игры.
effect_chromatic_aberration|Adds colour separation near the edges of the image.|Добавляет цветные контуры у краёв изображения.
effect_dof|Blurs objects outside the camera's focus.|Размывает объекты вне фокуса камеры.
effect_motion_blur|Blurs the image during fast movement.|Размывает изображение при быстром движении.
effect_ssao|Adds contact shadows in corners and between nearby surfaces.|Добавляет тени в углах и между близкими поверхностями.
effect_game_aa|Smooths jagged edges using the game's original anti-aliasing.|Сглаживает ступенчатые края средствами самой игры.
effect_dynamic_shadows|Enables shadows cast by moving lights.|Включает тени от движущихся источников света.
effect_ssr|Adds reflections of objects visible on screen.|Добавляет отражения объектов, видимых на экране.
fps_mode|Sets the target frame rate. Higher values require more performance.|Целевая частота кадров. Высокие значения требуют большей производительности.
frame_cap|Sets a frame rate limit when using unlocked frame rate.|Ограничивает FPS в режиме без фиксированной частоты кадров.
frames_ahead|Sets the render queue length. Lower values reduce input latency.|Длина очереди рендеринга. Меньшие значения снижают задержку управления.
fullscreen|Displays the game in fullscreen instead of a window.|Разворачивает игру на весь экран.
fullscreen_mode|Chooses between borderless and exclusive fullscreen.|Выбор между полноэкранным режимом без рамки и эксклюзивным.
display|Selects the monitor used to display the game.|Монитор, на котором будет открыта игра.
present_mode|Controls frame presentation, screen tearing and input latency.|Режим вывода кадров, влияющий на разрывы изображения и задержку.
hdr|Enables high dynamic range output on compatible displays.|Включает расширенный динамический диапазон на совместимых экранах.
game_dir|Folder containing the game's eboot.bin file.|Папка игры, содержащая файл eboot.bin.
user_dir|Folder used for your saves and player data.|Папка сохранений и данных игрока.
dlc_dir|Folder containing the separately installed expansion.|Папка отдельно установленного дополнения.
language|Sets the language of game menus and subtitles.|Язык меню и субтитров игры.
voice_language|Sets the voice language from the available audio tracks.|Язык озвучки из доступных звуковых дорожек.
player_name|Sets the player profile name.|Имя профиля игрока.
skip_intro|Skips logos and the opening movie.|Пропускает логотипы и вступительный ролик.
mouse_camera|Allows the mouse to control the camera.|Управление камерой с помощью мыши.
mouse_menu|Allows the mouse to select items in game menus.|Выбор пунктов игрового меню с помощью мыши.
mouse_sensitivity|Sets how quickly the camera responds to mouse movement.|Скорость поворота камеры при движении мыши.
mouse_invert_y|Reverses vertical mouse camera movement.|Меняет направление вертикального движения камеры мышью.
mouse_hide_cursor|Hides the cursor during gameplay.|Скрывает указатель мыши во время игры.
move_smoothing|Smooths changes of movement direction with the keyboard.|Сглаживает смену направления движения на клавиатуре.
debug_camera|Allows the camera to move freely. Cross + L3 or Space + Z.|Свободное перемещение камеры. Cross + L3 или Space + Z.
debug_menu|Enables the game's debug menu. Requires debug fonts.|Включает отладочное меню игры. Требуются отладочные шрифты.
cheat_no_death|Prevents health from dropping below 1 HP.|Не позволяет здоровью опуститься ниже 1 HP.
cheat_one_hit_kill|Defeats enemies with a single hit.|Позволяет побеждать врагов одним ударом.
cheat_stealth|Enemies cannot see you until you attack them.|Враги не замечают вас, пока вы не атакуете.
cheat_silent|Prevents enemies from hearing your movement.|Враги не слышат ваше передвижение.
cheat_rally_no_decay|Prevents recoverable health from fading over time.|Не даёт запасу восстанавливаемого здоровья убывать со временем.
cheat_enemy_control|Controls the targeted enemy with R3. Press L3 to return.|R3 — управление выбранным врагом, L3 — возврат к персонажу.
cheat_no_stamina|Removes stamina costs for actions.|Отключает расход выносливости при действиях.
cheat_stamina_out_of_combat|Removes stamina costs 8 seconds after your last attack or hit.|Отключает расход выносливости через 8 секунд после атаки или получения удара.
tweak_no_rally|Disables health recovery from counterattacks.|Отключает восстановление потерянного здоровья ответными ударами.
tweak_camera_distance|Moves the camera farther from your character.|Отдаляет камеру от персонажа.
tweak_no_camera_rotation|Disables automatic camera rotation while moving.|Отключает автоматический поворот камеры при движении.
tweak_easy_run|Reduces the stick tilt required to run.|Уменьшает наклон стика, необходимый для бега.
tweak_circle_confirm|Uses Circle to confirm and interact, and Cross to dodge.|Круг — подтверждение и взаимодействие, Крест — уклонение.
tweak_ragdoll|Makes defeated bodies react more strongly to impacts.|Усиливает реакцию тел побеждённых врагов на столкновения.
coop_name|Player name used in game and co-op. 3–16 Latin letters, digits, - or _.|Имя в игре и кооперативе: 3–16 латинских букв, цифр, - или _.
coop_password|Password for your account on the co-op server.|Пароль вашего аккаунта на сервере кооператива.
coop_invite|Invite code from your host. Leave empty to use the default server.|Код приглашения друга. Без кода используется общий сервер.
mods_enabled|Enables installed file mods.|Включает установленные файловые моды.
mods_dir|Folder containing your installed mods.|Папка установленных модов.
patches_dir|Folder containing additional game patches.|Папка дополнительных патчей игры.
pc_mirror_appearance|Allows appearance changes at the mirror in the Hunter's Dream.|Позволяет менять внешность у зеркала в Сне охотника.
pc_two_invaders|Allows two invaders in later areas. Required for all players.|Позволяет двум захватчикам появляться в поздних локациях. Требуется всем игрокам.
pc_rebirth|Allows character rebirth at the Altar of Despair.|Открывает перерождение персонажа у Алтаря отчаяния.
pc_enhanced_lamps|Adds level-up and storage access to lit lamps.|Добавляет повышение уровня и хранилище у зажжённых фонарей.
pc_boss_rematches|Allows rematches with defeated bosses at their lamps. Experimental.|Повторные бои с побеждёнными боссами у их фонарей. Экспериментально.
ui_language|Sets the language of the launcher interface.|Язык интерфейса лаунчера.
draw_pipe|Controls parallel processing of draw commands.|Управляет параллельной обработкой команд отрисовки.
readbacks|Controls how GPU results are read by the game.|Режим чтения результатов работы видеокарты игрой.
extra_env|Additional launch parameters for advanced configuration.|Дополнительные параметры запуска для ручной настройки.
frame_stats|Records detailed frame timing statistics.|Записывает подробную статистику времени отрисовки кадров.
gpu_profile|Enables detailed GPU performance measurements.|Включает подробные замеры производительности видеокарты.
vk_validation|Enables Vulkan diagnostic checks. May reduce performance.|Включает диагностику Vulkan. Может снижать производительность.
bbsc_dream_own|Guests use their own shops and workshop in the Hunter's Dream.|Гости используют свои магазины и мастерскую в Сне охотника.
bbsc_no_hp_penalty|Removes the summoned guest's maximum health reduction.|Отключает снижение максимального здоровья призванного гостя.
bbsc_death_penalty|Drops Blood Echoes at the place of death.|Оставляет отголоски крови на месте смерти.
bbsc_free_bell|Removes the Insight cost of summoning.|Отключает расход Озарения на призыв.
bbsc_scaling|Increases enemy strength for each additional player.|Усиливает врагов за каждого дополнительного игрока.
bbsc_scale_npc_hunters|Applies co-op scaling to hostile NPC hunters.|Применяет усиление кооператива к враждебным NPC-охотникам.
bbsc_scale_enemy_hp|Additional enemy health per guest.|Дополнительное здоровье обычных врагов за каждого гостя.
bbsc_scale_boss_hp|Additional boss health per guest.|Дополнительное здоровье боссов за каждого гостя.
bbsc_scale_damage|Additional enemy and boss damage per guest.|Дополнительный урон врагов и боссов за каждого гостя.
bbsc_scale_enemy_stagger|Additional enemy stagger resistance per guest.|Дополнительная устойчивость врагов к пошатыванию за каждого гостя.
bbsc_scale_boss_stagger|Additional boss stagger resistance per guest.|Дополнительная устойчивость боссов к пошатыванию за каждого гостя.
bbsc_shared_progress|Shares the host's bosses, lamps and opened paths with guests. NPC quests remain personal.|Переносит гостям победы над боссами, фонари и открытые пути хоста. Квесты NPC остаются личными.
bbsc_research|Records detailed diagnostic logs. May reduce performance.|Записывает подробные диагностические журналы. Может снижать производительность.'''
for _line in _DATA.splitlines():
    _key, _en, _ru = _line.split('|')
    HINTS[_key] = (_en, _ru)
