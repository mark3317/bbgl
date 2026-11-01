import QtQuick
import QtQuick.Controls

Item {
    id: home
    signal primaryRequested()
    signal openSettings(string category, string section)
    property bool gameBlocked: false
    property bool savesBlocked: false
    property bool onlineBlocked: false
    property real panelWidth: Math.min(610, width - Theme.railWidth - 32)
    Image { anchors.fill: parent; source: Qt.resolvedUrl("../assets/ui/home-background.png"); fillMode: Image.PreserveAspectCrop; smooth: true }
    Rectangle { anchors.fill: parent; color: "#180b0d10" }
    Rectangle {
        x: Theme.railWidth; width: home.panelWidth + 120; height: parent.height
        gradient: Gradient { orientation: Gradient.Horizontal
            GradientStop { position: 0; color: "#b00b0d10" }
            GradientStop { position: 0.75; color: "#600b0d10" }
            GradientStop { position: 1; color: "#000b0d10" }
        }
    }
    Flickable {
        id: homeScroll
        x: Theme.railWidth + 44; y: 64; width: home.panelWidth - 64; height: parent.height - 218
        clip: true; contentHeight: content.implicitHeight
        ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
        Column {
            id: content; width: parent.width - 24; spacing: 24
            Text { width: parent.width; text: "Bloodborne Game Launcher"; color: Theme.text; font.family: Theme.serif; font.pixelSize: 36; wrapMode: Text.WordWrap }
            Rectangle { width: 64; height: 2; color: Theme.accent }
            Text { width: parent.width; text: launcher.profileSummary; color: Theme.text; font.pixelSize: 14; wrapMode: Text.WordWrap }
            Text { width: parent.width; text: launcher.setupFacts.resolution + "  ·  " + launcher.setupFacts.frameRate + "  ·  " + launcher.setupFacts.upscaler + "  ·  " + launcher.setupFacts.display; color: Theme.text; font.family: Theme.serif; font.pixelSize: 17; wrapMode: Text.WordWrap }
            Text { width: parent.width; text: launcher.saveStatus; color: Theme.textDim; font.pixelSize: 12; wrapMode: Text.WordWrap }
            Rectangle {
                width: parent.width; height: 56; radius: 8; color: Theme.surface; border.color: Theme.line
                Row {
                    anchors.fill: parent; anchors.margins: 4
                    Repeater {
                        model: [{mode: "offline", label: launcher.tr("Single player")}, {mode: "coop", label: launcher.tr("Multiplayer")}]
                        delegate: Rectangle {
                            width: (content.width - 8) / 2; height: 48; radius: 6
                            color: launcher.playMode === modelData.mode ? Theme.accent : "transparent"
                            Text { anchors.centerIn: parent; text: modelData.label; color: Theme.text; font.pixelSize: 16 }
                            MouseArea { anchors.fill: parent; enabled: !launcher.running && !launcher.coopBusy; cursorShape: Qt.PointingHandCursor; onClicked: launcher.setPlayMode(modelData.mode) }
                        }
                    }
                }
            }
            CoopConnection {
                width: parent.width; visible: launcher.playMode === "coop"
                onAttentionRequested: (target) => {
                    if (!home.visible) return
                    homeScroll.contentY = Math.max(0, Math.min(target.mapToItem(content, 0, 0).y - 24, homeScroll.contentHeight - homeScroll.height))
                }
            }
            GlassButton { visible: launcher.running; text: launcher.tr("Stop"); onClicked: launcher.stop() }
            Text {
                width: parent.width; visible: home.gameBlocked || home.savesBlocked || launcher.setupRunning
                text: home.gameBlocked ? launcher.tr("Choose your game folder or download the game.") : home.savesBlocked ? launcher.tr("The saves folder cannot be written. Choose another one.") : launcher.gameDownloadStatus
                color: Theme.warn; font.pixelSize: 13; wrapMode: Text.WordWrap
            }
            GlassButton { visible: launcher.hasUpdate; text: launcher.tr("Install the new version"); onClicked: launcher.installUpdate() }
            Text { width: parent.width; visible: text !== ""; text: launcher.notice === launcher.tr("Ready to hunt.") ? "" : launcher.notice; color: Theme.textDim; font.pixelSize: 12; wrapMode: Text.WordWrap }
        }
    }
    Rectangle {
        x: Theme.railWidth + 28; width: home.panelWidth - 32
        anchors.bottom: parent.bottom; anchors.bottomMargin: 16
        height: 136; radius: 10; color: "#e60e1115"; border.color: Theme.line
        Row {
            anchors.horizontalCenter: parent.horizontalCenter; y: 16; spacing: 8
            Rectangle { width: 7; height: 7; radius: 4; color: home.gameBlocked || home.savesBlocked || home.onlineBlocked ? Theme.warn : Theme.good; anchors.verticalCenter: parent.verticalCenter }
            Text { text: launcher.playMode === "coop" ? launcher.tr("Multiplayer") : launcher.tr("Single player"); color: Theme.textDim; font.pixelSize: 13 }
        }
        GlassButton {
            anchors.horizontalCenter: parent.horizontalCenter; anchors.bottom: parent.bottom; anchors.bottomMargin: 18
            width: 250; height: 56; serif: true; highlighted: true
            text: launcher.tr("Play")
            enabled: !launcher.running && !launcher.setupRunning && !launcher.coopBusy && !home.gameBlocked && !home.savesBlocked && !home.onlineBlocked
            onClicked: home.primaryRequested()
        }
    }
}
