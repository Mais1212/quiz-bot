import logging
import os
import random
from functools import partial

import redis
import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from tools import database_tools, questions_tools

load_dotenv()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start_bot(
        tg_bot_token: str, questions: list[questions_tools.Question],
        database: redis.client.Redis) -> None:
    """Start the bot."""

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler(
            "start",
            _start)
    )
    dispatcher.add_handler(
        MessageHandler(
            Filters.text, partial(
                _message_check,
                questions=questions,
                database=database
            )
        )
    )

    updater.start_polling()
    updater.idle()


def _create_keyboard() -> telegram.replykeyboardmarkup.ReplyKeyboardMarkup:
    """Create keyboard markup."""
    key_Board = [
        ["Новый вопрос", "Сдаться"],
        ["Счёт"]
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


def _message_check(bot, update, questions: list[questions_tools.Question],
                   database: redis.client.Redis) -> None:
    """Echo the user message."""
    if update.message.text == "Новый вопрос":
        random_question = random.choice(questions)
        database.set(update.message.chat.id, random_question.answer)
        update.message.reply_text(random_question.question)


def main() -> None:
    questions = questions_tools.get_questions()
    tg_bot_token = os.getenv("TG_BOT_KEY")
    database = database_tools.connecte_database()

    start_bot(
        tg_bot_token=tg_bot_token,
        database=database,
        questions=questions
    )


if __name__ == "__main__":
    main()
