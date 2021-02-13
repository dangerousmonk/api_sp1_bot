import os
import time
import requests
import telegram
import logging.config
from requests.exceptions import RequestException
from json.decoder import JSONDecodeError

from helpers import LOGGING

PRAKTIKUM_TOKEN = os.environ['PRAKTIKUM_TOKEN']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PRAKTIKUM_API_HOMEWORK_URL = \
    'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


def parse_homework_status(homework):
    statuses = {
        'rejected': 'К сожалению в работе нашлись ошибки.',
        'reviewing': 'Вашу работу приняли на ревью!',
        'approved': 'Ревьюеру всё понравилось, можно приступать к следующему уроку.',
    }
    homework_name = homework.get('homework_name', 'unknown_name')
    homework_status = homework.get('status', 'unknown_status')
    verdict = statuses.get(homework_status, 'unknown_verdict')
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
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                    new_homework.get('homeworks')[0]
                ), bot)
                logger.info('Отправлено сообщение')
            current_timestamp = new_homework.get(
                'current_date',
                current_timestamp
            )
        except (RequestException, KeyError, JSONDecodeError) as error:
            send_message(f'Бот столкнулся с ошибкой: {error}', bot)
            logger.exception(error)
        time.sleep(20 * 60)


if __name__ == '__main__':
    main()
