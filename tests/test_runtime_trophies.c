#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <direct.h>
#include <process.h>
#include <time.h>

static char user_dir[900];
static int64_t visible[128];
static int toasts;
static int last_toast;

const char *runtime_file_user_dir(void) { return user_dir; }
void bbgpu_trophy_load(const int64_t *flags, uint32_t count) {
    assert(count == 128);
    memcpy(visible, flags, count * sizeof(visible[0]));
}
void bbgpu_trophy_unlocked(int32_t id, int64_t timestamp) {
    assert(id >= 0 && id < 128);
    visible[id] = timestamp;
    ++toasts;
    last_toast = id;
}
void runtime_trophy_configure(void);
int runtime_trophy_unlock(int id, int32_t *platinum);

int main(int argc, char **argv) {
    assert(argc == 2);
    int length = snprintf(user_dir, sizeof(user_dir), "%s/trophy-test-%lld-%u", argv[1],
                          (long long)time(NULL), (unsigned)_getpid());
    assert(length > 0 && (size_t)length < sizeof(user_dir));
    assert(_mkdir(user_dir) == 0);
    runtime_trophy_configure();
    assert(!visible[7] && !visible[127]);
    int32_t platinum;
    assert(runtime_trophy_unlock(7, &platinum) == 1 && platinum == -1);
    assert(runtime_trophy_unlock(7, &platinum) == 0 && platinum == -1);
    assert(runtime_trophy_unlock(127, NULL) == 1);
    assert(runtime_trophy_unlock(-1, NULL) == -1);
    assert(runtime_trophy_unlock(128, NULL) == -1);
    assert(runtime_trophy_unlock(0, NULL) == -1);
    assert(toasts == 2);
    memset(visible, 0, sizeof(visible));
    runtime_trophy_configure();
    assert(visible[7] && visible[127]);
    assert(visible[7] > 1000000000 && visible[127] > 1000000000);
    assert(runtime_trophy_unlock(7, NULL) == 0 && toasts == 2);

    // An unrelated ID cannot replace a missing DLC trophy.
    for (int id = 1; id <= 38; ++id) {
        if (id != 7) assert(runtime_trophy_unlock(id, &platinum) == 1 && platinum == -1);
        assert(!visible[0]);
    }
    runtime_trophy_configure();
    assert(!visible[0]);
    const int before_platinum = toasts;
    assert(runtime_trophy_unlock(39, &platinum) == 1 && platinum == 0);
    assert(visible[0] == visible[39] && visible[0] > 0);
    assert(toasts == before_platinum + 2 && last_toast == 0);
    const int64_t earned_at = visible[0];
    runtime_trophy_configure();
    assert(visible[0] == earned_at);
    assert(runtime_trophy_unlock(39, &platinum) == 0 && platinum == -1);
    assert(toasts == before_platinum + 2);

    // A different profile earned all ordinary trophies before the fix.
    length = snprintf(user_dir, sizeof(user_dir), "%s/trophy-legacy-%lld-%u", argv[1],
                      (long long)time(NULL), (unsigned)_getpid());
    assert(length > 0 && (size_t)length < sizeof(user_dir));
    assert(_mkdir(user_dir) == 0);
    char history[1024];
    length = snprintf(history, sizeof(history), "%s/trophies.txt", user_dir);
    assert(length > 0 && (size_t)length < sizeof(history));
    FILE *file = fopen(history, "w");
    assert(file);
    for (int id = 39; id > 0; --id) {
        assert(fprintf(file, "%d %d\n", id, 1700000000 + id) > 0);
    }
    assert(fclose(file) == 0);
    runtime_trophy_configure();
    assert(visible[0] == 1700000039 && !visible[127]);
    assert(toasts == before_platinum + 2);
    runtime_trophy_configure();
    file = fopen(history, "r");
    assert(file);
    int platinum_count = 0;
    int id;
    long long when;
    while (fscanf(file, "%d %lld", &id, &when) == 2) {
        platinum_count += id == 0;
    }
    assert(fclose(file) == 0 && platinum_count == 1);
    puts("trophy history: persistence, ID bounds, DLC requirement and platinum recovery passed");
    return 0;
}
