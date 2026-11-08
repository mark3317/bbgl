import QtQuick
import QtQuick.Controls

// Settings: the categories (and search) on the left, the chosen category on the right: its art,
// its sections as tabs, then the settings of that section. Changes save as they are made.
Item {
    id: workspace
    objectName: "settingsWorkspace"
    signal backToLauncher()
    signal openSetup(int step)
    signal openMods(string section, string key)
    property string category: "Visuals"
    property string section: ""
    property string targetKey: ""
    property string query: ""
    function sections() { return launcher.categorySections(category).filter(s => s !== "Join a host") }
    property var categories: [
        {name: "Visuals", icon: "visuals", detail: launcher.tr("Graphics, display & frame rate")},
        {name: "Controls", icon: "controls", detail: launcher.tr("Prompts, mouse & keyboard")},
        {name: "Game & Saves", icon: "folder", detail: launcher.tr("Game files, saves & language")},
        {name: "Co-op", icon: "online", detail: launcher.tr("Play with friends")},
        {name: "Mods & Patches", icon: "puzzle", detail: launcher.tr("Mods, enhancements & tweaks")},
        {name: "System", icon: "system", detail: launcher.tr("Startup, updates & diagnostics")}
    ]
    property var current: categories.find(c => c.name === category) || categories[0]
    property real listWidth: width < 1200 ? 262 : 300

    function openAt(nextCategory, nextSection, nextKey) {
        category = nextCategory || category || "Visuals"
        section = nextSection === "Your data" ? "Game files" : nextSection === "Host a session" || nextSection === "Join a host" ? "Seamless co-op" : nextSection || launcher.categorySections(category)[0]
        targetKey = nextKey || ""
        search.text = ""
        detailScroll.contentY = 0
        if (targetKey !== "") Qt.callLater(focusTarget)
    }
    function focusTarget() {
        for (var i = 0; i < fieldRepeater.count; i++) {
            var row = fieldRepeater.itemAt(i)
            if (row && row.settingKey === targetKey) {
                detailScroll.contentY = Math.max(0, row.y - 20)
                break
            }
        }
    }
    function is(cat, sec) { return workspace.category === cat && workspace.section === sec }

    Rectangle { anchors.fill: parent; color: Theme.base }

    // --- The category's art, behind the right side's header -----------------------------------
    Item {
        anchors.fill: parent; clip: true
        Image {
            anchors.fill: parent
            source: Qt.resolvedUrl("../assets/ui/settings-background.png")
            fillMode: Image.PreserveAspectCrop; horizontalAlignment: Image.AlignRight; verticalAlignment: Image.AlignVCenter
            smooth: true; asynchronous: true; opacity: 1
        }
        Rectangle {
            anchors.fill: parent
            gradient: Gradient { orientation: Gradient.Horizontal
                GradientStop { position: 0; color: "#e80b0d10" }
                GradientStop { position: 0.45; color: "#d00b0d10" }
                GradientStop { position: 1; color: "#900b0d10" }
            }
        }
        Rectangle {
            anchors.fill: parent
            gradient: Gradient { GradientStop { position: 0.35; color: "#000b0d10" } GradientStop { position: 1; color: "#a00b0d10" } }
        }
    }

    // --- Categories ---------------------------------------------------------------------------
    Rectangle {
        x: Theme.railWidth; width: listWidth; height: parent.height
        color: "#c00e1115"
        Rectangle { anchors.right: parent.right; width: 1; height: parent.height; color: Theme.line }
        Column {
            x: 28; y: 34; width: parent.width - 56; spacing: 0
            Item {
                width: parent.width; height: 40
                Row {
                    anchors.verticalCenter: parent.verticalCenter; spacing: 12


                    Text { text: launcher.tr("SETTINGS"); color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 12; font.letterSpacing: 2 }
                }
            }
            Rectangle { width: parent.width; height: 1; color: Theme.line }
            Item { width: 1; height: 22 }
            GlassTextField {
                id: search; width: parent.width; height: 40; leftPadding: 40
                placeholderText: launcher.tr("Find a setting")
                onTextChanged: workspace.query = text
                NavIcon { x: 13; anchors.verticalCenter: parent.verticalCenter; width: 17; height: 17; kind: "search"; strokeColor: Theme.textDim }
            }
            Item { width: 1; height: 18 }
            Column {
                width: parent.width; spacing: 6
                Repeater {
                    model: workspace.categories
                    delegate: Rectangle {
                        width: parent.width; height: Math.max(58, categoryLabels.implicitHeight + 12); radius: Theme.radius
                        property bool active: workspace.query === "" && workspace.category === modelData.name
                        color: active || hit.containsMouse ? "#16191d" : "transparent"
                        border.color: active ? Theme.accent : hit.containsMouse ? Theme.line : "transparent"
                        border.width: active ? 1.5 : 1
                        NavIcon { x: 16; anchors.verticalCenter: parent.verticalCenter; width: 22; height: 22; kind: modelData.icon; strokeColor: active ? Theme.text : "#bdb8b0" }
                        Column {
                            id: categoryLabels
                            x: 54; anchors.verticalCenter: parent.verticalCenter; width: parent.width - 70; spacing: 2
                            Text { width: parent.width; text: launcher.tr(modelData.name); color: Theme.text; font.family: Theme.serif; font.pixelSize: 17; wrapMode: Text.WordWrap }
                            Text { width: parent.width; text: modelData.detail; color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 12; wrapMode: Text.WordWrap }
                        }
                        MouseArea { id: hit; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: workspace.openAt(modelData.name, "", "") }
                    }
                }
            }
        }
        Text {
            x: 28; width: parent.width - 56; anchors.bottom: parent.bottom; anchors.bottomMargin: 22
            text: launcher.tr("Changes save as you make them. Some take effect the next time the game starts.")
            color: Theme.textFaint; font.family: Theme.sans; font.pixelSize: 11; wrapMode: Text.WordWrap; lineHeight: 1.3
        }
    }

    // --- The chosen category ------------------------------------------------------------------
    Item {
        id: content
        x: Theme.railWidth + listWidth + 48; y: 0
        width: Math.min(860, parent.width - x - 48); height: parent.height

        // Search results replace the category while there is a query.
        Column {
            visible: workspace.query !== ""
            y: 44; width: parent.width; spacing: 10
            Text { text: launcher.tr("Results"); color: Theme.text; font.family: Theme.serif; font.pixelSize: 36 }
            Text {
                property var hits: launcher.settingsRevision < 0 ? [] : launcher.searchSettings(workspace.query)
                width: parent.width; wrapMode: Text.Wrap
                visible: hits.length === 0; text: launcher.tr("Nothing matches “") + workspace.query + "”."
                color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 13
            }
            Item { width: 1; height: 8 }
            Repeater {
                model: launcher.settingsRevision < 0 || workspace.query === "" ? [] : launcher.searchSettings(workspace.query)
                delegate: MenuRow {
                    width: content.width; label: modelData.label; value: launcher.tr(modelData.category) + "  ›  " + launcher.tr(modelData.section)
                    onClicked: {
                        if (modelData.category === "Mods") workspace.openMods(modelData.section, modelData.key)
                        else workspace.openAt(modelData.category, modelData.section, modelData.key)
                    }
                }
            }
        }

        Column {
            id: header
            visible: workspace.query === ""
            y: 44; width: parent.width; spacing: 6
            Text { width: parent.width; wrapMode: Text.WordWrap; text: launcher.tr(workspace.category); color: Theme.text; font.family: Theme.serif; font.pixelSize: 42 }
            Text { width: parent.width; wrapMode: Text.WordWrap; text: workspace.current.detail; color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 14 }
            Item { width: 1; height: 22 }
            // Sections as tabs: the selected one is underlined in crimson.
            Flow {
                width: parent.width; spacing: 16
                Repeater {
                    model: workspace.sections()
                    delegate: Item {
                        width: tabText.implicitWidth; height: 34
                        property bool active: workspace.section === modelData
                        Text {
                            id: tabText; text: launcher.tr(modelData); anchors.top: parent.top
                            color: active ? Theme.text : tabHit.containsMouse ? "#d6d1c9" : Theme.textDim
                            font.family: Theme.sans; font.pixelSize: 14
                        }
                        Rectangle { visible: active; anchors.bottom: parent.bottom; width: parent.width; height: 2; color: Theme.accent }
                        MouseArea { id: tabHit; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                            onClicked: { workspace.section = modelData; detailScroll.contentY = 0 } }
                    }
                }
            }
            Rectangle { width: parent.width; height: 1; color: Theme.line }
        }

        // Presets stay above the scrolling fields on the two graphics tabs.
        Item {
            id: presetHeader
            objectName: "graphicsPresetHeader"
            visible: workspace.query === "" && (is("Visuals", "Display & frame rate") || is("Visuals", "Image effects"))
            y: header.y + header.height + 4
            width: parent.width - 14; height: visible ? presetBox.height + 26 : 0
            GraphicsPresetPicker { id: presetBox; y: 18; width: parent.width }
            Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: Theme.line }
        }

        Flickable {
            id: detailScroll
            objectName: "settingsDetailScroll"
            visible: workspace.query === ""
            y: presetHeader.y + presetHeader.height; width: parent.width; height: parent.height - y
            clip: true; boundsBehavior: Flickable.StopAtBounds
            contentHeight: detailColumn.implicitHeight + 40
            ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
            Column {
                id: detailColumn
                width: detailScroll.width - 14; spacing: 0

                Repeater {
                    id: fieldRepeater
                    // settingsRevision: rebuilt after a preset rewrites several rows.
                    model: launcher.settingsRevision < 0 || is("Co-op", "Seamless co-op") ? [] : launcher.sectionFields(workspace.category, workspace.section)
                    delegate: FieldRow { width: detailColumn.width; field: modelData }
                }

                // Actions beside the task that calls for them.
                Column {
                    width: parent.width; spacing: 12; topPadding: 20
                    ControlIconsPicker { width: parent.width; visible: is("Controls", "Button prompts") }
                    FsrAssets { width: parent.width; visible: is("Visuals", "Upscaling") }
                    Loader {
                        width: parent.width; active: workspace.visible && is("System", "Trophy notifications")
                        visible: active
                        sourceComponent: TrophyNotifications {}
                    }
                    Repeater {
                        model: is("Game & Saves", "Game files") ? [launcher.readiness[0], launcher.readiness[2]] : []
                        delegate: Note { text: modelData.detail; color: modelData.level === "error" ? Theme.warn : Theme.textDim }
                    }
                    GameDownload { width: parent.width; visible: is("Game & Saves", "Game files"); showDownloadButton: false }
                    Flow { visible: is("Game & Saves", "Game files"); width: parent.width; spacing: 10
                        GlassButton { text: launcher.tr("Open saves folder"); width: 180; onClicked: launcher.action("openSaves") }
                        GlassButton { text: launcher.tr("Download game"); enabled: !launcher.setupRunning && !launcher.running && launcher.readiness[0].level === "error"; onClicked: launcher.downloadGame() }
                        GlassButton { text: launcher.tr("Setup wizard"); width: 180; onClicked: workspace.openSetup(0) }
                    }
                    CoopConnection {
                        width: parent.width; visible: is("Co-op", "Seamless co-op")
                        onAttentionRequested: (target) => { if (workspace.visible) detailScroll.contentY = Math.max(0, Math.min(target.mapToItem(detailColumn, 0, 0).y - 24, detailScroll.contentHeight - detailScroll.height)) }
                    }
                    Flow { width: parent.width; visible: is("Mods & Patches", "Mod settings"); spacing: 10
                        GlassButton { text: launcher.tr("Open mods folder"); width: 180; height: 48; onClicked: launcher.action("openMods") }
                    }
                    Note { visible: is("Mods & Patches", "Mod settings") && launcher.patches.length > 0; text: launcher.tr("External patches") }
                    Repeater { model: is("Mods & Patches", "Mod settings") ? launcher.patches : []
                        delegate: GlassSwitch { text: modelData.name; checked: modelData.enabled; onToggled: launcher.setPatch(modelData.name, checked) }
                    }
                    Column { visible: is("System", "System"); width: parent.width; spacing: 14
                        Flow { width: parent.width; spacing: 10
                            GlassButton { text: launcher.tr("Desktop shortcut"); width: 180; height: 48; onClicked: launcher.createShortcut() }
                            GlassButton { text: launcher.tr("Open launcher folder"); width: 180; height: 48; onClicked: launcher.action("openPort") }
                            GlassButton { text: launcher.tr("Profile folder"); width: 180; height: 48; onClicked: launcher.action("openProfile") }
                        }
                        Note { text: launcher.tr("Current profile:") + " " + launcher.activeProfileFolder }
                    }
                    Column { visible: is("System", "System"); width: parent.width; spacing: 14
                        ToggleRow { label: launcher.tr("Check for updates"); hint: launcher.tr("Checks for new launcher versions at startup."); checked: launcher.checked("check_updates"); onToggled: (on) => launcher.setValue("check_updates", on) }
                        Flow { width: parent.width; spacing: 10
                            GlassButton { visible: launcher.hasUpdate; highlighted: true; text: launcher.tr("Install the new version"); width: 180; height: 48; onClicked: launcher.installUpdate() }
                            GlassButton { text: launcher.tr("Check now"); width: 180; height: 48; onClicked: launcher.checkForUpdates(true) }
                            GlassButton { text: launcher.tr("Releases ↗"); width: 180; height: 48; onClicked: launcher.action("releases") }
                        }
                    }
                    Flow { width: parent.width; visible: is("System", "Advanced system"); spacing: 10
                        GlassButton { text: launcher.tr("Clear shader cache"); width: 180; height: 48; onClicked: launcher.action("clearCache") }
                        GlassButton { text: launcher.tr("Setup wizard"); width: 180; height: 48; onClicked: workspace.openSetup(0) }
                    }
                    Flow { width: parent.width; visible: is("System", "Logs"); spacing: 10
                        GlassButton { text: launcher.tr("Copy log"); width: 180; height: 48; onClicked: launcher.action("copyLog") }
                        GlassButton { text: launcher.tr("Clear log"); width: 180; height: 48; onClicked: launcher.action("clearLog") }
                    }
                    TextArea {
                        visible: is("System", "Logs")
                        width: detailColumn.width; height: visible ? 380 : 0; readOnly: true
                        wrapMode: TextEdit.NoWrap; text: visible ? launcher.log : ""; color: Theme.text; selectByMouse: true
                        font.family: "Cascadia Mono"; font.pixelSize: 12
                        background: Rectangle { color: "#0f1216"; radius: Theme.radius; border.color: Theme.line }
                    }
                }
            }
        }
    }
}
