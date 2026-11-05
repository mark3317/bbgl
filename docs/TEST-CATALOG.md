# Каталог проверок BBGL / BBSC-GL — 04.11.2026

230 тестовых и вспомогательных файлов из обоих Git-деревьев; third_party/vendor/externals исключены. Все файлы прочитаны для статической инвентаризации структуры, assertions, импортов и точек запуска. Это не свидетельство прохождения всех тестов или построчное доказательство полноты покрытия. Ручная проверка и изменения сосредоточены на найденных остатках.

**Не запускать общий discover.** Native harness могут выполнять код при импорте; отдельные скрипты требуют VPS, ELF, Blender или игровых данных. Команды ниже — способы запуска, не обязательный набор. Python без пути — из папки файла; Qt — через out/qt-venv/Scripts/python.exe. Сейвовые/восстановительные методы не входят в стандартный прогон.

## `tests/allocator_fixture.py`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: Independent D015 fixture: the documented 393-byte allocator function.
- Запуск: `helper/import`; assertion/check sites: 0.

## `tests/cpu_harness.py`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: Independent arithmetic oracle and bounded Windows x64 execution harness.
- Запуск: `helper/import`; assertion/check sites: 0.

## `tests/game_code.h`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: scripts/prepare.py, src/code_check.h, stdint.h, stdio.h, stdlib.h, string.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `scripts/prepare.py`, `src/code_check.h`.

## `tests/launcher_log_flood_harness.py`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: child.py, self.c, self.gameFinished.c, self.logChanged.c
- Запуск: `helper/import`; assertion/check sites: 5.
- Ограничения: Qt venv/PySide6.

## `tests/paths.py`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: Repository paths for the Python tests (run: python3 -m unittest discover -s tests).
- Запуск: `helper/import`; assertion/check sites: 0.

## `tests/test_arena_overlap.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: stdint.h, stdio.h, stdlib.h, string.h, tests/test_arena_overlap.c, vulkan/vulkan.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `tests/test_arena_overlap.c`.

## `tests/test_arena_overlap.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Overlapping buffer cache arenas on the real GPU (tests/test_arena_overlap.c; no game, no window).
- Запуск: `python test_arena_overlap.py`; assertion/check sites: 2.
- Сценарии: `test_memory_bound_in_both_arenas_reads_the_same`.
- Имена файлов из ссылок исходника (существуют в дереве): `tests/test_arena_overlap.c`.

## `tests/test_aspect_ratio.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_container_padding_does_not_change_loaded_identity
- Запуск: `python test_aspect_ratio.py`; assertion/check sites: 2.
- Сценарии: `test_container_padding_does_not_change_loaded_identity`.

## `tests/test_aspect_thunk.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: src/aspect_thunk.h, windows.h
- Запуск: `CMake: aspect-thunk-test`; assertion/check sites: 6.
- Имена файлов из ссылок исходника (существуют в дереве): `src/aspect_thunk.h`.

## `tests/test_async_pacing.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Compile production pacing writer; exercise backpressure and snapshot lifetime.
- Запуск: `python test_async_pacing.py`; assertion/check sites: 4.
- Имена файлов из ссылок исходника (существуют в дереве): `core/libraries/videoout/async_perf_log.h`, `core/libraries/videoout/pacing_diagnostics.h`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `tests/test_atlas_features.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../gpu/shim/bbport_map_features.h, SDL3/SDL.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 25.
- Имена файлов из ссылок исходника (существуют в дереве): `../gpu/shim/bbport_map_features.h`.

## `tests/test_atlas_state.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../src/code_check.h, ../src/runtime_atlas_state.h, ../src/runtime_map.h, assert.h, game_code.h, stdint.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 12.
- Имена файлов из ссылок исходника (существуют в дереве): `../src/code_check.h`, `../src/runtime_atlas_state.h`, `../src/runtime_map.h`, `assert.h`, `game_code.h`.

## `tests/test_bbport_atlas_fade.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../gpu/shim/bbport_atlas_style.h, ../gpu/shim/bbport_map_art.h, a.c, b.c, box.h, c.c
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 11.
- Имена файлов из ссылок исходника (существуют в дереве): `../gpu/shim/bbport_atlas_style.h`, `../gpu/shim/bbport_map_art.h`.

## `tests/test_bbport_atlas_interiors.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../gpu/shim/bbport_atlas_interiors.h, c.h, id.c, nlohmann/json.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 22.
- Имена файлов из ссылок исходника (существуют в дереве): `../gpu/shim/bbport_atlas_interiors.h`, `nlohmann/json.h`.

## `tests/test_bbport_atlas_menu_state.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../gpu/shim/bbport_atlas_menu_state.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 9.
- Имена файлов из ссылок исходника (существуют в дереве): `../gpu/shim/bbport_atlas_menu_state.h`.

## `tests/test_bbport_atlas_style.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../gpu/shim/bbport_atlas_style.h, d.h, id.c, nlohmann/json.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 39.
- Имена файлов из ссылок исходника (существуют в дереве): `../gpu/shim/bbport_atlas_style.h`, `nlohmann/json.h`.

## `tests/test_boss_rematches.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Static validation of the experimental boss rematch events, lamp entries and texts.
- Запуск: `python test_boss_rematches.py`; assertion/check sites: 44.
- Сценарии: `test_emedf_alignment_is_explicit`, `test_every_boss_has_its_own_lamp_ids_and_text`, `test_the_cleric_beast_keeps_the_ids_its_saves_have`, `test_generated_events_keep_permanent_progress_flags`, `test_lamp_choice_and_text_are_generated_together`, `test_unknown_event_file_fails_closed`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; строковое извлечение production: чувствителен к переименованиям.

## `tests/test_bundled_release.py`

- Решение: Актуализирован в аудите.
- Назначение/контракт: test_offline_install_preserves_every_player_journal_and_host_config, test_stable_updates_ignore_preview_and_upstream_tags, test_settings_reach_mod_environment_and_cheat_is_available
- Запуск: `python test_bundled_release.py`; assertion/check sites: 12.
- Сценарии: `test_offline_install_preserves_every_player_journal_and_host_config`, `test_stable_updates_ignore_preview_and_upstream_tags`, `test_settings_reach_mod_environment_and_cheat_is_available`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; mock/stub не доказывает игровую интеграцию.

## `tests/test_camera_motion.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: cmd.c, device.c, video_core/host_shaders/camera_motion_comp.h, video_core/renderer_vulkan/vk_instance.h, video_core/renderer_vulkan/vk_scheduler.h, video_core/texture_cache/image.h
- Запуск: `CMake: camera-motion-test`; assertion/check sites: 3.
- Имена файлов из ссылок исходника (существуют в дереве): `video_core/renderer_vulkan/vk_instance.h`, `video_core/renderer_vulkan/vk_scheduler.h`, `video_core/texture_cache/image.h`.

## `tests/test_content.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: assert.h, b.c, direct.h, h.c, h.h, result.c
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 36.
- Имена файлов из ссылок исходника (существуют в дереве): `assert.h`, `runtime.h`, `runtime_file.c`.

## `tests/test_content.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_sfo_parameters_and_explicit_trial_profile, test_invalid_sfo_parameter_rejected, test_lifecycle_and_output_boundaries, test_missing_profile_does_not_report_loaded, test_other_modules_are_counted_independently
- Запуск: `unittest discover -s tests -p test_content.py`; assertion/check sites: 6.
- Сценарии: `test_sfo_parameters_and_explicit_trial_profile`, `test_invalid_sfo_parameter_rejected`, `test_lifecycle_and_output_boundaries`, `test_missing_profile_does_not_report_loaded`, `test_other_modules_are_counted_independently`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_coop.py`

- Решение: Актуализирован в аудите.
- Назначение/контракт: test_bbsc_is_told_where_the_saves_are, test_firewall_rules_stay_on_tailscale_and_the_home_network, test_firewall_script_quotes_an_apostrophe_in_the_path, test_tailscale_addresses, test_tailscale_is_found_on_path_outside_program_files, test_tailscale_found_in_program_files_when_not_on_path, test_tailscale_address_from_the_route_when_the_cli_is_missing
- Запуск: `python test_coop.py`; assertion/check sites: 18.
- Сценарии: `test_bbsc_is_told_where_the_saves_are`, `test_firewall_rules_stay_on_tailscale_and_the_home_network`, `test_firewall_script_quotes_an_apostrophe_in_the_path`, `test_tailscale_addresses`, `test_tailscale_is_found_on_path_outside_program_files`, `test_tailscale_found_in_program_files_when_not_on_path`, `test_tailscale_address_from_the_route_when_the_cli_is_missing`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; mock/stub не доказывает игровую интеграцию; 6 PASS; исторический save contract сохранён, explicit skip.

## `tests/test_coop_latency_diagnostics.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Bounded packet correlation and the actual Windows native log sink (no game required).
- Запуск: `python test_coop_latency_diagnostics.py`; assertion/check sites: 2.
- Имена файлов из ссылок исходника (существуют в дереве): `common/logging/log.h`, `core/net/p2p_latency.h`, `gpu/shim/common/logging/log.cpp`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `tests/test_coopdev_profile.ps1`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../tools/coop-dev/coopdev.ps1
- Запуск: `PowerShell -File`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `../tools/coop-dev/coopdev.ps1`.

## `tests/test_cpu_compat.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Independent CPU regressions. Run with unittest discover -s tests.
- Запуск: `python test_cpu_compat.py`; assertion/check sites: 112.
- Сценарии: `test_positive_jump_return_segment_report_and_input_immutability`, `test_disabled_ignores_invalid_or_missing_plan_and_keeps_bytes`, `test_reject_hash_signature_address_length_and_plan_defects`, `test_relocation_next_to_site_is_preserved`, `test_module_base_and_rip_fixup`, `test_image_limit_is_checked_without_large_allocation`, `test_atomic_publication_preserves_prior_artifact_on_failure`, `test_unhandled_count_instructions_fail_closed_and_override_is_explicit`, `test_documented_boundary_values`, `test_movbe_documented_byte_order_and_width`, `test_allocator_cmp_sub_defined_flag_boundaries`, `test_persisted_plan_bodies_match_generator_and_decode_as_baseline`, `test_every_gpr_width_alias_and_arithmetic_edges`, `test_bextr_position_length_grid`, `test_count_16_bit_preserves_upper_destination`, `test_memory_base_index_destination_alias_and_stack_redzone`, `test_movbe_load_store_all_gprs_aliases_widths_and_flags`, `test_movbe_stack_index_and_rip_memory`, `test_movbe_deliberate_endian_width_flag_and_source_defects_are_detected`, `test_movbe_rip_fixups_roundtrip_through_guarded_image`, `test_deliberate_result_flag_register_and_redzone_defects_are_detected`, `test_public_four_spans_transfer_report_and_unchanged_surroundings`, `test_full_state_flags_upper_halves_aliases_and_stack`, `test_arithmetic_context_and_zero_remainder_are_distinct`, `test_tzcnt_cmp_boundary_flags_and_following_jb`, `test_gate_is_independent_of_zero_remaining_counts_and_disabled_mode`, `test_tail_whitelist_context_body_and_version_defects_reject`, `test_entries_unknown_candidates_and_resolved_relocations_reject`, `test_entire_span_overlap_mapping_and_relocation_adjacency`, `test_purposeful_semantic_and_transfer_mutants_are_detected`.
- Имена файлов из ссылок исходника (существуют в дереве): `tools/build_cpu_compat.py`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_cpu_detection.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: The legacy CPU profile turns on by itself only where BMI1, LZCNT or MOVBE are missing.
- Запуск: `python test_cpu_detection.py`; assertion/check sites: 13.
- Сценарии: `test_ivy_bridge_lacks_all_three`, `test_haswell_and_later_need_nothing`, `test_absent_leaves_count_as_missing`, `test_this_cpu_answers`, `test_automatic_from_cpuid`, `test_ini_and_environment_override`, `test_partial_profile_is_the_default`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_dlss_startup.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_gpu_probe_is_delivered_before_first_settings_model, test_category_moves_keep_single_settings
- Запуск: `unittest discover -s tests -p test_dlss_startup.py`; assertion/check sites: 9.
- Сценарии: `test_gpu_probe_is_delivered_before_first_settings_model`, `test_category_moves_keep_single_settings`.
- Ограничения: mock/stub не доказывает игровую интеграцию; Qt venv/PySide6.

