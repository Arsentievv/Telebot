from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!\nВыберите одну из команд:\n "
                          f"/help - Вывести справку\n"
                          f"/highprice - Лучшие отели\n"
                          f"/lowprice - Эконом-вариант\n"
                          f"/bestdeal - Лучшее предложение\n"
                          f"/history - История поиска\n")

