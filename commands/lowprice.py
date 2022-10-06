import time

# import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from API.bigText import ANSWER
from loader import bot, history


class LowPrice:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.result = None
        self.number_hotels = None
        self.required_photo = False
        self.number_photo = None

    def __str__(self):
        temp = 'Удача' if self.result else 'Неудача'
        return (f'Ваш запрос: {temp}.\nТип: Дешевые отели.\nДата: {time.strftime("%x %X", time.localtime(self.date))}'
                f'\nГород: {self.city}.\nКоличество отелей {self.number_hotels}.')


@bot.message_handler(commands=['lowprice'])
def get_text_command_lowprice(message):
    msg = bot.send_message(message.from_user.id, text='Укажите город для поиска')
    bot.register_next_step_handler(msg, get_city)  # следующий шаг – функция get_started


@bot.callback_query_handler(func=lambda call: call.data in ['lowprice'])
def start_keyb_lowprice(call):
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
    bot.send_message(message.from_user.id, 'Укажите количество отелей (не более 25)')
    bot.register_next_step_handler(message, get_number_hotels)


def get_number_hotels(message):  # получаем количество отелей
    number_hotels = message.text
    user = message.chat.id
    if not number_hotels.isdigit():
        msg = bot.send_message(message.from_user.id, text='Ошибка. Должна быть цифра')
        bot.register_next_step_handler(msg, get_number_hotels)
        return
    if int(number_hotels) > 25:
        msg = bot.send_message(message.from_user.id, text='Ошибка. Должно быть не более 25')
        bot.register_next_step_handler(msg, get_number_hotels)
        return
    poll = history[user][len(history[user]) - 1]
    poll.number_hotels = number_hotels
    answer = InlineKeyboardMarkup()
    btns = [InlineKeyboardButton(text=value, callback_data=key) for key, value in ANSWER.items()]
    answer.row(btns[0], btns[1])
    bot.send_message(message.from_user.id, 'Показать фото?', reply_markup=answer)


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'not'])
def get_answer(call):
    user = call.from_user.id
    poll = history[user][len(history[user]) - 1]
    if call.data == 'yes':
        poll.required_photo = True
        msg = bot.send_message(call.from_user.id, text='Укажите количество (не более 5):')
        bot.register_next_step_handler(msg, get_photos)
    else:
        bot.send_message(user, text=poll)


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
    poll.number_photo = num_foto
    bot.send_message(message.from_user.id, text=poll)