## `tests/test_emevd.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Validate the rematch event writer against the player's unmodified 1.09 files.
- Запуск: `unittest discover -s tests -p test_emevd.py`; assertion/check sites: 16.
- Сценарии: `test_every_game_event_file_round_trips_byte_identically`, `test_insertion_keeps_existing_instructions_and_parameter_targets`, `test_unknown_layout_is_rejected`, `test_inserting_before_parameterized_instructions_rebases_refs`, `test_replacement_requires_exact_expected_instruction`, `test_malformed_append_does_not_change_input`.

## `tests/test_engine_hooks.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: assert.h, code_check.h, engine_hooks.c, engine_hooks.h, stdint.h, stdio.h
- Запуск: `CMake: engine-hooks-test`; assertion/check sites: 38.
- Имена файлов из ссылок исходника (существуют в дереве): `assert.h`, `code_check.h`, `engine_hooks.c`, `engine_hooks.h`.

## `tests/test_enhanced_lamps.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Static validation of the experimental lamp patch against a real 1.09 dump.
- Запуск: `python test_enhanced_lamps.py`; assertion/check sites: 23.
- Сценарии: `test_only_target_scripts_change_and_every_output_round_trips`, `test_modified_source_is_rejected`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям.

## `tests/test_enhancements.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_off_unless_switched_on_and_environment_wins, test_the_menu_is_on_unless_switched_off, test_overlay_and_launcher_offer_the_same_keys, test_event_instructions_reads_arguments, test_talk_script_bytecode, test_unknown_files_are_left_alone, test_every_talk_script_round_trips_and_the_altar_matches_bbhost, test_rewrites_match_bbhost_and_are_reused, test_experimental_rematch_keeps_the_lamps_and_rebirth, test_rematches_keep_the_two_invaders, test_lamps_and_rebirth_share_the_altar_archive
- Запуск: `python test_enhancements.py`; assertion/check sites: 44.
- Сценарии: `test_off_unless_switched_on_and_environment_wins`, `test_the_menu_is_on_unless_switched_off`, `test_overlay_and_launcher_offer_the_same_keys`, `test_event_instructions_reads_arguments`, `test_talk_script_bytecode`, `test_unknown_files_are_left_alone`, `test_every_talk_script_round_trips_and_the_altar_matches_bbhost`, `test_rewrites_match_bbhost_and_are_reused`, `test_experimental_rematch_keeps_the_lamps_and_rebirth`, `test_rematches_keep_the_two_invaders`, `test_lamps_and_rebirth_share_the_altar_archive`.
- Имена файлов из ссылок исходника (существуют в дереве): `gpu/shim/bbport_settings.h`, `launcher/bbport_launcher_win.py`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям.

## `tests/test_file_mods.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../src/runtime_file.c, assert.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 47.
- Имена файлов из ссылок исходника (существуют в дереве): `../src/runtime_file.c`, `assert.h`.

## `tests/test_file_offsets.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../src/runtime_file.c, assert.h, time.h
- Запуск: `CMake: file-offsets-test`; assertion/check sites: 7.
- Имена файлов из ссылок исходника (существуют в дереве): `../src/runtime_file.c`, `assert.h`, `time.h`.

## `tests/test_fromsoft.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_round_trip_and_template_header, test_rejects_other_formats, test_damaged_files_are_format_errors, test_real_header_matches_a_fresh_one, test_unchanged_archive_is_identical, test_replacing_a_file_moves_the_rest, test_ambiguous_name_is_refused, test_real_talk_archive_round_trips
- Запуск: `python test_fromsoft.py`; assertion/check sites: 20.
- Сценарии: `test_round_trip_and_template_header`, `test_rejects_other_formats`, `test_damaged_files_are_format_errors`, `test_real_header_matches_a_fresh_one`, `test_unchanged_archive_is_identical`, `test_replacing_a_file_moves_the_rest`, `test_ambiguous_name_is_refused`, `test_real_talk_archive_round_trips`.
- Имена файлов из ссылок исходника (существуют в дереве): `scripts/fromsoft.py`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям.

## `tests/test_fsr4_assets.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: The launcher's FSR 4 v07 download list covers every tier the provider can ask for.
- Запуск: `python test_fsr4_assets.py`; assertion/check sites: 6.
- Сценарии: `test_every_output_tier_is_downloaded`, `test_list_has_no_duplicates`, `test_script_downloads_the_same_tiers`, `test_install_without_4320_reports_only_4320_missing`.
- Имена файлов из ссылок исходника (существуют в дереве): `launcher/bbport_launcher_win.py`.

## `tests/test_fsr_availability.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_full_assets_required_and_removal_disables_selected_fsr4, test_all_presets_disable_upscaling_and_old_411_is_normalized
- Запуск: `unittest discover -s tests -p test_fsr_availability.py`; assertion/check sites: 12.
- Сценарии: `test_full_assets_required_and_removal_disables_selected_fsr4`, `test_all_presets_disable_upscaling_and_old_411_is_normalized`.
- Ограничения: Qt venv/PySide6.

## `tests/test_game_check.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_intact_shaders_pass, test_damaged_shaders, test_wrong_size_is_damaged, test_other_compressions_are_not_checked, test_script_lists_every_damaged_file, test_unreadable_file_does_not_stop_the_game
- Запуск: `python test_game_check.py`; assertion/check sites: 7.
- Сценарии: `test_intact_shaders_pass`, `test_damaged_shaders`, `test_wrong_size_is_damaged`, `test_other_compressions_are_not_checked`, `test_script_lists_every_damaged_file`, `test_unreadable_file_does_not_stop_the_game`.
- Имена файлов из ссылок исходника (существуют в дереве): `game_check.py`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_game_download.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_roundtrip_and_existing_folder, test_cancellation_keeps_completed_parts_for_retry, test_bad_checksum_never_installs, test_unsafe_paths, test_lock_prevents_second_installer, test_disk_full_never_installs
- Запуск: `python test_game_download.py`; assertion/check sites: 12.
- Сценарии: `test_roundtrip_and_existing_folder`, `test_cancellation_keeps_completed_parts_for_retry`, `test_bad_checksum_never_installs`, `test_unsafe_paths`, `test_lock_prevents_second_installer`, `test_disk_full_never_installs`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_game_process_lifetime.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Real Windows process/job/pipe regressions for the hidden launcher.
- Запуск: `unittest discover -s tests -p test_game_process_lifetime.py`; assertion/check sites: 2.
- Сценарии: `test_exit_does_not_wait_for_unrelated_pipe_writer`, `test_log_failure_still_drains_output_and_finishes`, `test_restart_successor_keeps_launcher_and_log_alive`.
- Ограничения: mock/stub не доказывает игровую интеграцию; Qt venv/PySide6.

## `tests/test_gpu_runtime_stubs.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: bbport_toggles.h, setjmp.h
- Запуск: `CMake: motion-shader-test`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `bbport_toggles.h`.

## `tests/test_graphics_presets.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_custom_preserves_values_and_can_switch_back_to_preset, test_presets_only_use_settings_that_exist, test_shipped_defaults_are_balanced_and_overrides_are_custom, test_preset_disables_upscaler_and_preserves_output_and_look, test_upscaling_and_frame_generation_do_not_change_preset_identity, test_new_installs_run_120_and_saved_settings_keep_their_frame_rate, test_window_options_reach_the_game, test_recommendation_from_gpu_status, test_video_memory_target_is_passed_to_the_game
- Запуск: `python test_graphics_presets.py`; assertion/check sites: 32.
- Сценарии: `test_custom_preserves_values_and_can_switch_back_to_preset`, `test_presets_only_use_settings_that_exist`, `test_shipped_defaults_are_balanced_and_overrides_are_custom`, `test_preset_disables_upscaler_and_preserves_output_and_look`, `test_upscaling_and_frame_generation_do_not_change_preset_identity`, `test_new_installs_run_120_and_saved_settings_keep_their_frame_rate`, `test_window_options_reach_the_game`, `test_recommendation_from_gpu_status`, `test_video_memory_target_is_passed_to_the_game`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; mock/stub не доказывает игровую интеграцию.

## `tests/test_host_connections.py`

- Решение: Актуализирован в аудите.
- Назначение/контракт: Network selection, firewall scope, and retained server endpoint compatibility.
- Запуск: `python test_host_connections.py`; assertion/check sites: 16.
- Сценарии: `test_auto_prefers_only_vpn_and_requires_choice_if_ambiguous`, `test_multiple_addresses_require_local_selection_and_absent_provider_is_rejected`, `test_custom_ipv4_requires_an_active_local_address`, `test_discovery_filters_disconnected_bad_addresses_and_groups_ipv4`, `test_firewall_scope_is_explicit_and_validated`, `test_server_local_summon_address_does_not_leak_to_guests`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_input_bindings.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: SDL3/SDL.h, assert.h, input_bindings.c, input_bindings.h, stdio.h, string.h
- Запуск: `CMake: input-bindings-test`; assertion/check sites: 30.
- Имена файлов из ссылок исходника (существуют в дереве): `assert.h`, `input_bindings.c`, `input_bindings.h`.

## `tests/test_kickedout_native.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production KICKEDOUT translation against Bloodborne's native presence guard.
- Запуск: `python test_kickedout_native.py`; assertion/check sites: 2.
- Имена файлов из ссылок исходника (существуют в дереве): `core/libraries/np/np_types2.h`, `gpu/bbnet/vendor/shadps4/core/libraries/np/np_matching2/np_matching2_mm.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `tests/test_language_files.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_brazilian_portuguese_text_where_the_game_reads, test_voice_apart_from_the_text, test_nothing_chosen_leaves_no_layer, test_links_not_copies_on_the_same_drive
- Запуск: `python test_language_files.py`; assertion/check sites: 7.
- Сценарии: `test_brazilian_portuguese_text_where_the_game_reads`, `test_voice_apart_from_the_text`, `test_nothing_chosen_leaves_no_layer`, `test_links_not_copies_on_the_same_drive`.

## `tests/test_launcher_defaults.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_language_is_resolved_at_launch_and_manual_override_survives, test_default_fullscreen_and_old_bypass_flag_open_launcher, test_information_has_localized_text_and_stable_notice_identity
- Запуск: `unittest discover -s tests -p test_launcher_defaults.py`; assertion/check sites: 9.
- Сценарии: `test_language_is_resolved_at_launch_and_manual_override_survives`, `test_default_fullscreen_and_old_bypass_flag_open_launcher`, `test_information_has_localized_text_and_stable_notice_identity`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_launcher_ingame_sync.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_launcher_change_keeps_the_games, test_launcher_own_change_wins, test_shown_after_the_game_exits
- Запуск: `python test_launcher_ingame_sync.py`; assertion/check sites: 7.
- Сценарии: `test_launcher_change_keeps_the_games`, `test_launcher_own_change_wins`, `test_shown_after_the_game_exits`.
- Ограничения: mock/stub не доказывает игровую интеграцию; Qt venv/PySide6.

## `tests/test_launcher_lifetime.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise Qt's real event loop and window closing in isolated processes.
- Запуск: `unittest discover -s tests -p test_launcher_lifetime.py`; assertion/check sites: 4.
- Сценарии: `test_close_without_game_exits`, `test_hidden_launcher_waits_for_game_then_exits`, `test_game_exit_keeps_visible_launcher_usable`.
- Ограничения: Qt venv/PySide6.

## `tests/test_launcher_output.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise output selection callbacks without opening a Tk window.
- Запуск: `python test_launcher_output.py`; assertion/check sites: 11.
- Сценарии: `test_saved_custom_size_is_preserved`, `test_typing_commits_on_return_and_focus_loss`, `test_invalid_size_restores_saved_value`, `test_preset_selection_updates_saved_size`, `test_1920x1200_preset_is_selectable`, `test_other_selectors_remain_readonly`.
- Имена файлов из ссылок исходника (существуют в дереве): `launcher/bbport_launcher_win.py`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон.

