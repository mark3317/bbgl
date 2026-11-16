/* SPDX-License-Identifier: GPL-2.0-or-later */
#include "engine_hooks.h"
#include "gpu/bbgpu.h"

#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum {
    EVENT_FLAG_MAN = 0x0553b100,
    IS_EVENT_FLAG = 0x013cfc00,
    SET_EVENT_FLAG = 0x013cfcc0,
    CREATE_LOCAL_PLAYER = 0x01939470,
};

/* The original common:7000 calls register these 44 base-game and DLC lamps.
 * Each registered flag has a companion warp-menu flag 10 IDs later. */
static const struct {
    uint32_t first;
    unsigned count;
} lamps[] = {
    {12117800, 1}, {12207800, 2}, {12307800, 3}, {12407800, 2},
    {12417800, 4}, {12427800, 3}, {12507800, 3}, {12607800, 4},
    {12707800, 2}, {12807800, 4}, {13207800, 4}, {13307800, 2},
    {13407800, 4}, {13507800, 3}, {13607800, 3},
};

enum { LAMP_RESET_APPLYING = BB_LAMP_RESET_DONE + 1 };
static atomic_int status;

static BbLampResetStatus overlay_action(int request) {
    int current = atomic_load(&status);
    if (request && (current == BB_LAMP_RESET_READY || current == BB_LAMP_RESET_DONE)) {
        if (atomic_compare_exchange_strong(&status, &current, BB_LAMP_RESET_PENDING))
            return BB_LAMP_RESET_PENDING;
    }
    return current == LAMP_RESET_APPLYING ? BB_LAMP_RESET_PENDING : (BbLampResetStatus)current;
}

static uint64_t read_pointer(uint32_t offset) {
    uint64_t address = 0;
    bb_read((uintptr_t)bb_guest(offset), &address, sizeof(address));
    return address;
}

static void BB_GUEST_ABI reset_at_load(uint64_t stage) {
    if (atomic_load(&status) != BB_LAMP_RESET_PENDING) return;
    uint32_t map = 0;
    if (!stage || !bb_read(stage + 0x58, &map, sizeof(map))) return;
    const uint32_t area = map >> 24;
    /* Let the player leave the Dream before removing its warp destinations. */
    if (map == 0x15000000u) {
        puts("Lamp reset: waiting to leave the Hunter's Dream");
        return;
    }
    if (area < 21 || area > 36) return;

    const uint64_t manager = read_pointer(EVENT_FLAG_MAN);
    int expected = BB_LAMP_RESET_PENDING;
    if (!manager || !atomic_compare_exchange_strong(&status, &expected, LAMP_RESET_APPLYING)) return;
    typedef uint32_t (BB_GUEST_ABI *IsFlag)(uint64_t, uint32_t, int *);
    typedef void (BB_GUEST_ABI *SetFlag)(uint64_t, uint32_t, uint32_t);
    const IsFlag is_on = (IsFlag)bb_guest(IS_EVENT_FLAG);
    const SetFlag set = (SetFlag)bb_guest(SET_EVENT_FLAG);
    unsigned changed = 0;
    for (size_t i = 0; i < sizeof(lamps) / sizeof(lamps[0]); ++i) {
        for (unsigned lamp = 0; lamp < lamps[i].count; ++lamp) {
            const uint32_t flag = lamps[i].first + lamp * 20u;
            for (uint32_t id = flag; id <= flag + 10u; id += 10u) {
                int exists;
                if (is_on(manager, id, &exists)) {
                    set(manager, id, 0);
                    ++changed;
                }
            }
        }
    }
    printf("Lamp reset: cleared %u lit/menu flags on stage %08x\n", changed, map);
    atomic_store(&status, BB_LAMP_RESET_DONE);
}

static int env_enabled(const char *key) {
    const char *value = getenv(key);
    return value && !strcmp(value, "1");
}

int bb_lamp_reset_install(void) {
    if (env_enabled("BB_COOP") || env_enabled("BB_ONLINE"))
        return 0;
    const BbCode read_code = {13, 0x640756cd63dfd3acull};
    const BbCode set_code = {12, 0x62c33c4e2b2a6053ull};
    const BbCode load_code = {6, 0x82d75a35aabe38aaull};
    if (!bb_code_is(bb_guest(IS_EVENT_FLAG), read_code) ||
        !bb_code_is(bb_guest(SET_EVENT_FLAG), set_code)) {
        puts("Lamp reset: unavailable on this game build");
        return 0;
    }
    /* StageFlow creates the local player after loading the save and before map
     * events. Its conditional ReloadFinish call only handles multiplayer. */
    if (bb_hook_entry(CREATE_LOCAL_PLAYER, load_code, (void *)reset_at_load)) {
        printf("Lamp reset: %s\n", bb_hooks_error());
        return 0;
    }
    bbgpu_overlay_bind_lamp_reset(overlay_action);
    return 1;
}
