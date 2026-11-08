import QtQuick
import QtQuick.Controls

// The left icon rail shares the in-game guide's navigation style.
Rectangle {
    id: rail
    property string current: "Home"
    property bool locked: false   // during first-time setup the rail only shows the mark
    signal navigate(string page)
    width: Theme.railWidth
    color: "#e6090b0e"
    Rectangle { anchors.right: parent.right; width: 1; height: parent.height; color: Theme.line }

    Column {
        y: 26; width: parent.width; spacing: 0
        Repeater {
            model: rail.locked ? [{kind: "hunter", page: "Setup", tip: launcher.tr("Setup")}]
                               : [{kind: "hunter", page: "Home", tip: launcher.tr("Play")},
                                  {kind: "trophy", page: "Trophies", tip: launcher.tr("Trophies")},
                                  {kind: "puzzle", page: "Mods", tip: launcher.tr("Mods")},
                                  {kind: "settings", page: "Settings", tip: launcher.tr("Settings")}]
            delegate: Item {
                id: destination
                objectName: "rail" + modelData.page
                width: rail.width; height: 76
                property bool active: rail.current === modelData.page
                activeFocusOnTab: !rail.locked
                Accessible.role: Accessible.Button
                Accessible.name: modelData.tip
                Accessible.selected: active
                Accessible.onPressAction: if (!rail.locked) rail.navigate(modelData.page)
                Keys.onReturnPressed: if (!rail.locked) rail.navigate(modelData.page)
                Keys.onSpacePressed: if (!rail.locked) rail.navigate(modelData.page)
                Rectangle { visible: active; x: 0; y: 8; width: 3; height: parent.height - 16; color: Theme.accent }
                Rectangle {
                    anchors.centerIn: parent; width: 52; height: 52; radius: 4
                    color: active ? "#11262c" : hit.containsMouse || destination.activeFocus ? "#15181c" : "transparent"
                }
                NavIcon {
                    anchors.centerIn: parent; width: 30; height: 30; kind: modelData.kind
                    strokeColor: active ? Theme.text : hit.containsMouse ? "#d9d4cc" : "#8f8a84"
                    stroke: modelData.kind === "hunter" ? 1.3 : 1.6
                }
                Rectangle { anchors.bottom: parent.bottom; x: 18; width: parent.width - 36; height: 1; color: Theme.line }
                MouseArea {
                    id: hit; anchors.fill: parent; hoverEnabled: true
                    cursorShape: rail.locked ? Qt.ArrowCursor : Qt.PointingHandCursor
                    onClicked: if (!rail.locked) rail.navigate(modelData.page)
                }
                ToolTipText { visible: (hit.containsMouse || destination.activeFocus) && !rail.locked; text: modelData.tip }
            }
        }
    }

    Button {
        id: updateButton
        objectName: "railUpdateButton"
        anchors.bottom: versionLabel.top; anchors.bottomMargin: 8
        width: rail.width; height: 64
        visible: !rail.locked && launcher.hasUpdate
        padding: 0
        hoverEnabled: true
        text: launcher.tr("Install the new version")
        onClicked: launcher.installUpdate()

        background: Item {
            Rectangle {
                anchors.centerIn: parent; width: 52; height: 52; radius: 4
                color: updateButton.down || updateButton.hovered || updateButton.visualFocus
                     ? Theme.accent : Theme.accentSoft
                border.color: Theme.accent
            }
        }
        contentItem: Item {
            NavIcon {
                anchors.centerIn: parent; width: 30; height: 30
                kind: "update"; strokeColor: Theme.text
            }
        }
        HoverHandler { cursorShape: Qt.PointingHandCursor }
        ToolTipText { visible: updateButton.hovered || updateButton.visualFocus; text: updateButton.text }
    }
    Text {
        id: versionLabel
        anchors.bottom: parent.bottom; anchors.bottomMargin: 18; anchors.horizontalCenter: parent.horizontalCenter
        text: launcher.version; color: Theme.textFaint; font.family: Theme.sans; font.pixelSize: 10
    }
}
