import os
import time
from dotenv import load_dotenv
import requests
import telegram
import datetime
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()


PRAKTIKUM_TOKEN = os.environ['PRAKTIKUM_TOKEN']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PRAKTIKUM_API_HOMEWORK_URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger('__name__')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('my_logger.log', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)

def parse_homework_status(homework):
    homework_name = homework['homework_name']
    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    params = {
        'from_date': current_timestamp
    }
    headers = {
        'Authorization': f'OAuth {PRAKTIKUM_TOKEN}',
    }
    homework_statuses = requests.get(PRAKTIKUM_API_HOMEWORK_URL, headers=headers, params=params)
    return homework_statuses.json()


def send_message(message, bot_client):
    bot_client = bot_client
    return bot_client.send_message(text=message, chat_id=CHAT_ID)


def main():
    # проинициализировать бота здесь
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    test_time_in_hours = datetime.datetime.fromtimestamp(current_timestamp) - datetime.timedelta(days=7)
    test_time_week = int(datetime.datetime.timestamp(test_time_in_hours))
    current_timestamp_week = test_time_week

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp_week)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]),bot)
            #current_timestamp = new_homework.get('current_date', current_timestamp)  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот столкнулся с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
