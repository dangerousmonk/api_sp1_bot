# Praktikum bot - бот для получения обновлений о статусе ревью проектов
## Развернут на https://www.heroku.com/


## Для работы потребуется
- Установить Python 3 в случае если он не установлен
- Склонировать проект и перейти в папку проекта
```bash
git clone https://github.com/dangerousmonk/api_sp1_bot/
cd api_sp1_bot
pip install -r requirements.txt
```
- Получить токен  https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a.
- Задать переменные окружения:
```bash
PRAKTIKUM_TOKEN = Здесь полученный ранее токен
TELEGRAM_TOKEN = Just talk to the @BotFather
CHAT_ID =Ваш ID, если не знаете - @userinfobot
```