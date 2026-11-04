"""Client-local Information page for the BBSC-GL bundled launcher."""
import base64
import json
from pathlib import Path

TEXT = {
    'en': ('BBSC-GL — Bloodborne Game Launcher',
           'This launcher includes BBSC-GL, a modified version of Bloodborne Seamless Co-op.\n\n'
           'Start co-op from the launcher. The host rings the Beckoning Bell; guests ring the Small Resonant Bell. '
           'Use the Silencing Blank to leave the session. The Sinister Resonant Bell searches for a world to invade.\n\n'
           'Stay together across areas, lamps, bosses and deaths. Each player keeps their own character. '
           'Guests have their own Hunter\'s Dream. Shared progress and enemy scaling are configured in the launcher.\n\n'
           'This fork includes fixes for chalice travel, reconnecting, key items and recovery after death. '
           'The mod is experimental; keep additional backups.\n\n'
           'BBSC-GL: github.com/mark3317/bbsc-gl\n'
           'Launcher: github.com/mark3317/bbgl\n'
           'Based on BBSC by CLS_AMG and its contributors. Original authors retain their credits and licences.'),
    'ru': ('BBSC-GL — Bloodborne Game Launcher',
           'В лаунчер включён BBSC-GL — модифицированная версия Bloodborne Seamless Co-op.\n\n'
           'Запустите кооператив из лаунчера. Хост звонит в Зовущий Колокол, гости — в Малый звонкий колокол. '
           'Бланк молчания позволяет покинуть сессию. Зловещий звонкий колокол ищет мир для вторжения.\n\n'
           'Играйте вместе при переходах между областями, использовании фонарей, сражениях с боссами и после смерти. '
           'Каждый сохраняет своего персонажа. У гостей — собственный Сон охотника. '
           'Общий прогресс и усиление врагов настраиваются в лаунчере.\n\n'
           'В этой версии исправлены ошибки переходов в чаши, повторного подключения, выдачи ключевых предметов '
           'и восстановления после смерти. '
           'Мод остаётся экспериментальным; храните дополнительные резервные копии.\n\n'
           'BBSC-GL: github.com/mark3317/bbsc-gl\n'
           'Лаунчер: github.com/mark3317/bbgl\n'
           'Основано на BBSC от CLS_AMG и участников проекта. Авторство и лицензии исходных компонентов сохранены.')
}


def response(language):
    title, text = TEXT['ru' if str(language) == '8' else 'en']
    encode = lambda value: base64.b64encode(value.encode('utf-8')).decode('ascii')
    stamp = 1793476800  # stable revision: reopening Information must not generate new notices
    return {'ResKind': 0, 'MessageId': 'NoticeNormalGetResponse', 'CheckTime': stamp,
            'NoticeList': [{'Id': stamp, 'NoticeId': stamp, 'CheckTime': stamp,
                            'Title': encode(title), 'Notice': encode(text)}]}


def prepare(user_dir, language):
    path = Path(user_dir) / 'bbsc-information.json'
    path.write_text(json.dumps(response(language)), encoding='utf-8')
    return str(path)
