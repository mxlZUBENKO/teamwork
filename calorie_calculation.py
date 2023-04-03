from untils import (emoji_to_the_number_of, initial_keyboard, calorie_сalculation,
                    activity_level_multiplier, keypad_with_weight_selection, keypad_with_target_selection,
                    main_keyboard)
from telegram.ext import ConversationHandler
from db import db, get_or_create_user, add_or_replace_something


def calorie_calculation_start(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    if 'questionnaire' not in user:
        update.message.reply_text("Чтобы расчитать калорий нужно заполнить данные!",
                                  reply_markup=initial_keyboard())
        return ConversationHandler.END
    update.message.reply_text("Укажите вашу цель",
                              reply_markup=keypad_with_target_selection())
    return "target_selection"


def target_selection(update, context):
    user_response = update.message.text
    if "Сбросить вес" in user_response:
        update.message.reply_text("Сколько кг вы хотите сбросить? Нажмите на кнопку или введите число с клавиатуры",
                                  reply_markup=keypad_with_weight_selection())
        context.user_data["calorie_calculation"] = {"change_multiplier": -1}
        return "target_weight"
    elif "Набрать вес" in user_response:
        update.message.reply_text("Сколько кг вы хотите набрать? Нажмите на кнопку или введите число с клавиатуры",
                                  reply_markup=keypad_with_weight_selection())
        context.user_data["calorie_calculation"] = {"change_multiplier": 1}
        return "target_weight"
    elif "Сохранить вес" in user_response:
        user = get_or_create_user(db, update.effective_user, update.message.chat.id)
        current_weight = user["questionnaire"][-1]["current_weight"]
        context.user_data["calorie_calculation"] = {"target_weight": current_weight}
        сalculate_сalorie_сount(update, context)
        return ConversationHandler.END
    else:
        update.message.reply_text("Выберите один из вариантов",
                                  reply_markup=keypad_with_target_selection())
        return "target_selection"


def target_weight(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    current_weight = user["questionnaire"][-1]["current_weight"]
    change_multiplier = context.user_data["calorie_calculation"]["change_multiplier"]
    user_response = update.message.text

    if user_response.isdigit():
        delta_weight = int(user_response)
        target_weight = current_weight + change_multiplier*delta_weight
    elif emoji_to_the_number_of(user_response).isdigit():
        delta_weight = int(emoji_to_the_number_of(user_response))
        target_weight = current_weight + change_multiplier*delta_weight
    else:
        update.message.reply_text("Введите целое число кг", reply_markup=keypad_with_weight_selection())
        return "target_weight"

    if target_weight < 0:
        update.message.reply_text("Желаемый вес меньше нуля", reply_markup=keypad_with_weight_selection())
        return "target_weight"
    else:
        context.user_data["calorie_calculation"]["target_weight"] = target_weight
        сalculate_сalorie_сount(update, context)
        return ConversationHandler.END


def сalculate_сalorie_сount(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_data = user["questionnaire"][-1]

    gender = user_data["gender"]
    age = user_data["age"]
    height = user_data["height"]
    weight = context.user_data["calorie_calculation"]["target_weight"]
    level_of_physical_activity = user_data["level_of_physical_activity"]
    multiplier_activity_level = activity_level_multiplier(level_of_physical_activity)

    calorie_count = calorie_сalculation(
        gender, age, height, weight, multiplier_activity_level
    )

    add_or_replace_something(db, user['user_id'], "calorie_count", calorie_count)
    add_or_replace_something(db, user['user_id'], "target_weight", weight)

    update.message.reply_text(f"Вам нужно потреблять {calorie_count} калорий ежедневно", reply_markup=main_keyboard())
    