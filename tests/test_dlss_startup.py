import unittest
from unittest.mock import patch
from PySide6.QtCore import QCoreApplication
import test_setup_wizard as fixture
from bbport_launcher_backend import LauncherBackend

class DlssStartupTests(unittest.TestCase):
    setUp = fixture.FirstRunWizardTests.setUp
    tearDown = fixture.FirstRunWizardTests.tearDown

    def test_gpu_probe_is_delivered_before_first_settings_model(self):
        app=QCoreApplication.instance() or QCoreApplication([])
        def detect(backend):
            backend.dlssDetected.emit(True)
            backend.gpuDetected.emit('fixture RTX')
        with patch.object(LauncherBackend,'_detect_gpu',detect):
            backend=LauncherBackend()
            revisions=[]
            backend.presetApplied.connect(lambda:revisions.append(True))
            backend.finish_graphics_detection()
            app.processEvents()
        rows=backend.sectionFields('Visuals','Upscaling')
        upscaler=next(row for row in rows if row['key']=='upscaler')
        self.assertIn('dlss',[option['value'] for option in upscaler['options']])
        self.assertEqual(backend.gpuStatus,'fixture RTX')
        self.assertTrue(revisions)
        backend._set_dlss_supported(False)
        upscaler=next(row for row in backend.sectionFields('Visuals','Upscaling') if row['key']=='upscaler')
        self.assertNotIn('dlss',[option['value'] for option in upscaler['options']])

    def test_category_moves_keep_single_settings(self):
        backend=LauncherBackend()
        self.assertEqual(backend.categorySections('Visuals')[:2],['Display & frame rate','Image effects'])
        keys=lambda cat,section:[f['key'] for f in backend.sectionFields(cat,section)]
        self.assertIn('skip_intro',keys('Game & Saves','Advanced'))
        self.assertNotIn('skip_intro',keys('Game & Saves','In-game preferences'))
        self.assertIn('debug_camera',keys('Mods & Patches','Cheats'))
        self.assertNotIn('debug_camera',keys('System','System'))
