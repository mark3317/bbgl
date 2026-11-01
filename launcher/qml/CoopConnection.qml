import QtQuick
import QtQuick.Controls

Column {
    id: connection
    spacing: 12
    property bool hosting: launcher.coopRole === "host"
    Repeater {
        model: launcher.settingsRevision < 0 ? [] : launcher.sectionFields("Co-op", "Seamless co-op")
        delegate: FieldRow { width: connection.width; field: modelData }
    }
    ToggleRow {
        width: parent.width
        enabled: !launcher.running && !launcher.coopBusy
        label: launcher.tr("Host on this PC")
        hint: connection.hosting ? launcher.tr("Send your invite code to friends.") : launcher.tr("Join a friend's server using their code.")
        checked: connection.hosting
        onToggled: (on) => launcher.setValue("coop_role", on ? "host" : "client")
    }
    Repeater {
        model: connection.hosting ? [] : launcher.sectionFields("Co-op", "Join a host")
        delegate: FieldRow { width: connection.width; field: modelData }
    }
    Flow {
        visible: connection.hosting; width: parent.width; spacing: 10
        GlassButton { text: launcher.coopHosting ? launcher.tr("Restart hosting") : launcher.tr("Start hosting"); width: 180; enabled: !launcher.coopBusy && !launcher.running; onClicked: launcher.coopStartHosting() }
        GlassButton { text: launcher.tr("Copy invite code"); width: 180; enabled: launcher.coopInvite !== ""; onClicked: launcher.coopCopyInvite() }
        GlassButton { text: launcher.tr("Stop hosting"); width: 180; enabled: launcher.coopHosting && !launcher.running; onClicked: launcher.coopStopHosting() }
    }
    Note { text: launcher.coopStatus }
    Text {
        visible: launcher.coopStatus.indexOf("https://tailscale.com/download/windows") >= 0
        text: '<a href="https://tailscale.com/download/windows">' + launcher.tr("Download Tailscale") + '</a>'
        linkColor: Theme.accentHover; font.pixelSize: 14
        onLinkActivated: (link) => Qt.openUrlExternally(link)
    }
    GlassButton {
        property bool expanded: false
        text: launcher.tr("Connection help"); onClicked: { expanded = !expanded; help.visible = expanded }
    }
    CoopFirewall { id: help; width: parent.width; visible: false }
}
