import QtQuick
import QtQuick.Controls

Rectangle {
    id: table
    objectName: "installedModsTable"
    property var mods: []
    readonly property int inset: 20
    readonly property int numberWidth: 54
    readonly property int enabledWidth: 88
    readonly property int orderWidth: 80
    readonly property real nameWidth: Math.max(80, body.width - 2 * inset - numberWidth - enabledWidth - orderWidth)
    readonly property int localModCount: mods.filter(mod => !mod.status).length
    implicitHeight: body.implicitHeight + 2
    height: visible ? implicitHeight : 0
    color: Theme.surface
    border.color: Theme.lineStrong
    radius: 12

    component ColumnTitle: Text {
        height: parent.height
        color: Theme.textDim
        font.family: Theme.sans
        font.pixelSize: 12
        font.weight: Font.DemiBold
        verticalAlignment: Text.AlignVCenter
    }

    Column {
        id: body
        x: 1; y: 1; width: parent.width - 2
        Rectangle {
            width: parent.width; height: 44
            color: "#232a32"
            topLeftRadius: table.radius - 1
            topRightRadius: table.radius - 1
            Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: Theme.lineStrong }
            Row {
                x: table.inset; width: parent.width - 2 * x; height: parent.height
                ColumnTitle { width: table.numberWidth; text: "№"; leftPadding: 9 }
                ColumnTitle { width: table.nameWidth; text: launcher.tr("Mod") }
                ColumnTitle { width: table.enabledWidth; text: launcher.tr("Enabled"); horizontalAlignment: Text.AlignHCenter }
                ColumnTitle { width: table.orderWidth; text: launcher.tr("Order"); horizontalAlignment: Text.AlignHCenter }
            }
        }
        Repeater {
            model: table.mods
            delegate: Rectangle {
                id: modRow
                required property int index
                required property var modelData
                readonly property bool remote: modelData.status === "missing" || modelData.status === "conflict"
                width: body.width; height: Math.max(remote ? 72 : 64, label.implicitHeight + 28)
                color: rowHover.hovered ? Theme.surfaceHover : remote ? "#1a1b1e" : Theme.surface
                bottomLeftRadius: index === table.mods.length - 1 ? table.radius - 1 : 0
                bottomRightRadius: bottomLeftRadius
                enabled: !launcher.modsDownloading
                HoverHandler { id: rowHover }
                Rectangle {
                    visible: modRow.index > 0
                    x: table.inset; width: parent.width - 2 * x; height: 1
                    color: modRow.remote && modRow.index === table.localModCount ? Theme.lineStrong : Theme.line
                }
                Row {
                    x: table.inset; width: parent.width - 2 * x; height: parent.height
                    Item {
                        width: table.numberWidth; height: parent.height
                        Rectangle {
                            anchors.verticalCenter: parent.verticalCenter
                            width: 32; height: 28; radius: 7
                            color: Theme.base; border.color: Theme.line
                            Text {
                                anchors.centerIn: parent; text: modRow.index + 1; color: Theme.textDim
                                font.family: Theme.sans; font.pixelSize: 12; font.weight: Font.DemiBold
                            }
                        }
                    }
                    Item {
                        width: table.nameWidth; height: parent.height
                        Column {
                            id: label
                            anchors.left: parent.left
                            anchors.right: installButton.visible ? installButton.left : parent.right
                            anchors.rightMargin: 14
                            anchors.verticalCenter: parent.verticalCenter
                            spacing: 5
                            Text {
                                width: parent.width; text: modelData.name; wrapMode: Text.Wrap
                                color: Theme.text; font.family: Theme.sans; font.pixelSize: 15; font.weight: Font.DemiBold
                            }
                            Row {
                                id: statusLine
                                visible: remote; width: parent.width; spacing: 7
                                Rectangle { y: 5; width: 6; height: 6; radius: 3; color: Theme.warn }
                                Text {
                                    width: parent.width - 6 - statusLine.spacing
                                    text: modRow.remote ? modRow.modelData.player + " · " + launcher.tr(modRow.modelData.status === "missing" ? "Inactive — installation required" : "Different contents — existing files will be kept") : ""
                                    wrapMode: Text.Wrap; color: Theme.warn; font.family: Theme.sans; font.pixelSize: 12
                                }
                            }
                        }
                        GlassButton {
                            id: installButton
                            visible: modelData.status === "missing"
                            anchors.right: parent.right
                            anchors.rightMargin: 5
                            anchors.verticalCenter: parent.verticalCenter
                            text: launcher.tr("Install"); width: 120; height: 34
                            highlighted: true
                            enabled: !launcher.running && !launcher.coopBusy
                            onClicked: launcher.downloadNetworkMod(modelData.peer, modelData.name)
                        }
                    }
                    Item {
                        width: table.enabledWidth; height: parent.height
                        GlassSwitch { anchors.centerIn: parent; enabled: !remote; checked: !remote && modelData.enabled; onToggled: launcher.setMod(modelData.name, checked) }
                    }
                    Item {
                        width: table.orderWidth; height: parent.height
                        Rectangle {
                            anchors.centerIn: parent
                            visible: !modRow.remote
                            width: 46; height: arrows.implicitHeight + 2; radius: 8
                            color: Theme.base; border.color: Theme.lineStrong
                            Rectangle { anchors.centerIn: parent; width: parent.width - 12; height: 1; color: Theme.lineStrong }
                        }
                        Column {
                            id: arrows
                            anchors.centerIn: parent
                            spacing: 1
                            Repeater {
                                model: modRow.remote ? [] : [-1, 1]
                                delegate: Button {
                                    id: arrow
                                    required property int modelData
                                    readonly property bool up: modelData < 0
                                    readonly property bool active: enabled && (hovered || visualFocus)
                                    objectName: up ? "moveModUp" : "moveModDown"
                                    width: 44; height: 25; padding: 0
                                    enabled: up ? modRow.index > 0 : modRow.index + 1 < table.localModCount
                                    hoverEnabled: true
                                    Accessible.name: launcher.tr(up ? "Move mod up" : "Move mod down")
                                    ToolTip.text: Accessible.name
                                    ToolTip.visible: hovered && enabled
                                    ToolTip.delay: 500
                                    contentItem: Item {
                                        NavIcon {
                                            anchors.centerIn: parent
                                            width: 18; height: 18
                                            kind: "chevron"
                                            rotation: arrow.up ? -90 : 90
                                            strokeColor: !arrow.enabled ? Theme.textFaint : arrow.active ? Theme.text : Theme.textDim
                                            opacity: arrow.enabled ? 1 : 0.55
                                        }
                                    }
                                    background: Rectangle {
                                        radius: 6
                                        color: arrow.down ? Theme.accent : arrow.active ? Theme.accentSoft : "transparent"
                                        border.color: arrow.visualFocus ? Theme.accentHover : "transparent"
                                    }
                                    onClicked: launcher.moveMod(modRow.modelData.name, modelData)
                                }
                            }
                        }
                    }
                }
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
