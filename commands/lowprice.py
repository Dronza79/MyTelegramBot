import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from api.big_text import ANSWER_LP_FOTO, ATTENTION
from api.handler_reqest_api_hotels import handler_city, display_result, give_list_foto
from loader import bot, history


class LowPrice:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.city_id = None
        self.number_hotels = None
        self.list_foto = []

    def __str__(self):
        temp = 'Удача' if self.city_id else 'Неудача'
        return (f'Ваш запрос: {temp}.\nТип: Дешевые отели.\nДата: '
                f'{time.strftime("%d-%m-%Y %a, %H:%M:%S", time.localtime(self.date))}'
                f'\nГород: {self.city}.\nКоличество отелей {self.number_hotels}.')


@bot.message_handler(commands=['lowprice'])
def get_text_command_lowprice(message):
    msg = bot.send_message(message.from_user.id, text='Укажите город для поиска')
    bot.register_next_step_handler(msg, get_city)  # следующий шаг – функция get_started


@bot.callback_query_handler(func=lambda call: call.data in ['lowprice'])
def start_keyb_lowprice(call):
    bot.send_message(call.from_user.id, ATTENTION)
    msg = bot.send_message(call.from_user.id, text='Укажите город для поиска')
    bot.register_next_step_handler(msg, get_city)  # следующий шаг – функция get_started


def get_city(message):  # получаем город
    user = message.chat.id
    date = message.date
    city = message.text
    poll = LowPrice(date, city)
    if user in history:
        user = history[user]
        user.append(poll)
    else:
        history[user] = [poll]
    bot.send_message(message.from_user.id, 'Проверяю....')
    result = handler_city(city)
    poll.city_id = result
    if not result:
        msg = bot.send_message(message.from_user.id, text='Такого города найти не смог\n'
                                                          'укажите другой город:')
        bot.register_next_step_handler(msg, get_city)
        return
    bot.send_message(message.from_user.id, 'Хорошо. Продолжим...')
    bot.send_message(message.from_user.id, 'Укажите количество отелей (не более 5)')
    bot.register_next_step_handler(message, get_number_hotels)


def get_number_hotels(message):  # получаем количество отелей
    number_hotels = message.text
    user = message.chat.id
    if not number_hotels.isdigit():
        msg = bot.send_message(message.from_user.id, text='Ошибка. Должна быть цифра')
        bot.register_next_step_handler(msg, get_number_hotels)
        return
    if int(number_hotels) > 5:
        msg = bot.send_message(message.from_user.id, text='Ошибка. Должно быть не более 5')
        bot.register_next_step_handler(msg, get_number_hotels)
        return
    poll = history[user][len(history[user]) - 1]
    poll.number_hotels = number_hotels
    answer = InlineKeyboardMarkup()
    btns = [InlineKeyboardButton(text=value, callback_data=key) for key, value in ANSWER_LP_FOTO.items()]
    answer.row(btns[0], btns[1])
    bot.send_message(message.from_user.id, 'Показать фото?', reply_markup=answer)


@bot.callback_query_handler(func=lambda call: call.data in ['yes_lp', 'not_lp'])
def get_answer(call):
    user = call.from_user.id
    poll = history[user][len(history[user]) - 1]
    if call.data == 'yes_lp':
        msg = bot.send_message(call.from_user.id, text='Укажите количество (не более 5):')
        bot.register_next_step_handler(msg, get_photos)
    else:
        for hotel, string in display_result(poll.city_id, poll.number_hotels, sort="PRICE"):
            bot.send_message(user, text=string)
        return_key = InlineKeyboardMarkup()
        return_key.add(InlineKeyboardButton(text='Главное меню', callback_data='go'))
        bot.send_message(user, text='Доклад закончил...', reply_markup=return_key)


def get_photos(message):
    num_foto = message.text
    user = message.from_user.id
    if not num_foto.isdigit():
        msg = bot.send_message(message.from_user.id, text='Ошибка. Должно быть число')
        bot.register_next_step_handler(msg, get_photos)
        return
    if int(num_foto) > 5:
        msg = bot.send_message(message.from_user.id, text='Ошибка. Число должно быть меньше или равно 5')
        bot.register_next_step_handler(msg, get_photos)
        return
    poll = history[user][len(history[user]) - 1]
    for hotel, string in display_result(poll.city_id, poll.number_hotels, sort="PRICE"):
        list_foto = give_list_foto(hotel, num_foto)
        poll.list_foto.append(list_foto)
        for foto in list_foto:
            bot.send_message(user, text=foto)
        bot.send_message(user, text=string)
    return_key = InlineKeyboardMarkup()
    return_key.add(InlineKeyboardButton(text='Главное меню', callback_data='go'))
    bot.send_message(user, text='Доклад закончил...', reply_markup=return_key)
