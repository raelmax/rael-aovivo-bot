import re
import os
import random
import logging

from telegram import Update
from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CallbackContext,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
audio_numbers = []
token = os.environ.get("RAELAOVIVOBOT_TELEGRAM_TOKEN")
assert token is not None, "RAELAOVIVOBOT_TELEGRAM_TOKEN envvar required, idiot."


def _get_random_audio():
    global audio_numbers

    if len(audio_numbers) == 0:
        audio_numbers = list(range(1, 17))

    random.shuffle(audio_numbers)
    random_number = audio_numbers.pop()
    return open(f"./audios/{random_number}.ogg", "rb")


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    audio = _get_random_audio()
    update.message.reply_audio(audio)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile(r"rael", re.IGNORECASE)), echo)
    )

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
