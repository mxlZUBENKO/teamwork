from telegram import ReplyKeyboardMarkup


def activity_level_multiplier(level_of_physical_activity):
    if level_of_physical_activity == "минимальный (сидячая работа, отсутствие физических нагрузок)":
        return 1.2
    elif level_of_physical_activity == "низкий (тренировки не менее 20 мин 1-3 раза в неделю)":
        return 1.375
    elif level_of_physical_activity == "умеренный (тренировки 30-60 мин 3-4 раза в неделю)":
        return 1.55
    elif level_of_physical_activity == "высокий (тренировки 30-60 мин 5-7 раза в неделю;тяжелая физическая работа":
        return 1.7
    return 1.9


def calorie_сalculation(gender, age, height, weight, activity_level_multiplier):
    if gender == "Женский":
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


def main_keyboard():
    return ReplyKeyboardMarkup([["Ввести данные"], ["Расчёт калорий"],
                                ["Пищевая ценность", "Дейли рацион"],
                                ["Рецепт", "Настройки"]])


def gender_selection_button():
    return ReplyKeyboardMarkup([
        ['Мужской', 'Женский']], one_time_keyboard=True
        )
