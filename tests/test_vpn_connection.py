"""VPN inventory and installer flow, using temporary folders and fake downloads."""
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'launcher'))
import bbport_coop as coop
import bbport_party as party


class Reply(io.BytesIO):
    def __init__(self, data, length=None):
        super().__init__(data)
        self.headers = {'Content-Length': str(len(data) if length is None else length)}

    def geturl(self):
        return 'https://pkgs.tailscale.com/stable/setup.exe'


class VpnTests(unittest.TestCase):
    def test_inventory_detects_stopped_programs_and_absence(self):
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(coop.sys, 'platform', 'test'), \
                patch.object(coop, 'tailscale_exe', return_value=None), \
                patch.dict(os.environ, {'ProgramFiles': folder, 'ProgramW6432': folder,
                                        'ProgramFiles(x86)': folder}):
            self.assertEqual(coop.installed_vpns(), [])
            exe = Path(folder) / 'Radmin VPN/RvRvpnGui.exe'
            exe.parent.mkdir()
            exe.touch()
            self.assertEqual(coop.installed_vpns(), ['radmin'])
            with patch.object(coop, 'tailscale_exe', return_value=Path('tailscale.exe')):
                self.assertEqual(coop.installed_vpns(), ['radmin', 'tailscale'])

    def test_current_installer_links_and_missing_link(self):
        pages = {
            'radmin': b'<a href="https://download.radmin-vpn.com/download/files/Radmin_VPN_2.1.exe">',
            'tailscale': b'<a href="tailscale-setup-1.2.3.exe">',
        }
        for provider, page in pages.items():
            with self.subTest(provider=provider), patch.object(coop.urllib.request, 'urlopen', return_value=Reply(page)):
                self.assertTrue(coop._vpn_installer_url(provider).endswith('.exe'))
        with patch.object(coop.urllib.request, 'urlopen', return_value=Reply(b'<html>error</html>')):
            with self.assertRaises(coop.CoopError):
                coop._vpn_installer_url('tailscale')

    def test_download_opens_only_complete_executable(self):
        for data, length, valid in [(b'MZinstaller', None, True), (b'<html>error</html>', None, False),
                                     (b'MZpartial', 1000, False)]:
            with self.subTest(data=data), tempfile.TemporaryDirectory() as folder, \
                    patch.object(coop, '_vpn_installer_url', return_value='https://example.test/setup.exe'), \
                    patch.object(coop.tempfile, 'mkdtemp', return_value=str(Path(folder) / 'download')), \
                    patch.object(coop.urllib.request, 'urlopen', return_value=Reply(data, length)), \
                    patch.object(coop.os, 'startfile', create=True) as start:
                (Path(folder) / 'download').mkdir()
                progress = Mock()
                if valid:
                    target = coop.install_vpn('tailscale', progress)
                    self.assertEqual(target.read_bytes(), data)
                    start.assert_called_once_with(str(target))
                    progress.assert_called()
                else:
                    with self.assertRaises(coop.CoopError):
                        coop.install_vpn('tailscale')
                    start.assert_not_called()
                    self.assertFalse((Path(folder) / 'download').exists())

    def test_failed_download_never_opens_installer(self):
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(coop, '_vpn_installer_url', return_value='https://example.test/setup.exe'), \
                patch.object(coop.tempfile, 'mkdtemp', return_value=str(Path(folder) / 'download')), \
                patch.object(coop.urllib.request, 'urlopen', side_effect=OSError('offline')), \
                patch.object(coop.os, 'startfile', create=True) as start:
            (Path(folder) / 'download').mkdir()
            with self.assertRaises(OSError):
                coop.install_vpn('radmin')
            start.assert_not_called()

    def test_lan_never_falls_back_to_vpn(self):
        vpn = dict(text='Tailscale', value='ts', vpn=True, addresses=['100.64.1.2'])
        with self.assertRaises(ValueError):
            party.choose_network([vpn], 'lan')
        lan = dict(text='Ethernet', value='lan', vpn=False, addresses=['192.168.1.2'])
        self.assertEqual(party.choose_network([vpn, lan])[0], '192.168.1.2')


