import datetime

import requests
from telebot.types import Message, BotCommand, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from API.bigText import ANSWER
from loader import BOT as bot, history


class LowPrice:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.result = None
        self.number_hotels = None
        self.required_photo = False
        self.number_photo = None

    def __str__(self):
        return f'Ваш запрос: lowprice; data: '


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
    if not number_hotels.isdigit() or number_hotels > 25:
        msg = bot.send_message(message.from_user.id, text='Ошибка. Количество не верное. попробуйте еще раз')
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
    if call.data == 'yes':
        user = call.from_user.id
        poll = history[user][len(history[user]) - 1]
        poll.required_photo = True
        msg = bot.send_message(call.from_user.id, text='Укажите количество (не более 5):')
        bot.register_next_step_handler(msg, get_photos)


def get_photos(message):
    num_foto = message.text
    user = message.from_user.id
    if not num_foto.isdigit() or num_foto > 5:
        msg = bot.send_message(message.from_user.id, text='Ошибка. Количество не верное. попробуйте еще раз')
        bot.register_next_step_handler(msg, get_photos)
        return
    poll = history[user][len(history[user]) - 1]
    poll.number_photo = num_foto
