# Bloodborne Game Launcher (BBGL)

**English** · [Русский](README.ru.md) · [Download 1.0.0](https://github.com/mark3317/bbgl/releases/latest) · [Report a problem](https://github.com/mark3317/bbgl/issues)

**Bloodborne for Windows, focused on convenience and playing through the game with friends.** BBGL is a fork of [yharnam-pc](https://github.com/Jgamrot/yharnam-pc), created to make getting into the game easier, especially in co-op. Game downloading is built into the launcher, and the modified **[BBSC-GL](https://github.com/mark3317/bbsc-gl)** co-op client and hosting server are bundled. After downloading BBGL, you do not need to find separate mod, loader or server packages and match their versions yourself.

## Why this fork exists

BBGL brings installation, configuration and launching into one interface. Guided setup helps prepare the game, choose a save folder and configure co-op. Play alone or gather friends without manually installing DLLs or assembling separate BBSC components.

Version **1.0.0** implements almost all of the planned core functionality. The latest build has passed gameplay validation; further work focuses on refinements and broader gameplay coverage.

## Co-op: changes from BBSC

BBSC-GL builds on [Bloodborne Seamless Co-op](https://github.com/CLSAMG22/BBSC). Seamless sessions, networking and the underlying co-op mechanics were created by the original authors. This fork extends that foundation for playing through the game together:

- **Personal quests, shared main story.** Each player keeps their own NPC quest progress and personal rewards, while main-story progress is synchronized across the party. Play together while retaining your own character and world.
- **Personal chalice progress, seamless group exploration.** Players retain their individual chalice progress while the party can play through chalice dungeons seamlessly together. This extends the original BBSC, where this scenario is not yet implemented.
- **Return to your own world.** Guest exit, world recovery and return locations have been improved, including after visiting the host's chalice dungeon.
- **Personal interactions and rewards.** Extended guest NPC interactions and personal quest-item grants, with an option to use your own Hunter's Dream.
- **Fixes to the original mod.** Addressed repeat-summon and stale-session issues, chalice combat latency, guest return problems and the camera after a party wipe. Key-item retries, death handling and guest menu exit have also been improved.

Core scenarios have been validated with two players. Broader coverage of chalices, progression stages and larger parties is ongoing. [BBSC-GL source and development status](https://github.com/mark3317/bbsc-gl/tree/develop).

## BBGL features

- **One package for getting started.** Built-in game downloading, bundled co-op client and server, and ready-to-use button prompt packs. Game files are downloaded separately through the interface and are not included in the launcher ZIP.
- **Full Russian interface localization.** The launcher, added in-game menus and overlay are translated into Russian; English is also available.
- **Graphics settings during gameplay.** Change resolution, upscaling and supported graphics effects through the in-game menu without restarting the game, so you can tune image quality and performance during a session.
- **Redesigned interface.** Guided first launch, settings search, solo/co-op launch selection and local server management from the launcher.
- **In-game overlay.** Open trophies, map options and diagnostics with **Insert** or **L3 + R3**. The overlay follows the launcher's language.
- **Included control prompts.** PlayStation, Xbox and keyboard prompts, with the alternative packs already bundled.
- **Profile stored separately.** Settings, launcher-managed saves and co-op data live in `%LOCALAPPDATA%\Bloodborne Game Launcher`. Manually selected save folders stay where you chose them.

Bundled mod/server integration, personal versus main-story progress, seamless chalice play, Russian in-game menus and expanded live graphics controls are key additions in this fork. Features inherited from the original port and BBSC remain credited to their authors.

## Launcher

The redesigned interface supports English and Russian. Screenshots show the Russian interface.

![Home](docs/screenshots/launcher-home.png)

![Graphics settings](docs/screenshots/launcher-graphics.png)

## Start playing

1. Download `bbgl-1.0.0-windows-x64.zip` from Releases and extract it. Open the **Bloodborne Game Launcher** folder.
2. Run **Bloodborne.exe**. Use the built-in download button in setup or select an existing Bloodborne **CUSA03173, update 1.09** folder. Game files are not included in the launcher archive.
3. For solo play, launch the game normally. For co-op, choose Co-op, enter your account and the host's invite code. One player can choose **Host a session**; friends need network access to that PC, for example through Tailscale.
4. Use the in-game co-op bells to gather your party. Keep everyone on the same BBGL release.

Windows x64 and a compatible Vulkan driver are required. For graphics, hardware, controls, extracting your game and other port details, use the **[original yharnam-pc README](https://github.com/Jgamrot/yharnam-pc#readme)**.

## Source and credits

[Build BBGL](BUILDING.md) · [Changes](CHANGELOG.md) · [Credits and licences](THIRD_PARTY.md)

`main` is the release source; `develop` is ongoing work. BBSC-GL is pinned as a submodule. Internal `bbport` / `bbsc` executable names and protocol identifiers are retained for compatibility.

Based on yharnam-pc / bbport and [BBSC by CLS_AMG and contributors](https://github.com/CLSAMG22/BBSC). Their licences and attribution remain included. Bloodborne belongs to FromSoftware and Sony Interactive Entertainment; this is an independent fan project.
