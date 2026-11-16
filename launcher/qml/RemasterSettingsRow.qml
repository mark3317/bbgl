import QtQuick
import QtQuick.Controls

Column {
    objectName: "remasterSettingsRow"
    spacing: 0
    onVisibleChanged: if (visible) launcher.refreshRemaster()

    FieldRow {
        width: parent.width
        showDivider: !details.visible
        controlWidth: actions.width
        field: ({
            kind: "display",
            label: "BB PC Remaster",
            hint: launcher.remasterInstalled
                ? launcher.tr("High-resolution textures. Applies at the next game start.")
                : launcher.tr("Download Remaster 1.10 and PATCH 1.13, then choose both archives.")
        })

        Row {
            id: actions
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            spacing: 8
            GlassButton {
                objectName: "remasterDownload"
                visible: !launcher.remasterInstalled && !launcher.remasterBusy
                width: 108; height: 35
                text: launcher.tr("Download")
                ToolTip.visible: hovered || visualFocus
                ToolTip.text: launcher.tr("Download · %1 GiB").replace("%1",
                    Number(launcher.remasterSizeGiB).toLocaleString(Qt.locale(launcher.russian ? "ru_RU" : "en_US"), "f", 1))
                onClicked: launcher.downloadRemaster()
            }
            GlassButton {
                objectName: "remasterImport"
                visible: !launcher.remasterInstalled && !launcher.remasterBusy
                width: 108; height: 35
                text: launcher.tr("Choose")
                onClicked: launcher.importRemaster()
            }
            GlassButton {
                visible: launcher.remasterBusy
                width: 108; height: 35
                text: launcher.tr("Cancel")
                onClicked: launcher.cancelRemaster()
            }
            GlassSwitch {
                objectName: "remasterSwitch"
                visible: launcher.remasterInstalled
                enabled: !launcher.remasterBusy
                height: 35
                checked: launcher.remasterSelected
                onToggled: launcher.setRemasterEnabled(checked)
            }
        }
    }
    Column {
        id: details
        width: parent.width
        visible: launcher.remasterBusy || launcher.remasterStatus !== ""
        spacing: 6
        bottomPadding: 8
        ProgressBar {
            objectName: "remasterProgress"
            visible: launcher.remasterBusy
            width: parent.width
            from: 0; to: 1; value: launcher.remasterProgress
        }
        Note {
            visible: text !== ""
            text: launcher.remasterStatus
        }
        GlassButton {
            visible: launcher.remasterDownloadFailed && !launcher.remasterInstalled && !launcher.remasterBusy
            width: 165; height: 35
            text: launcher.tr("Open Nexus Mods")
            onClicked: launcher.openRemasterNexus()
        }
        Rectangle { width: parent.width; height: 1; color: Theme.line }
    }
}
