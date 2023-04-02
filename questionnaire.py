from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from untils import (data_output, gender_selection_button, main_keyboard,
                    get_emoji, activity_level_selection_button,
                    list_of_activity_levels_and_multiplier)
# from handlers import calorie_count
from db import db, get_or_create_user, save_questionnaire


def questionnaire_start(update, context):
    update.message.reply_text(
        "Выберете пол",
        reply_markup=gender_selection_button()
    )
    return "gender"


def questionnaire_gender(update, context):
    user_gender = update.message.text
    if "Мужской" not in user_gender and "Женский" not in user_gender:
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
        update.message.reply_text("Введите текущий вес")
        context.user_data["questionnaire"]["height"] = user_height
    return "current_weight"


def questionnaire_current_weight(update, context):
    user_weight = update.message.text
    if user_weight.isdigit() is False or user_weight == '0':
        update.message.reply_text("Укажите корректный вес")
        return "current_weight"
    else:
        update.message.reply_text(
            "Выберете уровень физической активности",
            reply_markup=activity_level_selection_button()
            )
        context.user_data["questionnaire"]["current_weight"] = user_weight
    return "level_of_physical_activity"


def level_of_physical_activity(update, context):
    user_response = update.message.text
    level_of_physical_activity = [level[0] for level in list_of_activity_levels_and_multiplier()]
    if user_response not in level_of_physical_activity:
        update.message.reply_text("Выберете уровень физической активности")
        return "level_of_physical_activity"
    else:
        context.user_data["questionnaire"]["level_of_physical_activity"] = user_response
        user_text = data_output(context)
        reply_keyboard = [
            [f"Данные верны {get_emoji('check_mark')}", f"Данные неверны. {get_emoji('cross_mark')}"]
            ]
        update.message.reply_text(user_text, parse_mode=ParseMode.HTML,
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                   resize_keyboard=True)
                                  )
        return "data_validation"


def data_validation(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_response = update.message.text
    if "Данные верны" in user_response:
        save_questionnaire(db, user['user_id'], context.user_data['questionnaire'])
        update.message.reply_text("Ваши данные сохранены.", reply_markup=main_keyboard())
        return ConversationHandler.END
    else:
        update.message.reply_text("Ваши данные не сохранены.", reply_markup=main_keyboard())
        return ConversationHandler.END


def questionnaire_dontknow(update, context):
    update.message.reply_text("Некорректные данные(")
