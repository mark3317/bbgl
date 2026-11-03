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
        x: Theme.railWidth; width: home.panelWidth + 180; height: parent.height
        gradient: Gradient { orientation: Gradient.Horizontal
            GradientStop { position: 0; color: "#ed0b0d10" }
            GradientStop { position: 0.75; color: "#b00b0d10" }
            GradientStop { position: 1; color: "#000b0d10" }
        }
    }
    Flickable {
        id: homeScroll
        objectName: "homeScroll"
        x: Theme.railWidth + 44; y: 32; width: home.panelWidth - 64; height: parent.height - y - 184
        clip: true; contentHeight: content.implicitHeight
        boundsBehavior: Flickable.StopAtBounds
        ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
        Column {
            id: content; width: parent.width - 24; spacing: 12
            Text { width: parent.width; text: "Bloodborne Game Launcher"; color: Theme.text; font.family: Theme.serif; font.pixelSize: 32; wrapMode: Text.WordWrap }
            Rectangle { width: 36; height: 3; radius: 1.5; color: Theme.accentHover }
            Rectangle {
                width: parent.width; height: summary.implicitHeight + 24
                radius: 4; color: "#e6111519"; border.color: Theme.lineStrong
                Column {
                    id: summary; x: 18; y: 12; width: parent.width - 36; spacing: 8
                    Item {
                        width: parent.width; height: profileTitle.implicitHeight
                        Text {
                            id: profileTitle; width: parent.width
                            text: launcher.profileSummary; color: Theme.text
                            font.family: Theme.serif; font.pixelSize: 18; font.weight: Font.Medium; wrapMode: Text.WordWrap
                        }
                    }
                    Column {
                        width: parent.width; spacing: 0
                        Repeater {
                            model: [
                                {label: launcher.tr("Resolution"), value: launcher.setupFacts.resolution},
                                {label: launcher.tr("Window mode"), value: launcher.setupFacts.display},
                                {label: launcher.tr("Frame rate"), value: launcher.setupFacts.frameRate},
                                {label: launcher.tr("Upscaling"), value: launcher.setupFacts.upscaler},
                                {label: launcher.tr("Generation"), value: launcher.setupFacts.frameGeneration}
                            ]
                            delegate: Item {
                                width: parent.width; height: Math.max(18, factLabel.implicitHeight, factValue.implicitHeight) + 4
                                Rectangle { visible: index > 0; width: parent.width; height: 1; color: "#28374048" }
                                Text { id: factLabel; anchors.verticalCenter: parent.verticalCenter; width: parent.width * 0.46; text: modelData.label; color: Theme.textDim; font.family: Theme.serif; font.pixelSize: 16; wrapMode: Text.WordWrap }
                                Text { id: factValue; anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter; width: parent.width * 0.52; text: modelData.value; color: Theme.text; font.family: Theme.serif; font.pixelSize: 17; font.weight: Font.Medium; horizontalAlignment: Text.AlignRight; wrapMode: Text.WordWrap }
                            }
                        }
                    }
                    Rectangle { width: parent.width; height: 1; color: Theme.lineStrong }
                    Text { width: parent.width; text: launcher.saveStatus; color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 12; wrapMode: Text.WordWrap }
                }
            }
            Item {
                width: parent.width; height: connectionFields.implicitHeight + 16
                Column {
                    id: connectionFields; x: 16; y: 6; width: parent.width - 32; spacing: 4
            FieldRow {
                width: parent.width; compact: true; minimumHeight: 54; serifLabel: true
                showDivider: true
                field: launcher.settingsRevision < 0 ? ({}) : launcher.sectionFields("Co-op", "Seamless co-op").find(f => f.key === "coop_name")
            }
            CoopConnection {
                width: parent.width; compact: true; serifLabels: true; showPlayerName: false; visible: launcher.playMode === "coop"
                onAttentionRequested: (target) => {
                    if (!home.visible) return
                    homeScroll.contentY = Math.max(0, Math.min(target.mapToItem(content, 0, 0).y - 24, homeScroll.contentHeight - homeScroll.height))
                }
            }
                }
            }
            Text {
                x: 18; width: parent.width - 36; visible: home.gameBlocked || home.savesBlocked || launcher.setupRunning
                text: home.gameBlocked ? launcher.tr("Choose your game folder or download the game.") : home.savesBlocked ? launcher.tr("The saves folder cannot be written. Choose another one.") : launcher.gameDownloadStatus
                color: Theme.warn; font.family: Theme.sans; font.pixelSize: 12; wrapMode: Text.WordWrap
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
            width: 296; height: 56; serif: true; highlighted: !launcher.running && !launcher.coopBusy
            text: launcher.running || launcher.coopLaunchPending ? launcher.tr("Cancel launch") : launcher.tr("Play")
            enabled: launcher.running || launcher.coopLaunchPending || (!launcher.coopBusy && !launcher.setupRunning && !home.gameBlocked && !home.savesBlocked && !home.onlineBlocked)
            onClicked: launcher.running || launcher.coopLaunchPending ? launcher.cancelLaunch() : home.primaryRequested()
        }
        Text {
            y: 122; width: parent.width; wrapMode: Text.WordWrap; maximumLineCount: 3; elide: Text.ElideRight
            text: launcher.notice !== launcher.tr("Ready to hunt.") ? launcher.notice : launcher.playMode === "coop" ? launcher.coopStatus : ""
            color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 12; horizontalAlignment: Text.AlignHCenter
        }
    }
}