## `tests/test_launcher_output_buffer.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_flood_has_one_wakeup_bounded_tail_and_preserves_start, test_oversized_line_and_restart_marker
- Запуск: `unittest discover -s tests -p test_launcher_output_buffer.py`; assertion/check sites: 10.
- Сценарии: `test_flood_has_one_wakeup_bounded_tail_and_preserves_start`, `test_oversized_line_and_restart_marker`.
- Имена файлов из ссылок исходника (существуют в дереве): `run.py`.
- Ограничения: Qt venv/PySide6.

## `tests/test_launcher_readiness.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_fresh_install_then_game_and_save_are_detected, test_bad_pack_and_key_do_not_appear_ready, test_shadps4_savedata_folder_is_explained, test_save_id_comes_from_game_metadata
- Запуск: `python test_launcher_readiness.py`; assertion/check sites: 10.
- Сценарии: `test_fresh_install_then_game_and_save_are_detected`, `test_bad_pack_and_key_do_not_appear_ready`, `test_shadps4_savedata_folder_is_explained`, `test_save_id_comes_from_game_metadata`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; mock/stub не доказывает игровую интеграцию.

## `tests/test_launcher_redesign.py`

- Решение: Актуализирован в аудите.
- Назначение/контракт: test_name_edit_updates_both_names_without_migrating_existing_account, test_setup_name_follows_save_folder_until_manually_edited, test_setup_does_not_rename_existing_accounts, test_selected_folder_is_used_and_existing_folder_is_preserved
- Запуск: `unittest discover -s tests -p test_launcher_redesign.py`; assertion/check sites: 15.
- Сценарии: `test_name_edit_updates_both_names_without_migrating_existing_account`, `test_setup_name_follows_save_folder_until_manually_edited`, `test_setup_does_not_rename_existing_accounts`, `test_selected_folder_is_used_and_existing_folder_is_preserved`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; mock/stub не доказывает игровую интеграцию; Qt venv/PySide6.

## `tests/test_launcher_updates.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_backslash_zip_unpacks_into_folders, test_new_files_arrive_and_player_files_stay, test_update_folder_kept_while_installing
- Запуск: `python test_launcher_updates.py`; assertion/check sites: 12.
- Сценарии: `test_backslash_zip_unpacks_into_folders`, `test_new_files_arrive_and_player_files_stay`, `test_update_folder_kept_while_installing`.
- Имена файлов из ссылок исходника (существуют в дереве): `Launcher/scripts/game_check.py`, `run.py`, `scripts/game_check.py`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_link_libc.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Cross-module identity and TLS relocation tests without game binaries.
- Запуск: `unittest discover -s tests -p test_link_libc.py`; assertion/check sites: 14.
- Сценарии: `test_different_local_ids_bind_same_identity`, `test_same_nid_wrong_library_version_does_not_bind`, `test_tls_module_id_is_literal_not_image_pointer`, `test_unsupported_tls_symbol_rejected`, `test_relocation_outside_segments_rejected`, `test_fs_thread_pointer_loads_are_rewritten_to_gs`, `test_fs_loads_outside_executable_segments_are_kept`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_live_graphics.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Startup patch selection for the opt-in live graphics experiment.
- Запуск: `python test_live_graphics.py`; assertion/check sites: 5.
- Сценарии: `test_normal_startup_is_unchanged`, `test_live_start_prepares_all_effects_even_when_disabled`, `test_ssr_remains_a_startup_setting`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_local_party.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Local-three profile/port isolation; no production profiles or native games.
- Запуск: `python test_local_party.py`; assertion/check sites: 31.
- Сценарии: `test_native_launch_uses_name_and_keeps_party_member_id`, `test_three_real_embedded_clients_and_native_udp_ports`, `test_environment_uses_existing_profile_and_never_rewrites_settings`, `test_shared_user_dir_or_missing_profile_is_rejected_before_launch`, `test_child_cannot_inherit_another_players_paths`, `test_closed_native_games_keep_real_consensus_peers_until_owner_releases`, `test_shutdown_deadline_reports_unresolved_state_without_granting_release`.
- Ограничения: mock/stub не доказывает игровую интеграцию; FAIL в этом проходе: WinError 5 при atomic replace и timeout coordinator; остальные 6 PASS.

## `tests/test_lookup_online_id_protocol.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Source/protobuf compatibility checks; deliberately does not build the server.
- Запуск: `python test_lookup_online_id_protocol.py`; assertion/check sites: 19.
- Сценарии: `test_dispatch_and_authentication`, `test_request_reply_wire_compatibility`, `test_lookup_query_preserves_identity_without_presence`, `test_error_paths`.
- Имена файлов из ссылок исходника (существуют в дереве): `client.cpp`, `client.h`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям.

## `tests/test_low_handles.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: assert.h, pthread.h, runtime.h, runtime_memory.c, runtime_mutex.c, src/compat_win.c
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 14.
- Имена файлов из ссылок исходника (существуют в дереве): `assert.h`, `pthread.h`, `runtime.h`, `runtime_memory.c`, `runtime_mutex.c`, `src/compat_win.c`, `src/runtime_memory.c`, `src/runtime_mutex.c`, `tests/test_low_handles.c`.

## `tests/test_low_vram.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_discrete_cards_up_to_4_5_gb, test_setting_forces_or_disables_it, test_unknown_memory
- Запуск: `python test_low_vram.py`; assertion/check sites: 8.
- Сценарии: `test_discrete_cards_up_to_4_5_gb`, `test_setting_forces_or_disables_it`, `test_unknown_memory`.
- Имена файлов из ссылок исходника (существуют в дереве): `run.py`.

## `tests/test_map_controller.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../gpu/shim/bbport_map_controller.h, e.c
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 39.
- Имена файлов из ссылок исходника (существуют в дереве): `../gpu/shim/bbport_map_controller.h`.

## `tests/test_map_location.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../src/code_check.h, ../src/runtime_map.h, assert.h, game_code.h, math.h, stdio.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 30.
- Имена файлов из ссылок исходника (существуют в дереве): `../src/code_check.h`, `../src/runtime_map.h`, `assert.h`, `game_code.h`.

## `tests/test_matching2_rejoin_identity.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute production packet admission and callback guards with reused room slots.
- Запуск: `python test_matching2_rejoin_identity.py`; assertion/check sites: 1.
- Имена файлов из ссылок исходника (существуют в дереве): `core/libraries/error_codes.h`, `core/libraries/np/np_error.h`, `core/libraries/np/np_matching2/np_matching2_internal.h`, `core/libraries/np/np_matching2/np_matching2_signaling.h`, `np_matching2_internal.cpp`, `np_matching2_signaling.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `tests/test_matching2_slot_allocator.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: matching_types.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 11.

## `tests/test_menu_assets.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_fmg_round_trip, test_matrix_round_trip, test_messages_are_menu_or_event_text, test_runtime_and_movie_agree_on_sections_rows_and_strings, test_movie_gains_sections_and_system_rows_without_scrolling, test_graphics_has_persistent_widget_slots_and_native_scrollbar, test_system_frame_and_footer_enclose_all_thirteen_rows, test_title_lists_fit_all_commands_in_available_regions, test_missing_optional_eu_title_keeps_standard_title_support, test_every_language_gains_the_strings_and_keeps_its_own, test_a_damaged_message_bundle_turns_the_menu_off
- Запуск: `python test_menu_assets.py`; assertion/check sites: 55.
- Сценарии: `test_fmg_round_trip`, `test_matrix_round_trip`, `test_messages_are_menu_or_event_text`, `test_runtime_and_movie_agree_on_sections_rows_and_strings`, `test_movie_gains_sections_and_system_rows_without_scrolling`, `test_graphics_has_persistent_widget_slots_and_native_scrollbar`, `test_system_frame_and_footer_enclose_all_thirteen_rows`, `test_title_lists_fit_all_commands_in_available_regions`, `test_missing_optional_eu_title_keeps_standard_title_support`, `test_every_language_gains_the_strings_and_keeps_its_own`, `test_a_damaged_message_bundle_turns_the_menu_off`.
- Имена файлов из ссылок исходника (существуют в дереве): `src/pc_menu.c`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям.

## `tests/test_menu_sound.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../src/runtime_menu_sound.h, assert.h, stdio.h, stdlib.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 9.
- Имена файлов из ссылок исходника (существуют в дереве): `../src/runtime_menu_sound.h`, `assert.h`.

## `tests/test_mods.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_merge_replacement_new_file_and_directory_listing, test_direct_manifest_priority_and_new_directories, test_shader_prebuild_uses_direct_replacements, test_last_mod_wins_and_reordering_changes_winner, test_selection_disable_and_new_mod, test_no_mod_returns_original_game, test_directory_conflict_does_not_modify_base, test_mod_symlinks_rejected, test_windows_overlay_files_report_their_size, test_overlay_under_redirection_trust_policy, test_overlay_moves_off_a_drive_without_links, test_executable_replacement_rejected, test_shadps4_sibling_folder_and_global_disable, test_shadps4_sibling_folder_of_symlinks_is_left_out, test_empty_shadps4_sibling_folder_is_left_out, test_generated_files_lie_under_player_mods_and_apply_with_mods_off, test_app0_wrapped_mod_discovered, test_other_case_replaces_the_game_file, test_wrapped_and_bare_layouts, test_mod_site_layouts, test_unrecognized_folders_say_why, test_invalid_profile_fails, test_run_uses_manifest_and_propagates_exit, test_mod_menu_text_gains_the_pc_menu_strings, test_no_layer_without_a_mod_over_the_menu_text_or_without_the_pc_menu, test_a_copy_that_already_has_the_strings_is_used_as_it_is
- Запуск: `unittest discover -s tests -p test_mods.py`; assertion/check sites: 71.
- Сценарии: `test_merge_replacement_new_file_and_directory_listing`, `test_direct_manifest_priority_and_new_directories`, `test_shader_prebuild_uses_direct_replacements`, `test_last_mod_wins_and_reordering_changes_winner`, `test_selection_disable_and_new_mod`, `test_no_mod_returns_original_game`, `test_directory_conflict_does_not_modify_base`, `test_mod_symlinks_rejected`, `test_windows_overlay_files_report_their_size`, `test_overlay_under_redirection_trust_policy`, `test_overlay_moves_off_a_drive_without_links`, `test_executable_replacement_rejected`, `test_shadps4_sibling_folder_and_global_disable`, `test_shadps4_sibling_folder_of_symlinks_is_left_out`, `test_empty_shadps4_sibling_folder_is_left_out`, `test_generated_files_lie_under_player_mods_and_apply_with_mods_off`, `test_app0_wrapped_mod_discovered`, `test_other_case_replaces_the_game_file`, `test_wrapped_and_bare_layouts`, `test_mod_site_layouts`, `test_unrecognized_folders_say_why`, `test_invalid_profile_fails`, `test_run_uses_manifest_and_propagates_exit`, `test_mod_menu_text_gains_the_pc_menu_strings`, `test_no_layer_without_a_mod_over_the_menu_text_or_without_the_pc_menu`, `test_a_copy_that_already_has_the_strings_is_used_as_it_is`.
- Имена файлов из ссылок исходника (существуют в дереве): `enhancements.py`, `probe.c`, `scripts/mods.py`.
- Ограничения: mock/stub не доказывает игровую интеграцию; строковое извлечение production: чувствителен к переименованиям.

## `tests/test_motion_history.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: draw.vertices.c, gpu/shadps4/video_core/renderer_vulkan/motion_history.h, range.c
- Запуск: `CMake: motion-history-test`; assertion/check sites: 41.
- Имена файлов из ссылок исходника (существуют в дереве): `gpu/shadps4/video_core/renderer_vulkan/motion_history.h`.

## `tests/test_motion_shaders.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: info.h, runtime.h, runtime.hw.fs.c, setjmp.h, shader_recompiler/backend/spirv/emit_spirv.h, shader_recompiler/ir/ir_emitter.h
- Запуск: `CMake: motion-shader-test`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `info.h`, `runtime.h`, `shader_recompiler/backend/spirv/emit_spirv.h`, `shader_recompiler/ir/ir_emitter.h`.

