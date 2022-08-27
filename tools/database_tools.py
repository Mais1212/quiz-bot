import os

import redis
from dotenv import load_dotenv

load_dotenv()


def connecte_database():
    database = redis.Redis(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        password=os.getenv("DB_PASSWORD"),
        username=os.getenv("DB_USERNAME"),
        decode_responses=True
    )

    return database
