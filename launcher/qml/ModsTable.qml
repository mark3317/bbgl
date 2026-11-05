import QtQuick
import QtQuick.Controls

Rectangle {
    id: table
    objectName: "installedModsTable"
    property var mods: []
    readonly property real nameWidth: Math.max(80, width - 280)
    implicitHeight: body.implicitHeight
    height: visible ? implicitHeight : 0
    color: "#14171b"
    border.color: Theme.lineStrong
    radius: Theme.radius

    Column {
        id: body
        width: parent.width
        Rectangle {
            width: parent.width; height: 46
            color: "#20242a"
            Row {
                x: 16; width: parent.width - 32; height: parent.height
                Text { width: 40; height: parent.height; text: "№"; color: Theme.textDim; verticalAlignment: Text.AlignVCenter; font.family: Theme.sans; font.pixelSize: 12 }
                Text { width: table.nameWidth; height: parent.height; text: launcher.tr("Mod"); color: Theme.textDim; verticalAlignment: Text.AlignVCenter; font.family: Theme.sans; font.pixelSize: 12 }
                Text { width: 130; height: parent.height; text: launcher.tr("Order"); color: Theme.textDim; verticalAlignment: Text.AlignVCenter; horizontalAlignment: Text.AlignHCenter; font.family: Theme.sans; font.pixelSize: 12 }
                Text { width: 78; height: parent.height; text: launcher.tr("Enabled"); color: Theme.textDim; verticalAlignment: Text.AlignVCenter; horizontalAlignment: Text.AlignHCenter; font.family: Theme.sans; font.pixelSize: 12 }
            }
        }
        Repeater {
            model: table.mods
            delegate: Item {
                property bool remote: modelData.status === "missing" || modelData.status === "conflict"
                width: table.width; height: Math.max(64, label.implicitHeight + 28)
                enabled: !launcher.modsDownloading
                Row {
                    x: 16; width: parent.width - 32; height: parent.height
                    Text { width: 40; height: parent.height; text: index + 1; color: Theme.textDim; verticalAlignment: Text.AlignVCenter; font.family: Theme.sans; font.pixelSize: 13 }
                    Item {
                        width: table.nameWidth; height: parent.height
                        Column {
                            id: label; anchors.verticalCenter: parent.verticalCenter; width: parent.width - 14; spacing: 5
                            Text { width: parent.width; text: modelData.name; wrapMode: Text.WrapAnywhere; color: Theme.text; font.family: Theme.sans; font.pixelSize: 14 }
                            Text {
                                visible: remote; width: parent.width
                                text: remote ? modelData.player + " · " + launcher.tr(modelData.status === "missing" ? "Inactive — installation required" : "Different contents — existing files will be kept") : ""
                                wrapMode: Text.WordWrap; color: Theme.warn; font.family: Theme.sans; font.pixelSize: 12
                            }
                        }
                    }
                    Item {
                        width: 130; height: parent.height
                        GlassButton {
                            visible: remote && modelData.status === "missing"; anchors.centerIn: parent
                            text: launcher.tr("Install"); width: 120; height: 38
                            enabled: !launcher.running && !launcher.coopBusy
                            onClicked: launcher.downloadNetworkMod(modelData.peer, modelData.name)
                        }
                        Row {
                            anchors.centerIn: parent; spacing: 4; visible: !remote
                            GlassButton { text: "↑"; width: 44; height: 38; enabled: index > 0; onClicked: launcher.moveMod(modelData.name, -1) }
                            GlassButton { text: "↓"; width: 44; height: 38; enabled: index < table.mods.filter(m => !m.status).length - 1; onClicked: launcher.moveMod(modelData.name, 1) }
                        }
                    }
                    Item {
                        width: 78; height: parent.height
                        GlassSwitch { anchors.centerIn: parent; enabled: !remote; checked: !remote && modelData.enabled; onToggled: launcher.setMod(modelData.name, checked) }
                    }
                }
                Rectangle { anchors.top: parent.top; width: parent.width; height: 1; color: Theme.line }
            }
        }
        Text {
            visible: table.mods.length === 0
            width: parent.width; height: visible ? 64 : 0
            text: launcher.tr("No installed mods"); color: Theme.textDim
            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
            font.family: Theme.sans; font.pixelSize: 13
        }
    }
}
