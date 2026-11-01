import sys, threading, unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_setup_wizard as wizard_tests
import test_game_download as download_tests
import bbport_launcher_backend as backend_module
import bbport_coop as coop
import bbport_game_download as download

class RedesignTests(unittest.TestCase):
    setUp = wizard_tests.FirstRunWizardTests.setUp
    tearDown = wizard_tests.FirstRunWizardTests.tearDown
    def test_name_edit_updates_both_names_without_migrating_existing_account(self):
        backend = backend_module.LauncherBackend()
        backend.app.update(coop_name='ExistingAccount',player_name='OldHunter')
        self.assertEqual(backend.value('coop_name'),'ExistingAccount')
        self.assertEqual(backend.app['player_name'],'OldHunter')
        backend.setValue('coop_name','NewHunter')
        self.assertEqual(backend.app['player_name'],'NewHunter')
        self.assertEqual(backend._coop_account()[0],'NewHunter')

    def test_setup_name_follows_save_folder_until_manually_edited(self):
        backend = backend_module.LauncherBackend()
        backend.prepareSetupName()
        self.assertEqual(backend.value('coop_name'), 'user')
        backend.setValue('user_dir', str(self.root / 'HunterSave'))
        self.assertEqual(backend.app['player_name'], 'HunterSave')
        restarted = backend_module.LauncherBackend()
        restarted.prepareSetupName()
        restarted.setValue('user_dir', str(self.root / 'SecondSave'))
        self.assertEqual(restarted.value('coop_name'), 'SecondSave')
        restarted.setValue('coop_name', 'MyName')
        restarted.setValue('user_dir', str(self.root / 'ThirdSave'))
        self.assertEqual(restarted.value('coop_name'), 'MyName')
        restarted.setValue('coop_name', '')
        restarted.prepareSetupName()
        self.assertEqual(restarted.value('coop_name'), '')

    def test_setup_does_not_rename_existing_accounts(self):
        backend = backend_module.LauncherBackend()
        backend.app.update(coop_name='ExistingAccount', player_name='ExistingHunter')
        backend.prepareSetupName()
        backend.setValue('user_dir', str(self.root / 'OtherSave'))
        self.assertEqual(backend.app['coop_name'], 'ExistingAccount')
        self.assertEqual(backend.app['player_name'], 'ExistingHunter')

    def test_host_without_tailscale_reports_download_and_stops_failed_host(self):
        backend = backend_module.LauncherBackend()
        backend.app.update(coop_name='Hunter',coop_password='test-only')
        backend._coop_run=lambda message,work: work()
        with patch.object(backend,'_coop_ensure_packages'), patch.object(coop,'host_address',return_value=('192.168.1.2','LAN')), patch.object(coop,'registration_key',return_value='fixture'), patch.object(coop,'tailscale_exe',return_value=None), patch.object(backend._coop_host,'start',side_effect=coop.CoopError('Could not start')), patch.object(backend._coop_host,'stop') as stop:
            with self.assertRaisesRegex(coop.CoopError,'https://tailscale.com/download/windows'):
                backend.coopStartHosting()
            stop.assert_called_once()

    def test_host_mode_cannot_silently_join_old_invite(self):
        backend = backend_module.LauncherBackend()
        backend.app.update(coop_name='Hunter',coop_password='test-only',coop_role='host',coop_invite='old-invite')
        self.assertFalse(backend._coop_ready())
        with patch.object(coop,'read_invite') as read:
            backend.coopPlay()
            read.assert_not_called()

class SelectedDownloadTests(unittest.TestCase):
    setUp = download_tests.GameDownloadTests.setUp
    request = download_tests.GameDownloadTests.request
    def test_selected_folder_is_used_and_existing_folder_is_preserved(self):
        target=self.root/'chosen-location'/'Bloodborne'
        with patch.object(download,'request',self.request):
            installed=download.install(self.install,lambda *args:None,threading.Event(),target=target)
            self.assertEqual(installed,target)
            self.assertEqual((target/'eboot.bin').read_bytes(),b'example boot')
            with self.assertRaisesRegex(ValueError,'already exists'):
                download.install(self.install,lambda *args:None,threading.Event(),target=target)
            self.assertEqual((target/'eboot.bin').read_bytes(),b'example boot')
