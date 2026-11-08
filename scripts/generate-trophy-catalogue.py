"""Embed the launcher's offline trophy catalogue in the native overlay."""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
from bbport_trophy_catalog import BASE_TROPHY_COUNT, BLOODBORNE_TROPHY_SET, _HIDDEN_IDS, _TROPHIES


def main(output):
    rows = []
    for trophy_id, texts in enumerate(_TROPHIES):
        strings = ', '.join(json.dumps(text, ensure_ascii=False) for text in texts)
        hidden = 'true' if trophy_id in _HIDDEN_IDS else 'false'
        rows.append(f'    {{{strings}, {hidden}}},')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        '// Generated from launcher/bbport_trophy_catalog.py.\n'
        '#pragma once\n\n'
        'namespace BbTrophyCatalogue {\n'
        f'inline constexpr char PackId[] = "{BLOODBORNE_TROPHY_SET.decode("ascii")}";\n'
        f'inline constexpr int BaseCount = {BASE_TROPHY_COUNT};\n'
        'struct Text { const char* name_en; const char* detail_en; const char* name_ru; '
        'const char* detail_ru; bool hidden; };\n'
        'inline constexpr Text Entries[] = {\n' + '\n'.join(rows) + '\n};\n'
        '} // namespace BbTrophyCatalogue\n', encoding='utf-8')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
