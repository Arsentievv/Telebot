import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv('.env.template'):
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv('.env.template')

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

DEFAULT_COMMANDS = (
    ('/start', "Запустить бота"),
    ('/help', "Вывести справку"),
    ('/survey', "Опрос"),
    ('/highprice', "Лучшие отели"),
    ('/lowprice', "Эконом-вариант"),
    ('/bestdeal', "Лучшее предложение"),
    ('/history', "История поиска")

)
