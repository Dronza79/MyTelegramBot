import time


class LowPrice:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.city_id = None
        self.number_hotels = None
        self.list_foto = dict()
        self.price_min = None
        self.price_max = None
        self.sort_filter = 'PRICE'

    def __str__(self):
        temp = 'Удача' if self.city_id else 'Неудача'
        return (f'Ваш запрос: {temp}.\nТип: Дешевые отели.\nДата: '
                f'{time.strftime("%d-%m-%Y %a, %H:%M:%S", time.localtime(self.date))}'
                f'\nГород: {self.city}.\nКоличество отелей {self.number_hotels}.')

    def __repr__(self):
        return f'LowPrice: {time.strftime("%d-%m-%Y %a, %H:%M:%S", time.localtime(self.date))}'


class HighPrice:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.city_id = None
        self.number_hotels = None
        self.list_foto = dict()
        self.price_min = None
        self.price_max = None
        self.sort_filter = 'PRICE_HIGHEST_FIRST'

    def __str__(self):
        temp = 'Удача' if self.city_id else 'Неудача'
        return (f'Ваш запрос: {temp}.\nТип: Дорогие отели.\nДата: '
                f'{time.strftime("%d-%m-%Y %a, %H:%M:%S", time.localtime(self.date))}'
                f'\nГород: {self.city}.\nКоличество отелей {self.number_hotels}.')

    def __repr__(self):
        return f'LowPrice: {time.strftime("%d-%m-%Y %a, %H:%M:%S", time.localtime(self.date))}'


class BestDeal:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.city_id = None
        self.number_hotels = None
        self.list_foto = dict()
        self.price_min = None
        self.price_max = None
        self.sort_filter = 'DISTANCE_FROM_LANDMARK'

    def __str__(self):
        temp = 'Удача' if self.city_id else 'Неудача'
        return (f'Ваш запрос: {temp}.\nТип: Лучшие предложения.\nДата: '
                f'{time.strftime("%d-%m-%Y %a, %H:%M:%S", time.localtime(self.date))}'
                f'\nГород: {self.city}.\nКоличество отелей {self.number_hotels}.')

    def __repr__(self):
        return f'LowPrice: {time.strftime("%d-%m-%Y %a, %H:%M:%S", time.localtime(self.date))}'
