# Silver arrow (variant 1)

Approved by the user on 4 November 2026 for the in-game mouse cursor.
Created with the built-in ImageGen tool using the comparison sheet from this chat
as a reference; no original game assets are included.

`silver-arrow.png` is the transparent master. `silver-arrow-32x48.png` is the
normal-size preview. `python tools/build_silver_cursor.py` converts the master
to embedded RGBA surfaces in `gpu/shim/silver_cursor_data.h` (32x48 and 64x96).
Pillow is a development dependency only. SDL selects the appropriate DPI image.
The click hotspot is the first solid pixel at the upper-left tip, (1,1).

The game window owns the SDL cursor. Native menus, the guide and Atlas share it;
existing mouse capture and visibility rules remain in `WindowSDL::PollEvents`.
ImGui does not draw a second arrow. System cursors outside the game are untouched.

## Final image prompt (built-in ImageGen)

Extract and faithfully recreate ONLY cursor variant 1, the LEFTMOST large silver
arrow from the reference sheet, as one isolated production UI cursor on a truly
transparent background. Preserve the distinctive silhouette, narrow arrow
pointing upper-left, short lower-right stem, small rounded notch on the RIGHT
edge where head meets stem, tarnished silver surface, bright thin silver bevel
and dark outline. No other variants. No numbers, text, sheet, background, floor,
ambient shadow or duplicates. Flat front view sprite, no perspective. Tight
framing with small transparent padding, entire arrow fully inside image. High
contrast silver rather than black fill, restrained fine scratches that remain
legible after reduction to 40 pixels tall. Precise sharp upper-left tip is the
click hotspot. This is the selected variant 1 for in-game menus.
