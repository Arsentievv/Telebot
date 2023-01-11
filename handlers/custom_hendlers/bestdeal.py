from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from handlers.work_with_api import result_info
from keyboards.reply import location
from loader import bot
from states.required_info import UserInfoBest


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    """
        Функция для определения команды, введеной пользователем
        :param message: Сообщение пользователя
    """

    bot.set_state(message.from_user.id, UserInfoBest.city, message.chat.id)
    bot.send_message(message.from_user.id,
                     f'Привет {message.from_user.full_name}, я помогу вам с выбором отеля.'
                     f'\nВведите город на русском языке:')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = '/bestdeal'

@bot.message_handler(state=UserInfoBest.city)
def get_city(message: Message) -> None:
    """
            Функция для определения города, введеного пользователем
            :param message: Сообщение пользователя
    """

    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Отлично! Теперь введите сколько отелей выводить'
                                               '\n(Не более 5)')
        bot.set_state(message.from_user.id, UserInfoBest.hotel_amt, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Введите корректное название города.')


@bot.message_handler(state=UserInfoBest.hotel_amt)
def get_hotel_amt(message: Message) -> None:
    """
            Функция для определения количества отелей для вывода пользователю
            :param message: Сообщение пользователя
    """

    if message.text.isdigit() and int(message.text) <= 5:
        bot.send_message(message.from_user.id,
                         'Отлично! Теперь введите дату заезда в формате "yyyy-MM-dd":')
        bot.set_state(message.from_user.id, UserInfoBest.date_arrival, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotel_amt'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Введите число от 1 до 5')


@bot.message_handler(state=UserInfoBest.date_arrival)
def get_date_arrival(message: Message) -> None:
    """
            Функция для определения даты въезда в отель
            :param message: Сообщение пользователя
    """

    if message.text:
        bot.send_message(message.from_user.id,
                         'Отлично! Теперь введите дату выезда в формате "yyyy-MM-dd":')
        bot.set_state(message.from_user.id, UserInfoBest.date_depature, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['date_arrival'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Введите дату выезда в формате "yyyy-MM-dd"')

@bot.message_handler(state=UserInfoBest.date_depature)
def get_date_depatere(message: Message) -> None:
    """
            Функция для поределения даты выезда из отеля
            :param message: Сообщение пользователя
    """

    if message.text:
        bot.send_message(message.from_user.id,
                         'Отлично! Теперь введите максимально-допустимую дистанцию от центра города(км):')
        bot.set_state(message.from_user.id, UserInfoBest.max_distance, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['date_depature'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Введите численное значение расстояния.')


@bot.message_handler(state=UserInfoBest.max_distance)
def get_max_distance(message: Message) -> None:
    """
            Функция для определения максимальной дистанции от центра города
            :param message: Сообщение пользователя
    """

    if message.text:
        bot.send_message(message.from_user.id,
                         'Отлично! Теперь введите минимальную допустимую цену за сутки:')
        bot.set_state(message.from_user.id, UserInfoBest.min_price, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_distance'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Введите численное значение цены.')

@bot.message_handler(state=UserInfoBest.min_price)
def get_min_price(message: Message) -> None:
    """
            Функция для определения минимальной-допустимой цены за сутки проживания
            :param message: Сообщение пользователя
    """

    if message.text:
        bot.send_message(message.from_user.id,
                         'Отлично! Теперь введите максимальную допустимую цену за сутки:')
        bot.set_state(message.from_user.id, UserInfoBest.max_price, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Введите численное значение цены.')

@bot.message_handler(state=UserInfoBest.max_price)
def get_max_price(message: Message) -> None:
    """
            Функция для определения максимальной-допустимой цены за сутки проживания
            :param message: Сообщение пользователя
    """

    a = location.get_location(message)
    destinations = InlineKeyboardMarkup()
    for city in a:
        button = InlineKeyboardButton(text=city[0], callback_data=city[1])
        destinations.add(button)
    bot.send_message(message.from_user.id,
                     'Отлично! Теперь введите точную локацию:\n'
                     '(Набор цифр под названием места)', reply_markup=destinations)
    bot.set_state(message.from_user.id, UserInfoBest.location_id, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_price'] = message.text


@bot.callback_query_handler(func=lambda call: True)
def get_location_id(call) -> None:
    """
            Функция для определения точной локации в городе при помощи клавиатуры
            :param call: запрос обраатного вызова с сообщением
    """

    bot.send_message(call.from_user.id, 'Введите сколько фото выводить:\n'
                                            '(Введите число от 0 до 5)')

    bot.set_state(call.from_user.id, UserInfoBest.photo_amt)

    with bot.retrieve_data(call.from_user.id) as data:
        data['location_id'] = call.data


@bot.message_handler(state=UserInfoBest.photo_amt)
def photo_amt(message: Message) -> None:
    """
            Функция для определения необходимого количества фото отелей пользователю
            :param message: Сообщение пользователя
    """

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['photo_amt'] = message.text

    text = f'Ваш запрос: ' \
        f'\nГород : {data["city"]}' \
        f'\nКоличество отелей : {data["hotel_amt"]}' \
        f'\nКоличество фото : {data["photo_amt"]}' \
        f'\nДата заезда : {data["date_arrival"]}' \
        f'\nДата выезда: {data["date_depature"]}' \
        f'\nКоличество фото: {data["photo_amt"]}'
    bot.send_message(message.from_user.id, text)

    result_info.hotels(message.from_user.id, message.chat.id)







