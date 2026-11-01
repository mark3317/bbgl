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
        x: Theme.railWidth + 44; y: 36; width: home.panelWidth - 64; height: parent.height - 220
        clip: true; contentHeight: content.implicitHeight
        ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
        Column {
            id: content; width: parent.width - 24; spacing: 12
            Text { width: parent.width; text: "Bloodborne Game Launcher"; color: Theme.text; font.family: Theme.serif; font.pixelSize: 36; wrapMode: Text.WordWrap }
            Rectangle { width: 64; height: 2; color: Theme.accent }
            Text { width: parent.width; text: launcher.profileSummary; color: Theme.text; font.pixelSize: 16; wrapMode: Text.WordWrap }
            Column {
                width: parent.width; spacing: 5
                Repeater {
                    model: [
                        {label: launcher.tr("Resolution"), value: launcher.setupFacts.resolution},
                        {label: launcher.tr("Window mode"), value: launcher.setupFacts.display},
                        {label: launcher.tr("Frame rate"), value: launcher.setupFacts.frameRate},
                        {label: launcher.tr("Upscaling"), value: launcher.setupFacts.upscaler},
                        {label: launcher.tr("Generation"), value: launcher.setupFacts.frameGeneration}
                    ]
                    delegate: Item {
                        width: parent.width; height: Math.max(22, factLabel.implicitHeight, factValue.implicitHeight)
                        Text { id: factLabel; width: parent.width * 0.48; text: modelData.label; color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 15; wrapMode: Text.WordWrap }
                        Text { id: factValue; anchors.right: parent.right; width: parent.width * 0.50; text: modelData.value; color: Theme.text; font.family: Theme.sans; font.pixelSize: 15; horizontalAlignment: Text.AlignRight; wrapMode: Text.WordWrap }
                    }
                }
            }
            Text { width: parent.width; text: launcher.saveStatus; color: Theme.textDim; font.pixelSize: 12; wrapMode: Text.WordWrap }
            FieldRow {
                width: parent.width; compact: true; minimumHeight: 54
                field: launcher.settingsRevision < 0 ? ({}) : launcher.sectionFields("Co-op", "Seamless co-op").find(f => f.key === "coop_name")
            }
            CoopConnection {
                width: parent.width; compact: true; showPlayerName: false; visible: launcher.playMode === "coop"
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
        }
    }
    Item {
        x: Theme.railWidth + 44; width: home.panelWidth - 88
        anchors.bottom: parent.bottom; anchors.bottomMargin: 12; height: 160
        Item {
            id: modeSwitch
            anchors.horizontalCenter: parent.horizontalCenter; width: 296; height: 44
            Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: Theme.line }
            Row {
                anchors.fill: parent
                Repeater {
                    model: [{mode: "offline", label: launcher.tr("Single-player")}, {mode: "coop", label: launcher.tr("Cooperative")}]
                    delegate: Button {
                        id: modeButton
                        property bool selected: launcher.playMode === modelData.mode
                        width: modeSwitch.width / 2; height: modeSwitch.height
                        enabled: !launcher.running && !launcher.coopBusy
                        hoverEnabled: true
                        contentItem: Text {
                            text: modelData.label; color: modeButton.selected ? Theme.text : Theme.textDim
                            font.family: Theme.serif; font.pixelSize: 18
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }
                        background: Rectangle {
                            color: modeButton.hovered ? "#181c21" : "transparent"
                            Rectangle { visible: modeButton.selected; anchors.bottom: parent.bottom; anchors.horizontalCenter: parent.horizontalCenter; width: parent.width - 28; height: 2; color: Theme.accentHover }
                        }
                        onClicked: launcher.setPlayMode(modelData.mode)
                    }
                }
            }
        }
        GlassButton {
            id: playButton
            anchors.horizontalCenter: parent.horizontalCenter; y: 54
            width: 296; height: 56; serif: true; highlighted: true
            text: launcher.tr("Play")
            enabled: !launcher.running && !launcher.setupRunning && !launcher.coopBusy && !home.gameBlocked && !home.savesBlocked && !home.onlineBlocked
            onClicked: home.primaryRequested()
        }
        Text {
            y: 122; width: parent.width; wrapMode: Text.WordWrap; maximumLineCount: 3; elide: Text.ElideRight
            text: launcher.notice !== launcher.tr("Ready to hunt.") ? launcher.notice : launcher.playMode === "coop" ? launcher.coopStatus : ""
            color: Theme.textDim; font.pixelSize: 12; horizontalAlignment: Text.AlignHCenter
        }
    }
}
