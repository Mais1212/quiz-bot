import os
import random

import redis
import vk_api as vk
from dotenv import load_dotenv
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll

from tools import questions_tools

load_dotenv()


def start_bot(
        vk_session: vk.vk_api.VkApi, database: redis.client.Redis) -> None:
    """Start the bot."""
    vk_api = vk_session.get_api()
    keyboard = create_keyboard()
    longpoll = VkLongPoll(vk_session)
    questions = questions_tools.get_questions()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(
                event, vk_api, keyboard=keyboard, database=database,
                questions=questions
            )


def create_keyboard() -> vk.keyboard.VkKeyboard:
    "Create vk keyboard."
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.POSITIVE)

    return keyboard


def handle_message(
        event, vk_api, keyboard: vk.keyboard.VkKeyboard,
        database: redis.client.Redis,
        questions: list[questions_tools.Question]) -> None:

    user_id = event.user_id

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.text == "Новый вопрос":
            random_question = random.choice(questions)
            database.set(user_id, random_question.answer)
            message_text = random_question.question
        elif event.text == "Сдаться":
            if database.get(user_id):
                message_text = database.get(user_id)
                database.delete(user_id)
            else:
                message_text = "Нажмите 'Новый вопрос'."
        elif event.text == database.get(user_id):
            message_text = "Правильно."
            database.delete(user_id)
        else:
            message_text = "Неправильно."

    vk_api.messages.send(
        user_id=user_id,
        message=message_text,
        keyboard=keyboard.get_keyboard(),
        random_id=random.randint(1, 1000)
    )


def main() -> None:
    vk_token = os.getenv("VK_TOKEN")

    vk_session = vk.VkApi(token=vk_token)
    database = redis.Redis(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        password=os.getenv("DB_PASSWORD"),
        username=os.getenv("DB_USERNAME"),
        decode_responses=True
    )

    start_bot(vk_session, database)


if __name__ == "__main__":
    main()
