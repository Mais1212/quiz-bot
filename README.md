# QUIZ BOT

Бот-викторина.

Пример бота телеграм бота - https://t.me/quizzzzmow_bot.

## Как запустить 
- Для запуска библиотеки у вас уже должен быть установлен [Python 3](https://www.python.org/downloads/).
- Установите зависимости командой:
```
pip install -r requirements.txt
```
- Настроить переменные окружения.
- Запустите [telegram](https://telegram.org/) бота  командой:
```
python tg_bot.py
```
- Запустить [VK](https://vk.com/) бота:
```
python vk_bot.py
```

## Переменные окружения
Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл .env рядом в корне проекта и запишите туда данные в таком формате: ПЕРЕМЕННАЯ=значение.

Необходимы следущие переменные:
- `TELEGRAM_TOKEN` — Telegram token вашего бота, для получения нужно написать @BotFather в телеграме.
- `VK_TOKEN` — VK token c возможностью отправлять сообщения. Как [получить](https://pechenek.net/social-networks/vk/api-vk-poluchaem-klyuch-dostupa-token-gruppy/).
- `DB_HOST` – URL адрес бызы данных [Redis](https://redis.com/).
- `DB_PASSWORD` – Порт [Redis](https://redis.com/).
- `DB_USERNAME` – Пароль от [Redis](https://redis.com/).
- `DB_PORT` – Имя пользователя [Redis](https://redis.com/).
## Вопросы
Вопросы берутся из файлов, находящихся внутри папки `questions`. Каждый файл `questions` должен иметь кодировку `KOI-8` и следовать формату:
```
Вопрос xx:
...

Ответ:
...
```