class VpnUiTests(unittest.TestCase):
    def test_inventory_updates_russian_connection_menus(self):
        os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
        from PySide6.QtCore import QUrl, QObject, Slot
        from PySide6.QtQml import QQmlApplicationEngine
        from PySide6.QtQuick import QQuickWindow
        from PySide6.QtTest import QTest
        from PySide6.QtWidgets import QApplication
        import bbport_launcher_win as core
        from bbport_launcher_backend import LauncherBackend
        install = Mock()
        class PreviewBackend(LauncherBackend):
            @Slot(str)
            def coopInstallVpn(self, provider):
                install(provider)
        app = QApplication.instance() or QApplication([])
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.object(core, 'PORT_DIR', root), patch.object(core, 'DATA_DIR', root), \
                    patch.object(core, 'CONFIG_FILE', root / 'settings.json'), \
                    patch.object(LauncherBackend, 'start_background_checks'), \
                    patch.object(LauncherBackend, 'coopCheckConnection'), \
                    patch.dict(core.APP_DEFAULTS, ui_language='ru'), \
                    patch.dict(os.environ, BB_CONFIG=str(root / 'bbport.ini')):
                backend = PreviewBackend()
                self.assertTrue(backend.coopNetworksLoading)
                backend.app['play_mode'] = 'coop'
                self.assertEqual(backend.coopMissingVpns, [])
                for timer in (backend._party_timer, backend._party_network_timer, backend._addons_timer):
                    timer.stop()
                try:
                    for screen, body in [('settings', 'SettingsWorkspace { anchors.fill: parent; category: "Co-op"; section: "Seamless co-op" }'),
                                         ('wizard', 'SetupWizard { anchors.fill: parent; Component.onCompleted: step = 2 }'),
                                         ('home', 'HomePage { anchors.fill: parent }')]:
                        backend.app['coop_connection'] = 'auto'
                        backend._coop_networks_finished([], [])
                        self.assertEqual(backend.coopConnection, 'lan')
                        self.assertEqual([x['value'] for x in backend.coopConnections], ['lan'])
                        engine = QQmlApplicationEngine()
                        engine.rootContext().setContextProperty('launcher', backend)
                        warnings = []
                        engine.warnings.connect(lambda rows: warnings.extend(str(row) for row in rows))
                        width = 760 if screen == 'wizard' else 1100
                        qml = '''import QtQuick
import QtQuick.Window
Window {
    property QtObject networkPopup
    function findNetwork(item) {
        if (item.objectName === "coopNetworkPicker") networkPopup = item.popup
        for (let child of item.children) findNetwork(child)
    }
    Component.onCompleted: findNetwork(contentItem)
    width: ''' + str(width) + '; height: 850; visible: true; color: "#0b0d0f"; ' + body + ' }'
                        engine.loadData(qml.encode(), QUrl.fromLocalFile(str(ROOT / 'launcher/qml/VpnPreview.qml')))
                        self.assertTrue(engine.rootObjects())
                        window = engine.rootObjects()[0]
                        try:
                            for _ in range(20):
                                app.processEvents()
                            def find_item(item, name):
                                if item.objectName() == name:
                                    return item
                                for child in item.childItems():
                                    match = find_item(child, name)
                                    if match is not None:
                                        return match
                                return None
                            picker = find_item(window.contentItem(), 'coopNetworkPicker')
                            self.assertIsNotNone(picker)
                            popup = window.property('networkPopup')
                            self.assertTrue(picker.property('enabled'))
                            install.reset_mock()
                            popup.setProperty('visible', True)
                            backend._coop_networks_loading = True
                            backend.coopNetworksChanged.emit()
                            app.processEvents()
                            self.assertFalse(picker.property('enabled'))
                            self.assertFalse(popup.property('visible'))
                            picker.activated.emit(1)
                            install.assert_not_called()
                            self.assertEqual(backend.coopConnection, 'lan')
                            backend._coop_networks_loading = False
                            backend.coopNetworksChanged.emit()
                            app.processEvents()
                            self.assertTrue(picker.property('enabled'))
                            popup.setProperty('visible', True)
                            for _ in range(10):
                                app.processEvents()
                            self.assertEqual(picker.property('count'), 3)
                            # Missing VPN rows cannot replace the selected connection.
                            picker.setProperty('currentIndex', 1)
                            with self.subTest(screen=screen):
                                install.reset_mock()
                                picker.activated.emit(1)
                                self.assertEqual(backend.coopConnection, 'lan')
                                self.assertEqual(picker.property('currentIndex'), 0)
                                install.assert_not_called()
                                for provider in ('radmin', 'tailscale'):
                                    popup.setProperty('visible', True)
                                    QTest.qWait(200)
                                    button = find_item(popup.property('contentItem'), 'installVpn_' + provider)
                                    self.assertIsNotNone(button)
                                    self.assertTrue(button.property('visible'))
                                    self.assertFalse(button.property('contentItem').property('truncated'))
                                    button.clicked.emit()
                                    install.assert_called_with(provider)
                                    self.assertFalse(popup.property('visible'))
                                    self.assertEqual(backend.coopConnection, 'lan')
                                    QTest.qWait(200)
                            popup.setProperty('visible', True)
                            app.processEvents()
                            self.assertTrue(window.grabWindow().save(str(ROOT / ('out/vpn-' + screen + '-preview.png'))))
                            backend._coop_networks_finished([], ['radmin', 'tailscale'])
                            app.processEvents()
                            self.assertEqual([x['value'] for x in backend.coopConnections], ['lan', 'radmin', 'tailscale'])
                            self.assertEqual(backend.coopMissingVpns, [])
                            self.assertEqual(picker.property('count'), 3)
                            app.processEvents()
                            self.assertIsNone(find_item(popup.property('contentItem'), 'installVpn_radmin'))
                            picker.setProperty('currentIndex', 1)
                            picker.activated.emit(1)
                            self.assertEqual(backend.coopConnection, 'radmin')
                            self.assertEqual([w for w in warnings if any(s in w for s in
                                             ('ReferenceError', 'TypeError', 'Binding loop', 'Cannot assign'))], [])
                        finally:
                            window.close()
                            engine.deleteLater()
                            app.processEvents()
                finally:
                    backend.shutdown_coop()


if __name__ == '__main__':
    unittest.main()
