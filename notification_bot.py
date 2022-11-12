import os
import time

import requests
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import CommandHandler, Updater


def start(update, context):
    user_fullname = str(update.message.from_user['first_name']) + ' ' + str(
        update.message.from_user['last_name'])

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Здравствуйте {user_fullname}. Этот бот будет контролировать'
             f'статус проверки сданных вами работ на платформе Dewman'
    )
    return check_status_lesson_verification(update, context)


def send_dewman_request(dewman_token, url):
    headers = {
        "Authorization": dewman_token
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def send_dewman_params_request(timestamp, dewman_token, url):
    headers = {
        "Authorization": dewman_token
    }
    params = {'timestamp': timestamp}
    response = requests.get(url,
                            headers=headers,
                            params=params,
                            timeout=10)
    response.raise_for_status()
    return response.json()


def send_text(update, context, response_params):
    lesson_title = response_params['new_attempts'][0]['lesson_title']
    lesson_url = response_params['new_attempts'][0]['lesson_url']
    if response_params['new_attempts'][0]['is_negative']:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Преподаватель проверил урок: "{lesson_title}" \n \n'
                 f'К сожалению, в работе нашлись ошибки. \n'
                 f'Вот ссылка на работу: {lesson_url}'
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Преподаватель проверил урок: "{lesson_title}" \n \n'
                 f'Ваша работа принята!\n'
                 f'Отлично! Приступайте к следующему уроку')


def check_status_lesson_verification(update, context):
    response_params = send_dewman_request(dewman_token=dewman_token,
                                          url=url)
    if response_params['status'] == 'found':
        send_text(update, context,
                  response_params=response_params)
        timestamp = response_params['last_attempt_timestamp']

    elif response_params['status'] == 'timeout':
        timestamp = response_params['timestamp_to_request']

    while True:
        try:
            response_params = send_dewman_params_request(timestamp=timestamp,
                                                         dewman_token=dewman_token,
                                                         url=url)
            if response_params['status'] == 'found':
                send_text(update, context,
                          response_params=response_params)
                timestamp = response_params['last_attempt_timestamp']
            elif response_params['status'] == 'timeout':
                timestamp = response_params['timestamp_to_request']

        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Нет соединения с интернетом"
            )
            time.sleep(10)
            pass


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TG_BOT_TOKEN")
    dewman_token = os.getenv("DEWMAN_TOKEN")

    url = 'https://dvmn.org/api/long_polling/'

    bot = Bot(token=token)
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    updater.idle()
