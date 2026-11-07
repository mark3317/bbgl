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
    readonly property real contentWidth: panelWidth - 88
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
        x: Theme.railWidth + 44; y: 32; width: home.contentWidth + 24
        height: Math.max(0, launchActions.y - y - 24)
        clip: true; contentHeight: content.implicitHeight
        boundsBehavior: Flickable.StopAtBounds
        ScrollBar.vertical: ScrollBar {
            policy: homeScroll.contentHeight > homeScroll.height + 1 ? ScrollBar.AsNeeded : ScrollBar.AlwaysOff
            active: homeScroll.contentHeight > homeScroll.height + 1
            width: 4; padding: 0
            contentItem: Rectangle { implicitWidth: 4; implicitHeight: 24; radius: 2; color: Theme.textFaint }
            background: Item {}
        }
        Column {
            id: content; width: home.contentWidth; spacing: 16
            Text { width: parent.width; text: "Bloodborne Game Launcher"; color: Theme.text; font.family: Theme.serif; font.pixelSize: 32; wrapMode: Text.WordWrap }
            Rectangle { width: 36; height: 3; radius: 1.5; color: Theme.accentHover }
            Item {
                width: parent.width; height: summary.implicitHeight + 28
                Column {
                    id: summary; x: 18; y: 14; width: parent.width - 36; spacing: 10
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
                                width: parent.width; height: Math.max(18, factLabel.implicitHeight, factValue.implicitHeight) + 6
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
                width: parent.width; height: connectionFields.implicitHeight + 24
                visible: launcher.playMode === "coop"
                Column {
                    id: connectionFields; x: 18; y: 12; width: parent.width - 36; spacing: 0
                    FieldRow {
                        width: parent.width; compact: true; minimumHeight: 56; serifLabel: true
                        field: launcher.settingsRevision < 0 ? ({}) : launcher.sectionFields("Co-op", "Seamless co-op").find(f => f.key === "coop_name")
                    }
                    CoopConnection {
                        width: parent.width; compact: true; serifLabels: true; showPlayerName: false; showStatus: false
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
        }
    }
    Column {
        id: launchActions
        x: Theme.railWidth + 44; width: home.contentWidth
        anchors.bottom: parent.bottom; anchors.bottomMargin: 24; spacing: 12
        Item {
            id: modeSwitch
            anchors.horizontalCenter: parent.horizontalCenter; width: Math.min(320, parent.width); height: 44
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
            objectName: "playButton"
            anchors.horizontalCenter: parent.horizontalCenter
            width: modeSwitch.width; height: 56; serif: true; highlighted: !launcher.running && !launcher.coopBusy
            text: launcher.running || launcher.coopLaunchPending ? launcher.tr("Cancel launch") : launcher.tr("Play")
            enabled: launcher.running || launcher.coopLaunchPending || (!launcher.coopBusy && !launcher.setupRunning && !home.gameBlocked && !home.savesBlocked && !home.onlineBlocked)
            onClicked: launcher.running || launcher.coopLaunchPending ? launcher.cancelLaunch() : home.primaryRequested()
        }
        // Reserve space for the status so updates never move the launch controls.
        Flickable {
            id: noticeArea
            width: parent.width; height: 42
            contentWidth: width; contentHeight: noticeText.implicitHeight
            clip: true; boundsBehavior: Flickable.StopAtBounds
            flickableDirection: Flickable.VerticalFlick
            interactive: contentHeight > height
            ScrollBar.vertical: ScrollBar {
                visible: noticeArea.interactive
                active: noticeArea.interactive
                width: 4; padding: 0
                contentItem: Rectangle { implicitWidth: 4; implicitHeight: 24; radius: 2; color: Theme.textFaint }
                background: Item {}
            }
            Text {
                id: noticeText
                x: 8; width: noticeArea.width - 16; wrapMode: Text.Wrap
                text: launcher.notice !== launcher.tr("Ready to hunt.") ? launcher.notice : launcher.playMode === "coop" ? launcher.coopStatus : ""
                onTextChanged: noticeArea.contentY = 0
                color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 12; horizontalAlignment: Text.AlignHCenter
            }
        }
    }
}
