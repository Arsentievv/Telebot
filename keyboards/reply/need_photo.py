from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def need_photo() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True, row_width=1)
    yes = KeyboardButton('Да!')
    no = KeyboardButton('Нет')
    keyboard.add(yes, no)

    return keyboard