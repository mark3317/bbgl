// Standalone SDL smoke: no Vulkan, game files, profile or save access.
// clang++ -std=c++20 -I. $(pkg-config --cflags sdl3) tests/test_silver_cursor.cpp
//     $(pkg-config --libs sdl3) -o out/silver-cursor-test.exe
#include "gpu/shim/silver_cursor.h"
#include <cstdio>

int main() {
    using namespace BbSilverCursor;
    static_assert(sizeof(Pixels1x) == Width * Height * 4);
    static_assert(sizeof(Pixels2x) == Width * Height * 16);
    static_assert(HotX >= 0 && HotX < Width && HotY >= 0 && HotY < Height);
    if (Pixels1x[(HotY * Width + HotX) * 4 + 3] < 128 || Pixels1x[3] != 0) {
        std::puts("FAIL: tip/transparent padding");
        return 1;
    }
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::printf("FAIL: SDL init: %s\n", SDL_GetError());
        return 1;
    }
    SDL_Window* window = SDL_CreateWindow("Silver cursor smoke", 320, 240, SDL_WINDOW_HIDDEN);
    if (!window) {
        std::printf("FAIL: SDL window: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }
    bool ok = true;
    for (int i = 0; i < 2; ++i) {
        SDL_Cursor* cursor = Create();
        if (!cursor || !SDL_SetCursor(cursor) || SDL_GetCursor() != cursor) {
            std::printf("FAIL: create/set cursor: %s\n", SDL_GetError());
            ok = false;
        }
        SDL_SetCursor(SDL_GetDefaultCursor());
        SDL_DestroyCursor(cursor);
    }
    SDL_DestroyWindow(window);
    SDL_Quit();
    if (ok) std::puts("PASS: RGBA sizes, transparent padding, tip hotspot, SDL create/set/destroy twice");
    return ok ? 0 : 1;
}