## `tests/test_navigation_map.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../gpu/shim/bbport_map.h, ../gpu/shim/bbport_map_direction.h, ../src/runtime_map.h, SDL3/SDL.h, imgui.h, nlohmann/json.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 31.
- Имена файлов из ссылок исходника (существуют в дереве): `../gpu/shim/bbport_map.h`, `../gpu/shim/bbport_map_direction.h`, `../src/runtime_map.h`, `nlohmann/json.h`.

## `tests/test_output_settings.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: bbport_settings.h
- Запуск: `CMake: output-settings-test`; assertion/check sites: 16.
- Имена файлов из ссылок исходника (существуют в дереве): `bbport_settings.h`.

## `tests/test_overlay_language.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_interface_language_is_independent_of_game_language
- Запуск: `python test_overlay_language.py`; assertion/check sites: 2.
- Сценарии: `test_interface_language_is_independent_of_game_language`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_overlay_text.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: bbport_overlay_text.h, bbport_settings.h, bbport_trophy_toast_model.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 10.
- Имена файлов из ссылок исходника (существуют в дереве): `bbport_overlay_text.h`, `bbport_settings.h`, `bbport_trophy_toast_model.h`.

## `tests/test_p2p_attempt_trace.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: core/net/p2p_relay.cpp, sent.c
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 19.
- Имена файлов из ссылок исходника (существуют в дереве): `core/net/p2p_relay.cpp`.

## `tests/test_p2p_diagnostic_snapshot.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run current transport source (not the previously built archive object) with diagnostics.
- Запуск: `python test_p2p_diagnostic_snapshot.py`; assertion/check sites: 2.
- Имена файлов из ссылок исходника (существуют в дереве): `gpu/bbnet/vendor/shadps4/core/net/p2p_relay.cpp`, `gpu/bbnet/vendor/shadps4/core/net/p2p_transport.cpp`, `gpu/shim/common/logging/log.cpp`, `tests/test_p2p_latency_transport.cpp`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `tests/test_p2p_latency_transport.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: core/net/p2p_codec.h, core/net/p2p_transport.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 11.
- Имена файлов из ссылок исходника (существуют в дереве): `core/net/p2p_codec.h`, `core/net/p2p_transport.h`.

## `tests/test_p2p_socket_contract.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: core/libraries/net/net.h, core/net/guest_net.h, core/net/p2p_codec.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 18.
- Имена файлов из ссылок исходника (существуют в дереве): `core/libraries/net/net.h`, `core/net/guest_net.h`, `core/net/p2p_codec.h`.

## `tests/test_p2p_socket_contract.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run production recv adapter + production transport, without loading the game runtime.
- Запуск: `python test_p2p_socket_contract.py`; assertion/check sites: 1.
- Имена файлов из ссылок исходника (существуют в дереве): `core/libraries/net/net.h`, `core/libraries/net/net_error.h`, `core/libraries/net/net_flag_watch.h`, `core/libraries/net/net_translate.h`, `core/net/guest_net.h`, `gpu/bbnet/vendor/shadps4/core/libraries/net/net.cpp`, `gpu/shim/common/logging/log.cpp`, `tests/test_p2p_socket_contract.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `tests/test_p2p_vps_relay.cpp`

- Решение: Ручной; внешняя среда.
- Назначение/контракт: core/net/p2p_codec.h, core/net/p2p_relay.h, windows.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 10.
- Имена файлов из ссылок исходника (существуют в дереве): `core/net/p2p_codec.h`, `core/net/p2p_relay.h`.
- Ограничения: реальный VPS; только отдельный ручной запуск.

## `tests/test_pacing_summary.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Analysis checks only: does not invoke a compiler or start the game.
- Запуск: `python test_pacing_summary.py`; assertion/check sites: 12.
- Сценарии: `test_complete_windows_and_corruption`, `test_weights_and_missing_fields`, `test_processes_and_modes_separate`, `test_duplicate_windows_rejected`.
- Имена файлов из ссылок исходника (существуют в дереве): `tools/coop-dev/summarize-pacing.py`.

## `tests/test_packaged_vulkan.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Driver discovery at the AppImage's GTK/game entry point, without a GPU.
- Запуск: `unittest discover -s tests -p test_packaged_vulkan.py`; assertion/check sites: 15.
- Сценарии: `test_amd_intel_keep_bundled_drivers`, `test_explicit_and_legacy_overrides_are_preserved`, `test_host_nvidia_and_compiler_are_exposed_without_host_libc`, `test_absolute_and_relative_icd_paths`, `test_32_bit_and_malformed_icds_are_skipped`, `test_additional_user_icds_are_not_lost`, `test_host_driver_can_be_supplied_outside_hidden_nix_store`.
- Имена файлов из ссылок исходника (существуют в дереве): `launcher/bbport_vulkan.py`.

## `tests/test_pad.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../src/runtime_pad.c, assert.h, unistd.h, windows.h
- Запуск: `CMake: pad-test`; assertion/check sites: 53.
- Имена файлов из ссылок исходника (существуют в дереве): `../src/runtime_pad.c`, `assert.h`.

## `tests/test_party_connection.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Real discovery/preflight sockets; no game, production profile or VPN changes.
- Запуск: `python test_party_connection.py`; assertion/check sites: 23.
- Сценарии: `test_names_preserved_and_rename_keeps_group_identity`, `test_full_mesh_and_launch_without_server_or_invite_code`, `test_udp_failure_blocks_start`, `test_inconsistent_roster_and_stale_readiness_block_start`, `test_old_live_group_cannot_be_replaced`, `test_network_selection_and_tailscale_peer_inventory`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_party_log_ownership.py`

- Решение: Актуализирован в аудите.
- Назначение/контракт: Run actual runner launch logic with a Windows-locked launcher log and real pipes.
- Запуск: `python test_party_log_ownership.py`; assertion/check sites: 8.
- Сценарии: `test_launcher_pipe_does_not_rotate_locked_log_and_receives_all_output`, `test_direct_runner_rotates_and_owns_native_log`.
- Имена файлов из ссылок исходника (существуют в дереве): `run.py`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям.

## `tests/test_patches.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_presets_keep_ui_native, test_explicit_scene_resolution_keeps_native_ui, test_coordinate_and_aspect_fixes_are_preserved, test_unexpected_or_missing_ui_instruction_is_rejected, test_native_and_disabled_upscaler_need_no_resolution_patch, test_output_other_than_1080p_scales_the_scene, test_arbitrary_aspect_and_native_movie_viewport, test_invalid_custom_resolutions_fall_back, test_fps_physics_write_preserves_unrelated_instruction, test_fps_presets_set_the_physics_step_per_frame_rate, test_other_versions_keep_their_xml_addresses, test_presets_use_the_base, test_90_is_the_list_as_it_is, test_120_and_144_values, test_another_list_under_the_name_is_refused, test_other_code_gets_no_scaled_preset, test_game_matches_and_the_base_keeps_no_game_bytes, test_effects_keep_the_games_rate, test_cloth_stiffness_and_the_1_0_sites_above_60, test_camera_only_when_asked, test_existing_presets_are_unchanged_by_default, test_only_steps_the_game_has_at_1_30, test_60_uncapped_and_off_keep_the_list, test_sites_in_the_game, test_copies_of_the_built_in_file_are_ignored, test_an_external_fps_patch_replaces_the_preset, test_switch, test_guard_covers_both_writes, test_guard_matches_the_game, test_switch_and_guard, test_guard_matches_the_game, test_blocked_movement_check_divides_by_frame_time, test_unexpected_code_is_left_alone, test_switch, test_camera_patch_is_optional_and_compatible_with_fps_and_debug_menu, test_debug_menu_needs_both_fonts_but_camera_does_not, test_debug_menu_fonts_in_adhoc_font_with_a_mods_own_case, test_fixes_raise_the_frame_heaps_without_touching_other_patches, test_conflicting_enemy_control_patch_is_rejected, test_selection_and_unsupported_lines, test_built_in_file_is_not_external, test_sites_merge_and_ignore_other_patches, test_image_bytes_past_the_file_are_zero, test_only_patched_bytes_count, test_stored_fingerprint_matches_the_prepared_game, test_goty_dump_with_the_109_code_is_109, test_other_code_keeps_the_app_ver, test_missing_eboot_keeps_the_app_ver, test_109_app_ver_skips_the_fingerprint, test_unreadable_eboot_is_not_109
- Запуск: `python test_patches.py`; assertion/check sites: 127.
- Сценарии: `test_presets_keep_ui_native`, `test_explicit_scene_resolution_keeps_native_ui`, `test_coordinate_and_aspect_fixes_are_preserved`, `test_unexpected_or_missing_ui_instruction_is_rejected`, `test_native_and_disabled_upscaler_need_no_resolution_patch`, `test_output_other_than_1080p_scales_the_scene`, `test_arbitrary_aspect_and_native_movie_viewport`, `test_invalid_custom_resolutions_fall_back`, `test_fps_physics_write_preserves_unrelated_instruction`, `test_fps_presets_set_the_physics_step_per_frame_rate`, `test_other_versions_keep_their_xml_addresses`, `test_presets_use_the_base`, `test_90_is_the_list_as_it_is`, `test_120_and_144_values`, `test_another_list_under_the_name_is_refused`, `test_other_code_gets_no_scaled_preset`, `test_game_matches_and_the_base_keeps_no_game_bytes`, `test_effects_keep_the_games_rate`, `test_cloth_stiffness_and_the_1_0_sites_above_60`, `test_camera_only_when_asked`, `test_existing_presets_are_unchanged_by_default`, `test_only_steps_the_game_has_at_1_30`, `test_60_uncapped_and_off_keep_the_list`, `test_sites_in_the_game`, `test_copies_of_the_built_in_file_are_ignored`, `test_an_external_fps_patch_replaces_the_preset`, `test_switch`, `test_guard_covers_both_writes`, `test_guard_matches_the_game`, `test_switch_and_guard`, `test_guard_matches_the_game`, `test_blocked_movement_check_divides_by_frame_time`, `test_unexpected_code_is_left_alone`, `test_switch`, `test_camera_patch_is_optional_and_compatible_with_fps_and_debug_menu`, `test_debug_menu_needs_both_fonts_but_camera_does_not`, `test_debug_menu_fonts_in_adhoc_font_with_a_mods_own_case`, `test_fixes_raise_the_frame_heaps_without_touching_other_patches`, `test_conflicting_enemy_control_patch_is_rejected`, `test_selection_and_unsupported_lines`, `test_built_in_file_is_not_external`, `test_sites_merge_and_ignore_other_patches`, `test_image_bytes_past_the_file_are_zero`, `test_only_patched_bytes_count`, `test_stored_fingerprint_matches_the_prepared_game`, `test_goty_dump_with_the_109_code_is_109`, `test_other_code_keeps_the_app_ver`, `test_missing_eboot_keeps_the_app_ver`, `test_109_app_ver_skips_the_fingerprint`, `test_unreadable_eboot_is_not_109`.
- Имена файлов из ссылок исходника (существуют в дереве): `prepare.py`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_prepare.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_plain_elf_is_read_without_the_self_wrapper, test_libc_ret_contract_is_verified_from_symbol_and_code, test_file_offset_is_not_virtual_address, test_truncated_payload_rejected, test_encrypted_or_compressed_payload_rejected, test_missing_required_segment_rejected, test_bad_program_header_index_rejected
- Запуск: `python test_prepare.py`; assertion/check sites: 15.
- Сценарии: `test_plain_elf_is_read_without_the_self_wrapper`, `test_libc_ret_contract_is_verified_from_symbol_and_code`, `test_file_offset_is_not_virtual_address`, `test_truncated_payload_rejected`, `test_encrypted_or_compressed_payload_rejected`, `test_missing_required_segment_rejected`, `test_bad_program_header_index_rejected`.

