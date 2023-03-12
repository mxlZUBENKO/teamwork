from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from untils import gender_selection_button, main_keyboard


def list_of_activity_levels():
    return [
            ["минимальный (сидячая работа, отсутствие физических нагрузок)"],
            ["низкий (тренировки не менее 20 мин 1-3 раза в неделю)"],
            ["умеренный (тренировки 30-60 мин 3-4 раза в неделю)"],
            ["высокий (тренировки 30-60 мин 5-7 раза в неделю;тяжелая физическая работа"],
            ["экстремальный (несколько интенсивных тренировок в день 6-7 раз в неделю; очень трудоемкая работа)"]
        ]


def data_output(context):
    text = f"""<b>Пол</b>: {context.user_data['questionnaire']['gender']}
<b>Возраст</b>: {context.user_data['questionnaire']['age']}
<b>Рост</b>: {context.user_data['questionnaire']['height']}
<b>Вест</b>: {context.user_data['questionnaire']['weight']}
<b>Уровень физической активности</b>: {context.user_data['questionnaire']['level_of_physical_activity']}
"""
    return text


def questionnaire_start(update, context):
    update.message.reply_text(
        "Выберете пол",
        reply_markup=gender_selection_button()
    )
    return "gender"


def questionnaire_gender(update, context):
    user_gender = update.message.text
    if user_gender != "Мужской" and user_gender != "Женский":
        update.message.reply_text("Выберете пол")
        return "gender"
    else:
        update.message.reply_text("Введите возраст")
        context.user_data["questionnaire"] = {"gender": user_gender}
    return "age"


def questionnaire_age(update, context):
    user_age = update.message.text
    if user_age.isdigit() is False or user_age == '0':
        update.message.reply_text("Укажите корректный возраст")
        return "age"
    else:
        update.message.reply_text("Введите рост")
        context.user_data["questionnaire"]["age"] = user_age
    return "height"


def questionnaire_height(update, context):
    user_height = update.message.text
    if user_height.isdigit() is False or user_height == '0':
        update.message.reply_text("Укажите корректный рост")
        return "height"
    else:
        update.message.reply_text("Введите вес")
        context.user_data["questionnaire"]["height"] = user_height
    return "weight"


def questionnaire_weight(update, context):
    user_weight = update.message.text
    if user_weight.isdigit() is False or user_weight == '0':
        update.message.reply_text("Укажите корректный вес")
        return "height"
    else:
        context.user_data["questionnaire"]["weight"] = user_weight
        reply_keyboard = list_of_activity_levels()
        update.message.reply_text(
            "Выберете уровень физической активности",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            )
    return "level_of_physical_activity"


def level_of_physical_activity(update, context):
    user_level_of_physical_activity = update.message.text
    level_of_physical_activity = [level[0] for level in list_of_activity_levels()]
    if user_level_of_physical_activity not in level_of_physical_activity:
        update.message.reply_text("Выберете уровень физической активности")
        return "level_of_physical_activity"
    else:
        context.user_data["questionnaire"]["level_of_physical_activity"] = user_level_of_physical_activity
        user_text = data_output(context)
        reply_keyboard = [["Данные верны", "Данные неверны. Заполнить снова"]]
        update.message.reply_text(user_text, parse_mode=ParseMode.HTML,
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                                  )
        return "data_validation"


def data_validation(update, context):
    user_response = update.message.text
    if user_response == "Данные верны":
        update.message.reply_text("Поздравляем!", reply_markup=main_keyboard())
        return ConversationHandler.END
    else:
        print("(((")


def questionnaire_dontknow(update, context):
    update.message.reply_text("Некорректные данные(")
