"""Exercise the production bounded retry policy without a server or game."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CODE = r'''
#include <cassert>
#include <vector>
#include "core/libraries/network/bbsc_connect_retry.h"
using namespace Libraries::Http;
enum Result { Connected, ConnectTimeout, ReadError, WriteError, HttpError };
int main() {
    assert(BbscClaimRetryEnabled(true, "/summon_messenger/request?user_id=1", true));
    assert(!BbscClaimRetryEnabled(false, "/summon_messenger/request", true));
    assert(!BbscClaimRetryEnabled(true, "/summon_messenger/request", false));
    for (auto path : {"/summon_messenger/create", "/summon_messenger/get",
                      "/summon_messenger/delete", "/summon_messenger/request-extra"})
        assert(!BbscClaimRetryEnabled(true, path, true));
    auto exercise = [](bool enabled, std::vector<Result> sequence, unsigned sends,
                       Result expected) {
        unsigned calls=0, retries=0;
        auto result=SendBbscClaim(enabled, [&] { return sequence.at(calls++); },
            [](Result r) { return r==ConnectTimeout; },
            [&](unsigned n) { assert(n==++retries); });
        assert(calls==sends && retries==sends-1 && result==expected);
    };
    exercise(true, {ConnectTimeout, ConnectTimeout, Connected}, 3, Connected);
    exercise(true, {ConnectTimeout, ConnectTimeout, ConnectTimeout}, 3, ConnectTimeout);
    exercise(false, {ConnectTimeout}, 1, ConnectTimeout);
    for (Result r : {Connected, ReadError, WriteError, HttpError}) {
        exercise(true, {r}, 1, r);
        exercise(true, {ConnectTimeout, r}, 2, r);
    }
}
'''

with tempfile.TemporaryDirectory(prefix="bbsc-connect-retry-") as temporary:
    cpp, exe = Path(temporary) / "fixture.cpp", Path(temporary) / "fixture.exe"
    cpp.write_text(CODE, encoding="utf-8")
    subprocess.run([os.environ.get("CXX", "g++"), "-std=c++20", "-I",
                    str(ROOT / "gpu/bbnet/vendor/shadps4"), str(cpp), "-o", str(exe)],
                   check=True)
    subprocess.run([str(exe)], check=True, timeout=10)
print("Summon TCP connect retry: scope, bounded recovery, no ambiguous POST replay: PASS")
