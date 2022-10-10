import json

import requests
from loader import RapidAPI_Key, tomorrow, next_day


def get_index_named_city(city):
    url = "https://hotels4.p.rapidapi.com/locations/search"
    headers = {"X-RapidAPI-Key": RapidAPI_Key, "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
    querystring = {"query": city, "locale": "ru_RU"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    index = None
    data = data.get('suggestions')
    for elem in data:
        if elem['group'] == "CITY_GROUP":
            for item in elem.get('entities'):
                if item['type'] == "CITY":
                    index = item.get('destinationId')
                    break
            break
    print(f'\n{city}', end=' ')
    return index


def display_result_getting_list_hotels(town_id, amount_htls, sort, p_from=None, p_to=None):
    print(f'ИД города: {town_id}, кол-во отелей: {amount_htls}, условие сортировки: {sort}')
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": town_id, "pageNumber": "1", "pageSize": amount_htls,
                   "checkIn": tomorrow, "checkOut": next_day, "adults1": "1",
                   "sortOrder": sort, "locale": "ru_RU", "currency": "USD"}
    if p_from and p_to:
        querystring['priceMin'] = p_from
        querystring['priceMax'] = p_to
    print(querystring)
    headers = {"X-RapidAPI-Key": RapidAPI_Key, "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    hotels = data.get('data').get('body').get('searchResults').get('results')
    for hotel in hotels:
        try:
            street = hotel.get('address').get('streetAddress')
            address = f"{hotel['address']['locality']}. {street}"
        except Exception as exc:
            print(f'Упс... улицы нет. Ошибка: {exc}')
            region = hotel.get('address').get('region')
            address = f"{hotel['address']['locality']}. {region}"
        hotel_id = hotel.get('id')
        try:
            price = '$' + str(hotel.get('ratePlan').get('price').get('exactCurrent'))
        except Exception as exc:
            print(hotel_id, "Ошибка:", exc)
            price = 'Цену получить не удалось...'
        substring = ''
        for loc in hotel.get('landmarks'):
            substring += f'\n{loc.get("label")} - {loc.get("distance")}'
        string = (
            f"Отель: {hotel.get('name')}\nАдрес: {address}\nРасположен от: {substring}"
            f"\nЦена за сутки: {price}"
        )
        yield hotel_id, string


def give_list_photos_of_hotel(id_hotel, num_fotos):
    num = int(num_fotos)
    list_foto = []
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": id_hotel}
    headers = {"X-RapidAPI-Key": RapidAPI_Key, "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    try:
        data = json.loads(response.text)
        list_items = data.get('hotelImages')
        for item in list_items[:num]:
            foto = item.get('baseUrl').format(size='w')
            list_foto.append(foto)
    except Exception as exc:
        print(f"Ошибка получения фотографий отель: {id_hotel}", exc)

    return list_foto
