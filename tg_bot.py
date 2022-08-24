import logging
import os
from functools import partial
import random

import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from tools.questions import get_questions

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start_bot(tg_bot_token: str) -> None:
    """Start the bot."""
    questions = get_questions()

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", _start))
    dispatcher.add_handler(MessageHandler(
        Filters.text, partial(_message_check, questions=questions)))
    updater.start_polling()
    updater.idle()


def _create_keyboard() -> telegram.replykeyboardmarkup.ReplyKeyboardMarkup:
    """Create keyboard markup."""
    key_Board = [
        ["Новый вопрос", "Сдаться"],
        ['Счёт']
    ]
    markup = telegram.ReplyKeyboardMarkup(
        key_Board,
        resize_keyboard=True
    )

    return markup


def _start(bot, update) -> None:
    """Send a message when the command /start is issued."""
    keyboard = _create_keyboard()
    update.message.reply_text("Я - викторина.", reply_markup=keyboard)


def _message_check(bot, update, questions) -> None:
    """Echo the user message."""
    if update.message.text == "Новый вопрос":
        random_question = random.choice(questions)
        update.message.reply_text(random_question.question)


def main() -> None:
    tg_bot_token = os.getenv("TG_BOT_KEY")
    start_bot(tg_bot_token)


if __name__ == '__main__':
    main()
