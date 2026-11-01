import QtQuick
import QtQuick.Controls

Item {
    id: wizard
    objectName: "setupWizard"
    property int step: 0
    property int startStep: 0
    property var checks: launcher.readiness
    property bool gameValid: checks[0].level !== "error"
    property bool savesValid: checks[2].level !== "error" && launcher.savesWritable
    signal exitRequested(string page)
    onVisibleChanged: if (visible) step = 0
    function finish() { launcher.completeSetup(); wizard.exitRequested("Home") }
    Text { text: launcher.tr("FIRST-TIME SETUP"); color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 13 }
    Text { y: 36; width: parent.width; text: [launcher.tr("Game files & saves"), launcher.tr("Co-op"), launcher.tr("Finish setup")][wizard.step]; color: Theme.text; font.family: Theme.serif; font.pixelSize: 36; wrapMode: Text.WordWrap }
    Row {
        y: 110; width: parent.width; spacing: 8
        Repeater { model: 3; delegate: Rectangle { width: (wizard.width - 16) / 3; height: 3; color: index <= wizard.step ? Theme.accent : Theme.lineStrong } }
    }
    Flickable {
        id: scroll
        y: 138; width: parent.width; height: parent.height - y - 90
        clip: true; boundsBehavior: Flickable.StopAtBounds
        contentHeight: (wizard.step === 0 ? files.implicitHeight : wizard.step === 1 ? coopStep.implicitHeight : finishStep.implicitHeight) + 20
        ScrollBar.vertical: ScrollBar {}
        Column {
            id: files; width: parent.width - 12; spacing: 14; visible: wizard.step === 0
            Note { text: launcher.tr("Choose your game folder or download the game. You can change both paths below.") }
            Repeater { model: launcher.sectionFields("Game & Saves", "Game files"); delegate: FieldRow { width: files.width; field: modelData } }
            GameDownload { width: parent.width }
            Repeater {
                model: [wizard.checks[0], wizard.checks[2]]
                delegate: Note { text: (modelData.level === "error" ? "●  " : "✓  ") + modelData.detail; color: modelData.level === "error" ? Theme.warn : Theme.good }
            }
        }
        Column {
            id: coopStep; width: parent.width - 12; spacing: 12; visible: wizard.step === 1
            Note { text: launcher.tr("Optional. You can set up co-op later in Settings.") }
            CoopConnection { width: parent.width; onAttentionRequested: (target) => { if (wizard.visible && wizard.step === 1) scroll.contentY = Math.max(0, Math.min(target.mapToItem(coopStep, 0, 0).y - 24, scroll.contentHeight - scroll.height)) } }
        }
        Column {
            id: finishStep; width: parent.width - 12; spacing: 20; visible: wizard.step === 2
            Note { text: launcher.tr("Choose a graphics preset. You can change it later.") }
            Flow {
                width: parent.width; spacing: 8
                Repeater { model: ["low", "balanced", "high", "ultra"]; delegate: GlassButton {
                    width: (finishStep.width - 24) / 4; height: 48; text: launcher.presetLabel(modelData) + (launcher.recommendedPreset === modelData ? " ★" : "")
                    highlighted: launcher.graphicsPreset === modelData; onClicked: launcher.applyGraphicsPreset(modelData)
                } }
            }
            Note { text: launcher.presetDescription(launcher.graphicsPreset) }
            GlassButton { text: launcher.tr("Add desktop shortcut"); width: 180; onClicked: launcher.createShortcut() }
            Note { text: launcher.tr("The shortcut will be named Bloodborne.") }
            Note { text: launcher.notice === launcher.tr("Ready to hunt.") ? "" : launcher.notice }
        }
    }
    Rectangle { y: parent.height - 76; width: parent.width; height: 1; color: Theme.line }
    Item {
        y: parent.height - 60; width: parent.width; height: 48
        GlassButton { anchors.left: parent.left; visible: wizard.step > 0; text: launcher.tr("Back"); onClicked: { wizard.step--; scroll.contentY = 0 } }
        GlassButton { anchors.left: parent.left; visible: wizard.step === 0; text: launcher.tr("Skip for now"); enabled: !launcher.setupRunning; onClicked: { launcher.skipSetup(); wizard.exitRequested("Home") } }
        GlassButton {
            anchors.right: parent.right
            text: wizard.step === 2 ? launcher.tr("Finish") : launcher.tr("Continue"); highlighted: true
            enabled: !launcher.setupRunning && (wizard.step === 1 || (wizard.gameValid && wizard.savesValid))
            onClicked: { if (wizard.step === 2) wizard.finish(); else wizard.step++; scroll.contentY = 0 }
        }
    }
}