## `tests/test_probe.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Boundary tests for the native loader; uses tiny synthetic x86-64 images.
- Запуск: `python test_probe.py`; assertion/check sites: 35.
- Сценарии: `test_invalid_content_profile_is_rejected`, `test_original_instruction_reaches_named_import`, `test_native_initializer_and_export_return`, `test_host_contract_takes_priority_over_native_export`, `test_strict_mode_skips_native_initialization_and_binding`, `test_native_metadata_and_bindings_are_validated`, `test_failed_native_initializer_does_not_enter_game`, `test_base_relative_address_is_relocated`, `test_out_of_bounds_relocation_is_rejected`, `test_truncated_image_is_rejected`, `test_illegal_instruction_reports_guest_offset`, `test_runtime_returns_from_verified_init_env`, `test_unverified_runtime_stays_disabled`, `test_unknown_capabilities_rejected`.

## `tests/test_profile_entrypoints.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise real native entry points against a stand-in child, without starting the game.
- Запуск: `python test_profile_entrypoints.py`; assertion/check sites: 7.
- Сценарии: `test_three_concurrent_children_have_distinct_profiles_and_ports`.
- Имена файлов из ссылок исходника (существуют в дереве): `probe.c`.

## `tests/test_profile_layout.py`

- Решение: Актуализирован в аудите.
- Назначение/контракт: test_retired_online_mode_and_credentials_do_not_reach_a_launch, test_offline_client_is_verified_in_place_and_damage_is_reported, test_profile_import_keeps_saves_host_database_and_existing_settings, test_bbgl_imports_local_before_roaming_and_preserves_existing_data, test_host_keeps_both_servers_database_and_logs_in_profile, test_game_uses_one_profile_and_upstream_graphics_defaults
- Запуск: `python test_profile_layout.py`; assertion/check sites: 32.
- Сценарии: `test_retired_online_mode_and_credentials_do_not_reach_a_launch`, `test_offline_client_is_verified_in_place_and_damage_is_reported`, `test_profile_import_keeps_saves_host_database_and_existing_settings`, `test_bbgl_imports_local_before_roaming_and_preserves_existing_data`, `test_host_keeps_both_servers_database_and_logs_in_profile`, `test_game_uses_one_profile_and_upstream_graphics_defaults`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; mock/stub не доказывает игровую интеграцию; строковое извлечение production: чувствителен к переименованиям; исторический Host/profile contract сохранён, explicit skip; миграции не запускались.

## `tests/test_profile_migration.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_rename_preserves_saves_and_cache_and_rewrites_only_profile_paths, test_merge_never_overwrites_existing_data
- Запуск: `python test_profile_migration.py`; assertion/check sites: 11.
- Сценарии: `test_rename_preserves_saves_and_cache_and_rewrites_only_profile_paths`, `test_merge_never_overwrites_existing_data`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; mock/stub не доказывает игровую интеграцию.

## `tests/test_quiet_output.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Scripts keep running when the launcher reading their output has closed (issues #84, #91).
- Запуск: `python test_quiet_output.py`; assertion/check sites: 4.
- Сценарии: `test_closed_reader_fails_unguarded_print`, `test_guarded_script_finishes`.

## `tests/test_redzone.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Red-zone-safe trampolines for guest stores (link_modules.protect_red_zones), D087.
- Запуск: `python test_redzone.py`; assertion/check sites: 23.
- Сценарии: `test_site_jumps_to_trampoline_that_lowers_rsp_around_the_store`, `test_other_instructions_of_a_site_are_copied_unchanged`, `test_changed_bytes_or_relocations_leave_the_site_alone`, `test_site_next_to_a_cpu_translation_is_left_alone`, `test_applied_site_adds_one_aligned_executable_segment`, `test_disabled_leaves_the_image_unchanged`, `test_attack_trail_stores_are_covered`, `test_sites_do_not_overlap_community_patches`, `test_exception_frame_overwrites_the_red_zone`, `test_trampoline_keeps_the_red_zone`.
- Имена файлов из ссылок исходника (существуют в дереве): `tests/test_redzone.py`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_rejoin_trace_queue.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: bbsc_network_attempt.h, bbsc_relay_io.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 19.
- Имена файлов из ссылок исходника (существуют в дереве): `bbsc_network_attempt.h`, `bbsc_relay_io.h`.

## `tests/test_relay_vps_reconnect.py`

- Решение: Ручной; внешняя среда.
- Назначение/контракт: Real BBSC TCP relay on the public VPS; ephemeral identities, no account/save writes.
- Запуск: `python test_relay_vps_reconnect.py`; assertion/check sites: 7.
- Ограничения: исполняемый скрипт: импорт может запускать проверку; реальный VPS; только отдельный ручной запуск.

## `tests/test_relay_writer_vps.py`

- Решение: Ручной; внешняя среда.
- Назначение/контракт: Opt-in: compile real DLL I/O functions and exchange frames through the public VPS.
- Запуск: `python test_relay_writer_vps.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `bbsc_relay_io.h`, `mods-src/BBSC/emulator/mod/bbsc_relay.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку; реальный VPS; только отдельный ручной запуск.

## `tests/test_release_logging.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Compile actual GPU/DLL sinks and verify release filtering and unified output.
- Запуск: `python test_release_logging.py`; assertion/check sites: 9.
- Имена файлов из ссылок исходника (существуют в дереве): `common/logging/log.h`, `emulator/mod/bbsc_mod.cpp`, `emulator/src/core/bloodborne_re.cpp`, `gpu/shim/common/logging/log.cpp`, `launcher/bbport_launcher_backend.py`.
- Ограничения: mock/stub не доказывает игровую интеграцию; строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку; Qt venv/PySide6.

## `tests/test_respawn_patch.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: assert.h, game_code.h, respawn_patch.h, stdint.h, stdio.h, stdlib.h
- Запуск: `CMake: respawn-patch-test`; assertion/check sites: 30.
- Имена файлов из ссылок исходника (существуют в дереве): `assert.h`, `game_code.h`, `respawn_patch.h`.

## `tests/test_run_scripts.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_success_gives_the_output_or_an_empty_string, test_a_failure_stops_the_start_unless_the_script_is_optional, test_an_incomplete_port_says_what_is_missing
- Запуск: `python test_run_scripts.py`; assertion/check sites: 10.
- Сценарии: `test_success_gives_the_output_or_an_empty_string`, `test_a_failure_stops_the_start_unless_the_script_is_optional`, `test_an_incomplete_port_says_what_is_missing`.
- Имена файлов из ссылок исходника (существуют в дереве): `game_check.py`, `run.py`, `scripts/game_check.py`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `tests/test_run_settings.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise run.sh across a re-exec with lightweight preparation/probe stand-ins.
- Запуск: `unittest discover -s tests -p test_run_settings.py`; assertion/check sites: 15.
- Сценарии: `test_outputs_other_than_1080p_patch_the_render_size_and_restarts_recompute_it`, `test_live_resolution_keeps_guest_sizes_native`, `test_live_resolution_setting_and_gpu_check`, `test_live_resolution_without_sed_or_grep`, `test_explicit_render_override_survives_restart`.
- Имена файлов из ссылок исходника (существуют в дереве): `probe.c`, `scripts/mods.py`, `scripts/patches.py`.

## `tests/test_runtime.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: assert.h, probe.c, pthread.h, runtime.h, stdatomic.h, stdio.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 142.
- Имена файлов из ссылок исходника (существуют в дереве): `assert.h`, `probe.c`, `pthread.h`, `runtime.h`, `time.h`.

## `tests/test_runtime.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_runtime_contracts, test_recursive_guard_fails_explicitly, test_stack_corruption_is_not_ignored, test_tls_bounds_are_checked, test_rwlock_lifecycle_and_ownership, test_rwlock_multiple_readers_exclude_writer, test_rwlock_timeouts_use_orbis_errors
- Запуск: `unittest discover -s tests -p test_runtime.py`; assertion/check sites: 11.
- Сценарии: `test_runtime_contracts`, `test_recursive_guard_fails_explicitly`, `test_stack_corruption_is_not_ignored`, `test_tls_bounds_are_checked`, `test_rwlock_lifecycle_and_ownership`, `test_rwlock_multiple_readers_exclude_writer`, `test_rwlock_timeouts_use_orbis_errors`.

## `tests/test_runtime_menu_mix.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: ../src/runtime_audio.c, assert.h
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 26.
- Имена файлов из ссылок исходника (существуют в дереве): `../src/runtime_audio.c`, `assert.h`.

## `tests/test_runtime_network_settings.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run production bridge settings installation before the first native P2P use.
- Запуск: `python test_runtime_network_settings.py`; assertion/check sites: 1.
- Имена файлов из ссылок исходника (существуют в дереве): `core/emulator_settings.h`, `gpu/bbnet/bbnet_glue.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `tests/test_runtime_trophies.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: assert.h, direct.h, process.h, stdint.h, stdio.h, stdlib.h
- Запуск: `CMake: trophy-history-test`; assertion/check sites: 15.
- Имена файлов из ссылок исходника (существуют в дереве): `assert.h`, `process.h`, `time.h`.

## `tests/test_scene_resolution.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: clear.c, cmd.c, common/slot_vector.h, di.props.h, size.h, video_core/renderer_vulkan/vk_instance.h
- Запуск: `CMake: scene-resolution-test`; assertion/check sites: 14.
- Имена файлов из ссылок исходника (существуют в дереве): `common/slot_vector.h`, `video_core/renderer_vulkan/vk_instance.h`, `video_core/renderer_vulkan/vk_runtime.h`, `video_core/renderer_vulkan/vk_scene_resolution.h`, `video_core/renderer_vulkan/vk_scheduler.h`, `video_core/texture_cache/blit_helper.h`.

## `tests/test_sema.c`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: assert.h, limits.h, probe.c, pthread.h, runtime.h, s.c
- Запуск: `native harness/helper; flags in source/caller`; assertion/check sites: 60.
- Имена файлов из ссылок исходника (существуют в дереве): `assert.h`, `probe.c`, `pthread.h`, `runtime.h`, `time.h`.

## `tests/test_sema.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_counts_errors_timeout_and_stale_ids, test_fifo_wakeup_and_token_reservation, test_cancel_and_delete_wake_all_waiters, test_priority_wait_blocks_until_signal
- Запуск: `unittest discover -s tests -p test_sema.py`; assertion/check sites: 4.
- Сценарии: `test_counts_errors_timeout_and_stale_ids`, `test_fifo_wakeup_and_token_reservation`, `test_cancel_and_delete_wake_all_waiters`, `test_priority_wait_blocks_until_signal`.

## `tests/test_settings_navigation.py`

- Решение: Актуализирован в аудите.
- Назначение/контракт: Checks that the task-based Settings hub can reach existing controls.
- Запуск: `python test_settings_navigation.py`; assertion/check sites: 3.
- Сценарии: `test_every_existing_control_has_one_destination`, `test_common_searches_open_the_relevant_section`.
- Ограничения: Qt venv/PySide6.

## `tests/test_setup_wizard.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_wizard_survives_partial_setup_and_stops_after_finish, test_finished_setup_with_game_opens_home, test_skip_opens_game_page_with_fix_banner, test_fix_banner_clears_once_game_folder_is_valid, test_bundled_prompts_switch_without_download_and_follow_ingame_choice, test_launch_options_moved_out_of_advanced
- Запуск: `python test_setup_wizard.py`; assertion/check sites: 30.
- Сценарии: `test_wizard_survives_partial_setup_and_stops_after_finish`, `test_finished_setup_with_game_opens_home`, `test_skip_opens_game_page_with_fix_banner`, `test_fix_banner_clears_once_game_folder_is_valid`, `test_bundled_prompts_switch_without_download_and_follow_ingame_choice`, `test_launch_options_moved_out_of_advanced`.
- Ограничения: mock/stub не доказывает игровую интеграцию; Qt venv/PySide6.

