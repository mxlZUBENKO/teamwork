import logging
from telegram.ext import Updater
import settings

logging.basicConfig(filename="bot.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def main():
    bot = Updater(settings.API_KEY, use_context=True)

    dp = bot.dispatcher

    logging.info("bot started")
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
