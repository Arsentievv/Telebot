# from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
#
# from handlers.work_with_api import result_info
# from keyboards.reply import location
# from keyboards.reply.location import get_location
# from loader import bot
# from states.required_info import UserInfoSurvey
# from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
#
#
#
# @bot.message_handler(commands=['survey'])
# def lowprice(message: Message) -> None:
#     bot.set_state(message.from_user.id, UserInfoSurvey.city, message.chat.id)
#     bot.send_message(message.from_user.id,
#                      f'Привет {message.from_user.full_name}, я помогу вам с выбором отеля.'
#                      f'\nВведите город на русском языке:')
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['command'] = 'survey'
#
# @bot.message_handler(state=UserInfoSurvey.city)
# def get_city(message: Message) -> None:
#     if message.text.isalpha():
#         bot.send_message(message.from_user.id, 'Отлично! Теперь введите сколько отелей выводить'
#                                                '\n(Не более 5)')
#         bot.set_state(message.from_user.id, UserInfoSurvey.hotel_amt, message.chat.id)
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['city'] = message.text
#
#     else:
#         bot.send_message(message.from_user.id, 'Введите корректное название города.')
#
#
# @bot.message_handler(state=UserInfoSurvey.hotel_amt)
# def get_hotel_amt(message: Message) -> None:
#     if message.text.isdigit() and int(message.text) <= 5:
#         calendar, step = DetailedTelegramCalendar(calendar_id=1, locale='ru').build()
#         bot.send_message(message.chat.id,
#                          f"Select {LSTEP[step]}",
#                          reply_markup=calendar)
#
#         bot.set_state(message.from_user.id, UserInfoSurvey.date_arrival, message.chat.id)
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['hotel_amt'] = message.text
#
#     else:
#         bot.send_message(message.from_user.id, 'Введите число от 1 до 5')
#
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
# def cal(c):
#     result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='ru').process(c.data)
#     if not result and key:
#         bot.edit_message_text(f"Select {LSTEP[step]}",
#                               c.message.chat.id,
#                               c.message.message_id,
#                               reply_markup=key)
#     elif result:
#         bot.edit_message_text(f"You selected {result}",
#                               c.message.chat.id,
#                               c.message.message_id)
#
#     bot.set_state(c.from_user.id, UserInfoSurvey.date_arrival)
#
#     with bot.retrieve_data(c.from_user.id) as data:
#         data['date_arrival'] = c.data
#
#
# @bot.message_handler(state=UserInfoSurvey.date_arrival)
# def get_date_arrival(message: Message) -> None:
#     if message.text:
#         bot.send_message(message.from_user.id,
#                          'Отлично! Теперь введите дату выезда в формате "yyyy-MM-dd":')
#         bot.set_state(message.from_user.id, UserInfoSurvey.date_depature, message.chat.id)
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['date_arrival'] = message.text
#
#     else:
#         bot.send_message(message.from_user.id, 'Введите дату выезда в формате "yyyy-MM-dd"')
#
# @bot.message_handler(state=UserInfoSurvey.date_depature)
# def get_date_depatere(message: Message) -> None:
#
#     a = location.get_location(message)
#     destinations = InlineKeyboardMarkup()
#     for city in a:
#
#         print(city[0])
#         button = InlineKeyboardButton(text=city[0], callback_data=city[1])
#         destinations.add(button)
#     bot.send_message(message.from_user.id,
#                         'Отлично! Теперь введите точную локацию:\n'
#                         '(Набор цифр под названием места)', reply_markup=destinations)
#     bot.set_state(message.from_user.id, UserInfoSurvey.location_id, message.chat.id)
#
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['date_depature'] = message.text
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def get_location_id(call) -> None:
#     bot.send_message(call.from_user.id, 'Введите сколько фото выводить:\n'
#                                             '(Введите число от 0 до 5)')
#
#     bot.set_state(call.from_user.id, UserInfoSurvey.photo_amt)
#
#     with bot.retrieve_data(call.from_user.id) as data:
#         data['location_id'] = call.data
#
#         text = f'Ваш запрос: ' \
#                f'\nГород : {data["location_id"]}' \
#                f'\nКоличество отелей : {data["hotel_amt"]}' \
#                f'\nКоличество фото : {data["photo_amt"]}' \
#                f'\nДата заезда : {data["date_arrival"]}' \
#                f'\nДата выезда: {data["date_depature"]}' \
#                f'\nКоличество фото: {data["photo_amt"]}'
#         print(text)
#
#
# @bot.message_handler(state=UserInfoSurvey.photo_amt)
# def photo_amt(message: Message) -> None:
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['photo_amt'] = message.text
#
#     text = f'Ваш запрос: ' \
#         f'\nГород : {data["city"]}' \
#         f'\nКоличество отелей : {data["hotel_amt"]}' \
#         f'\nКоличество фото : {data["photo_amt"]}' \
#         f'\nДата заезда : {data["date_arrival"]}' \
#         f'\nДата выезда: {data["date_depature"]}' \
#         f'\nКоличество фото: {data["photo_amt"]}'
#     bot.send_message(message.from_user.id, text)
#
#
#
#
#
#
