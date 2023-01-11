from telebot import types

from loader import bot


@bot.message_handler(commands=['help'])
def options(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    lowprice = types.KeyboardButton('Низкая цена')
    highprice = types.KeyboardButton('Высокая цена')
    bestdeal = types.KeyboardButton('Лучшее предложение')
    history = types.KeyboardButton('История поиска')
    keyboard.add(lowprice, highprice, bestdeal, history)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    return keyboard