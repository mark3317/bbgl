import QtQuick

ChoiceStrip {
    objectName: "controlIconsPicker"
    title: launcher.tr("Control icons")
    choices: ["PlayStation", "Xbox", "Keyboard"]
    currentValue: launcher.promptChoice
    labelFor: (value) => launcher.tr(value)
    description: launcher.tr("Sets the button icons shown in game menus. Keyboard also applies matching key bindings.")
    enabled: !launcher.modsDownloading
    onChosen: (value) => launcher.setPrompt(value)
}
