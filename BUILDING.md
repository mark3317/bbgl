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

Staging: `out/stage/Bloodborne Game Launcher`. Release: `dist/bbgl-1.2.0-windows-x64.zip` and its `.zip.sha256`. Staging is recreated during packaging; never point it at an installed launcher. Player settings, saves, accounts, logs and game files must not be included.

Button prompts and the optional Diamond Sword use binary deltas from `bundled-mods`, applied to the player's own 1.09 files. No game folder is needed to build the release. Diamond Sword and all cheats are disabled by default. Detailed logging, research, profiling and Vulkan validation are opt-in; see [logging policy](docs/LOGGING.md).

`SKIP_BUILD=1` skips only the port for verified launcher-only iterations. BBSC is still rebuilt. A release candidate uses the full command without `BB_FAST_DEPLOY=1`; the fast option is for ordinary local deployment and skips release verification.

`package.sh` verifies the final staging payload once. The wrapper creates the versioned archive and SHA-256. Check the ZIP structure and CRC, then smoke-test the frozen launcher in an isolated temporary profile. Follow [targeted testing rules](docs/TESTING.md); no full test sweep is required just for packaging. Record build, deployment and gameplay validation separately, and disclose untested gameplay changes.

Commit the intended BBSC changes before updating the parent gitlink. `coop/SOURCE.json` records the mod commit and whether its checkout had local changes; a candidate with local changes is not a reproducible tagged source. Do not publish or push until the user has reviewed the release text. Published tags are immutable.

`develop` holds ongoing work; `main` holds release source. Historical BBGL tags include `v1.0.0` and `v1.1.0`; `v1.2.0` identifies BBGL 1.2.0 and its matching bundled BBSC-GL source.
