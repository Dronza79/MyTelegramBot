import json
import random

import requests
from commands.loader import RapidAPI_Key


def get_index_named_city(city):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    headers = {"X-RapidAPI-Key": RapidAPI_Key, "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
    querystring = {"q": city, "locale": "ru_RU"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    try:
        print('response.text=', response.text)
        data = json.loads(response.text)
        print('data=', data)
    except Exception as bug:
        print(bug)
        get_index_named_city(city)
    index = None
    data = data.get('sr')
    for elem in data:
        if elem['type'] == "CITY":
            index = elem.get('gaiaId')
            break
    print(f'\n{city}: {index}')
    return index


def display_result_getting_list_hotels(town_id, amount_htls, sort, checkin, checkout, p_from=None, p_to=None):
    print(f'ИД города: {town_id}, кол-во отелей: {amount_htls}, условие сортировки: {sort}')
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "destination": {"regionId": town_id},
        "checkInDate": {
            "day": checkin.tm_mday,
            "month": checkin.tm_mon,
            "year": checkin.tm_year
        },
        "checkOutDate": {
            "day": checkout.tm_mday,
            "month": checkout.tm_mon,
            "year": checkout.tm_year
        },
        "rooms": [{"adults": 1}],
        "resultsSize": int(amount_htls),
        "sort": sort
    }
    if p_from and p_to:
        payload['filters']['price']['min'] = p_from
        payload['filters']['price']['max'] = p_to
    print("payload=", payload)
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RapidAPI_Key,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print("response=", response)
    data = json.loads(response.text)
    hotels = data.get('data').get('propertySearch').get('properties')
    with open('temp/1.json', 'w') as f:
        json.dump(data, f, indent=4)
    count = 0
    for hotel in hotels:
        count += 1
        hotel_id = hotel.get('id')
        hotel_name = hotel.get('name')
        try:
            price = hotel.get('price').get('lead').get('amount')
            timedelta = checkout.tm_yday - checkin.tm_yday
            total = price * timedelta
        except Exception as exc:
            print(hotel_id, "Ошибка:", exc)
            price = 'Цену получить не удалось...'
            total = 'Цену получить не удалось...'
        string = (
            f"<b>{count} вариант:</b>\n"
            f"{'*' * 50}\n"
            f"Отель: {hotel_name}" 
            f"\nЦена за сутки: $ {price: .2f}"
            f"\nЦена за весь срок: $ {total: .2f}"
            # f"\nУзнать больше: www.hotels.com/ho{hotel_id}"
        )

        yield hotel_id, hotel_name, string


def give_list_photos_of_hotel(id_hotel, name, num_fotos):
    num = int(num_fotos)
    list_foto = [name]
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {"propertyId": id_hotel}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RapidAPI_Key,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    data = json.loads(response.text)
    try:
        list_items = data.get('data').get('propertyInfo').get('propertyGallery').get('images')
        for item in [random.choice(list_items) for _ in range(num)]:
            print(item)
            foto = item.get('image').get('url').split('?')[0]
            # foto = foto
            list_foto.append(foto)
    except Exception as exc:
        print(f"Ошибка получения фотографий отель: {id_hotel}", exc)

    return list_foto
