import time

from api.handler_step_poll import get_min_and_max_value
from api.handler_request_api_hotels import get_index_named_city
from loader import bot, history


class BestDeal:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.city_id = None
        self.number_hotels = None
        self.list_foto = dict()
        self.price_min = None
        self.price_max = None
        self.checkin = None
        self.checkout = None
        self.deltatime = None
        self.sort_filter = 'DISTANCE_FROM_LANDMARK'

    def __repr__(self):
        temp = 'Удача' if self.city_id else 'Неудача'
        return (f'Ваш запрос: {temp}.\nТип: Лучшие предложения.\nДата: '
                f'{time.strftime("%d-%m-%Y %a, %H:%M:%S", time.localtime(self.date))}'
                f'\nГород: {self.city}.\nКоличество отелей {self.number_hotels}.')


def get_city_name_for_bestdeal(message):  # получаем город, инициализируем запрос
    user = message.chat.id
    date = message.date
    city = message.text
    poll = BestDeal(date, city)
    if user in history:
        user = history[user]
        user.append(poll)
    else:
        history[user] = [poll]
    bot.send_message(message.from_user.id, 'Проверяю....')
    result = get_index_named_city(city)
    poll.city_id = result
    if not result:
        msg = bot.send_message(message.from_user.id, text='Такого города найти не смог\n'
                                                          'укажите другой город:')
        bot.register_next_step_handler(msg, get_city_name_for_bestdeal)
        return
    bot.send_message(message.from_user.id, 'Хорошо. Продолжим...')
    bot.send_message(message.from_user.id, 'Укажите min&max цену через пробел')
    bot.register_next_step_handler(message, get_min_and_max_value)
