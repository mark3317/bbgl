import QtQuick
Column {
    spacing: 8
    GlassButton {
        width: 180; height: 48
        text: launcher.fsrReady ? launcher.tr("Remove FSR 4 assets") : launcher.tr("Download FSR 4 assets")
        enabled: !launcher.fsrBusy && !launcher.running
        onClicked: launcher.fsrReady ? launcher.removeFsr4() : launcher.downloadFsr4()
    }
    Note { text: launcher.fsrStatus }
}
