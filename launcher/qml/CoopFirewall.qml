import QtQuick

Column {
    spacing: 12
    Text {
        width: parent.width; wrapMode: Text.WordWrap
        color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 13
        text: launcher.tr("Firewall setup is optional. If players cannot connect, use this button to allow incoming connections. Only this action asks for administrator rights; starting co-op does not.")
    }
    GlassButton {
        text: launcher.tr("Configure firewall"); width: Math.max(190, implicitWidth); height: 40
        enabled: !launcher.coopBusy && !launcher.running
        onClicked: launcher.coopConfigureFirewall()
    }
    Text {
        width: parent.width; wrapMode: Text.WordWrap
        text: launcher.coopStatus
        color: Theme.textDim; font.family: Theme.sans; font.pixelSize: 13
    }
}
