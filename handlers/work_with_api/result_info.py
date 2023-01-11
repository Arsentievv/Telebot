import datetime
import json
from json import JSONDecodeError

from loguru import logger
from telebot.types import InputMediaPhoto

from config_data.config import headers
from database.models import *
from handlers.work_with_api import request
from loader import bot


def hotels(user, chat):

    """
        Функция для получуния необходимых данных из API по заданной от пользователя команде
        :param user: Any - id пользователя
        :param chat: Any - id чата
        :return None

    """
    url = "https://hotels4.p.rapidapi.com/properties/list"
    with bot.retrieve_data(user, chat) as data:
        priceMin = ''
        priceMax = ''
        landmarkIds = ''
        if data['command'] == '/lowprice':
            sortOrder = 'PRICE'

        elif data['command'] == '/highprice':
            sortOrder = 'PRICE_HIGHEST_FIRST'

        elif data['command'] == '/bestdeal':
            sortOrder = 'DISTANCE_FROM_LANDMARK'
            landmarkIds = 'Центр города'
            priceMin = data['min_price']
            priceMax = data['max_price']

        querystring = {"destinationId": data['location_id'], "pageNumber": "1", "pageSize": "25",
                       "checkIn": data['date_arrival'], "checkOut": data['date_depature'],
                       "adults1": "1", "sortOrder": sortOrder, "locale": "ru_RU",
                       "currency": "RUB", 'landmarkIds': landmarkIds}

        querystring_best = {"destinationId": data['location_id'], "pageNumber": '1', "pageSize": '25',
                            "checkIn": data['date_arrival'], "checkOut": data['date_depature'],
                            "adults1": '1', "priceMin": priceMin, "priceMax": priceMax,
                            "sortOrder": sortOrder, "locale": 'ru_RU', "currency": 'RUB',
                            "landmarkIds": landmarkIds}

        if data['command'] == '/lowprice' or data['command'] == '/highprice':
            hotels_low_high(user=user, chat=chat, url=url, querystring=querystring)

        elif data['command'] == '/bestdeal':
            try:

                response = request.get_request(url=url, headers=headers, params=querystring_best)
                data_hotels = json.loads(response.text)
                hotels_info = data_hotels['data']['body']['searchResults']['results']
                result_hotels = []

                for hotel in hotels_info:
                    if hotel['name'] and hotel['id'] and hotel['address']['streetAddress'] and hotel[
                        'landmarks'][0]['label'] and hotel['landmarks'][1]['label'] and hotel['ratePlan']['price'][
                        'exactCurrent'] and float(hotel['landmarks'][0]['distance'][:3].replace(',', '.')) <= float(
                        data['max_distance']):
                        result_hotels.append(hotel)

            except (KeyError, TypeError, LookupError, ValueError, IndexError) as exc:
                logger.exception(exc)
            result_hotels_sorted = sorted(result_hotels, key=lambda elem: elem['ratePlan']['price']['exactCurrent'])

            if len(result_hotels_sorted) == 0:
                bot.send_message(user, 'К сожалению, не удалось найти отели, удовлетворяющие вашему запросу.\n'
                                       'Попробуйте изменить условия поиска и попробуйте снова.')
                logger.info('К сожалению, не удалось найти отели, удовлетворяющие вашему запросу.\n'
                            'Попробуйте изменить условия поиска и попробуйте снова.')

            elif len(result_hotels_sorted) < int(data['hotel_amt']):
                bot.send_message(user, f'К сожалению, удалось найти только {len(result_hotels_sorted)} отелей.\n'
                                       f'Попробуйте изменить условия поиска и попробуйте снова.')
                logger.info(f'К сожалению, удалось найти только {len(result_hotels_sorted)} отелей.\n'
                            f'Попробуйте изменить условия поиска и попробуйте снова.')

            if result_hotels_sorted:
                logger.info(f'Результат поиска отелей для пользователя {user}:\n')
                for hotel in result_hotels_sorted[:int(data['hotel_amt'])]:
                    send_info_hotel(user, chat, hotel=hotel)


