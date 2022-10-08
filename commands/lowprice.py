import time

from api.big_text import ATTENTION
from api.handler_step_poll import get_city
from loader import bot


class LowPrice:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.city_id = None
        self.number_hotels = None
        self.list_foto = []

    def __repr__(self):
        temp = 'Удача' if self.city_id else 'Неудача'
        return (f'Ваш запрос: {temp}.\nТип: Дешевые отели.\nДата: '
                f'{time.strftime("%d-%m-%Y %a, %H:%M:%S", time.localtime(self.date))}'
                f'\nГород: {self.city}.\nКоличество отелей {self.number_hotels}.')


handler_command = LowPrice
sort_filter = 'PRICE'


@bot.message_handler(commands=['lowprice'])
def get_text_command_lowprice(message):
    msg = bot.send_message(message.from_user.id, text='Укажите город для поиска')
    bot.register_next_step_handler(msg, get_city)  # следующий шаг – функция get_started


@bot.callback_query_handler(func=lambda call: call.data in ['lowprice'])
def start_keyb_command(call):
    bot.send_message(call.from_user.id, ATTENTION)
    bot.send_message(call.from_user.id, text="Выбраны дешевые отели")
    msg = bot.send_message(call.from_user.id, text='Укажите город для поиска')
    bot.register_next_step_handler(msg, get_city)  # следующий шаг – функция get_started