## `tests/test_shader_prebuild.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_code_follows_the_header_and_a_copy_shader_follows_its_footer, test_a_damaged_archive_is_skipped, test_only_current_records_are_merged_once, test_rejected_translations_are_left_out, test_every_shader_archive_program_is_found
- Запуск: `python test_shader_prebuild.py`; assertion/check sites: 9.
- Сценарии: `test_code_follows_the_header_and_a_copy_shader_follows_its_footer`, `test_a_damaged_archive_is_skipped`, `test_only_current_records_are_merged_once`, `test_rejected_translations_are_left_out`, `test_every_shader_archive_program_is_found`.

## `tests/test_shader_user_data.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: shader_recompiler/frontend/fetch_shader.h
- Запуск: `CMake: shader-user-data-test`; assertion/check sites: 12.
- Имена файлов из ссылок исходника (существуют в дереве): `shader_recompiler/frontend/fetch_shader.h`.

## `tests/test_signaling_activation_race.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute production activation code with deterministic receive/dispatch interleavings.
- Запуск: `python test_signaling_activation_race.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `gpu/bbnet/vendor/shadps4/core/libraries/np/np_signaling/np_signaling_state.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `tests/test_signaling_generation.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise production control dispatch with delayed packets from an old attempt.
- Запуск: `python test_signaling_generation.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `gpu/bbnet/vendor/shadps4/core/libraries/np/np_signaling/np_signaling_state.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `tests/test_signaling_readiness_loss.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise production readiness/keepalive code with deterministic UDP loss.
- Запуск: `python test_signaling_readiness_loss.py`; assertion/check sites: 1.
- Имена файлов из ссылок исходника (существуют в дереве): `gpu/bbnet/vendor/shadps4/core/libraries/np/np_signaling/np_signaling_state.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `tests/test_srt_walker.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: shader_recompiler/ir/passes/srt.h
- Запуск: `CMake: srt-walker-test`; assertion/check sites: 5.
- Имена файлов из ссылок исходника (существуют в дереве): `shader_recompiler/ir/passes/srt.h`.

## `tests/test_stage_point.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: gpu/shim/stage_point.h, stage_point.h
- Запуск: `CMake: stage-point-test`; assertion/check sites: 8.
- Имена файлов из ссылок исходника (существуют в дереве): `gpu/shim/stage_point.h`, `stage_point.h`.

## `tests/test_startup_routing.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_fresh_install_opens_wizard_even_with_overrides, test_completed_setup_opens_launcher, test_skipped_setup_without_game_opens_game_page, test_missing_game_folder_shows_fix_banner, test_overrides_open_launcher, test_newer_wizard_version_prompts_again, test_existing_user_with_game_is_marked_complete, test_dismissed_old_wizard_without_game_counts_as_skipped, test_fresh_install_is_not_migrated, test_missing_folder_under_writable_parent
- Запуск: `python test_startup_routing.py`; assertion/check sites: 22.
- Сценарии: `test_fresh_install_opens_wizard_even_with_overrides`, `test_completed_setup_opens_launcher`, `test_skipped_setup_without_game_opens_game_page`, `test_missing_game_folder_shows_fix_banner`, `test_overrides_open_launcher`, `test_newer_wizard_version_prompts_again`, `test_existing_user_with_game_is_marked_complete`, `test_dismissed_old_wizard_without_game_counts_as_skipped`, `test_fresh_install_is_not_migrated`, `test_missing_folder_under_writable_parent`.

## `tests/test_summon_connect_retry.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise the production bounded retry policy without a server or game.
- Запуск: `python test_summon_connect_retry.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/libraries/network/bbsc_connect_retry.h`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `tests/test_taa_shader.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: cmd.c, device.c, video_core/host_shaders/taa_comp.h, video_core/host_shaders/taa_sharpen_comp.h, video_core/renderer_vulkan/vk_instance.h, video_core/renderer_vulkan/vk_scheduler.h
- Запуск: `CMake: taa-shader-test`; assertion/check sites: 13.
- Имена файлов из ссылок исходника (существуют в дереве): `video_core/renderer_vulkan/vk_instance.h`, `video_core/renderer_vulkan/vk_scheduler.h`, `video_core/texture_cache/image.h`.

## `tests/test_test_profiles.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Independent launcher profiles using a shared, read-only installation.
- Запуск: `python test_test_profiles.py`; assertion/check sites: 18.
- Сценарии: `test_open_uses_selected_profile_without_switching_parent`, `test_relative_path_and_file_are_rejected_without_launching`, `test_child_profile_replaces_parent_port`, `test_numbered_profiles_have_stable_ports`, `test_game_environment_selects_profile_port_and_respects_override`, `test_explicit_profile_skips_legacy_import_and_routes_all_data`.
- Ограничения: mock/stub не доказывает игровую интеграцию; Qt venv/PySide6.

## `tests/test_trophy_data.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: bbport_trophies.h, common/aes.h, platinum.h
- Запуск: `CMake: trophy-data-test`; assertion/check sites: 23.
- Имена файлов из ссылок исходника (существуют в дереве): `bbport_trophies.h`, `common/aes.h`.

## `tests/test_trophy_toast.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: a.c, a.h, all.c, all.h, bbport_trophy_media.h, bbport_trophy_toast_model.h
- Запуск: `CMake: trophy-toast-test`; assertion/check sites: 77.
- Имена файлов из ссылок исходника (существуют в дереве): `bbport_trophy_media.h`, `bbport_trophy_toast_model.h`, `libavutil/log.h`.

## `tests/test_ui_composition.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: gpu/shadps4/video_core/renderer_vulkan/ui_composition.h
- Запуск: `CMake: ui-composition-test`; assertion/check sites: 17.
- Имена файлов из ссылок исходника (существуют в дереве): `gpu/shadps4/video_core/renderer_vulkan/ui_composition.h`.

## `tests/test_ultrawide.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_canvas, test_2560x1080_matches_the_community_patch, test_3440x1440_values, test_matrix_round_trip, test_moves_named_placements, test_full_screen_backdrop_is_widened_around_the_centre, test_nothing_to_widen
- Запуск: `python test_ultrawide.py`; assertion/check sites: 15.
- Сценарии: `test_canvas`, `test_2560x1080_matches_the_community_patch`, `test_3440x1440_values`, `test_matrix_round_trip`, `test_moves_named_placements`, `test_full_screen_backdrop_is_widened_around_the_centre`, `test_nothing_to_widen`.

## `tests/test_upscaler_assets.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_tier_depends_on_output_not_render_preset, test_partial_model_is_not_reported_available, test_complete_model_and_wrong_initializer
- Запуск: `unittest discover -s tests -p test_upscaler_assets.py`; assertion/check sites: 6.
- Сценарии: `test_tier_depends_on_output_not_render_preset`, `test_partial_model_is_not_reported_available`, `test_complete_model_and_wrong_initializer`.

## `tests/test_upscaler_support.cpp`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: bbport_settings.h, unistd.h
- Запуск: `CMake: upscaler-support-test`; assertion/check sites: 28.
- Имена файлов из ссылок исходника (существуют в дереве): `bbport_settings.h`.

## `tools/test_signaling_startup.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Compile actual signaling startup functions against a threaded rollback fixture.
- Запуск: `python test_signaling_startup.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `np_signaling.cpp`, `np_signaling_helpers.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/emulator/tests/gcn/gcn_test_runner.cpp`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: dev.c, device_.c, gcn_test_runner.h, physical_device_.c, shader_recompiler/resource.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `shader_recompiler/resource.h`.

## `mods-src/BBSC/emulator/tests/gcn/test_gcn_instructions.cpp`

- Решение: Сохранить upstream emulator/test support.
- Назначение/контракт: gcn_test_runner.h, gtest/gtest.h, half.h, instructions.h, no_overflow.h, overflow.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 141.

## `mods-src/BBSC/emulator/tests/gcn/translator.cpp`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: common/io_file.h, runtime_info.c, shader_recompiler/backend/spirv/emit_spirv.h, shader_recompiler/frontend/decode.h, shader_recompiler/frontend/translate/translate.h, shader_recompiler/info.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `common/io_file.h`, `shader_recompiler/backend/spirv/emit_spirv.h`, `shader_recompiler/frontend/decode.h`, `shader_recompiler/frontend/translate/translate.h`, `shader_recompiler/info.h`, `shader_recompiler/ir/basic_block.h`, `shader_recompiler/ir/passes/ir_passes.h`, `shader_recompiler/ir/post_order.h`, `shader_recompiler/ir/program.h`, `shader_recompiler/profile.h`, `shader_recompiler/recompiler.h`.

## `mods-src/BBSC/emulator/tests/network/test_http_lifecycle.cpp`

- Решение: Сохранить upstream emulator/test support.
- Назначение/контракт: //example.c, //host.example.c, //new.example.c, //path.example.c, //secure.example.c, analytics.example.c
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 604.
- Имена файлов из ссылок исходника (существуют в дереве): `common/types.h`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `mods-src/BBSC/emulator/tests/network/test_http_parse_response_header.cpp`

- Решение: Сохранить upstream emulator/test support.
- Назначение/контракт: common/types.h, core/libraries/network/http.h, core/libraries/network/http_error.h, gtest/gtest.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 67.
- Имена файлов из ссылок исходника (существуют в дереве): `common/types.h`, `core/libraries/network/http.h`, `core/libraries/network/http_error.h`.

## `mods-src/BBSC/emulator/tests/network/test_http_status_line.cpp`

- Решение: Сохранить upstream emulator/test support.
- Назначение/контракт: common/types.h, core/libraries/network/http.h, core/libraries/network/http_error.h, gtest/gtest.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 79.
- Имена файлов из ссылок исходника (существуют в дереве): `common/types.h`, `core/libraries/network/http.h`, `core/libraries/network/http_error.h`.

## `mods-src/BBSC/emulator/tests/network/test_http_uri.cpp`

- Решение: Сохранить upstream emulator/test support.
- Назначение/контракт: ../sibling.h, ./bar.h, ./default.h, //bar.c, //cdn.example.c, //example.c
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 217.

## `mods-src/BBSC/emulator/tests/stubs/bloodborne_http_stub.cpp`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: core/bloodborne_re.h, core/debugger.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/bloodborne_re.h`, `core/debugger.h`.

## `mods-src/BBSC/emulator/tests/stubs/common_stub.cpp`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: common_stub
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 0.

## `mods-src/BBSC/emulator/tests/stubs/core_stub.cpp`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: emulator.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator.h`.

## `mods-src/BBSC/emulator/tests/stubs/kernel_stub.cpp`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: core/libraries/kernel/process.h, tests/stubs/kernel_stub.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/libraries/kernel/process.h`, `tests/stubs/kernel_stub.h`.

## `mods-src/BBSC/emulator/tests/stubs/kernel_stub.h`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: common/types.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `common/types.h`.

## `mods-src/BBSC/emulator/tests/stubs/loader_stub.cpp`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: common/types.h, core/loader/symbols_resolver.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `common/types.h`, `core/loader/symbols_resolver.h`.

## `mods-src/BBSC/emulator/tests/stubs/resource_tracking_pass_stub.cpp`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: desc.c, existing.c, shader_recompiler/frontend/control_flow_graph.h, shader_recompiler/info.h, shader_recompiler/ir/basic_block.h, shader_recompiler/ir/breadth_first_search.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 1.
- Имена файлов из ссылок исходника (существуют в дереве): `shader_recompiler/frontend/control_flow_graph.h`, `shader_recompiler/info.h`, `shader_recompiler/ir/basic_block.h`, `shader_recompiler/ir/breadth_first_search.h`, `shader_recompiler/ir/ir_emitter.h`, `shader_recompiler/ir/operand_helper.h`, `shader_recompiler/ir/program.h`, `shader_recompiler/ir/reinterpret.h`, `shader_recompiler/profile.h`, `video_core/amdgpu/resource.h`.

## `mods-src/BBSC/emulator/tests/stubs/scm_rev_stub.cpp`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: //github.c, common/scm_rev.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `common/scm_rev.h`.

## `mods-src/BBSC/emulator/tests/stubs/sdl_stub.cpp`

- Решение: Сохранить вспомогательный файл.
- Назначение/контракт: SDL3/SDL_messagebox.h, sdl_window.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `sdl_window.h`.

