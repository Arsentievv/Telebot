import json
import re

import requests

from loader import bot
from states import required_info
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_location(message):

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        url = "https://hotels4.p.rapidapi.com/locations/v2/search"
        querystring = {"query": data['city'], "locale": "ru_RU", "currency": "RUB"}
        headers = {
            "X-RapidAPI-Key": "27f91ee8ecmsh9b7fca5aca8b640p1badfajsnb1f98d2e4d1d",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.get(url=url, params=querystring, headers=headers)
        pattern = r'(?<="CITY_GROUP",).+?[\]]'
        find = re.search(pattern, response.text)
        if find:
            result = json.loads(f"{{{find[0]}}}")
            result_info = []
            for i in result['entities']:
                result_info += [(i['name'], i['destinationId'])]
            return result_info


# def get_location(message):
#
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         url = "https://hotels4.p.rapidapi.com/locations/v2/search"
#         querystring = {"query": data['city'], "locale": "ru_RU", "currency": "RUB"}
#         headers = {
#             "X-RapidAPI-Key": "27f91ee8ecmsh9b7fca5aca8b640p1badfajsnb1f98d2e4d1d",
#             "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
#         }
#
#         response = requests.get(url=url, params=querystring, headers=headers)
#         pattern = r'(?<="CITY_GROUP",).+?[\]]'
#         find = re.search(pattern, response.text)
#         if find:
#             result = json.loads(f"{{{find[0]}}}")
#             result_info = []
#             for i in result['entities']:
#                 result_info.append({'city_name': i['name'], 'destination_id': i['destinationId']})
#             print(result_info)
#             return result_info



