import QtQuick
import QtQuick.Controls

// One setting: label and what it does on the left, its control on the right, a hairline below.
Item {
    id: fieldRow
    property var field: ({})
    property string settingKey: field.key || ""
    property bool compact: false
    property bool showDivider: true
    property bool hasHint: !compact && (field.hint || "") !== ""
    property bool isFolder: field.kind === "folder"
    property real controlWidth: Math.min(330, width * 0.44)
    property real minimumHeight: 62
    property real folderInputY: labels.y + labels.implicitHeight + 10
    implicitHeight: isFolder ? folderInputY + 48 + 16 : Math.max(minimumHeight, labels.implicitHeight + 28)
    height: implicitHeight

    Column {
        id: labels
        x: 2
        y: isFolder || hasHint ? 15 : (parent.height - height) / 2
        width: isFolder ? parent.width - 4 : parent.width - fieldRow.controlWidth - 28
        spacing: 3
        Text {
            width: parent.width; text: field.label || ""; color: Theme.text; wrapMode: Text.WordWrap
            font.family: Theme.sans; font.pixelSize: 14
        }
        Text {
            visible: hasHint; width: parent.width; text: field.hint || ""; color: Theme.textDim
            font.family: Theme.sans; font.pixelSize: 12; wrapMode: Text.WordWrap
        }
    }
    GlassSwitch {
        visible: field.kind === "toggle"
        anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter
        checked: launcher.checked(settingKey)
        onToggled: launcher.setValue(settingKey, checked)
    }
    GlassComboBox {
        visible: field.kind === "choice"
        anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter
        width: fieldRow.controlWidth; height: 38
        model: field.options || []
        textRole: "text"
        valueRole: "value"
        Component.onCompleted: currentIndex = indexOfValue(String(launcher.value(settingKey)))
        onActivated: launcher.setValue(settingKey, currentValue)
    }
    GlassTextField {
        id: editor
        Connections {
            target: launcher
            function onChanged() { if (!editor.activeFocus) editor.text = String(launcher.value(fieldRow.settingKey)) }
        }
        visible: field.kind !== "toggle" && field.kind !== "choice"
        x: isFolder ? 2 : parent.width - width
        y: isFolder ? folderInputY : (parent.height - height) / 2
        width: isFolder ? parent.width - 194 : fieldRow.controlWidth
        height: compact ? 40 : 48
        text: String(launcher.value(settingKey))
        placeholderText: isFolder ? launcher.tr("Default location") : ""
        echoMode: field.kind === "password" ? TextInput.Password : TextInput.Normal
        // Saved as it is typed or pasted: a page change destroys the field before it loses
        // focus, and a pasted co-op invite code was lost that way.
        onTextEdited: launcher.setValue(settingKey, text)
        onEditingFinished: launcher.setValue(settingKey, text)
    }
    GlassButton {
        visible: isFolder
        text: launcher.tr("Browse")
        anchors.right: parent.right; y: folderInputY; height: 48; width: 180
        onClicked: launcher.browse(settingKey)
    }
    Rectangle { visible: fieldRow.showDivider; anchors.bottom: parent.bottom; width: parent.width; height: 1; color: Theme.line }
}
