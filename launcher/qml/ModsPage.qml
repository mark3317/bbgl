import QtQuick
import QtQuick.Controls

Item {
    id: page
    objectName: "modsPage"
    signal openModSettings()
    property string section: "Installed mods"
    readonly property bool cheats: section === "Cheats"

    function openAt(nextSection, key) {
        section = nextSection === "Cheats" ? "Cheats" : "Installed mods"
        scroll.cancelFlick()
        scroll.contentY = 0
        if (cheats && key) Qt.callLater(() => revealCheat(key))
    }

    function revealCheat(key) {
        if (!visible || !cheats) return
        for (let i = 0; i < cheatFields.count; i++) {
            const row = cheatFields.itemAt(i)
            if (row && row.settingKey === key) {
                const y = row.mapToItem(details, 0, 0).y
                scroll.contentY = Math.max(0, Math.min(y - 20, scroll.contentHeight - scroll.height))
                return
            }
        }
    }

    Rectangle { anchors.fill: parent; color: Theme.base }
    Image {
        anchors.fill: parent; source: Qt.resolvedUrl("../assets/ui/settings-background.png")
        fillMode: Image.PreserveAspectCrop; horizontalAlignment: Image.AlignRight; asynchronous: true
    }
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0; color: Theme.base }
            GradientStop { position: 0.72; color: "#ef0b0d10" }
            GradientStop { position: 1; color: "#a00b0d10" }
        }
    }

    Column {
        id: header
        x: Theme.railWidth + 38; y: 28
        width: Math.min(960, page.width - x - 38); spacing: 12
        Text { text: launcher.tr("Mods"); color: Theme.text; font.family: Theme.serif; font.pixelSize: 32 }
        Rectangle { width: 36; height: 3; radius: 1.5; color: Theme.accentHover }
        Item {
            width: parent.width; height: 42
            Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: Theme.line }
            Row {
                spacing: 24
                Repeater {
                    model: ["Installed mods", "Cheats"]
                    delegate: Button {
                        id: tab
                        required property string modelData
                        readonly property bool selected: page.section === modelData
                        objectName: modelData === "Cheats" ? "cheatsTab" : "installedModsTab"
                        text: launcher.tr(modelData)
                        width: label.implicitWidth + 16; height: 42; padding: 0
                        hoverEnabled: true
                        Accessible.selected: selected
                        contentItem: Text {
                            id: label
                            text: tab.text; color: tab.selected || tab.hovered || tab.visualFocus ? Theme.text : Theme.textDim
                            font.family: Theme.sans; font.pixelSize: 15
                            verticalAlignment: Text.AlignVCenter; horizontalAlignment: Text.AlignHCenter
                        }
                        background: Rectangle {
                            color: tab.visualFocus ? Theme.surfaceHover : "transparent"
                            Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 2; visible: tab.selected; color: Theme.accentHover }
                        }
                        onClicked: page.openAt(modelData)
                    }
                }
            }
        }
    }

    Flickable {
        id: scroll
        objectName: "modsScroll"
        anchors { left: header.left; right: header.right; top: header.bottom; topMargin: 22; bottom: parent.bottom; bottomMargin: 24 }
        contentWidth: width; contentHeight: details.implicitHeight
        clip: true; boundsBehavior: Flickable.StopAtBounds; flickableDirection: Flickable.VerticalFlick
        ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }

        Column {
            id: details
            width: scroll.width - 12; spacing: 14
            Column {
                width: parent.width; spacing: 14; visible: !page.cheats
                Item {
                    width: parent.width; height: Math.max(actions.height, modsSwitch.implicitHeight)
                    Row {
                        id: actions
                        anchors.verticalCenter: parent.verticalCenter; spacing: 10
                        GlassButton { text: launcher.tr("Open mods folder"); width: 180; height: 38; onClicked: launcher.action("openMods") }
                        GlassButton { objectName: "modsSettingsButton"; text: launcher.tr("Mod settings"); width: 180; height: 38; onClicked: page.openModSettings() }
                    }
                    GlassSwitch {
                        id: modsSwitch
                        objectName: "modsEnabledSwitch"
                        anchors.right: parent.right; anchors.rightMargin: 12; anchors.verticalCenter: parent.verticalCenter
                        text: launcher.tr("Enable mods")
                        enabled: !launcher.modsDownloading
                        checked: launcher.modsEnabled
                        onToggled: launcher.setValue("mods_enabled", checked)
                    }
                }
                ModsTable { width: parent.width; mods: visible ? launcher.modTableRows : [] }
                Note { text: launcher.tr("The mod list updates automatically. Changes apply at the next game start. Lower mods override earlier ones.") }
                Note { visible: launcher.contentMods.length === 0; text: launcher.tr("Put each mod in its own folder. Mods shared by players appear in this table automatically.") }
                Note { visible: launcher.modsDownloading; text: launcher.tr("Downloading mods… Please wait.") }
            }
            Note {
                visible: page.cheats
                text: launcher.tr("Optional gameplay changes. All are off by default and apply the next time the game starts.")
            }
            Repeater {
                id: cheatFields
                model: !page.visible || !page.cheats || launcher.settingsRevision < 0 ? [] : launcher.sectionFields("Mods", "Cheats")
                delegate: FieldRow { width: details.width; field: modelData }
            }
        }
    }
}
