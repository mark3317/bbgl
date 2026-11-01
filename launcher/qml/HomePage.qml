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
    Column {
        x: Theme.railWidth + 44; y: Math.max(64, parent.height * 0.16)
        width: home.panelWidth - 88; spacing: 22
        Text { width: parent.width; text: "Bloodborne\nGame Launcher"; color: Theme.text; font.family: Theme.serif; font.pixelSize: 46; wrapMode: Text.WordWrap }
        Rectangle { width: 64; height: 2; color: Theme.accent }
        Text { width: parent.width; text: launcher.profileSummary; color: Theme.text; font.family: Theme.sans; font.pixelSize: 15; wrapMode: Text.WrapAnywhere }
        Text { width: parent.width; text: launcher.saveStatus; color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 13; wrapMode: Text.WordWrap }
        Item { width: 1; height: 10 }
        Repeater {
            model: [{mode: "offline", label: launcher.tr("Play offline")}, {mode: "coop", label: launcher.tr("Play co-op")}]
            delegate: GlassButton {
                width: parent.width; height: 56; serif: true
                text: launcher.coopBusy ? launcher.tr("Getting co-op ready…") : modelData.label
                highlighted: modelData.mode === "offline"
                enabled: !launcher.running && !launcher.setupRunning && !launcher.coopBusy
                onClicked: { launcher.setPlayMode(modelData.mode); home.primaryRequested() }
            }
        }
        GlassButton { visible: launcher.running; width: parent.width; text: launcher.tr("Stop"); onClicked: launcher.stop() }
        Text {
            width: parent.width; visible: home.gameBlocked || home.savesBlocked || launcher.setupRunning
            text: home.gameBlocked ? launcher.tr("Choose your game folder or download the game.") : home.savesBlocked ? launcher.tr("The saves folder cannot be written. Choose another one.") : launcher.gameDownloadStatus
            color: Theme.warn; font.family: Theme.sans; font.pixelSize: 13; wrapMode: Text.WordWrap
        }
        GlassButton { visible: launcher.hasUpdate; text: launcher.tr("Install the new version"); onClicked: launcher.installUpdate() }
        Text {
            width: parent.width; visible: text !== ""
            text: launcher.notice === launcher.tr("Ready to hunt.") ? "" : launcher.notice
            color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 12; wrapMode: Text.WordWrap
        }
    }
}
