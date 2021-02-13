import os
import time
import requests
import telegram
import logging
from logging.handlers import RotatingFileHandler

from helpers import TokenFormatter

PRAKTIKUM_TOKEN = os.environ['PRAKTIKUM_TOKEN']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PRAKTIKUM_API_HOMEWORK_URL = \
    'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
LOG_FORMAT = '%(asctime)s, %(levelname)s, %(message)s, %(name)s'

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
)
logger = logging.getLogger(__name__)
handler = RotatingFileHandler('program.log', maxBytes=50000000, backupCount=5)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
handler.setFormatter(TokenFormatter(LOG_FORMAT))
logger.addHandler(handler)
for handler in logging.root.handlers:
    handler.setFormatter(TokenFormatter(LOG_FORMAT))


def parse_homework_status(homework):
    homework_name = homework['homework_name']
    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    elif homework['status'] == 'reviewing':
        verdict = 'Вашу работу приняли на ревью!'
    else:
        verdict = 'Ревьюеру всё понравилось, ' \
                  'можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    params = {
        'from_date': current_timestamp
    }
    headers = {
        'Authorization': f'OAuth {PRAKTIKUM_TOKEN}',
    }
    homework_statuses = requests.get(
        PRAKTIKUM_API_HOMEWORK_URL,
        headers=headers,
        params=params
    )
    return homework_statuses.json()


def send_message(message, bot_client):
    return bot_client.send_message(text=message, chat_id=CHAT_ID)


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    logger.debug('Запуск бота')
    current_timestamp = 0#int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                    new_homework.get('homeworks')[0]
                ), bot)
                logging.info('Отправлено сообщение')
            current_timestamp = new_homework.get(
                'current_date',
                current_timestamp
            )
            time.sleep(1200)

        except requests.exceptions.RequestException as error:
            send_message(f'Бот столкнулся с ошибкой: {error}', bot)
            logger.exception(error)
            time.sleep(1200)
        except KeyError as error:
            send_message(f'Бот столкнулся с ошибкой: {error}', bot)
            logger.exception(error)
            time.sleep(1200)
        except ValueError as error:
            send_message(f'Бот столкнулся с ошибкой: {error}', bot)
            logger.exception(error)
            time.sleep(1200)


if __name__ == '__main__':
    main()
