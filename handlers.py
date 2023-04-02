from untils import initial_keyboard, main_keyboard, questionnaire_completion, calorie_сalculation, get_emoji

from db import db, get_or_create_user


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(
        f"Здравствуй {user['first_name']}! {get_emoji('waving_hand')}",
        reply_markup=initial_keyboard(),
    )


def calorie_count(update, context):
    user_data = questionnaire_completion(context)
    if user_data is None:
        update.message.reply_text(
            f"Заполните анкету! {get_emoji('pencil')}",
            reply_markup=main_keyboard()
        )
    else:
        user_gender = user_data[0]
        user_age = int(user_data[1])
        user_height = int(user_data[2])
        user_weight = int(user_data[3])
        user_activity_level_multiplier = user_data[4]
        calorie_count = calorie_сalculation(
            user_gender, user_age, user_height, user_weight, user_activity_level_multiplier)
        update.message.reply_text(
            f"Вам нужно потреблять {round(calorie_count, 0)} калорий",
            reply_markup=main_keyboard())


def unknown_command(update, context):
    update.message.reply_text(f"Неизвестная команда {get_emoji('red_question_mark')}", reply_markup=main_keyboard())
