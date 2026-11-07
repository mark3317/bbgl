#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "game_code.h"
#include "network_heap_patch.h"

int main(void) {
    bb_test_require_game("network heap patch");
    const size_t image_size = BB_NETWORK_HEAP_TABLE + BB_NETWORK_HEAP_TABLE_SIZE;
    unsigned char *image = calloc(1, image_size);
    assert(image);
    bb_test_place_game_code(image, BB_NETWORK_HEAP_LOOKUP, 21);
    bb_test_place_game_code(image, BB_NETWORK_HEAP_TABLE, BB_NETWORK_HEAP_TABLE_SIZE);
    unsigned char *table = image + BB_NETWORK_HEAP_TABLE;
    unsigned char original[BB_NETWORK_HEAP_TABLE_SIZE];
    memcpy(original, table, sizeof(original));

    assert(!bb_patch_network_heap(NULL, image_size));
    assert(!bb_patch_network_heap(image, image_size - 1));
    image[BB_NETWORK_HEAP_LOOKUP] ^= 1;
    assert(!bb_patch_network_heap(image, image_size));
    assert(!memcmp(original, table, sizeof(original)));
    image[BB_NETWORK_HEAP_LOOKUP] ^= 1;

    const size_t last_network = 7 * 128 + 8 * sizeof(uint64_t);
    table[last_network + 2] ^= 1;
    assert(!bb_patch_network_heap(image, image_size));
    table[last_network + 2] ^= 1;
    assert(!memcmp(original, table, sizeof(original)));

    assert(bb_patch_network_heap(image, image_size));
    for (unsigned row = 0; row < 9; ++row) {
        for (unsigned column = 0; column < 16; ++column) {
            const size_t offset = (row * 16 + column) * sizeof(uint64_t);
            uint64_t before, after;
            memcpy(&before, original + offset, sizeof(before));
            memcpy(&after, table + offset, sizeof(after));
            const uint64_t expected = column == 8 && before == 14 * 1024 * 1024
                ? 16 * 1024 * 1024 : before;
            assert(after == expected);
        }
    }
    assert(!bb_patch_network_heap(image, image_size));
    free(image);
    puts("PASS: original NETWORK profiles, unchanged neighboring heaps and fail-closed checks");
    return 0;
}
