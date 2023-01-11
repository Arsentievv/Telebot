from peewee import *
from telebot.types import Message

from database.models import History, database
from loader import bot


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:

    with database:
        a = History.select().where(History.id)
        for i in a:
            bot.send_message(message.from_user.id, f'Номер запроса :{i.id}\n Дата и время : {i.date}\n'
                                                   f'Информация об отеле : {i.info}')