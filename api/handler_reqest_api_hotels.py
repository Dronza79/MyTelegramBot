import time
import json
from string import ascii_letters
import re

import requests
from transliterate import translit
from loader import bot, history, RapidAPI_Key


url = "https://hotels4.p.rapidapi.com/locations/v3/search"
headers = {"X-RapidAPI-Key": RapidAPI_Key, "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}


def handler_city(city: str) -> bool:
    querystring = {"q": city}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    if not data['rs'] == 'OK':
        return False
    if all(map(lambda l: l not in ascii_letters, city)):
        city = translit(city, 'ru', reversed=True)
        regexp = f'{city[:-2]}\w+'
    list_result = []
    for elem in data['sr']:
        if elem['type'] == "CITY" and re.search(regexp, elem["regionNames"]["fullName"]):
            list_result.append(elem["gaiaId"])
    return list_result

