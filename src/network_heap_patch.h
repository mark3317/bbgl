#ifndef BB_NETWORK_HEAP_PATCH_H
#define BB_NETWORK_HEAP_PATCH_H

#include <stddef.h>
#include <stdint.h>
#include <string.h>

#include "code_check.h"

/* CUSA03173 1.09: the allocator at 0x1fc7870 selects a size by memory
 * profile and heap name. NETWORK is column 8. Its five 14 MiB profiles
 * receive 2 MiB more direct memory at startup. Leave the 30 MiB profile
 * and profiles without a NETWORK allocation alone. */
enum {
    BB_NETWORK_HEAP_LOOKUP = 0x1fc7924,
    BB_NETWORK_HEAP_TABLE = 0x4736d40,
    BB_NETWORK_HEAP_TABLE_SIZE = 9 * 0x80,
};

static inline int bb_patch_network_heap(unsigned char *image, size_t size) {
    static const BbCode lookup = {21, 0xb3d634583472ac52ull};
    static const unsigned profiles[] = {1, 3, 4, 6, 7};
    static const uint64_t original_size = 14 * 1024 * 1024;
    static const uint64_t expanded_size = 16 * 1024 * 1024;
    enum { ROW_SIZE = 0x80, NETWORK_COLUMN = 8 * sizeof(uint64_t) };

    if (!image || size < BB_NETWORK_HEAP_TABLE + BB_NETWORK_HEAP_TABLE_SIZE ||
        !bb_code_is(image + BB_NETWORK_HEAP_LOOKUP, lookup))
        return 0;

    unsigned char *network = image + BB_NETWORK_HEAP_TABLE + NETWORK_COLUMN;
    for (size_t i = 0; i < sizeof(profiles) / sizeof(*profiles); ++i) {
        if (memcmp(network + profiles[i] * ROW_SIZE, &original_size, sizeof(original_size)))
            return 0;
    }
    for (size_t i = 0; i < sizeof(profiles) / sizeof(*profiles); ++i)
        memcpy(network + profiles[i] * ROW_SIZE, &expanded_size, sizeof(expanded_size));
    return 1;
}

#endif
