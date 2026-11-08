import QtQuick
import QtQuick.Controls

Item {
    id: page
    objectName: "trophiesPage"
    readonly property var entries: launcher.trophyEntries
    readonly property var selected: entries[trophyList.currentIndex] || null

    function trophyName(entry) {
        if (entry.secret) return launcher.tr("Secret trophy")
        return entry.name || launcher.tr("Trophy #%1").arg(entry.id)
    }
    function statusText(entry) {
        if (entry.status === "earned") return launcher.tr("Earned")
        if (entry.status === "unknown") return launcher.tr("Progress unavailable")
        return launcher.tr("Not earned")
    }

    Rectangle { anchors.fill: parent; color: Theme.base }
    Image {
        anchors.fill: parent; source: Qt.resolvedUrl("../assets/ui/home-background.png")
        fillMode: Image.PreserveAspectCrop; horizontalAlignment: Image.AlignRight; asynchronous: true
    }
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0; color: Theme.base }
            GradientStop { position: 0.4; color: "#f00b0d10" }
            GradientStop { position: 1; color: "#cd0b0d10" }
        }
    }

    Column {
        id: header
        anchors { left: parent.left; leftMargin: Theme.railWidth + 38; right: parent.right; rightMargin: 38; top: parent.top; topMargin: 28 }
        spacing: 12
        Text {
            text: launcher.tr("Trophies"); color: Theme.text
            font.family: Theme.serif; font.pixelSize: 32
        }
        Rectangle { width: 36; height: 3; radius: 1.5; color: Theme.accentHover }
        TrophyProgress {
            objectName: "pageTrophyProgress"
            width: parent.width; label: launcher.profileSummary; showIcon: false
        }
        Text {
            objectName: "trophyMetadataHint"
            width: parent.width; visible: !launcher.trophyHasMetadata && page.entries.length > 0
            text: launcher.tr("Names and descriptions are unavailable for this trophy pack.")
            color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 12; wrapMode: Text.WordWrap
        }
    }

    Text {
        anchors { top: header.bottom; topMargin: 28; left: header.left; right: header.right }
        visible: page.entries.length === 0
        text: launcher.tr("No trophies loaded yet. Launch the game to load the trophy list.")
        color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 14; wrapMode: Text.WordWrap
    }

    Row {
        id: columns
        anchors { top: header.bottom; topMargin: 22; left: header.left; right: header.right; bottom: parent.bottom; bottomMargin: 28 }
        visible: page.entries.length > 0
        spacing: 24
        ListView {
            id: trophyList
            objectName: "trophyList"
            width: Math.round((columns.width - columns.spacing) * 0.54); height: columns.height
            clip: true; boundsBehavior: Flickable.StopAtBounds
            model: page.entries
            keyNavigationEnabled: true; activeFocusOnTab: true
            ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }

            delegate: Button {
                id: trophyRow
                required property var modelData
                required property int index
                objectName: "trophyRow" + modelData.id
                width: trophyList.width - 10
                height: Math.max(54, nameLabel.implicitHeight + 16, statusLabel.implicitHeight + 16)
                padding: 0; hoverEnabled: true; focusPolicy: Qt.NoFocus
                text: page.trophyName(modelData)
                Accessible.name: text + ", " + statusLabel.text
                Accessible.selected: ListView.isCurrentItem
                onClicked: {
                    trophyList.currentIndex = index
                    trophyList.forceActiveFocus()
                }
                background: Rectangle {
                    color: trophyRow.ListView.isCurrentItem ? Theme.accentSoft : trophyRow.hovered ? Theme.surfaceHover : "transparent"
                    Rectangle {
                        visible: trophyRow.ListView.isCurrentItem
                        width: 2; height: parent.height; color: Theme.accentHover
                    }
                    Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: Theme.lineStrong }
                }
                contentItem: Item {
                    Rectangle {
                        id: thumbnail
                        x: 10; anchors.verticalCenter: parent.verticalCenter
                        width: 36; height: 36; radius: 3; color: Theme.surface
                        Image {
                            id: thumbnailArt
                            anchors.fill: parent; source: trophyRow.modelData.icon
                            sourceSize.width: 72; sourceSize.height: 72; asynchronous: true
                            fillMode: Image.PreserveAspectFit
                        }
                        NavIcon {
                            anchors.centerIn: parent; width: 18; height: 18
                            visible: thumbnailArt.status !== Image.Ready
                            kind: trophyRow.modelData.secret ? "lock" : "trophy"; strokeColor: Theme.textDim
                        }
                    }
                    Text {
                        id: nameLabel
                        anchors { left: thumbnail.right; leftMargin: 10; right: statusLabel.left; rightMargin: 10; verticalCenter: parent.verticalCenter }
                        text: trophyRow.text; color: Theme.text; textFormat: Text.PlainText
                        font.family: Theme.serif; font.pixelSize: 18; wrapMode: Text.Wrap
                    }
                    Text {
                        id: statusLabel
                        anchors { right: parent.right; rightMargin: 10; verticalCenter: parent.verticalCenter }
                        width: Math.min(implicitWidth, parent.width * 0.34)
                        text: page.statusText(trophyRow.modelData)
                        color: trophyRow.modelData.status === "earned" ? Theme.good : Theme.textDim
                        font.family: Theme.sans; font.pixelSize: 12
                        horizontalAlignment: Text.AlignRight; wrapMode: Text.WordWrap
                    }
                }
            }
        }

        Rectangle {
            width: columns.width - trophyList.width - columns.spacing; height: columns.height
            visible: page.selected !== null
            radius: Theme.radius; color: Theme.panel; border.color: Theme.lineStrong
            Flickable {
                id: detailScroll
                anchors.fill: parent; anchors.margins: 20
                clip: true; contentHeight: detail.implicitHeight; boundsBehavior: Flickable.StopAtBounds
                ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
                Connections {
                    target: page
                    function onSelectedChanged() { detailScroll.contentY = 0 }
                }
                Column {
                    id: detail
                    width: parent.width - 10; spacing: 10
                    Rectangle {
                        width: 140; height: 140; radius: 4; color: Theme.surface
                        Image {
                            id: detailArt
                            objectName: "trophyDetailArt"
                            anchors.fill: parent; source: page.selected ? page.selected.icon : ""
                            asynchronous: true; fillMode: Image.PreserveAspectFit
                        }
                        NavIcon {
                            anchors.centerIn: parent; width: 38; height: 38
                            visible: detailArt.status !== Image.Ready
                            kind: page.selected && page.selected.secret ? "lock" : "trophy"; strokeColor: Theme.textDim
                        }
                    }
                    Text {
                        objectName: "trophyDetailStatus"
                        width: parent.width; wrapMode: Text.WordWrap
                        text: {
                            if (!page.selected) return ""
                            const status = page.statusText(page.selected)
                            const when = page.selected.unlockedAt
                            return when > 0 ? status + "  ·  " + Qt.formatDateTime(new Date(when * 1000),
                                launcher.russian ? "dd.MM.yyyy" : "MMM d, yyyy") : status
                        }
                        color: page.selected && page.selected.status === "earned" ? Theme.good : Theme.textDim
                        font.family: Theme.sans; font.pixelSize: 13
                    }
                    Text {
                        objectName: "trophyDetailTitle"
                        width: parent.width; text: page.selected ? page.trophyName(page.selected) : ""
                        wrapMode: Text.Wrap; textFormat: Text.PlainText
                        color: Theme.text; font.family: Theme.serif; font.pixelSize: 28
                    }
                    Text {
                        objectName: "trophyDetailDescription"
                        width: parent.width; wrapMode: Text.Wrap; textFormat: Text.PlainText
                        text: !page.selected ? "" : page.selected.secret
                            ? launcher.tr("The name and requirement are revealed when this trophy is earned.")
                            : page.selected.description || launcher.tr("Description unavailable.")
                        color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 14
                    }
                }
            }
        }
    }
}
