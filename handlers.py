from untils import initial_keyboard, main_keyboard, get_emoji

from db import db, get_or_create_user


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    if 'questionnaire' not in user:
        keyboard = initial_keyboard()
    else:
        keyboard = main_keyboard()
    update.message.reply_text(
        f"Здравствуй {user['first_name']}! {get_emoji('waving_hand')}",
        reply_markup=keyboard,
    )


def unknown_command(update, context):
    update.message.reply_text(f"Неизвестная команда {get_emoji('red_question_mark')}", reply_markup=main_keyboard())
