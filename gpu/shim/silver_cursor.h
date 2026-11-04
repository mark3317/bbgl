// The approved minimalist silver arrow, embedded so packaging needs no loose assets.
#pragma once
#include <SDL3/SDL.h>
#include "silver_cursor_data.h"

namespace BbSilverCursor {
// Window-thread only, like SDL_CreateColorCursor. The returned cursor is owned
// by WindowSDL; SDL copies the surface pixels when creating it.
inline SDL_Cursor* Create() {
    // SDL defaults to fixed-size cursors; opt in so it uses our 2x image.
    // SDL_SetHint still respects an explicit environment override.
    SDL_SetHint("SDL_MOUSE_DPI_SCALE_CURSORS", "1");
    SDL_Surface* normal = SDL_CreateSurfaceFrom(Width, Height, SDL_PIXELFORMAT_RGBA32,
        const_cast<unsigned char*>(Pixels1x), Width * 4);
    if (!normal) return nullptr;
    SDL_Surface* high = SDL_CreateSurfaceFrom(Width * 2, Height * 2, SDL_PIXELFORMAT_RGBA32,
        const_cast<unsigned char*>(Pixels2x), Width * 8);
    if (high) {
        SDL_AddSurfaceAlternateImage(normal, high);
        SDL_DestroySurface(high);
    }
    SDL_Cursor* cursor = SDL_CreateColorCursor(normal, HotX, HotY);
    SDL_DestroySurface(normal);
    return cursor;
}
} // namespace BbSilverCursor
