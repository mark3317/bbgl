import unittest
from pathlib import Path
import test_setup_wizard as wizard
import bbport_launcher_win as core
from bbport_launcher_backend import LauncherBackend

class FsrAvailabilityTests(unittest.TestCase):
    setUp = wizard.FirstRunWizardTests.setUp
    tearDown = wizard.FirstRunWizardTests.tearDown

    def test_full_assets_required_and_removal_disables_selected_fsr4(self):
        backend = LauncherBackend()
        options = lambda: [o['value'] for f in backend.sectionFields('Visuals','Upscaling') if f['key']=='upscaler' for o in f['options']]
        self.assertNotIn('fsr411', options())
        self.assertNotIn('fsr4', options())
        folder=self.root/'fsr4_shaders';folder.mkdir()
        for name in core.fsr4_files(): (folder/name).write_bytes(b'fixture')
        last=folder/core.fsr4_files()[-1];last.write_bytes(b'')
        self.assertFalse(backend.fsrReady)
        last.write_bytes(b'fixture')
        self.assertTrue(backend.fsrReady)
        self.assertIn('fsr4', options())
        (folder/'personal-note.txt').write_text('preserve')
        backend.setValue('upscaler','fsr4')
        backend.removeFsr4()
        self.assertEqual(backend.ini['upscaler'],'off')
        self.assertFalse(backend.fsrReady)
        self.assertNotIn('fsr4', options())
        self.assertTrue((folder/'personal-note.txt').is_file())

    def test_all_presets_disable_upscaling_and_old_411_is_normalized(self):
        self.assertEqual(core.INI_DEFAULTS['upscaler'],'off')
        for name in core.GRAPHICS_PRESETS:
            ini=dict(core.INI_DEFAULTS,upscaler='fsr3');app=dict(core.APP_DEFAULTS)
            core.apply_graphics_preset(name,ini,app)
            self.assertEqual(ini['upscaler'],'off')
        core.ini_path().write_text('upscaler=fsr411\n')
        self.assertEqual(core.load_ini()[0]['upscaler'],'off')
