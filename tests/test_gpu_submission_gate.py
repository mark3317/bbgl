"""Execute the real Gnm admission/idle callbacks with delayed IRQ delivery.

No game, graphics device, profiles or savedata are opened.
"""
from pathlib import Path
import os, subprocess, tempfile, unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "gpu/shadps4/core/libraries/gnmdriver/gnmdriver.cpp"

def function(text, signature):
    start = text.index(signature)
    at = text.index("{", start) + 1
    depth = 1
    while depth:
        depth += (text[at] == "{") - (text[at] == "}")
        at += 1
    return text[start:at]

class SubmissionGateTests(unittest.TestCase):
    def test_delayed_idle_irq_cannot_release_new_work(self):
        source = SOURCE.read_text(encoding="utf-8")
        production = "\n".join(function(source, signature) for signature in (
            "static void ResetSubmissionLock(", "static void WaitGpuIdle(",
            "s32 PS4_SYSV_ABI sceGnmSubmitDone(", "int PS4_SYSV_ABI sceGnmAreSubmitsAllowed("))
        fixture = r'''
#include <atomic>
#include <cassert>
#include <condition_variable>
#include <cstdint>
#include <mutex>
#include <thread>
using s32=int32_t;using u64=uint64_t;
#define PS4_SYSV_ABI
#define HLE_TRACE
#define LOG_DEBUG(...)
#define LOG_TRACE(...)
constexpr int ORBIS_OK=0;
namespace Platform { enum class InterruptId { GpuIdle }; }
bool submission_lock=false,send_init_packet=false;
std::mutex m_wait_idle,m_submit_lock;
std::condition_variable cv_lock;
u64 frames_submitted=0;
struct { void IncGnmFrameNum(){} } DebugState;
struct Liverpool {
    std::atomic<bool> idle{true};
    bool check_publish_lock=false;
    bool IsGpuIdle() const {
        if(check_publish_lock){
            bool acquired=false;
            std::thread observer([&]{
                acquired=m_wait_idle.try_lock();
                if(acquired)m_wait_idle.unlock();
            });
            observer.join();
            assert(!acquired && "idle check and wait publication must exclude the IRQ callback");
        }
        return idle.load();
    }
    void SubmitDone(){}
} gpu;
Liverpool* liverpool=&gpu;
''' + production + r'''
int main(){
    gpu.idle=false;
    gpu.check_publish_lock=true;
    sceGnmSubmitDone();
    gpu.check_publish_lock=false;
    gpu.idle=true;
    ResetSubmissionLock(Platform::InterruptId::GpuIdle);
    // Batch A has retired. Its IRQ is delayed until batch B is submitted and
    // sceGnmSubmitDone has closed admission for B. No GPU/device is required
    // to control this valid interleaving.
    for(int i=0;i<1000;++i){
        gpu.idle=true;
        assert(!submission_lock);
        gpu.idle=false; // B queued before A's already-scheduled IRQ is delivered
        assert(sceGnmSubmitDone()==0);
        assert(submission_lock);
        assert(!sceGnmAreSubmitsAllowed());
        ResetSubmissionLock(Platform::InterruptId::GpuIdle); // A's stale IRQ
        assert(submission_lock && "stale idle IRQ released unfinished batch B");
        gpu.idle=true;
        ResetSubmissionLock(Platform::InterruptId::GpuIdle); // B is retired
        assert(!submission_lock);
        assert(sceGnmAreSubmitsAllowed());
        assert(sceGnmSubmitDone()==0); // truly idle: never arm an unfulfillable wait
        assert(!submission_lock);
    }
    // The real waiter remains blocked through the stale notification and
    // wakes only once the draws/fences of the current work have retired.
    gpu.idle=false;
    sceGnmSubmitDone();
    std::atomic<bool> entered=false,passed=false;
    std::thread waiter([&]{entered=true;WaitGpuIdle();passed=true;});
    while(!entered)std::this_thread::yield();
    ResetSubmissionLock(Platform::InterruptId::GpuIdle);
    {std::scoped_lock lk{m_wait_idle};assert(submission_lock&&!passed);}
    gpu.idle=true;
    ResetSubmissionLock(Platform::InterruptId::GpuIdle);
    waiter.join();
    assert(passed);
}
'''
        compiler = Path("C:/msys64/clang64/bin/clang++.exe")
        env = dict(os.environ, PATH=str(compiler.parent)+os.pathsep+os.environ.get("PATH", ""))
        with tempfile.TemporaryDirectory(prefix="bb-gpu-gate-") as tmp:
            cpp,exe=Path(tmp)/"gate.cpp",Path(tmp)/"gate.exe"
            cpp.write_text(fixture,encoding="utf-8")
            subprocess.run([str(compiler),"-std=c++20","-O2",str(cpp),"-o",str(exe)],env=env,check=True)
            subprocess.run([str(exe)],env=env,check=True,timeout=10)

if __name__ == "__main__": unittest.main()
