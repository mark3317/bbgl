"""Run actual runner launch logic with a Windows-locked launcher log and real pipes."""
import os, subprocess, sys, tempfile, textwrap, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PARTY=ROOT/'mods-src/BBSC/party'
RUNNER=(ROOT/'run.py').read_text(encoding='utf-8')
launch=textwrap.dedent(RUNNER[RUNNER.index('    party_log = None'):RUNNER.index('    try:\n        code = game_proc.wait()')])
wait_start=RUNNER.index('        code = game_proc.wait()')
wait_end=RUNNER.index('        if party is not None:\n            from bbport_local_test',wait_start)
finish=textwrap.dedent(RUNNER[wait_start:wait_end])
FIXTURE='''
import os,sys,subprocess
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,PARTY_PATH)
user_dir=Path(sys.argv[1]);env={'BB_COOP':'1','BBSC_PARTY_TOKEN':'must-never-be-logged'}
party=SimpleNamespace(close=lambda:None)
command=[sys.executable,'-c','import sys; print("native stdout"); print("native stderr",file=sys.stderr)']
def no_console():return getattr(subprocess,'CREATE_NO_WINDOW',0)
'''.replace('PARTY_PATH',repr(str(PARTY)))+launch+finish+'''
if party_log is not None:party_log.close()
print('reader remains alive',flush=True)
'''

class PartyLogOwnershipTests(unittest.TestCase):
    def test_launcher_pipe_does_not_rotate_locked_log_and_receives_all_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with (root/'last_run.log').open('w',encoding='utf-8') as locked:
                locked.write('launcher preparation\n');locked.flush()
                child=subprocess.run([sys.executable,'-c',FIXTURE,str(root)],capture_output=True,
                                     text=True,encoding='utf-8',timeout=10)
                self.assertEqual(child.returncode,0,child.stderr)
                locked.write(child.stdout);locked.flush()
            text=(root/'last_run.log').read_text(encoding='utf-8')
            for marker in ('launcher preparation','BBGL party launch','native stdout','native stderr','exit=0','reader remains alive'):
                self.assertIn(marker,text)
            self.assertNotIn('must-never',text)
            self.assertEqual(list(root.glob('run_*.log')), [])
            self.assertFalse((root/'last_run.1.log').exists())

    def test_direct_runner_owns_timestamped_native_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'last_run.log').write_text('previous run',encoding='utf-8')
            with (root/'wrapper.log').open('w',encoding='utf-8') as wrapper:
                child=subprocess.run([sys.executable,'-c',FIXTURE,str(root)],stdout=wrapper,
                                     stderr=subprocess.STDOUT,timeout=10)
            self.assertEqual(child.returncode,0,(root/'wrapper.log').read_text())
            logs=list(root.glob('run_*.log'))
            self.assertEqual(len(logs),1)
            text=logs[0].read_text(encoding='utf-8')
            for marker in ('BBGL party launch','native stdout','native stderr','exit=0'):
                self.assertIn(marker,text)
            self.assertEqual((root/'last_run.log').read_text(),'previous run')
            self.assertFalse((root/'last_run.1.log').exists())
            self.assertNotIn('must-never',text)

if __name__=='__main__':unittest.main()
