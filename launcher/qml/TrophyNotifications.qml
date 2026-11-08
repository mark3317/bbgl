import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Column {
    id: page
    objectName: "trophyNotifications"
    spacing: 12
    readonly property var options: launcher.trophyNotifications
    readonly property bool modern: options.theme !== "original"
    readonly property var grades: ["bronze", "silver", "gold", "platinum"]
    readonly property var gradeLabels: ["Bronze", "Silver", "Gold", "Platinum"]
    property var previewGrades: [3]
    property int nextGrade: 0
    property string soundFiles: ""
    property int previewRevision: 0

    function refreshSounds() { soundFiles = launcher.trophySoundFiles() }
    function playPreview(kind) {
        sequence.stop()
        nextGrade = 0
        previewGrades = kind === 5 ? [0, 0, 0] : [kind === 4 ? 0 : kind]
        ++previewRevision
        if (kind === 4) { nextGrade = 1; sequence.start() }
    }
    Component.onCompleted: {
        launcher.refreshTrophyNotifications()
        refreshSounds()
    }
    Timer {
        id: sequence
        interval: page.options.hold_seconds > 0 ? page.options.hold_seconds * 1000 : 2000
        onTriggered: {
            page.previewGrades = [page.nextGrade++]
            ++page.previewRevision
            if (page.nextGrade < page.grades.length) restart()
        }
    }

    component SectionTitle: Text {
        color: Theme.text; font.family: Theme.serif; font.pixelSize: 20
        wrapMode: Text.WordWrap
    }
    component OptionSlider: Column {
        id: setting
        required property string optionKey
        required property string label
        property bool seconds: false
        property alias value: control.value
        spacing: 3
        Item {
            width: parent.width
            height: Math.max(labelText.implicitHeight, readout.implicitHeight)
            Text {
                id: labelText; width: parent.width - readout.width - 10
                text: setting.label; wrapMode: Text.WordWrap; color: Theme.text
                font.family: Theme.sans; font.pixelSize: 13
            }
            Text {
                id: readout; anchors.right: parent.right; color: Theme.textDim
                text: setting.seconds
                    ? control.value === 0 ? launcher.tr("Theme default")
                                          : launcher.tr("%1 s").arg(control.value.toLocaleString(Qt.locale(launcher.russian ? "ru_RU" : "en_US"), "f", 1))
                    : control.value + "%"
                font.family: Theme.sans; font.pixelSize: 12
            }
        }
        Slider {
            id: control
            objectName: setting.optionKey + "Slider"
            width: parent.width; from: 0; to: setting.seconds ? 20 : 100
            stepSize: setting.seconds ? .1 : 1
            value: page.options[setting.optionKey]
            Accessible.name: setting.label
            function saveValue() {
                if (Math.abs(value - page.options[setting.optionKey]) > .00001)
                    launcher.setTrophyNotification(setting.optionKey, Number(value.toFixed(1)))
            }
            onMoved: if (!pressed) saveValue()
            onPressedChanged: if (!pressed) saveValue()
            background: Rectangle {
                x: control.leftPadding; y: control.topPadding + (control.availableHeight - height) / 2
                width: control.availableWidth; height: 4; radius: 2; color: Theme.lineStrong
                Rectangle { width: control.visualPosition * parent.width; height: parent.height; radius: 2; color: control.enabled ? Theme.accent : Theme.textFaint }
            }
        }
    }

    Text {
        width: parent.width; text: launcher.tr("Trophy notifications")
        color: Theme.text; font.family: Theme.serif; font.pixelSize: 28; wrapMode: Text.WordWrap
    }
    Note { width: parent.width; text: launcher.tr("The launcher and in-game overlay share these settings for the current save profile.") }
    GridLayout {
        width: parent.width
        columns: width >= 570 ? 2 : 1
        columnSpacing: 22; rowSpacing: 14
        uniformCellWidths: true

        Column {
            Layout.fillWidth: true; Layout.minimumWidth: 0; Layout.alignment: Qt.AlignTop
            spacing: 8; enabled: !launcher.running
            SectionTitle { width: parent.width; text: launcher.tr("Appearance") }
            GlassComboBox {
                id: themeBox
                objectName: "trophyNotificationTheme"
                width: parent.width; textRole: "text"
                Accessible.name: launcher.tr("Notification style")
                model: [
                    {key: "original", text: launcher.tr("Original banner")},
                    {key: "card", text: launcher.tr("Card")},
                    {key: "card_cinematic", text: launcher.tr("Card, cinematic platinum")},
                    {key: "corner", text: launcher.tr("Corner popup")}
                ]
                currentIndex: model.findIndex(item => item.key === page.options.theme)
                onActivated: (index) => launcher.setTrophyNotification("theme", model[index].key)
            }
            OptionSlider {
                visible: page.options.theme === "card_cinematic"; width: parent.width
                optionKey: "cinematic_intensity"; label: launcher.tr("Platinum light")
            }
            GlassSwitch {
                visible: page.modern; text: launcher.tr("Animate the platinum")
                checked: page.options.platinum_animation
                onToggled: launcher.setTrophyNotification("platinum_animation", checked)
            }
            GlassSwitch {
                visible: page.modern; text: launcher.tr("Write the grade")
                checked: page.options.grade_label
                onToggled: launcher.setTrophyNotification("grade_label", checked)
            }
            Rectangle { width: parent.width; height: 1; color: Theme.lineStrong }
            SectionTitle { width: parent.width; text: launcher.tr("Sound and timing") }
            GlassSwitch {
                objectName: "trophyNotificationMuted"; text: launcher.tr("Mute the sound")
                checked: page.options.muted
                onToggled: launcher.setTrophyNotification("muted", checked)
            }
            OptionSlider {
                width: parent.width; enabled: !page.options.muted
                optionKey: "volume"; label: launcher.tr("Volume")
            }
            OptionSlider {
                width: parent.width; seconds: true
                optionKey: "hold_seconds"; label: launcher.tr("Time on screen")
            }
        }

        Column {
            Layout.fillWidth: true; Layout.minimumWidth: 0; Layout.alignment: Qt.AlignTop
            spacing: 8
            SectionTitle { width: parent.width; text: launcher.tr("Preview") }
            Rectangle {
                id: scene
                objectName: "trophyNotificationPreview"
                width: parent.width; height: Math.max(175, width * .54)
                color: Theme.base; clip: true
                Image {
                    anchors.fill: parent; source: Qt.resolvedUrl("../assets/ui/home-background.png")
                    fillMode: Image.PreserveAspectCrop; asynchronous: true
                }
                Rectangle { anchors.fill: parent; color: "#500b0d10" }
                Column {
                    id: toasts
                    width: page.options.theme === "original" ? parent.width - 16 : Math.min(238, parent.width - 16)
                    x: parent.width - width - 8
                    y: page.options.theme === "card" || page.options.theme === "card_cinematic"
                        ? 8 : parent.height - height - 8
                    spacing: 4
                    Repeater {
                        model: page.previewGrades
                        delegate: Rectangle {
                            id: toast
                            required property int modelData
                            readonly property var trophy: launcher.trophyEntries.find(
                                entry => entry.id === [14, 7, 5, 0][modelData])
                            readonly property string grade: page.options["name_" + page.grades[modelData]]
                                || launcher.tr(page.gradeLabels[modelData])
                            width: toasts.width; height: Math.max(43, caption.implicitHeight + 12)
                            radius: 4
                            color: page.options.theme === "original" ? "#23382c" : Theme.surface
                            border.color: page.options.theme === "card_cinematic" && modelData === 3
                                ? Qt.lighter(Theme.accent, 1 + page.options.cinematic_intensity / 70)
                                : Theme.lineStrong
                            NumberAnimation {
                                id: entrance; target: toast; property: "opacity"; from: .2; to: 1; duration: 330
                            }
                            Connections {
                                target: page
                                function onPreviewRevisionChanged() {
                                    if (toast.modelData !== 3 || !page.modern || page.options.platinum_animation)
                                        entrance.restart()
                                }
                            }
                            Image {
                                id: icon; x: 6; anchors.verticalCenter: parent.verticalCenter
                                width: 31; height: 31; source: toast.trophy ? toast.trophy.icon : ""
                                fillMode: Image.PreserveAspectFit
                            }
                            NavIcon {
                                anchors.centerIn: icon; kind: "trophy"; width: 19; height: 19
                                visible: icon.status !== Image.Ready; strokeColor: Theme.accentHover
                            }
                            Column {
                                id: caption; x: 43; width: parent.width - x - 7
                                anchors.verticalCenter: parent.verticalCenter
                                Text {
                                    width: parent.width; wrapMode: Text.Wrap; textFormat: Text.PlainText
                                    text: toast.trophy && toast.trophy.name || launcher.tr("Hunter's trophy")
                                    color: Theme.text; font.family: Theme.serif; font.pixelSize: 15
                                }
                                Text {
                                    width: parent.width; wrapMode: Text.Wrap; textFormat: Text.PlainText
                                    text: page.modern
                                        ? (page.options.grade_label ? toast.grade + "  ·  " : "") + (page.options.text_unlocked || launcher.tr("Trophy unlocked!"))
                                        : page.options.text_banner || launcher.tr("Achievement preview")
                                    color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 11
                                }
                            }
                        }
                    }
                }
            }
            Flow {
                width: parent.width; spacing: 6
                Repeater {
                    model: page.gradeLabels.concat(["All four in a row", "Three at once"])
                    GlassButton {
                        required property int index
                        required property string modelData
                        width: Math.max(67, contentItem.implicitWidth + 18); height: 36
                        text: launcher.tr(modelData)
                        onClicked: page.playPreview(index)
                    }
                }
            }
            Note { width: parent.width; text: launcher.tr("Visual preview. The game uses the selected sound and volume.") }
        }
    }
    Rectangle { width: parent.width; height: 1; color: Theme.lineStrong }
    SectionTitle { width: parent.width; text: launcher.tr("Custom sounds and pictures") }
    Note {
        width: parent.width
        text: launcher.tr("Files in the save profile's custom_trophy folder are loaded by the game.")
    }
    Note { width: parent.width; text: page.soundFiles || launcher.tr("No custom sound files found.") }
    GlassButton { text: launcher.tr("Refresh sound files"); height: 38; onClicked: page.refreshSounds() }
}
