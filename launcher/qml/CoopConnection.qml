import QtQuick
import QtQuick.Controls

Column {
    id: connection
    property bool compact: false
    property bool showFirewall: false
    property bool showPlayerName: true
    property bool serifLabels: false
    spacing: compact ? 8 : 16
    signal attentionRequested(var target)
    Repeater {
        model: launcher.settingsRevision < 0 ? [] : launcher.sectionFields("Co-op", "Seamless co-op").filter(f => connection.showPlayerName || f.key !== "coop_name")
        delegate: FieldRow { width: connection.width; compact: connection.compact; serifLabel: connection.serifLabels; field: modelData }
    }
    Row {
        width: parent.width; spacing: 16
        Text { width: parent.width * 0.35; anchors.verticalCenter: parent.verticalCenter; text: launcher.tr("Connection"); color: Theme.text; font.family: Theme.sans; font.pixelSize: 14 }
        GlassComboBox {
            objectName: "coopNetworkPicker"
            width: parent.width * 0.65 - 16; height: 38
            enabled: !launcher.running && !launcher.coopBusy
            model: launcher.coopConnections; textRole: "text"; valueRole: "value"
            currentIndex: Math.max(0, indexOfValue(launcher.coopConnection))
            onActivated: launcher.setValue("coop_connection", currentValue)
        }
    }
    GlassTextField {
        width: parent.width; visible: launcher.coopConnection === "custom"
        enabled: !launcher.running && !launcher.coopBusy
        text: launcher.value("coop_custom_address")
        placeholderText: launcher.tr("Local IPv4 of your network adapter")
        onEditingFinished: if (text !== launcher.value("coop_custom_address")) launcher.setValue("coop_custom_address", text)
    }
    GlassTextField {
        width: parent.width; visible: launcher.coopConnection === "custom"
        enabled: !launcher.running && !launcher.coopBusy
        text: launcher.value("coop_peer_addresses")
        placeholderText: launcher.tr("Player IPv4 addresses, separated by commas (optional)")
        onEditingFinished: if (text !== launcher.value("coop_peer_addresses")) launcher.setValue("coop_peer_addresses", text)
    }
    Note { text: launcher.tr("Open the launcher on every PC in the same VPN or local network. Roles are chosen with bells in the game.") }
    Row {
        width: parent.width; spacing: 10
        GlassButton {
            width: Math.min(220, (connection.width - 10) / 2)
            text: launcher.tr("Check connection")
            enabled: !launcher.running && !launcher.coopBusy && !launcher.coopNetworksLoading
            onClicked: launcher.coopRefreshNetworks()
        }
        GlassButton {
            id: firewallButton
            visible: connection.showFirewall
            width: Math.min(220, (connection.width - 10) / 2)
            text: launcher.tr("Configure firewall")
            highlighted: launcher.coopFirewallError
            enabled: !launcher.running && !launcher.coopBusy
            onClicked: launcher.coopConfigureFirewall()
        }
    }
    Note { text: launcher.coopStatus }
}