## `mods-src/BBSC/emulator/tests/test_emulator_settings.cpp`

- Решение: Сохранить upstream emulator/test support.
- Назначение/контракт: after.c, common/path_util.h, common/scm_rev.h, core/emulator_settings.h, core/emulator_state.h, gtest/gtest.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 204.
- Имена файлов из ссылок исходника (существуют в дереве): `common/path_util.h`, `common/scm_rev.h`, `core/emulator_settings.h`, `core/emulator_state.h`, `nlohmann/json.h`.

## `mods-src/BBSC/emulator/tests/test_ngs2.cpp`

- Решение: Сохранить upstream emulator/test support.
- Назначение/контракт: core/libraries/error_codes.h, core/libraries/ngs2/ngs2.h, core/libraries/ngs2/ngs2_error.h, gtest/gtest.h, info.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 10.
- Имена файлов из ссылок исходника (существуют в дереве): `core/libraries/error_codes.h`, `core/libraries/ngs2/ngs2.h`, `core/libraries/ngs2/ngs2_error.h`, `info.h`.

## `mods-src/BBSC/emulator/tests/test_windows_guest_red_zone_protection_settings.cpp`

- Решение: Сохранить upstream emulator/test support.
- Назначение/контракт: common/path_util.h, core/emulator_settings.h, core/emulator_state.h, encoded.c, gtest/gtest.h, nlohmann/json.h
- Запуск: `GoogleTest/CMake emulator`; assertion/check sites: 24.
- Имена файлов из ссылок исходника (существуют в дереве): `common/path_util.h`, `core/emulator_settings.h`, `core/emulator_state.h`, `nlohmann/json.h`.

## `mods-src/BBSC/party/test_compat.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Actual socket probes against compatibility components in independent client processes.
- Запуск: `python test_compat.py`; assertion/check sites: 52.
- Сценарии: `test_chosen_names_roundtrip_without_changing_durable_identity`, `test_closed_room_retires_with_bell_and_recreation_fences_late_leave`, `test_compatibility_native_contract`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон.

## `mods-src/BBSC/party/test_data_flow.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Network regressions: status refresh and pending/idle relay recipients.
- Запуск: `unittest discover -s mods-src/BBSC/party -p test_data_flow.py`; assertion/check sites: 13.
- Сценарии: `test_status_refresh`, `test_pending_guest_chunks_idle_roster`, `test_routing`.

## `mods-src/BBSC/party/test_host_rotation.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Host rotation, failed admission withdrawal and guest cancellation over real sockets.
- Запуск: `python test_host_rotation.py`; assertion/check sites: 22.
- Сценарии: `test_former_host_sign_returned_after_rotation_with_another_guest`, `test_rotation_with_failed_claim_and_quit_during_join`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `mods-src/BBSC/party/test_identity.py`

- Решение: Актуализирован в аудите.
- Назначение/контракт: test_recorded_ids_no_longer_change_in_native_int32, test_collision_rejected_before_startup
- Запуск: `python test_identity.py`; assertion/check sites: 5.
- Сценарии: `test_recorded_ids_no_longer_change_in_native_int32`, `test_collision_rejected_before_startup`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `mods-src/BBSC/party/test_idle.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_real_np_and_relay_survive_idle, test_partial_header_and_body_share_deadline, test_stdout_rotation_and_no_secret_dump
- Запуск: `python test_idle.py`; assertion/check sites: 7.
- Сценарии: `test_real_np_and_relay_survive_idle`, `test_partial_header_and_body_share_deadline`, `test_stdout_rotation_and_no_secret_dump`.

## `mods-src/BBSC/party/test_io_workers.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Durability barriers and network isolation without native compilation or game data.
- Запуск: `unittest discover -s mods-src/BBSC/party -p test_io_workers.py`; assertion/check sites: 25.
- Сценарии: `test_batched_receipts_ack_after_disk_and_restart_dedup`, `test_legacy_receipts_migrated_before_control_rewrite`, `test_final_revision_not_visible_before_control_write`, `test_disk_failure_never_acknowledged`, `test_slow_peer_does_not_block_other_peer`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `mods-src/BBSC/party/test_logging.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Diagnostic event output must not touch disk or session state in release mode.
- Запуск: `python test_logging.py`; assertion/check sites: 1.
- Сценарии: `test_release_skips_io_and_diagnostic_mode_records_events`.

## `mods-src/BBSC/party/test_menu_rejoin.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Explicit menu/Blank cancellation must not poison a later admission.
- Запуск: `unittest discover -s mods-src/BBSC/party -p test_menu_rejoin.py`; assertion/check sites: 7.
- Сценарии: `test_cancel_retired_after_guest_idle_and_final_leave`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `mods-src/BBSC/party/test_native_gate.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production gate dispatch + actual Windows trampoline and exact item entry bytes.
- Запуск: `python test_native_gate.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/cpu_patches.h`, `emulator/mod/bbsc_hooks.cpp`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/party/test_native_member_ids.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: The real party allocator and protobuf replies must use shadNet native member IDs.
- Запуск: `python test_native_member_ids.py`; assertion/check sites: 20.
- Сценарии: `test_allocator_reuses_places_and_changes_incarnation_across_generation_wrap`, `test_legacy_live_room_is_not_rewritten_and_can_drain`, `test_three_real_native_api_clients_receive_correct_ids_and_slot_mask`, `test_host_blank_requires_real_native_idle_before_another_beckoner`.

## `mods-src/BBSC/party/test_pipeline.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Ordered, bounded multipart traffic over independent faulted clients.
- Запуск: `unittest discover -s mods-src/BBSC/party -p test_pipeline.py`; assertion/check sites: 8.
- Сценарии: `test_windowed_chunks_with_latency_reorder_and_recipient_gaps`, `test_recipient_gaps_and_new_connection_stream`.

## `mods-src/BBSC/party/test_processes.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: test_one_cancel_generation, test_three_concurrent_rotation, test_admission_leave_rejoin, test_crash_partition_restore, test_faults_and_chunk_delivery, test_membership, test_coordinator_restart_after_durable_commit, test_explicit_close_waits_for_guest_acknowledgements, test_network_rejects_wrong_group_sender_mac_and_generation, test_stale_generations_and_wrong_coordinator
- Запуск: `python test_processes.py`; assertion/check sites: 53.
- Сценарии: `test_one_cancel_generation`, `test_three_concurrent_rotation`, `test_admission_leave_rejoin`, `test_crash_partition_restore`, `test_faults_and_chunk_delivery`, `test_membership`, `test_coordinator_restart_after_durable_commit`, `test_explicit_close_waits_for_guest_acknowledgements`, `test_network_rejects_wrong_group_sender_mac_and_generation`, `test_stale_generations_and_wrong_coordinator`.
- Имена файлов из ссылок исходника (существуют в дереве): `lite.py`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон.

## `mods-src/BBSC/party/test_rpc.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Combined bridge RPC, HTTP pooling and final leave checks without native builds.
- Запуск: `unittest discover -s mods-src/BBSC/party -p test_rpc.py`; assertion/check sites: 42.
- Сценарии: `test_timeout_is_bounded_and_never_submits_another_claim`, `test_rejection_and_other_operations_are_not_retried`, `test_claim_recovers_confirmation_after_first_deadline`, `test_combined_status_keepalive_and_current_title_ticket`, `test_host_menu_retained_bell_waits_for_guest_then_releases`, `test_bell_notice_generation_excludes_host_and_legacy_reply`, `test_bell_release_is_explicit_final_and_legacy_compatible`, `test_private_http_backlog_capacity`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `mods-src/BBSC/party/test_winhttp_bridge.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Real production Windows WinHTTP bridge against independent party clients, no game.
- Запуск: `python test_winhttp_bridge.py`; assertion/check sites: 18.
- Сценарии: `test_notice_reply_versions_and_malformed_release`, `test_blocked_http_does_not_block_cancel_or_revive_grant`, `test_native_title_waits_for_unanimous_leave`, `test_actual_winhttp_and_native_process_fence`.
- Имена файлов из ссылок исходника (существуют в дереве): `bbsc_party.h`, `emulator/mod/bbsc_party.cpp`.

## `mods-src/BBSC/server/gameserver/tests/test_relay_departures.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Relay EOF notifications must be scoped to the departing player's party.
- Запуск: `python test_relay_departures.py`; assertion/check sites: 29.
- Сценарии: `test_guest_eof_notifies_host_and_other_guest_only`, `test_host_eof_identifies_host_without_closing_other_connections`, `test_duplicate_eof_does_not_repeat_notification`, `test_solo_or_unidentified_socket_cannot_end_a_party`, `test_changed_party_does_not_notify_previous_party`, `test_replacement_before_old_eof_preserves_party`, `test_replacement_after_eof_cancels_even_racing_timer`, `test_new_socket_genuine_eof_not_hidden_by_old_socket`, `test_explicit_leave_is_immediate_but_stale_socket_cannot_send_it`, `test_wrong_identity_or_party_does_not_cancel_pending`, `test_old_callback_cannot_remove_newer_pending_decision`.
- Имена файлов из ссылок исходника (существуют в дереве): `bbsc_gameserver.py`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `mods-src/BBSC/server/gameserver/tests/test_relay_queue_diagnostics.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production TCP writer queue accounting; no socket or worker threads in fixtures.
- Запуск: `python test_relay_queue_diagnostics.py`; assertion/check sites: 20.
- Сценарии: `test_batch_bytes_order_and_inflight_accounting`, `test_failure_preserves_inflight_evidence_and_clears_queue`, `test_oldest_age_and_overflow`.
- Имена файлов из ссылок исходника (существуют в дереве): `bbsc_gameserver.py`.
- Ограничения: mock/stub не доказывает игровую интеграцию.

## `mods-src/BBSC/server/gameserver/tests/test_udp_packet_trace.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production BBR1 relay trace: identical frame hashes, drops, failures and bound.
- Запуск: `python test_udp_packet_trace.py`; assertion/check sites: 24.
- Сценарии: `test_attempt_renewal_duplicates_expiry_and_isolation`, `test_production_forward_drop_error_and_bound`.

## `mods-src/BBSC/tools/souls/test_anim.py`

