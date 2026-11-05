"""Both real log openers preserve previous files, including same-second launches."""
import ast
import importlib.util
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]

def launcher_opener():
    path=ROOT/'launcher/bbport_launcher_win.py'
    tree=ast.parse(path.read_text(encoding='utf8'))
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='open_run_log')
    scope={'Path':Path,'time':time}
    exec(compile(ast.Module(body=[fn],type_ignores=[]),str(path),'exec'),scope)
    return scope['open_run_log']

class RunLogNameTests(unittest.TestCase):
    def test_launcher_and_direct_runner_use_unique_launch_timestamps(self):
        path=ROOT/'mods-src/BBSC/party/run_log.py'
        spec=importlib.util.spec_from_file_location('runner_logs_under_test',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        for opener in (launcher_opener(),lambda p:module.open_log(p,{})):
            with self.subTest(opener=opener),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp)/'new user'
                root.mkdir();legacy=root/'last_run.log';legacy.write_text('legacy')
                with patch.object(time,'strftime',return_value='run_20261104_204500') as clock:
                    with opener(root) as first:
                        first.write('first run\n');first.flush()
                        with opener(root) as second:
                            second.write('second run\n')
                            self.assertEqual(Path(first.name).name,'run_20261104_204500.log')
                            self.assertEqual(Path(second.name).name,'run_20261104_204500_2.log')
                clock.assert_any_call('run_%Y%m%d_%H%M%S')
                self.assertIn('first run', (root/'run_20261104_204500.log').read_text())
                self.assertIn('second run', (root/'run_20261104_204500_2.log').read_text())
                self.assertEqual(legacy.read_text(),'legacy')
                self.assertFalse((root/'last_run.1.log').exists())

if __name__=='__main__':unittest.main()
