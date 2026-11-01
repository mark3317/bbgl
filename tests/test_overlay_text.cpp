// SPDX-License-Identifier: GPL-2.0-or-later
#include "bbport_overlay_text.h"
#include "bbport_settings.h"
#include "bbport_trophy_toast_model.h"
#include <cassert>
#include <iostream>
#include <regex>
#include <string>
#include <vector>

static std::vector<std::string> Formats(const std::string& text) {
    static const std::regex pattern("%[-+ #0]*[0-9]*[.]?[0-9]*[a-zA-Z%]");
    std::vector<std::string> result;
    for (auto it = std::sregex_iterator(text.begin(), text.end(), pattern);
         it != std::sregex_iterator(); ++it) result.push_back(it->str());
    return result;
}

int main(int argc, char** argv) {
    const bool ru = argc > 1 && std::string(argv[1]) == "ru";
    assert(BbOverlayText::Russian() == ru);
    using BbOverlayText::L;
    for (const auto& [en, translated] : BbOverlayText::Translations()) {
        assert(Formats(std::string(en)) == Formats(translated));
        assert(std::string(L(en.data())) == (ru ? translated : en));
    }
    // Effects are loaded by key; every dynamic label must have a translation too.
    for (const auto& effect : BbSettings::Effects) {
        std::string label(effect.label);
        if (label.starts_with("Cheat: ")) {
            label.erase(0, 7);
            label[0] = char(std::toupper(static_cast<unsigned char>(label[0])));
        }
        assert(BbOverlayText::Translations().count(label));
    }
    assert(std::string(L("future label")) == "future label");
    BbToast::Options options;
    assert(BbToast::UnlockedText(options) == (ru ? "Трофей получен!" : "Trophy unlocked!"));
    assert(BbToast::BannerText(options, true) == (ru ? "Проверка уведомления" : "Achievement preview"));
    options.text_unlocked = "My custom text";
    options.text_banner = "My banner";
    options.grade_names[1] = "My bronze";
    assert(BbToast::UnlockedText(options) == "My custom text");
    assert(BbToast::BannerText(options, false) == "My banner");
    assert(BbToast::GradeName(options, 1) == "My bronze");
    std::cout << "overlay language, format strings and custom notification text: PASS\n";
}