- Решение: Ручной; внешняя среда.
- Назначение/контракт: Render a few frames of the rigged Hunter playing one animation (checks skinning + orientation).
- Запуск: `python test_anim.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `test_anim.py`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку; Blender bpy + game data.

## `mods-src/BBSC/tools/souls/test_cast.py`

- Решение: Ручной; внешняя среда.
- Назначение/контракт: Cast line-up: both hunters, Gascoigne (human) and Lady Maria built from parts, idle pose.
- Запуск: `python test_cast.py`; assertion/check sites: 0.
- Ограничения: исполняемый скрипт: импорт может запускать проверку; Blender bpy + game data.

## `mods-src/BBSC/tools/souls/test_map.py`

- Решение: Ручной; внешняя среда.
- Назначение/контракт: Import an exported map area and render a few views (checks placement, rotation, textures).
- Запуск: `python test_map.py`; assertion/check sites: 0.
- Ограничения: исполняемый скрипт: импорт может запускать проверку; Blender bpy + game data.

## `mods-src/BBSC/tools/test_bell_refund.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: emulator/src/core/bloodborne_re.cpp, test_bell_refund.cpp
- Запуск: `python test_bell_refund.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_blank_host_end.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute production host Blank completion with native Stop stubbed in executable memory.
- Запуск: `python test_blank_host_end.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_boss_load_cleanup.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise production pre-load boss cleanup ordering; no game or saves used.
- Запуск: `python test_boss_load_cleanup.py`; assertion/check sites: 4.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_boss_quit.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run the production boss-clear hook through delayed quit callbacks.
- Запуск: `python test_boss_quit.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_cainhurst_reveal.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production Cainhurst reveal/pickup fixture; optional read-only BB_GAME data audit.
- Запуск: `python test_cainhurst_reveal.py`; assertion/check sites: 6.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_chalice_scope.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise production dungeon reads, snapshot assembly and scope switches without a game.
- Запуск: `python test_chalice_scope.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/bbsc_chalice.h`, `core/libraries/np/np_signaling/np_signaling_bbsc.h`, `emulator/mod/bbsc_relay.cpp`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_coop_selection_masks.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute both native slot-mask blocks with the production Hunters patches.
- Запуск: `python test_coop_selection_masks.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/bbsc_patch_tables.h`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_death_hotpaths.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production death event deduplication and hot-path guard/cache regression fixtures.
- Запуск: `python test_death_hotpaths.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/mod/bbsc_mod.cpp`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_departure_banner.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise departure identity selection through the production native trampoline.
- Запуск: `python test_departure_banner.py`; assertion/check sites: 2.
- Имена файлов из ссылок исходника (существуют в дереве): `core/cpu_patches.h`, `emulator/mod/bbsc_hooks.cpp`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_dream_finale_static.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Read-only finale inventory/native-site checks. Does not compile or run the mod.
- Запуск: `python test_dream_finale_static.py`; assertion/check sites: 22.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bbsc_dream_finale.h`, `emulator/src/core/bloodborne_re.cpp`, `tools/test_dream_finale_static.py`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_echo_hud.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise production HUD acknowledgement, without touching game memory or saves.
- Запуск: `python test_echo_hud.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_explicit_host_return.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production explicit-host-leave grace and native/fallback return ownership.
- Запуск: `python test_explicit_host_return.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_follow_arrival.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: emulator/src/core/bloodborne_re.cpp, t.cpp
- Запуск: `python test_follow_arrival.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_guest_bells.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise the production goods-use result: guest bell restriction is not a UI-only rule.
- Запуск: `python test_guest_bells.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_guest_transition_doors.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production guest guard and actual native action rejection; read-only ELF input.
- Запуск: `python test_guest_transition_doors.py`; assertion/check sites: 2.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_home_return.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production home-return functions, without game files or saves.
- Запуск: `python test_home_return.py`; assertion/check sites: 4.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_home_return_order.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Source control-flow checks for the shared native/fallback return transaction.
- Запуск: `python test_home_return_order.py`; assertion/check sites: 14.
- Сценарии: `test_native_claims_before_continuing_and_duplicate_returns`, `test_fallback_waits_for_native_and_shares_claim`, `test_failed_prerequisites_do_not_claim`, `test_load_does_not_reset_ownership`.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям.

## `mods-src/BBSC/tools/test_hook_resume.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run the production Windows hook trampoline on synthetic code, never on the game.
- Запуск: `python test_hook_resume.py`; assertion/check sites: 2.
- Имена файлов из ссылок исходника (существуют в дереве): `core/cpu_patches.h`, `emulator/mod/bbsc_hooks.cpp`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_http_accept_burst.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Real loopback burst against the production HTTP server's pending-accept queue.
- Запуск: `python test_http_accept_burst.py`; assertion/check sites: 2.
- Имена файлов из ссылок исходника (существуют в дереве): `server/gameserver/bbsc_gameserver.py`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_join_destination.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Never apply a dungeon transform in a Dream loaded by the native summon.
- Запуск: `python test_join_destination.py`; assertion/check sites: 6.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_join_stop_deadline.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute the production hook and exact native deadline predicate/trampoline.
- Запуск: `python test_join_stop_deadline.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/cpu_patches.h`, `emulator/mod/bbsc_hooks.cpp`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_join_teleport.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise the production initial placement tick; no game/DLL build or live saves.
- Запуск: `python test_join_teleport.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_load_readiness.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production inventory barrier: never open a guest world before its generation is reconciled.
- Запуск: `python test_load_readiness.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_local_key_bank.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise the production hook and native bank switch (read-only ELF argument).
- Запуск: `python test_local_key_bank.py`; assertion/check sites: 2.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_matchmaking_native.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: emulator/src/core/bloodborne_re.cpp, test_matchmaking_native.cpp
- Запуск: `python test_matchmaking_native.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_member_binding.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise the production binding/watchdog logic without a DLL or game build.
- Запуск: `python test_member_binding.py`; assertion/check sites: 5.
- Имена файлов из ссылок исходника (существуют в дереве): `core/bbsc_patch_tables.h`, `emulator/src/core/bbsc_patch_tables.h`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_memory_hotpath.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production access checks and map snapshots: permissions, bounds, reload and lookup count.
- Запуск: `python test_memory_hotpath.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_menu_quit.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise production menu-exit/save ordering without a game or player saves.
- Запуск: `python test_menu_quit.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_native_kit_sources.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: emulator/src/core/bloodborne_re.cpp, test_native_kit_sources.cpp
- Запуск: `python test_native_kit_sources.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_native_leave_release.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute the native-leave policy; active sessions must keep their persistence patches.
- Запуск: `python test_native_leave_release.py`; assertion/check sites: 3.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_negotiation_failure_trace.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute the production failure observer through its exact native instruction hook.
- Запуск: `python test_negotiation_failure_trace.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/cpu_patches.h`, `emulator/mod/bbsc_channel.cpp`, `emulator/mod/bbsc_hooks.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_notebook_popup.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: emulator/src/core/bloodborne_re.cpp, popups.c, test_notebook_popup.cpp
- Запуск: `python test_notebook_popup.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_original_bells.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: emulator/src/core/bloodborne_re.cpp, test_original_bells.cpp
- Запуск: `python test_original_bells.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_party_bell_notice.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute the production bell-notice tick without the game.
- Запуск: `python test_party_bell_notice.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_party_item_async.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute the production deferred item gate + mailbox, including late HTTP answers.
- Запуск: `python test_party_item_async.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `bbsc_party_acquire.h`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_party_menu_barrier.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run production menu/save fixture with the actual party title gate compiled in.
- Запуск: `python test_party_menu_barrier.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `test_menu_quit.py`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_party_tick_gate.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Compile the production tick observation block: disabled mode does no game reads.
- Запуск: `python test_party_tick_gate.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_pending_work.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run production work notifications and scaling code in a concurrent C++ fixture.
- Запуск: `python test_pending_work.py`; assertion/check sites: 3.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_perf_policy.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Regression checks for production trace selection and reload-safe param lookup.
- Запуск: `python test_perf_policy.py`; assertion/check sites: 5.
- Имена файлов из ссылок исходника (существуют в дереве): `bloodborne_re.cpp`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_personal_progress_commit.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Targeted production-function fixtures. Run explicitly before the next build.
- Запуск: `python test_personal_progress_commit.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_post_load_recovery.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run the production post-load recovery and kept-death override in a memory fixture.
- Запуск: `python test_post_load_recovery.py`; assertion/check sites: 5.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_pvp_dregs.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production lethal-hook/award bodies, plus byte checks on an optional research ELF.
- Запуск: `python test_pvp_dregs.py`; assertion/check sites: 4.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/mod/bbsc_register.h`, `emulator/src/core/bbsc_dreg_rules.h`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_quest_rewards.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production gates + real native death predicate/trampoline, fake actors only.
- Запуск: `python test_quest_rewards.py`; assertion/check sites: 10.
- Имена файлов из ссылок исходника (существуют в дереве): `core/bbsc_quest_reward_rules.h`, `core/cpu_patches.h`, `emulator/mod/bbsc_hooks.cpp`, `emulator/src/core/bbsc_quest_reward_rules.h`, `emulator/src/core/bloodborne_re.cpp`, `tools/gamedata/quest_reward_rules.py`, `tools/test_quest_rewards.py`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_register_wait.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute the native wait predicate through the production Windows trampoline.
- Запуск: `python test_register_wait.py`; assertion/check sites: 5.
- Имена файлов из ссылок исходника (существуют в дереве): `bbsc_register_wait.h`, `core/cpu_patches.h`, `emulator/mod/bbsc_hooks.cpp`, `emulator/mod/bbsc_register.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_relay_dispatch.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute the actual shared relay/P2P dispatcher, including the mount/register collision.
- Запуск: `python test_relay_dispatch.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/bbsc_chalice.h`, `emulator/mod/bbsc_relay.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_repeat_death.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise production HP death lifecycle without game files.
- Запуск: `python test_repeat_death.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_repeated_consumable_awards.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run the production repeated-lot guard against isolated inventory/ledger state.
- Запуск: `python test_repeated_consumable_awards.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_resident_guest_leave.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run production send-home hook and deferred lock release without game files.
- Запуск: `python test_resident_guest_leave.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_resident_summon_completion.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production resident-completion policy plus exact native drain and selection gate.
- Запуск: `python test_resident_summon_completion.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/cpu_patches.h`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_responder_area_gate.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run exact native responder area eligibility: reproduce crossed bell, then patch it.
- Запуск: `python test_responder_area_gate.py`; assertion/check sites: 1.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_runtime_perf.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production progress merge and NPC event index regressions; isolated memory only.
- Запуск: `python test_runtime_perf.py`; assertion/check sites: 3.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_scaling_repository.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Live repository discovery, real table preparation, span/fallback scaling and owner lifetime.
- Запуск: `python test_scaling_repository.py`; assertion/check sites: 2.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_second_guest_cooldown.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production selector hook + exact native scan/consume and builder cooldown.
- Запуск: `python test_second_guest_cooldown.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/cpu_patches.h`, `emulator/mod/bbsc_hooks.cpp`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_session_register.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise the real provider with a deterministic clock and no running game.
- Запуск: `python test_session_register.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/mod/bbsc_register.cpp`, `emulator/mod/bbsc_register.h`, `emulator/mod/bbsc_register_wait.h`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_shared_keys.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Permanent shared-key receipts survive trip completion and a journal reload.
- Запуск: `python test_shared_keys.py`; assertion/check sites: 3.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_shared_progress_policy.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Compile production home-merge policy; no game or save files touched.
- Запуск: `python test_shared_progress_policy.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: сейвы/восстановление/durable state: выбирать методы; не обязательный полный прогон; строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_sign_refresh.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Exercise the native own-sign dirty queue, not a second HTTP claim consumer.
- Запуск: `python test_sign_refresh.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_silence_beckoning_hook.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Confirmed Blank menu callback: exact native store through production trampoline.
- Запуск: `python test_silence_beckoning_hook.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/cpu_patches.h`, `emulator/mod/bbsc_hooks.cpp`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_stop_phases.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Execute production Stop drain hook against memory fixtures.
- Запуск: `python test_stop_phases.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `core/bbsc_stop_policy.h`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_summon_cleanup.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run the production HTTP lifecycle functions against a deterministic broker.
- Запуск: `python test_summon_cleanup.py`; assertion/check sites: 0.
- Имена файлов из ссылок исходника (существуют в дереве): `bbsc_network_attempt.h`, `emulator/mod/bbsc_http.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_targeted_kick.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Production targeted-kick policy and the real native host-entry trampoline.
- Запуск: `python test_targeted_kick.py`; assertion/check sites: 4.
- Имена файлов из ссылок исходника (существуют в дереве): `core/cpu_patches.h`, `emulator/mod/bbsc_hooks.cpp`, `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_title_request_native.py`

- Решение: Ручной; внешняя среда.
- Назначение/контракт: Execute native title/reload commands on fake memory, without starting the game.
- Запуск: `python test_title_request_native.py`; assertion/check sites: 9.
- Имена файлов из ссылок исходника (существуют в дереве): `tools/test_title_request_native.py`.
- Ограничения: исполняемый скрипт: импорт может запускать проверку.

## `mods-src/BBSC/tools/test_wipe_join_banners.py`

- Решение: Сохранить; статический обзор.
- Назначение/контракт: Run production per-member wipe banner filtering, including concurrent real joins.
- Запуск: `python test_wipe_join_banners.py`; assertion/check sites: 4.
- Имена файлов из ссылок исходника (существуют в дереве): `emulator/src/core/bloodborne_re.cpp`.
- Ограничения: строковое извлечение production: чувствителен к переименованиям; исполняемый скрипт: импорт может запускать проверку.

## `tests/test_localization.py`

- Сохранить: подстановки русского перевода, генерация BBSC, строки меню и геометрия компонентов Qt.
- Запуск: `out/qt-venv/Scripts/python.exe tests/test_localization.py` из корня; без игры и профилей.