def hotels_low_high(user, chat, url, querystring):

    """
    Функция для получения необходимой информации об отелях для команд lowprice и highprice
    :param user: Any - id пользователя
    :param chat: Any - id чата
    :param url: Any - вэб-страница API
    :param querystring - параметры поиска в API
    :return None


    """
    with bot.retrieve_data(user, chat) as data:
        try:
            response = request.get_request(url=url, headers=headers, params=querystring)
            data_loads = json.loads(response.text)
            hotels_info = data_loads['data']['body']['searchResults']['results']
            result_hotels = []

            for hotel in hotels_info:

                if hotel['name'] and hotel['id'] and hotel['address']['streetAddress'] and hotel[
                    'landmarks'][0]['label'] and hotel['landmarks'][1]['label'] and hotel['ratePlan']['price'][
                    'exactCurrent']:
                    result_hotels.append(hotel)

        except (KeyError, ValueError, LookupError, TypeError, IndexError, JSONDecodeError) as exc:
            logger.exception(exc)

        if len(result_hotels) == 0:
            bot.send_message(user, 'К сожалению, не удалось найти отели, удовлетворяющие вашему запросу.\n'
                                   'Попробуйте изменить условия поиска и попробуйте снова.')
            logger.info('К сожалению, не удалось найти отели, удовлетворяющие вашему запросу.\n'
                        'Попробуйте изменить условия поиска и попробуйте снова.')

        elif len(result_hotels) < int(data['hotel_amt']):
            bot.send_message(user, f'К сожалению, удалось найти только {len(result_hotels)} отелей.\n'
                                   f'Попробуйте изменить условия поиска и попробуйте снова.')

        if result_hotels:
            logger.info(f'Результат поиска отелей для пользователя {user}:\n')
            for hotel in result_hotels[:int(data['hotel_amt'])]:
                send_info_hotel(user, chat, hotel=hotel)

        # except (KeyError, ValueError, LookupError, TypeError, IndexError, JSONDecodeError) as exc:
        #     logger.exception(exc)


def photo(user, chat, id_hotel):
    """
    Функция для получения фото отеля из API
    :param user: Any - id пользователя
    :param chat: Any - id чата
    :param id_hotel: int - id отеля
    :return: [photo]
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    try:
        with bot.retrieve_data(chat, user) as data:
            querystring = {'id': id_hotel}

            response = request.get_request(url=url, headers=headers, params=querystring)
            photos = json.loads(response.text)
            photos_info = photos['hotelImages'][:int(data['photo_amt'])]
            photo_medea = []
            for picture in photos_info:
                url_photo = picture['baseUrl'].replace('_{size}', '')
                photo_medea.append(url_photo)
            return photo_medea

    except (TypeError, AttributeError, JSONDecodeError) as exc:
        logger.exception(exc)


def send_info_hotel(user, chat, hotel):
    """
    Функция для отправки пользователю информации об отелях в виде сформированной медиаг-группы
    :param user: Any - id пользователя
    :param chat: Any - id чата
    :param hotel: Any - найденный отель
    :return: [media-group]
    """
    try:
        with bot.retrieve_data(user, chat) as data:
            hotel_name = hotel['name']
            hotel_id = data['hotel_id'] = hotel['id']
            address = hotel['address']['streetAddress']
            rating = hotel['starRating']
            name_lable_1 = hotel['landmarks'][0]['label']
            distance_from_lable_1 = hotel['landmarks'][0]['distance']
            name_lable_2 = hotel['landmarks'][1]['label']
            distance_from_lable_2 = hotel['landmarks'][1]['distance']
            price = hotel['ratePlan']['price']['exactCurrent']
            a = data['date_depature'].split('-')
            b = data['date_arrival'].split('-')
            aa = datetime.date(int(a[0]), int(a[1]), int(a[2]))
            bb = datetime.date(int(b[0]), int(b[1]), int(b[2]))
            rest_days = (aa - bb).days
            full_price = round(price * rest_days, 2)

            find_info = (f'Название отеля : {hotel_name}\n'
                         f'Сайт : https://hotels4.p.rapidapi.com/no{hotel_id}\n'
                         f'Адресс : {address}\n'
                         f'Рейтинг (количество звезд): {rating}\n'
                         f'Расстояние от отеля до {name_lable_1}: {distance_from_lable_1}\n'
                         f'Расстояние от отеля до {name_lable_2}: {distance_from_lable_2}\n'
                         f'Стоимость проживания за 1 сутки : {price} рублей\n'
                         f'Стоимость проживания за {rest_days} суток: {full_price} рублей')
            logger.info(f'Отель по результатам поиска для пользователя {user}: {find_info}\n')

            if data['photo_amt'] == '0':
                bot.send_message(user, find_info)

            else:
                find_media = photo(user, chat, id_hotel=hotel_id)

                media_group = [InputMediaPhoto(find_media[num_photo], find_info)
                               if num_photo == len(find_media) - 1 else InputMediaPhoto(
                    find_media[num_photo]) for num_photo in range(len(find_media))]

                bot.send_media_group(chat, media_group)
            hotel_bd = History(command=data['command'], date=datetime.datetime.now(), info=str(find_info)).save(
                force_insert=True)
    except (KeyError, ValueError, LookupError, TypeError, IndexError, JSONDecodeError) as exc:
        logger.exception(exc)
