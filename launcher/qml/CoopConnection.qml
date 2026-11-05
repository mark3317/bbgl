import QtQuick
import QtQuick.Controls

Column {
    id: connection
    property bool compact: false
    property bool showPlayerName: true
    property bool serifLabels: false
    property bool showStatus: true
    spacing: compact ? 8 : 16
    signal attentionRequested(var target)
    Repeater {
        model: launcher.settingsRevision < 0 ? [] : launcher.sectionFields("Co-op", "Seamless co-op").filter(f => connection.showPlayerName || f.key !== "coop_name")
        delegate: FieldRow { width: connection.width; compact: connection.compact; serifLabel: connection.serifLabels; field: modelData }
    }
    Item {
        width: parent.width
        height: Math.max(connection.compact ? 56 : 62, networkLabel.implicitHeight + 24, networkPicker.implicitHeight + 16)
        Text {
            id: networkLabel
            x: 2; width: parent.width - networkPicker.width - 28; anchors.verticalCenter: parent.verticalCenter
            text: launcher.tr("Connection"); color: Theme.text; wrapMode: Text.WordWrap
            font.family: connection.serifLabels ? Theme.serif : Theme.sans
            font.pixelSize: connection.serifLabels ? 17 : 14
        }
        GlassComboBox {
            id: networkPicker
            objectName: "coopNetworkPicker"
            anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter
            width: Math.min(330, parent.width * 0.44)
            enabled: !launcher.running && !launcher.coopBusy && !launcher.vpnInstalling && !launcher.coopNetworksLoading
            opacity: enabled ? 1 : 0.45
            onEnabledChanged: { if (!enabled) popup.close() }
            model: launcher.coopConnections.concat(launcher.coopMissingVpns.map(v => ({
                text: v.text,
                name: v.text, value: "install_" + v.value, provider: v.value
            })))
            textRole: "text"; valueRole: "value"
            popup.width: Math.max(networkPicker.width, 340)
            currentIndex: Math.max(0, indexOfValue(launcher.coopConnection))
            onActivated: (index) => {
                if (!enabled) return
                const option = model[index]
                if (option.provider) {
                    currentIndex = Math.max(0, indexOfValue(launcher.coopConnection))
                } else launcher.setValue("coop_connection", option.value)
            }
            Connections {
                target: launcher
                function onCoopNetworksChanged() {
                    networkPicker.currentIndex = Math.max(0, networkPicker.indexOfValue(launcher.coopConnection))
                }
            }
            delegate: ItemDelegate {
                id: networkOption
                width: networkPicker.popup.availableWidth
                height: Math.max(modelData.provider ? 62 : 44, optionLabels.implicitHeight + 20)
                highlighted: networkPicker.highlightedIndex === index
                contentItem: Item {
                    Column {
                        id: optionLabels
                        x: 12
                        width: parent.width - x - (modelData.provider ? 124 : 12)
                        anchors.verticalCenter: parent.verticalCenter; spacing: 3
                        Text {
                            width: parent.width; text: modelData.name || modelData.text
                            color: Theme.text; font.family: Theme.sans; font.pixelSize: 13; wrapMode: Text.WordWrap
                        }
                        Text {
                            visible: !!modelData.provider; width: parent.width
                            text: launcher.tr("Not installed"); color: Theme.textDim
                            font.family: Theme.sans; font.pixelSize: 12; wrapMode: Text.WordWrap
                        }
                    }
                    GlassButton {
                        objectName: "installVpn_" + (modelData.provider || "")
                        visible: !!modelData.provider
                        anchors.right: parent.right; anchors.rightMargin: 8; anchors.verticalCenter: parent.verticalCenter
                        width: 104; height: 34
                        text: launcher.tr("Download")
                        enabled: !launcher.vpnInstalling && !launcher.coopNetworksLoading && !launcher.running && !launcher.coopBusy
                        onClicked: {
                            // Closing the popup destroys its delegates.
                            const backend = launcher
                            const provider = modelData.provider
                            networkPicker.popup.close()
                            backend.coopInstallVpn(provider)
                        }
                    }
                }
                background: Rectangle {
                    radius: 4; color: networkOption.highlighted ? Theme.surfaceHover : "transparent"
                    Rectangle {
                        visible: index === launcher.coopConnections.length
                        x: 8; width: parent.width - 16; height: 1; color: Theme.lineStrong
                    }
                    Rectangle {
                        visible: !modelData.provider && index === networkPicker.currentIndex
                        width: 2; height: parent.height - 16; anchors.verticalCenter: parent.verticalCenter; color: Theme.accent
                    }
                }
            }
        }
    }
    Note { visible: launcher.vpnInstallStatus.length > 0; text: launcher.vpnInstallStatus }
    Note { text: launcher.tr("For Internet play, install a VPN and join the same network as your friends.") }
    Note { text: launcher.tr("Players with an open launcher or game are found automatically in the selected network. Roles are chosen with bells in the game.") }
    Note { visible: connection.showStatus; text: launcher.coopStatus }
}
