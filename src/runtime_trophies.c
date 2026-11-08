/* Local trophy history for the native port. Never writes to the game dump or PSN. */
#include "runtime.h"
#include "gpu/bbgpu.h"
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

enum {
    TROPHY_LIMIT = 128,
    PLATINUM_TROPHY = 0,
    LAST_BLOODBORNE_TROPHY = 39, /* The Old Hunters ends at ID 39. */
};
static pthread_mutex_t trophy_lock = PTHREAD_MUTEX_INITIALIZER;
static int64_t unlocked[TROPHY_LIMIT];
static char trophy_path[1024];

/* Call with trophy_lock held. Publish only entries that reached the history. */
static int record_unlock(int id, int64_t when) {
    FILE *file = trophy_path[0] ? fopen(trophy_path, "a") : NULL;
    if (!file) {
        fprintf(stderr, "Runtime: could not open local trophy history for trophy %d\n", id);
        return 0;
    }
    const int written = fprintf(file, "%d %lld\n", id, (long long)when);
    if (fclose(file) != 0 || written < 0) {
        fprintf(stderr, "Runtime: could not save trophy %d\n", id);
        return 0;
    }
    unlocked[id] = when;
    printf("Runtime: local trophy %d unlocked\n", id);
    return 1;
}

static int unlock_platinum(void) {
    if (unlocked[PLATINUM_TROPHY]) return 0;
    int64_t latest = 0;
    for (int id = 1; id <= LAST_BLOODBORNE_TROPHY; ++id) {
        if (!unlocked[id]) return 0;
        if (unlocked[id] > latest) latest = unlocked[id];
    }
    return record_unlock(PLATINUM_TROPHY, latest);
}

void runtime_trophy_configure(void) {
    pthread_mutex_lock(&trophy_lock);
    memset(unlocked, 0, sizeof(unlocked));
    int length = snprintf(trophy_path, sizeof(trophy_path), "%s/trophies.txt",
                          runtime_file_user_dir());
    if (length < 0 || (size_t)length >= sizeof(trophy_path)) {
        trophy_path[0] = 0;
    }
    FILE *file = trophy_path[0] ? fopen(trophy_path, "r") : NULL;
    if (file) {
        char line[96];
        while (fgets(line, sizeof(line), file)) {
            int id;
            long long when;
            char extra;
            if (sscanf(line, "%d %lld %c", &id, &when, &extra) == 2 &&
                id >= 0 && id < TROPHY_LIMIT) {
                unlocked[id] = when > 0 ? when : 1;
            }
        }
        fclose(file);
    }
    unlock_platinum();
    bbgpu_trophy_load(unlocked, TROPHY_LIMIT);
    pthread_mutex_unlock(&trophy_lock);
}

int runtime_trophy_unlock(int id, int32_t *platinum) {
    if (id <= PLATINUM_TROPHY || id >= TROPHY_LIMIT) return -1;
    if (platinum) *platinum = -1;
    pthread_mutex_lock(&trophy_lock);
    const int awarded = !unlocked[id] && record_unlock(id, (int64_t)time(NULL));
    if (awarded) bbgpu_trophy_unlocked(id, unlocked[id]);
    if (id <= LAST_BLOODBORNE_TROPHY && unlock_platinum()) {
        if (platinum) *platinum = PLATINUM_TROPHY;
        bbgpu_trophy_unlocked(PLATINUM_TROPHY, unlocked[PLATINUM_TROPHY]);
    }
    pthread_mutex_unlock(&trophy_lock);
    return awarded;
}
