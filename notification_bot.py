import argparse
import logging
import os
import time

import requests
import textwrap as tw
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from telegram import Bot


def send_text(chat_id, reviews_params, bot):
    lesson_title = reviews_params['new_attempts'][0]['lesson_title']
    lesson_url = reviews_params['new_attempts'][0]['lesson_url']
    if reviews_params['new_attempts'][0]['is_negative']:
        bot.send_message(
            chat_id=chat_id,
            text=tw.dedent(f'''
Преподаватель проверил урок: "{lesson_title}"
               
К сожалению, в работе нашлись ошибки. 
Вот ссылка на работу: {lesson_url}'''
            )
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text=tw.dedent(f'''
Преподаватель проверил урок: "{lesson_title}"
                
Ваша работа принята!
Отлично! Приступайте к следующему уроку'''
            )
        )


def check_status_lesson_verification(chat_id, url, devman_token, bot):
    timestamp = int(time.time())
    while True:
        try:
            headers = {
                "Authorization": devman_token
            }
            params = {'timestamp': timestamp}
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=10
                )
            response.raise_for_status()
            reviews_params = response.json()
            if reviews_params['status'] == 'found':
                send_text(
                    chat_id=chat_id,
                    reviews_params=reviews_params,
                    bot=bot
                    )
                timestamp = reviews_params['last_attempt_timestamp']
            elif reviews_params['status'] == 'timeout':
                timestamp = reviews_params['timestamp_to_request']

        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            bot.send_message(
                chat_id=chat_id,
                text="Нет соединения с интернетом"
            )
            time.sleep(10)
            pass

class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'chat_id',
        type=int,
        help='chat_id вашего телеграма'
    )
    args = parser.parse_args()

    load_dotenv()
    token = os.getenv('TG_BOT_TOKEN')
    devman_token = os.getenv('DEVMAN_TOKEN')

    url = 'https://dvmn.org/api/long_polling/'
    bot = Bot(token=token)

    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger = logging.getLogger("Devbot")
    logger.setLevel(logging.INFO)
    # logger.info("Бот запущен")
    logger.addHandler(TelegramLogsHandler(
        bot=bot,
        chat_id=args.chat_id
        )
    )
    logger.info("Бот запущен")

    check_status_lesson_verification(
        chat_id=args.chat_id,
        url=url,
        devman_token=devman_token,
        bot=bot
    )



