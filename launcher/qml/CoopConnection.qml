import QtQuick
import QtQuick.Controls

Column {
    id: connection
    property bool compact: false
    property bool showFirewall: false
    property bool showPlayerName: true
    property bool serifLabels: false
    spacing: compact ? 6 : 16
    signal attentionRequested(var target)
    onVisibleChanged: if (visible && showFirewall && launcher.coopFirewallError) Qt.callLater(function() { connection.attentionRequested(firewallButton) })
    Connections {
        target: launcher
        function onCoopChanged() { if (connection.visible && showFirewall && launcher.coopFirewallError) Qt.callLater(function() { connection.attentionRequested(firewallButton) }) }
    }
    property bool hosting: launcher.coopRole === "host"
    Repeater {
        model: launcher.settingsRevision < 0 ? [] : launcher.sectionFields("Co-op", "Seamless co-op").filter(f => connection.showPlayerName || f.key !== "coop_name")
        delegate: FieldRow { width: connection.width; minimumHeight: connection.compact ? 54 : 62; compact: connection.compact; serifLabel: connection.serifLabels; field: modelData }
    }
    ToggleRow {
        width: parent.width
        serifLabel: connection.serifLabels
        enabled: !launcher.running && !launcher.coopBusy
        label: launcher.tr("Host on this PC")
        hint: connection.hosting ? launcher.tr("Send your invite code to friends.") : launcher.tr("Join a friend's server using their code.")
        checked: connection.hosting
        onToggled: (on) => launcher.setValue("coop_role", on ? "host" : "client")
    }
    Repeater {
        model: connection.hosting ? [] : launcher.sectionFields("Co-op", "Join a host")
        delegate: FieldRow { width: connection.width; minimumHeight: connection.compact ? 54 : 62; compact: connection.compact; serifLabel: connection.serifLabels; field: modelData }
    }
    Row {
        width: parent.width; spacing: 10
        GlassButton {
            visible: connection.hosting
            width: Math.min(180, (connection.width - 20) / 3)
            text: launcher.coopHosting ? launcher.tr("Stop server") : launcher.tr("Start server")
            enabled: !launcher.coopBusy && !launcher.running
            onClicked: launcher.coopHosting ? launcher.coopStopHosting() : launcher.coopStartHosting()
        }
        GlassButton {
            id: firewallButton
            visible: connection.showFirewall
            width: Math.min(180, (connection.width - 20) / 3)
            text: launcher.tr("Configure firewall")
            highlighted: launcher.coopFirewallError
            enabled: !launcher.coopBusy && !launcher.running
            onClicked: launcher.coopConfigureFirewall()
        }
        GlassButton {
            visible: connection.hosting && launcher.coopHosting
            width: Math.min(180, (connection.width - 20) / 3)
            text: launcher.tr("Copy invite code")
            enabled: launcher.coopInvite !== ""
            onClicked: launcher.coopCopyInvite()
        }
    }
    Note { visible: connection.showFirewall; text: launcher.tr("Allows co-op server connections through Windows Firewall on local and Tailscale networks.") }
    Note { visible: !connection.compact; text: launcher.coopStatus }
    Text {
        visible: launcher.coopStatus.indexOf("https://tailscale.com/download/windows") >= 0
        text: '<a href="https://tailscale.com/download/windows">' + launcher.tr("Download Tailscale") + '</a>'
        linkColor: Theme.accentHover; font.pixelSize: 14
        onLinkActivated: (link) => Qt.openUrlExternally(link)
    }
}
