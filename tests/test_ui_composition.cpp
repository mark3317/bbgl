// SPDX-License-Identifier: GPL-2.0-or-later
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <limits>
#include "gpu/shadps4/video_core/renderer_vulkan/ui_composition.h"

int main() {
    using namespace Vulkan::UiComposition;
    // A subpixel uncovered edge must move past the first/last pixel centres at
    // every output size, for either Vulkan Y direction. Alpha is still provided
    // by the original fade shader (no second overlay or repeated blending).
    for (const auto size : {std::pair{1280,720}, {1920,1080}, {2560,1440},
                            {3440,1440}, {3840,2160}, {5120,1440}}) {
        for (bool flipped : {false, true}) {
            float x = 0, y = flipped ? float(size.second) : 0;
            float w = float(size.first), h = flipped ? -float(size.second) : float(size.second);
            assert(ExpandFadeViewport(0x17e76c08, x, y, w, h));
            const float top = std::min(y, y + h), bottom = std::max(y, y + h);
            // Model an inward one-pixel raster edge at each side.
            assert(x + 1 < 0.5f && x + w - 1 > size.first - 0.5f);
            assert(top + 1 < 0.5f && bottom - 1 > size.second - 0.5f);
        }
    }
    for (uint64_t hash : {uint64_t{0x34e8a281}, uint64_t{0x0b0acf50}}) {
        float x=0, y=0, w=1920, h=1080;
        assert(!ExpandFadeViewport(hash,x,y,w,h));
        assert(x==0 && y==0 && w==1920 && h==1080);
    }
    for (float offset : {20.0f, std::numeric_limits<float>::quiet_NaN()}) {
        float x=offset, y=0, w=1920, h=1080;
        assert(!ExpandFadeViewport(0x17e76c08,x,y,w,h));
        assert(w==1920 && h==1080);
    }
    // Title/loading menus have no depth/camera. UI must still go to the native target.
    assert(Choose(true, true, false, true) == Background::Copy);
    assert(Choose(true, true, false, false) == Background::Copy);
    // The title/loading fade can be the frame's only color draw.
    assert(Choose(true, MovieShader(0x17e76c08), false, true) == Background::Copy);
    // In-game HUD: first reconstruct the scene, then draw the native UI over it.
    assert(Choose(true, true, true, true) == Background::Temporal);
    // Runtime FSR disable/failure must not change UI resolution.
    assert(Choose(true, true, true, false) == Background::Copy);
    assert(Choose(true, false, true, true) == Background::None);
    assert(Choose(false, true, true, true) == Background::None);
    const auto [w,h] = MovieViewport();
    assert(NativeViewport(float(w), -float(h)));
    if (std::getenv("BB_UI_RES")) {
        const auto native = Scale(960,540,w,h,true);
        assert(native[0]==1 && native[1]==1);
        const auto scene = Scale(960,540,w,h,false);
        assert(scene[0]==float(w)/960 && scene[1]==float(h)/540);
        std::puts("UI composition: custom movie viewport preserved without doubling PASS");
        return 0;
    }
    assert(!NativeViewport(960, -540));
    assert(MovieShader(0x34e8a281) && MovieShader(0x24042a9b));
    assert(!MovieShader(0x0b0acf50)); // fullscreen post/tonemap also has a native viewport
    assert(!MovieShader(0x6c62a79f)); // shadow geometry
    const auto display = Scale(960, 540, 1920, 1080, false);
    assert(display[0] == 2 && display[1] == 2);
    const auto ui = Scale(960, 540, 1920, 1080, true);
    assert(ui[0] == 1 && ui[1] == 1); // don't double an already native UI viewport
    const auto larger = Scale(960, 540, 3840, 2160, true);
    assert(larger[0] == 2 && larger[1] == 2);
    std::puts("UI composition: PASS (menu without camera, HUD, FSR off, viewport scaling)");
}
