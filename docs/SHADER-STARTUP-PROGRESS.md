# Startup shader progress — 2026-11-02

The game window now shows a localized preparation label and a percentage bar
while the stored shader/pipeline catalog is warmed. Work is counted after each
record, including rejected records, with updates throttled to 100 ms. Empty or
disabled caches skip the screen. This measures catalog preparation, not an
estimate of every shader that may be encountered later in gameplay.

WarmUp runs at the end of Presenter construction, after motion buffers, the
swapchain, frame resources and ImGui are initialized, before VideoOut is started.
Startup frames use PrepareBlankFrame/Present synchronously with is_game_frame=false.
No additional rendering thread or SDL renderer is introduced. Completion hides
the overlay for subsequent game frames.

Validation: native bb-probe build exit=0; git diff --check for GPU paths passed.
Output: out/gpu/bb-probe.exe, copied to out/bb-probe.exe.
Deployment skipped: bb-probe and Bloodborne were running on the local PC.
Visual/fullscreen, resize/minimize and empty-cache runtime validation pending;
no game launched, no installed binaries/settings/saves changed.
