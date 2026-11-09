"""Run actual runner launch logic with a Windows-locked launcher log and real pipes."""
import json, os, subprocess, sys, tempfile, textwrap, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PARTY=ROOT/'mods-src/BBSC/party'
RUNNER=(ROOT/'run.py').read_text(encoding='utf-8')
launch=textwrap.dedent(RUNNER[RUNNER.index('    party_log = None'):RUNNER.index('    try:\n        code = game_proc.wait()')])
wait_start=RUNNER.index('        code = game_proc.wait()')
wait_end=RUNNER.index('        if party is not None:\n            from bbport_local_test',wait_start)
finish=textwrap.dedent(RUNNER[wait_start:wait_end])
FIXTURE='''
import os,sys,subprocess,threading
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,PARTY_PATH)
from compat import Compatibility
user_dir=Path(sys.argv[1]);env={'BB_COOP':'1','BBSC_PARTY_TOKEN':'must-never-be-logged',
                               'BB_DIAGNOSTICS':sys.argv[2] if len(sys.argv)>2 else '1'}
party=Compatibility.__new__(Compatibility)
party.diagnostics=party.file_diagnostics=False
party.run_log=None
party.log_lock=threading.Lock()
party.logfile=user_dir/'party-events.jsonl'
party.e=SimpleNamespace(id='A', cfg={'group':'test'}, disk={'incarnation':1},
                        lock=threading.RLock(), state={'generation':0,'revision':0,'owner':None,'room':None})
command=[sys.executable,'-c','import sys; print("native stdout"); print("native stderr",file=sys.stderr)']
def no_console():return getattr(subprocess,'CREATE_NO_WINDOW',0)
'''.replace('PARTY_PATH',repr(str(PARTY)))+launch+'''
party.log('admission_committed',peer='B',ticket=5)
party.log('np_reply',command=105)
party.log('np_reply',command=111)
'''+finish+'''
if party_log is not None:party_log.close()
print('reader remains alive',flush=True)
'''

class PartyLogOwnershipTests(unittest.TestCase):
    def assert_party_events(self,text):
        prefix='[BBGL Party] '
        events=[json.loads(line[len(prefix):]) for line in text.splitlines() if line.startswith(prefix)]
        self.assertEqual([event['event'] for event in events],
                         ['run_log_attached','admission_committed','np_reply'])
        self.assertEqual(events[1]['ticket'],5)
        self.assertEqual(events[2]['command'],105)

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
            self.assert_party_events(text)
            self.assertFalse((root/'party-events.jsonl').exists())
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
            self.assert_party_events(text)
            self.assertFalse((root/'party-events.jsonl').exists())

    def test_normal_launch_keeps_party_events_out_of_run_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            child=subprocess.run([sys.executable,'-c',FIXTURE,tmp,'0'],capture_output=True,
                                 text=True,encoding='utf-8',timeout=10)
            self.assertEqual(child.returncode,0,child.stderr)
            self.assertIn('native stdout',child.stdout)
            self.assertNotIn('[BBGL Party]',child.stdout)

if __name__=='__main__':unittest.main()
