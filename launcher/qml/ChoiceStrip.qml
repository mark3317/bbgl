import QtQuick
import QtQuick.Controls

Column {
    id: strip
    required property string title
    required property var choices
    required property string currentValue
    property string description: ""
    property string recommendedValue: ""
    property var labelFor: (value) => value
    signal chosen(string value)
    spacing: 10

    Text { text: strip.title; visible: text.length > 0; color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 12 }
    Item {
        width: strip.width; height: 56
        Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: Theme.line }
        Row {
            anchors.fill: parent
            Repeater {
                model: strip.choices
                delegate: Button {
                    id: option
                    required property string modelData
                    readonly property bool selected: strip.currentValue === modelData
                    objectName: strip.objectName + "_" + modelData
                    width: strip.width / strip.choices.length; height: 56
                    hoverEnabled: true
                    text: strip.labelFor(modelData)
                    Accessible.selected: selected
                    contentItem: Text {
                        text: option.text
                        color: option.selected || option.hovered || option.activeFocus ? Theme.text : Theme.textDim
                        font.family: Theme.serif; font.pixelSize: 16
                        horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        wrapMode: Text.WordWrap
                    }
                    background: Rectangle {
                        color: "transparent"
                        Rectangle {
                            visible: option.selected || option.activeFocus
                            height: option.selected ? 2 : 1; width: parent.width - 28
                            anchors.bottom: parent.bottom; anchors.horizontalCenter: parent.horizontalCenter
                            color: option.selected ? Theme.accentHover : Theme.lineStrong
                        }
                    }
                    ToolTip.visible: hovered && strip.recommendedValue === modelData
                    ToolTip.text: launcher.tr("Recommended")
                    onClicked: strip.chosen(modelData)
                }
            }
        }
    }
    Note { text: strip.description; visible: text.length > 0 }
}
