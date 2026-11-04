# Classic minimalist arrow (variant 1, current)

The user selected variant 1 of the minimalist sheet and requested approximately
the default Windows cursor size. `classic-arrow.png` is the new ImageGen master;
`classic-arrow-32x32.png` is the normal-size preview. The converter packs a 32x32
canvas with an arrow at most 28px tall, plus a 64x64 high-DPI representation.
This replaces the previous 32x48/64x96 cursor (at most 46px tall at normal DPI).
The click hotspot is derived from the upper-left solid tip, as before.
The historical masters below are retained, not used at runtime.

## Classic image prompt (built-in ImageGen)

Extract and faithfully recreate ONLY variant 1, the FIRST column of the reference
comparison sheet: the CLASSIC COMPACT arrow mouse pointer. A simple conventional
arrow pointing upper-left with a vertical left edge, diagonal right edge, angular
shoulders and short stem extending lower-right. Preserve the silhouette of variant
1, NOT the elongated narrow variant 2. Solid uniform warm off-white fill, very thin
crisp near-black outline. Completely flat 2D UI sprite. Truly transparent background
and clean alpha outside the outline. NO glow, NO shadow, NO gradients, NO texture,
NO scratches, NO bevel, NO shine, NO text or number, NO other arrows. Single isolated
arrow with sharp upper-left tip and only a small transparent margin. Suitable for a
Windows-default-sized 32x32 cursor canvas. Match the minimalist reference exactly.

## Minimalist arrow (variant 2, historical)

Selected on 4 November 2026 from the second, minimalist comparison sheet:
a narrow pale arrow with a short stem and a thin dark outline.
`minimal-arrow.png` is the ImageGen master; `minimal-arrow-32x48.png` is the
normal-size preview. The existing `tools/build_silver_cursor.py` packs this
artwork into `gpu/shim/silver_cursor_data.h` for the same SDL integration.
The current click hotspot is (1,2), matching the upper-left tip after downscaling.
Old variant 1 assets below are retained as design history, not used at runtime.

## Minimalist image prompt (built-in ImageGen)

Create one production-ready transparent mouse cursor sprite by extracting ONLY
variant 2 (the second column) from the supplied comparison sheet. Preserve the
exact narrow elongated conventional arrow silhouette, pointed upper-left tip,
short lower-right stem and simple angular shoulders. Single solid pale
silver/off-white fill and a crisp thin near-black outline. Completely flat 2D UI
graphic. No texture, no grain, no scratches, no gradients, no bevels, no shine,
no shadow, no decorative details, no symbols, no text or number, no other arrows,
no dark background. The selected arrow must match variant 2, not wide variant 1
and not hollow variant 3. Keep the whole arrow inside the frame with only a little
transparent padding. Actual alpha transparency. Sharp upper-left tip for the
click hotspot. Design must be readable when scaled to 32x48 pixels.

## Silver arrow (variant 1, historical)

Approved by the user on 4 November 2026 for the in-game mouse cursor.
Created with the built-in ImageGen tool using the comparison sheet from this chat
as a reference; no original game assets are included.

`silver-arrow.png` is the transparent master. `silver-arrow-32x48.png` is the
normal-size preview. Originally packed to embedded RGBA surfaces (32x48 and 64x96);
the converter now uses the minimalist master above.
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
