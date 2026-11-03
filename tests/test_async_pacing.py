"""Compile production pacing writer; exercise backpressure and snapshot lifetime."""
from pathlib import Path
import os, subprocess, tempfile

ROOT=Path(__file__).resolve().parents[1]
CPP=r'''
#include <cassert>
#include <future>
#include <vector>
#include "core/libraries/videoout/pacing_diagnostics.h"
#include "core/libraries/videoout/async_perf_log.h"
using namespace Libraries::VideoOut;
PacingDiagnostics::Cpu PacingDiagnostics::ReadCpu(){return {100,25,200,400,123,true};}
int main(){
 std::promise<void> entered,release;
 auto released=release.get_future();std::vector<int> written;
 {
  AsyncDiagnosticQueue<int> queue([&](int n){
   if(n==1){entered.set_value();released.wait();}written.push_back(n);
  });
  assert(queue.Submit(1));entered.get_future().wait();
  assert(queue.Submit(2));assert(queue.Submit(3));
  // Slow output cannot delay the producer; storage never grows past capacity.
  auto frame=std::async(std::launch::async,[&]{return queue.Submit(4);});
  assert(frame.wait_for(std::chrono::seconds(1))==std::future_status::ready&&!frame.get());
  release.set_value();
 }
 assert((written==std::vector<int>{1,2,3})); // destruction flushes pending snapshots
 {
  PacingDiagnostics p;p.Start();p.frames=300;p.ready_by_deadline=299;
  p.ready_late.Add(3);p.dispatch_late.Add(.25);p.slow_count=1;
  p.slow[0]={123456,80,63,.3,.3,.1,.2};p.swap_count=300;p.swap_work_us=150000;
  p.window_start-=std::chrono::seconds(5);p.Report(60,true,false);
  assert(p.frames==0&&p.slow_count==0&&p.ready_late.count==0);
  // Resetting the live window must not mutate a queued report.
  p.frames=999;p.ready_late.Add(999);
 }
 assert(QueuePerfLine("Perf stall: epoch_ms=%lld frame_ms=%.3f\n",123456LL,80.0));
}
'''
with tempfile.TemporaryDirectory(prefix='bbgl-async-pacing-') as tmp:
    cpp,exe=Path(tmp)/'test.cpp',Path(tmp)/'test.exe';cpp.write_text(CPP)
    subprocess.run(['C:/msys64/clang64/bin/clang++.exe','-std=c++23','-Wall','-Wextra',
                    '-I'+str(ROOT/'gpu/shadps4'),str(cpp),'-o',str(exe)],check=True)
    env=dict(os.environ,PATH='C:/msys64/clang64/bin;'+os.environ.get('PATH',''))
    out=subprocess.check_output([str(exe)],text=True,env=env,timeout=10)
    pacing=next(line for line in out.splitlines() if line.startswith('Perf pacing:'))
    fields=dict(field.split('=') for field in pacing.split()[2:])
    assert fields['frames']=='300' and fields['ready_by_deadline']=='299'
    assert fields['ready_late_ms']=='3.000' and fields['report_async']=='1'
    assert 'Perf pacing slow: epoch_ms=123456 pid=123' in out
    assert 'Perf stall: epoch_ms=123456 frame_ms=80.000' in out
print('PASS: blocked diagnostic sink, bounded backpressure, flush, immutable pacing windows and legacy output')
