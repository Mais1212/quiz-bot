import logging
import os
import random
from enum import Enum
from functools import partial

import redis
import telegram
from dotenv import load_dotenv
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, RegexHandler, Updater)

from tools import database_tools, questions_tools

load_dotenv()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class States(Enum):
    new_question = 0


def start_bot(
        tg_bot_token: str, questions: list[questions_tools.Question],
        database: redis.client.Redis) -> None:
    """Start the bot."""

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler(
        "start",
        _start
    )
    questions_handler = RegexHandler(
        "^Новый вопрос$",
        partial(
            _handle_new_question_request,
            questions=questions,
            database=database
        )
    )
    solution_handler = MessageHandler(
        Filters.text,
        partial(
            handle_solution_attempt,
            database=database
        )
    )
    give_up_handler = RegexHandler(
        "^Сдаться$",
        partial(
            _give_up_handle,
            database=database
        )
    )

    quiz_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            States.new_question: [
                questions_handler,
                give_up_handler,
            ],
        },
        fallbacks=[solution_handler]
    )

    dispatcher.add_handler(quiz_handler)

    updater.start_polling()
    updater.idle()


def _create_keyboard() -> telegram.replykeyboardmarkup.ReplyKeyboardMarkup:
    """Create keyboard markup."""
    key_Board = [
        ["Новый вопрос", "Сдаться"],
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

    return States.new_question


def _handle_new_question_request(
        bot, update, questions: list[questions_tools.Question],
        database: redis.client.Redis) -> None:
    """Echo the user message."""
    user_id = update.message.chat.id
    random_question = random.choice(questions)
    database.set(user_id, random_question.answer)
    update.message.reply_text(random_question.question)


def handle_solution_attempt(bot, update, database) -> None:
    user_id = update.message.chat.id
    correct_answer = database.get(user_id)
    if update.message.text == correct_answer:
        update.message.reply_text("Гратз, ты ответил правильно.")
    else:
        update.message.reply_text("Ты ошибаешься.")


def _give_up_handle(bot, update, database) -> None:
    user_id = update.message.chat.id
    if database.get(user_id):
        correct_answer = database.get(user_id)
        update.message.reply_text(f"Правильный ответ: {correct_answer}.")
        database.delete(user_id)
    else:
        update.message.reply_text(f"Нажмите 'Новый вопрос'.")


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
