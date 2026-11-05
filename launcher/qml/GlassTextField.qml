import QtQuick
import QtQuick.Controls

TextField {
    id: control
    color: Theme.text
    placeholderTextColor: Theme.textFaint
    selectedTextColor: "#ffffff"
    selectionColor: "#287c8d"
    font.family: Theme.sans
    font.pixelSize: 13
    leftPadding: 12
    rightPadding: 12
    topPadding: 8
    bottomPadding: 8
    verticalAlignment: TextInput.AlignVCenter
    hoverEnabled: true
    background: Rectangle {
        radius: Theme.radius
        color: Theme.surface
        border.color: control.activeFocus ? Theme.accent : control.hovered ? Theme.lineStrong : Theme.line
        border.width: 1
    }
}
