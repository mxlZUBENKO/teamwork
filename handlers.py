from untils import main_keyboard, questionnaire_completion, calorie_сalculation


def greet_user(update, context):
    update.message.reply_text(
        "Здравствуй пользователь!",
        reply_markup=main_keyboard(),
    )


def calorie_count(update, context):
    user_information = questionnaire_completion(context)
    if user_information is None:
        update.message.reply_text(
            "Заполните анкету!",
            reply_markup=main_keyboard()
        )
    else:
        user_gender = user_information[0]
        user_age = int(user_information[1])
        user_height = int(user_information[2])
        user_weight = int(user_information[3])
        user_activity_level_multiplier = user_information[4]
        calorie_count = calorie_сalculation(
            user_gender, user_age, user_height, user_weight, user_activity_level_multiplier)
        update.message.reply_text(
            f"Вам нужно потреблять {round(calorie_count, 0)} калорий",
            reply_markup=main_keyboard())
