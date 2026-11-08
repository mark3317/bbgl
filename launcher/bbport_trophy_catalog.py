"""Offline Bloodborne trophy names and short descriptions for the launcher."""

BLOODBORNE_TROPHY_SET = b'NPWR05818_00'
BASE_TROPHY_COUNT = 34

# IDs follow the PS4 catalogue. Names are identifiers; requirements are written
# for BBGL. Cross-check names against the Russian and English PS4 trophy lists
# and spoiler flags against InferGames' base and Old Hunters lists.
# https://www.exophase.com/game/bloodborne-ps4/trophies/ru/
# https://infergames.com/ps4/bloodborne/list-of-trophies
# https://infergames.com/ps4/bloodborne-the-old-hunters/list-of-trophies
_TROPHIES = (
    ("Bloodborne", "Earn every trophy in the base game.",
     "Bloodborne", "Получите все трофеи основной игры."),
    ("Yharnam Sunrise", "Accept Gehrman's offer and see the morning in Yharnam.",
     "Ярнамский восход", "Примите предложение Германа и встретите рассвет в Ярнаме."),
    ("Honouring Wishes", "Take Gehrman's place as keeper of the Hunter's Dream.",
     "Исполнение желаний", "Займите место Германа и станьте хранителем Сна охотника."),
    ("Childhood's Beginning", "Become a newborn Great One.",
     "Начало детства", "Станьте новорождённым Великим."),
    ("Yharnam, Pthumerian Queen", "Overcome Queen Yharnam in the Great Pthumeru Ihyll labyrinth.",
     "Ярнам, Птумерианская Королева", "Одолейте королеву Ярнам в лабиринте Великого Птумеру Айилл."),
    ("Hunter's Essence", "Complete the base game's hunter weapon collection.",
     "Сущность охотника", "Соберите полную коллекцию оружия охотника из основной игры."),
    ("Hunter's Craft", "Complete the collection of special hunter tools.",
     "Ремесло охотника", "Соберите полную коллекцию особых инструментов охотника."),
    ("Weapon Master", "Fortify a weapon to +10.",
     "Оружейник", "Улучшите любое оружие до +10."),
    ("Blood Gem Master", "Find a high-grade blood gem.",
     "Мастер по кровавым самоцветам", "Найдите кровавый самоцвет высокого ранга."),
    ("Rune Master", "Find a high-grade Caryll Rune.",
     "Мастер рун", "Найдите редкую руну Кэрилла."),
    ("Cainhurst", "Reach the castle of Cainhurst.",
     "Кейнхёрст", "Доберитесь до замка Кейнхёрст."),
    ("The Choir", "Reach the Choir's domain in Upper Cathedral Ward.",
     "Хор", "Доберитесь до владений Хора в Верхнем Соборном округе."),
    ("The Source of the Dream", "Find the real-world workshop that inspired the Hunter's Dream.",
     "Источник сна", "Найдите заброшенную мастерскую, послужившую прообразом Сна охотника."),
    ("Nightmare Lecture Building", "Enter the lecture building within the nightmare.",
     "Лекционный зал кошмара", "Попадите в Лекционный корпус, оказавшийся в кошмаре."),
    ("Father Gascoigne", "Win the fight against Father Gascoigne.",
     "Отец Гаскойн", "Одержите победу в бою с отцом Гаскойном."),
    ("Vicar Amelia", "Overcome Vicar Amelia in the Grand Cathedral.",
     "Викарий Амелия", "Одолейте викария Амелию в Великом соборе."),
    ("Shadow of Yharnam", "Overcome the Shadow of Yharnam in the Forbidden Woods.",
     "Тень Ярнама", "Одолейте Тень Ярнама в Запретном лесу."),
    ("Rom, the Vacuous Spider", "Win the fight against Rom at Moonside Lake.",
     "Ром, Праздный Паук", "Победите Ром в сражении на Лунном озере."),
    ("The One Reborn", "Overcome the One Reborn in Yahar'gul.",
     "Возродившийся", "Одолейте Возродившегося в Яаар’гуле."),
    ("Micolash, Host of the Nightmare", "Track down and overcome Micolash in the Nightmare of Mensis.",
     "Миколаш, Хозяин Кошмара", "Настигните и одолейте Миколаша в Кошмаре Менсиса."),
    ("Mergo's Wet Nurse", "Win the battle against the guardian of Mergo.",
     "Кормилица Мерго", "Одержите победу в сражении с Кормилицей Мерго."),
    ("Cleric Beast", "Overcome the beast on Central Yharnam's Great Bridge.",
     "Церковное чудовище", "Одолейте чудовище на Великом мосту Центрального Ярнама."),
    ("Blood-starved Beast", "Overcome the Blood-starved Beast in Old Yharnam.",
     "Чудовище-кровоглот", "Одолейте Чудовище-кровоглота в Старом Ярнаме."),
    ("The Witch of Hemwick", "Overcome the witch at Hemwick Charnel Lane.",
     "Ведьма Хемвика", "Одолейте ведьму на Молитвенном переулке Хемвик."),
    ("Darkbeast Paarl", "Overcome Paarl, the lightning-wreathed darkbeast.",
     "Черное чудовище Паарл", "Одолейте Паарла, чёрное чудовище, окружённое молниями."),
    ("Amygdala", "Win the fight against Amygdala at the Nightmare Frontier.",
     "Амигдала", "Одержите победу над Амигдалой на Границе Кошмара."),
    ("Martyr Logarius", "Overcome Logarius on the roof of Cainhurst Castle.",
     "Мученик Логариус", "Одолейте Логариуса на крыше замка Кейнхёрст."),
    ("Celestial Emissary", "Overcome the Celestial Emissary in the Lumenflower Gardens.",
     "Посланник Небес", "Одолейте Посланника Небес в саду светящихся цветов."),
    ("Ebrietas, Daughter of the Cosmos", "Overcome Ebrietas at the Altar of Despair.",
     "Ибраитас, дочь Космоса", "Одолейте Ибраитас у Алтаря Отчаяния."),
    ("Blood Gem Contact", "Obtain a blood gem for strengthening a hunter weapon.",
     "Связь кровавого самоцвета", "Получите кровавый самоцвет для усиления оружия."),
    ("Rune Contact", "Obtain a Caryll Rune that can grant a hunter a new ability.",
     "Связь Руны", "Получите руну Кэрилла, дающую охотнику новую способность."),
    ("Chalice of Pthumeru", "Obtain the chalice that opens the Pthumerian labyrinth.",
     "Чаша Птумеру", "Получите чашу, открывающую путь в лабиринт Птумеру."),
    ("Chalice of Ailing Loran", "Obtain the chalice that opens the ruins of Ailing Loran.",
     "Чаша Больного Лорана", "Получите чашу, открывающую путь в руины Больного Лорана."),
    ("Chalice of Isz", "Obtain the Great Isz Chalice to open the Isz labyrinth.",
     "Чаша Исза", "Получите Великую чашу Исза, открывающую одноимённый лабиринт."),
    ("Old Hunter's Essence", "Complete the weapon collection in The Old Hunters.",
     "Сущность старого охотника", "Соберите полную коллекцию оружия дополнения The Old Hunters."),
    ("Orphan of Kos", "Overcome the Orphan of Kos at the Fishing Hamlet.",
     "Сирота Коса", "Одолейте Сироту Коса в Рыбацкой деревне."),
    ("Ludwig, the Holy Blade", "Overcome Ludwig in the Hunter's Nightmare.",
     "Людвиг Священный клинок", "Одолейте Людвига в Кошмаре охотника."),
    ("Lady Maria of the Astral Clocktower", "Win the duel with Lady Maria in the Astral Clocktower.",
     "Леди Мария из Астральной часовой башни", "Одержите победу в поединке с леди Марией в Астральной часовой башне."),
    ("Living Failures", "Overcome the Living Failures at the Research Hall.",
     "Живые неудачи", "Одолейте Живых неудач в Исследовательском зале."),
    ("Laurence, the First Vicar", "Overcome Laurence in the nightmare's Grand Cathedral.",
     "Первый викарий Лоренс", "Одолейте Лоренса в Великом соборе Кошмара охотника."),
)

_HIDDEN_IDS = {*range(1, 5), *range(10, 29), 32, 33, *range(35, 40)}


def bloodborne_catalogue(ids, russian):
    """Accept the known base or expanded ID layout for this trophy set."""
    if ids not in (set(range(BASE_TROPHY_COUNT)), set(range(len(_TROPHIES)))):
        return {}
    return {
        trophy_id: {
            'name': _TROPHIES[trophy_id][2 if russian else 0],
            'description': _TROPHIES[trophy_id][3 if russian else 1],
            'hidden': trophy_id in _HIDDEN_IDS,
        }
        for trophy_id in sorted(ids)
    }
