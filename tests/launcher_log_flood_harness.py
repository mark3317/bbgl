import os, sys, subprocess, threading, time
from pathlib import Path
from PySide6.QtCore import QTimer
import bbport_launcher_qml as ui
import bbport_launcher_win as core
root=Path(os.environ['BB_LIFETIME_ROOT'])
root.mkdir(parents=True, exist_ok=True)
class Backend(ui.LauncherBackend):
    def start_background_checks(self): pass
    def __init__(self, route=None):
        super().__init__(route)
        self.app['user_dir']=str(root/'user')
        self.updates=0
        self.logChanged.connect(self.count_update)
        QTimer.singleShot(200, self.launch_fake)
    def count_update(self): self.updates+=1
    def launch_fake(self):
        self.began=time.monotonic()
        child=root/'child.py'
        child.write_text("print('Entering original x86-64 code', flush=True)\nfor i in range(100000): print('P2P sample '+str(i)+': '+('x'*150))\nprint('final output', flush=True)\n")
        cmd=[sys.executable,'--script',str(child)] if core.FROZEN else [sys.executable,str(child)]
        self.process=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,creationflags=core.NO_WINDOW)
        self.job=core.GameJob(self.process)
        reader=threading.Thread(target=self._read_output,args=(self.process,),daemon=True)
        reader.start()
        threading.Thread(target=self._wait_for_game,args=(self.process,self.job,reader),daemon=True).start()
        self.gameFinished.connect(self.finished)
    def finished(self, code, started):
        assert code==0 and started
        elapsed=time.monotonic()-self.began
        assert elapsed<12, elapsed
        assert self.updates<150, self.updates
        assert 'final output' in (root/'user/last_run.log').read_text()
        assert 'P2P sample 0:' in (root/'user/last_run.log').read_text()
        (root/'finished').write_text(f'PASS elapsed={elapsed:.2f}s UI_updates={self.updates}')
ui.LauncherBackend=Backend
sys.exit(ui.run_ui())
