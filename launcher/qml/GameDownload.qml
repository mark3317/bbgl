import QtQuick
import QtQuick.Controls

Column {
    spacing: 10
    Row {
        spacing: 12
        GlassButton {
            text: launcher.tr("Download game")
            width: 180; height: 42
            enabled: !launcher.setupRunning && !launcher.running
            onClicked: launcher.downloadGame()
        }
        GlassButton {
            visible: launcher.setupRunning && launcher.gameDownloadStatus !== ""
            text: launcher.tr("Cancel download")
            width: 180; height: 42
            onClicked: launcher.cancelGameDownload()
        }
    }
    Text {
        width: parent.width; wrapMode: Text.WordWrap
        text: launcher.tr("Downloads into the game folder selected above.")
        color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 13
    }
    ProgressBar {
        width: parent.width; from: 0; to: 1
        visible: launcher.gameDownloadStatus !== ""
        value: launcher.gameDownloadProgress
        indeterminate: launcher.setupRunning && value === 0
    }
    Text {
        width: parent.width; wrapMode: Text.WordWrap
        visible: launcher.gameDownloadStatus !== ""
        text: launcher.gameDownloadStatus
        color: Theme.text; font.family: Theme.sans; font.pixelSize: 13
    }
}
