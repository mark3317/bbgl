# Build and release

Use Windows x64, Visual Studio C++ Build Tools (with Clang), Windows Python 3.10+ and MSYS2 CLANG64. Install the dependencies in [the Windows toolchain guide](packaging/windows/README.md).

```sh
git clone https://github.com/mark3317/bbgl.git
cd bbgl
git checkout develop
git submodule update --init gpu/third_party/fsr-vulkan gpu/third_party/imgui third_party/LibAtrac9 gpu/third_party/magic_enum gpu/third_party/miniz gpu/third_party/xbyak mods-src/BBSC
bash packaging/windows/build-coop-package.sh
```

The command builds BBSC-GL from `mods-src/BBSC`, builds the port, freezes the launcher and assembles the P2P runtime. FSR-Vulkan is pinned from the [BBGL dependency fork](https://github.com/mark3317/UniversalScalers-Vulkan), which includes the frame-resource lifetime fix used by this release. The current co-op path needs no separate game server, shadNet account or invitation. Historical server build scripts are not part of this release path.

Staging is recreated at `out/stage/Bloodborne Game Launcher`. The release files are `dist/bbgl-1.5.8-windows-x64.zip` and its `.zip.sha256`. Keep the staging path separate from installed launchers and keep player settings, saves, accounts, logs and game files outside the package.

Button prompts and the optional Diamond Sword use binary deltas from `bundled-mods`. Packaging uses prepared button prompts from `out/vendor/ready-prompts`. If the cache is empty, set `BB_PROMPT_GAME_DIR` to your own original 1.09 game folder to prepare the prompts. Diamond Sword and all cheats are disabled by default. Detailed logging, research, profiling and Vulkan validation are opt-in. See the [logging policy](docs/LOGGING.md).

`SKIP_BUILD=1` skips only the port for verified launcher-only iterations. BBSC is still rebuilt. A release candidate uses the full command without `BB_FAST_DEPLOY=1`; the fast option is for ordinary local deployment and skips release verification.

`package.sh` verifies the final staging payload once. The wrapper creates the versioned archive and SHA-256. Check ZIP structure, CRC, and file names and contents against verified staging. Extract the matching BBSC-GL ZIP from this validated launcher ZIP using its bundled DLL, Party, metadata and licences. Smoke-test the frozen launcher from the extracted ZIP in separate English and Russian temporary profiles. Follow [targeted testing rules](docs/TESTING.md); no full test sweep is required just for packaging. Record build, deployment and gameplay validation separately, and disclose untested gameplay changes.

Commit the intended BBSC changes before updating the parent gitlink. `coop/SOURCE.json` records the mod commit and whether its checkout had local changes; a candidate with local changes is not a reproducible tagged source. Do not publish or push until the user has reviewed the release text. Published tags are immutable.

When building a Git for Windows checkout from MSYS2, use the same line-ending configuration in both environments. If Git for Windows reports a clean checkout but MSYS2 reports only CRLF differences in BBSC dependencies, run the build with `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.autocrlf GIT_CONFIG_VALUE_0=true` in the MSYS2 command environment. Verify that both Git clients report a clean BBSC checkout and that `source_dirty` is false in the final ZIP.

`develop` holds ongoing work. `main` holds release source. BBGL 1.5.8 uses update tag `v1.5.8` and bundles BBSC-GL 1.5.8.
