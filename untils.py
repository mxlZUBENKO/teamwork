from telegram import ReplyKeyboardMarkup
from emoji import emojize


def list_of_activity_levels_and_multiplier():
    return [
            [f"Минимальный {get_emoji('yawning_face')}", 1.2],
            [f"Низкий {get_emoji('flushed_face')}", 1.375],
            [f"Умеренный {get_emoji('smiling_face_with_sunglasses')}", 1.55],
            [f"Высокий {get_emoji('face_with_steam_from_nose')}", 1.7],
            [f"Экстремальный {get_emoji('smiling_face_with_horns')}", 1.9]
        ]


def calorie_сalculation(gender: str, age: int, height: int, weight: float, activity_level_multiplier: float) -> float:
    if "Женский" in gender:
        calorie_count = 655.1 + (9.563*weight) + (1.85*height) - (4.676*age)
        return calorie_count
    calorie_count = 66.5 + (13.75*weight) + (5.003*height) - (6.775*age)
    return calorie_count


def questionnaire_completion(context):
    user_information = context.user_data.get('questionnaire', None)
    if user_information is None:
        return None
    user_gender = context.user_data['questionnaire'].get('gender')
    user_age = context.user_data['questionnaire'].get('age')
    user_height = context.user_data['questionnaire'].get('height')
    user_weight = context.user_data['questionnaire'].get('weight')
    user_level_of_physical_activity = context.user_data['questionnaire'].get('level_of_physical_activity')
    return [user_gender, user_age, user_height, user_weight,
            activity_level_multiplier(user_level_of_physical_activity)]


def initial_keyboard():
    return ReplyKeyboardMarkup([[f"Заполнить данные {get_emoji('pencil')}"], ["Расчёт калорий"],
                                ["Пищевая ценность", "Дейли рацион"],
                                ["Рецепт", f"Настройки {get_emoji('gear')}"]
                                ])


def main_keyboard():
    return ReplyKeyboardMarkup([["Расчёт калорий"],
                                ["Пищевая ценность", "Дейли рацион"],
                                ["Рецепт блюда", f"Профиль {get_emoji('bust_in_silhouette')}"]
                                ])


def gender_selection_button():
    return ReplyKeyboardMarkup([
        [f"Мужской {get_emoji('man')}", f"Женский {get_emoji('woman')}"]
        ], one_time_keyboard=True, resize_keyboard=True)


def activity_level_selection_button():
    buttons = [[level[0]] for level in list_of_activity_levels_and_multiplier()]
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
