import logging
from telegram.ext import (CommandHandler, MessageHandler, Filters, Updater,
                          ConversationHandler)
import settings

from questionnaire import (questionnaire_start, questionnaire_gender, questionnaire_age,
                           questionnaire_height, questionnaire_current_weight, level_of_physical_activity,
                           data_validation, questionnaire_dontknow)

from handlers import greet_user, calorie_count, unknown_command

logging.basicConfig(filename="bot.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def main():
    bot = Updater(settings.API_KEY, use_context=True)

    dp = bot.dispatcher

    questionnaire = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить данные)|^(Данные неверны. Заполнить снова)'), questionnaire_start)
            ],
        states={
            "gender": [MessageHandler(Filters.text, questionnaire_gender)],
            "age": [MessageHandler(Filters.text, questionnaire_age)],
            "height": [MessageHandler(Filters.text, questionnaire_height)],
            "current_weight": [MessageHandler(Filters.text, questionnaire_current_weight)],
            "level_of_physical_activity": [MessageHandler(Filters.text, level_of_physical_activity)],
            "data_validation": [MessageHandler(Filters.text, data_validation)]
        },
        fallbacks=[
            MessageHandler(Filters.video | Filters.photo | Filters.document | Filters.location,
                           questionnaire_dontknow)
        ]
    )
    dp.add_handler(questionnaire)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^Расчёт калорий$'), calorie_count))
    dp.add_handler(MessageHandler(
        Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location,
        unknown_command))

    logging.info("bot started")
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
