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
        x: Theme.railWidth + 44; y: 42; width: home.panelWidth - 88; height: parent.height - 84
        clip: true; contentHeight: content.implicitHeight
        ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
        Column {
            id: content; width: parent.width; spacing: 14
            Text { width: parent.width; text: "Bloodborne Game Launcher"; color: Theme.text; font.family: Theme.serif; font.pixelSize: 36; wrapMode: Text.WordWrap }
            Rectangle { width: 64; height: 2; color: Theme.accent }
            Text { width: parent.width; text: launcher.profileSummary; color: Theme.text; font.pixelSize: 14; wrapMode: Text.WordWrap }
            Text { width: parent.width; text: launcher.setupFacts.resolution + "  ·  " + launcher.setupFacts.frameRate + "  ·  " + launcher.setupFacts.upscaler + "  ·  " + launcher.setupFacts.display; color: Theme.text; font.family: Theme.serif; font.pixelSize: 17; wrapMode: Text.WordWrap }
            Text { width: parent.width; text: launcher.saveStatus; color: Theme.textDim; font.pixelSize: 12; wrapMode: Text.WordWrap }
            ToggleRow {
                width: parent.width; height: 48
                label: launcher.tr("Play mode")
                checked: launcher.playMode === "coop"
                onToggled: launcher.setPlayMode(checked ? "coop" : "offline")
            }
            GlassButton {
                property bool playAction: true
                width: Math.min(250, parent.width); height: 46; serif: true; highlighted: true
                text: launcher.running ? launcher.tr("Game running") : launcher.coopBusy ? launcher.tr("Getting co-op ready…") : launcher.playMode === "coop" ? launcher.tr("Play co-op") : launcher.tr("Play offline")
                enabled: !launcher.running && !launcher.setupRunning && !launcher.coopBusy && !home.gameBlocked && !home.savesBlocked && !home.onlineBlocked
                onClicked: home.primaryRequested()
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
}
