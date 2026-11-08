import QtQuick

ChoiceStrip {
    objectName: "graphicsPresetPicker"
    title: launcher.tr("Preset")
    choices: ["low", "high", "ultra", "custom"]
    currentValue: launcher.graphicsPreset
    recommendedValue: launcher.recommendedPreset
    labelFor: (value) => launcher.presetLabel(value)
    description: launcher.presetDescription(currentValue)
    onChosen: (value) => launcher.applyGraphicsPreset(value)
}
