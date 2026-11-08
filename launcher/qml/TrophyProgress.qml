import QtQuick

Column {
    id: trophySummary
    property string label: launcher.tr("Trophies")
    property bool showIcon: true
    spacing: 6
    readonly property var progress: launcher.trophyProgress
    readonly property bool hasTotal: progress.total > 0
    readonly property string count: hasTotal
        ? launcher.tr("%1 of %2").arg(progress.earned).arg(progress.total)
        : progress.earned >= 0 ? launcher.tr("%1 earned").arg(progress.earned)
                               : launcher.tr("Progress unavailable")
    Accessible.role: Accessible.ProgressBar
    Accessible.name: label + ": " + count

    Item {
        width: parent.width
        height: Math.max(trophySummary.showIcon ? trophyIcon.height : 0, trophyLabel.implicitHeight, trophyCount.implicitHeight)
        NavIcon {
            id: trophyIcon; kind: "trophy"; width: 18; height: 18
            visible: trophySummary.showIcon
            anchors.verticalCenter: parent.verticalCenter; strokeColor: Theme.accentHover
        }
        Text {
            id: trophyLabel; text: trophySummary.label; color: Theme.text
            x: trophySummary.showIcon ? trophyIcon.width + 8 : 0
            width: Math.max(0, parent.width - x - trophyCount.width - 12)
            wrapMode: Text.Wrap
            anchors.verticalCenter: parent.verticalCenter
            font.family: Theme.sans; font.pixelSize: 13
        }
        Text {
            id: trophyCount; objectName: trophySummary.objectName + "Count"
            text: trophySummary.count; color: Theme.text
            anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter
            font.family: Theme.sans; font.pixelSize: 13; font.weight: Font.Medium
        }
    }
    Rectangle {
        objectName: trophySummary.objectName + "Track"
        visible: trophySummary.hasTotal
        width: parent.width; height: 4; radius: 2; color: Theme.lineStrong
        Rectangle {
            width: trophySummary.hasTotal
                ? parent.width * trophySummary.progress.earned / trophySummary.progress.total : 0
            height: parent.height; radius: parent.radius; color: Theme.accentHover
        }
    }
}
