"""Client-local Information page for the BBSC-GL bundled launcher."""
import base64
import json
from pathlib import Path

TEXT = {
    'en': ('BBSC-GL — Bloodborne Game Launcher',
           'Seamless co-op: play through the main story and Chalice Dungeons together. '
           'Stay together across areas, at lamps, through boss battles and after death. '
           'Each player has their own side quests.\n\n'
           'Pick up the Notebook from the messengers in the Hunter\'s Dream to receive co-op items automatically. '
           'If you already have the Notebook, missing items will be added when you load your own world.\n\n'
           'Beckoning Bell — call other players.\n'
           'Small Resonant Bell — join a host.\n'
           'Silencing Blank — stop searching or end co-op.\n'
           'Sinister Resonant Bell — find a world to invade.\n\n'
           'Shared progress and enemy scaling are configured in the launcher. '
           'The mod is experimental — keep backups.\n\n'
           'BBSC-GL: github.com/mark3317/bbsc-gl\n'
           'Launcher: github.com/mark3317/bbgl\n'
           'Based on BBSC by CLS_AMG and its contributors. Credits and licences are preserved.'),
    'ru': ('BBSC-GL — Bloodborne Game Launcher',
           'Бесшовный кооператив: проходите вместе основной сюжет и подземелья чаш. '
           'Оставайтесь вместе при переходах между областями, у фонарей, в битвах с боссами и после смерти. '
           'Побочные квесты у каждого игрока свои.\n\n'
           'Заберите Блокнот у посланников в Сне охотника — предметы для кооператива выдадутся автоматически. '
           'Если Блокнот уже есть, недостающие предметы добавятся при загрузке своего мира.\n\n'
           'Зовущий Колокол — позвать игроков.\n'
           'Малый звонкий колокол — присоединиться к хозяину мира.\n'
           'Бланк молчания — остановить поиск или завершить кооператив.\n'
           'Зловещий звонкий колокол — найти мир для вторжения.\n\n'
           'Общий прогресс и усиление врагов настраиваются в лаунчере. '
           'Мод экспериментальный — сохраняйте резервные копии.\n\n'
           'BBSC-GL: github.com/mark3317/bbsc-gl\n'
           'Лаунчер: github.com/mark3317/bbgl\n'
           'На основе BBSC от CLS_AMG и участников проекта. Авторство и лицензии сохранены.')
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
