/* SPDX-License-Identifier: GPL-2.0-or-later
 * Opt-in BB_LIVE_GRAPHICS=1 experiment for CUSA03173 1.09.
 * Startup keeps render resources available; guarded hooks mask render decisions.
 * No game instruction bytes are distributed, only site lengths and fingerprints.
 */
#include "engine_hooks.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
extern int bbgpu_setting_get(const char *, int *);
extern void bbgpu_setting_set(const char *, int);
static const char *keys[] = {"effect_chromatic_aberration", "effect_dof", "effect_motion_blur", "effect_ssao", "effect_game_aa", "effect_dynamic_shadows", "effect_ssr", "model_lod", "object_motion"};
static int current[9];
static unsigned long long visits[8];
static int value(int index) { return __atomic_load_n(&current[index], __ATOMIC_RELAXED); }
/* cmp byte,0 with a zero operand: PF=ZF=1; CF=AF=SF=OF=0. */
static void mask(BbRegs *r, int index) {
    __atomic_fetch_add(&visits[index], 1, __ATOMIC_RELAXED);
    if (!value(index)) r->flags = (r->flags & ~0x8d5ull) | 0x44;
}
static BB_GUEST_ABI void ca(BbRegs *r) { __atomic_fetch_add(&visits[0], 1, __ATOMIC_RELAXED); if (!value(0)) r->rax = 0; }
static BB_GUEST_ABI void dof(BbRegs *r) { mask(r, 1); }
static BB_GUEST_ABI void lod(BbRegs *r) { __atomic_fetch_add(&visits[7], 1, __ATOMIC_RELAXED); int v = value(7); if (v) r->rcx = (uint32_t)v; }
static BB_GUEST_ABI void ssao(BbRegs *r) { mask(r, 3); }
static BB_GUEST_ABI void blur(BbRegs *r) { mask(r, 2); }
static BB_GUEST_ABI void aa(BbRegs *r) { mask(r, 4); }
static BB_GUEST_ABI void shadows(BbRegs *r) { mask(r, 5); }
static BB_GUEST_ABI void ssr(BbRegs *r) { mask(r, 6); }
typedef struct { uint64_t address; BbCode code; int index, after; void (BB_GUEST_ABI *hook)(BbRegs *); } Site;
static const Site sites[] = {
    {BB_BN(0x269faae), {6, 0x269d45d570be1299ull}, 0, 0, ca},
    {BB_BN(0x25d7bb5), {7, 0xf1af6c0efe3515a4ull}, 1, 1, dof},
    {BB_BN(0x216fc0f), {5, 0x9427c043db844958ull}, 7, 0, lod},
    {BB_BN(0x26a113c), {8, 0x64b8c75dd63b2500ull}, 3, 1, ssao},
    {BB_BN(0x26a33bb), {8, 0x64b8c75dd63b2500ull}, 3, 1, ssao},
    {BB_BN(0x26a3687), {8, 0x64b8c75dd63b2500ull}, 3, 1, ssao},
    {BB_BN(0x26a3eed), {8, 0x64b8c75dd63b2500ull}, 3, 1, ssao},
    {BB_BN(0x26a5275), {8, 0x64b8c75dd63b2500ull}, 3, 1, ssao},
    {BB_BN(0x26a7557), {8, 0x64b8c75dd63b2500ull}, 3, 1, ssao},
    {BB_BN(0x269ef04), {9, 0x0a9d5eee79ebf31eull}, 2, 1, blur},
    {BB_BN(0x269f021), {9, 0x0a9d5eee79ebf31eull}, 2, 1, blur},
    {BB_BN(0x26a0572), {9, 0x0a9d5eee79ebf31eull}, 2, 1, blur},
    {BB_BN(0x26a168d), {8, 0x97a9fcc968b2fccfull}, 2, 1, blur},
    {BB_BN(0x26ab0a1), {8, 0x1c1a3751b6316661ull}, 2, 1, blur},
    {BB_BN(0x26ab2f2), {8, 0x1c1a3751b6316661ull}, 2, 1, blur},
    {BB_BN(0x26c5a8e), {7, 0x0167fa45057dd2b6ull}, 2, 1, blur},
    {BB_BN(0x26a073e), {9, 0x5796d9a4404b0d93ull}, 4, 1, aa},
    {BB_BN(0x26a5c89), {8, 0x7cc18fc85e491e06ull}, 5, 1, shadows},
    {BB_BN(0x26a8f7a), {8, 0x4a3babe00645a2bdull}, 6, 1, ssr},
    {BB_BN(0x26c55b7), {7, 0x181a40712dacc048ull}, 6, 1, ssr},
};
static int last[9], mask_ready;
static void report(void) {
    for (int i = 0; i < 9; ++i) {
        int v = 0; bbgpu_setting_get(keys[i], &v);
        __atomic_store_n(&current[i], v, __ATOMIC_RELAXED);
        if (v != last[i]) {
            printf("Live graphics: %s = %d (hook %s, visits=%llu)\n", keys[i], v,
                   (mask_ready & (1 << i)) ? "ready" : "unavailable",
                   i < 8 ? __atomic_load_n(&visits[i], __ATOMIC_RELAXED) : 0ull);
            last[i] = v;
        }
    }
}
int bb_live_graphics_install(void) {
    const char *enabled = getenv("BB_LIVE_GRAPHICS");
    if (!enabled || strcmp(enabled, "1")) return 0;
    /* Validate the entire set BEFORE changing anything. Other patches may own these sites. */
    for (size_t i = 0; i < sizeof(sites)/sizeof(*sites); ++i) {
        if (!bb_code_is(bb_guest(sites[i].address), sites[i].code)) {
            fprintf(stderr, "Live graphics: unsupported/modified site 0x%llx; experiment refused\n",
                    (unsigned long long)(sites[i].address + 0x400000));
            /* Startup omitted effect patches: refusing must never masquerade as a working test. */
            exit(1);
        }
    }
    int hooks = 0;
    for (size_t i = 0; i < sizeof(sites)/sizeof(*sites); ++i) {
        const Site *s = &sites[i];
        int result = s->after ? bb_hook_mid_after(s->address, s->code, s->hook)
                              : bb_hook_mid(s->address, s->code, s->hook);
        if (result) { fprintf(stderr, "Live graphics: install failed: %s\n", bb_hooks_error()); exit(1); }
        ++hooks;
        mask_ready |= 1 << s->index;
    }
    int motion = 0; bbgpu_setting_get("live_graphics_mask", &motion);
    mask_ready |= motion & 256;
    bbgpu_setting_set("live_graphics_mask", mask_ready);
    for (int i = 0; i < 9; ++i) last[i] = -999;
    report();
    bb_on_main_frame(report);
    printf("Live graphics: EXPERIMENT active, %d hooks, mask=0x%x; SSR infrastructure always prepared\n", hooks, mask_ready);
    return hooks;
}
