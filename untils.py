from telegram import ReplyKeyboardMarkup
from emoji import emojize


def list_of_activity_levels():
    return [
            [f"Минимальный {get_emoji('yawning_face')}"],
            [f"Низкий {get_emoji('flushed_face')}"],
            [f"Умеренный {get_emoji('smiling_face_with_sunglasses')}"],
            [f"Высокий {get_emoji('face_with_steam_from_nose')}"],
            [f"Экстремальный {get_emoji('smiling_face_with_horns')}"]
        ]


def activity_level_multiplier(level):
    if level == f"Минимальный {get_emoji('yawning_face')}":
        return 1.2
    elif level == f"Низкий {get_emoji('flushed_face')}":
        return 1.375
    elif level == f"Умеренный {get_emoji('smiling_face_with_sunglasses')}":
        return 1.55
    elif level == f"Высокий {get_emoji('face_with_steam_from_nose')}":
        return 1.7
    return 1.9


def calorie_сalculation(gender: str, age: int, height: int, weight: int, activity_level_multiplier: float) -> int:
    if "Женский" in gender:
        calorie_count = 655.1 + (9.563*weight) + (1.85*height) - (4.676*age)
        return calorie_count
    calorie_count = 66.5 + (13.75*weight) + (5.003*height) - (6.775*age)
    return int(calorie_count)


def initial_keyboard():
    return ReplyKeyboardMarkup([[f"Заполнить данные {get_emoji('pencil')}"], [f"Расчёт калорий {get_emoji('abacus')}"],
                                [f"Пищевая ценность {get_emoji('fire')}", f"Дейли рацион {get_emoji('receipt')}"],
                                [f"Рецепт блюда {get_emoji('man_cook')}", f"Профиль {get_emoji('bust_in_silhouette')}"]
                                ])


def main_keyboard():
    return ReplyKeyboardMarkup([[f"Расчёт калорий {get_emoji('abacus')}"],
                                [f"Пищевая ценность {get_emoji('fire')}", f"Дейли рацион {get_emoji('receipt')}"],
                                [f"Рецепт блюда {get_emoji('man_cook')}", f"Профиль {get_emoji('bust_in_silhouette')}"]
                                ])


def gender_selection_button():
    return ReplyKeyboardMarkup([
        [f"Мужской {get_emoji('man')}", f"Женский {get_emoji('woman')}"]
        ], one_time_keyboard=True, resize_keyboard=True)


def activity_level_selection_button():
    buttons = list_of_activity_levels()
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=True)


def get_emoji(emoji_name: str):
    return emojize(f":{emoji_name}:")


def data_output(context):
    text = f"""<b>Пол</b>: {context.user_data['questionnaire']['gender']}
<b>Возраст</b>: {context.user_data['questionnaire']['age']}
<b>Рост</b>: {context.user_data['questionnaire']['height']}
<b>Текцщий вес</b>: {context.user_data['questionnaire']['current_weight']}
<b>Уровень физической активности</b>: {context.user_data['questionnaire']['level_of_physical_activity']}
"""
    return text


def emoji_to_the_number_of(emoji):
    if f"{get_emoji('keycap_2')}{get_emoji('keycap_0')}" in emoji:
        return "20"
    elif f"{get_emoji('keycap_1')}{get_emoji('keycap_5')}" in emoji:
        return "15"
    elif f"{get_emoji('keycap_1')}{get_emoji('keycap_0')}" in emoji:
        return "10"
    elif f"{get_emoji('keycap_5')}" in emoji:
        return "5"
    return "unknown emoji or missing emoji"


def keypad_with_weight_selection():
    return ReplyKeyboardMarkup([
        [f"{get_emoji('keycap_5')} кг", f"{get_emoji('keycap_1')}{get_emoji('keycap_0')} кг"],
        [f"{get_emoji('keycap_1')}{get_emoji('keycap_5')} кг", f"{get_emoji('keycap_2')}{get_emoji('keycap_0')} кг"]
        ], one_time_keyboard=True, resize_keyboard=True)


def keypad_with_target_selection():
    return ReplyKeyboardMarkup([
            [f"Сбросить вес {get_emoji('down_arrow')}"],
            [f"Набрать вес {get_emoji('up_arrow')}"],
            [f"Сохранить вес {get_emoji('left-right arrow')}"]
        ], one_time_keyboard=True, resize_keyboard=True)
