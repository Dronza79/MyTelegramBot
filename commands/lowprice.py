# import re

# import requests
from telebot.types import Message, BotCommand, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from API.bigText import ANSWER
from loader import BOT as bot

# from telebot import types

poll = dict()

@bot.message_handler(regexp='\b[^/]\w+')
def get_city(message):  # получаем город
    print(message.text)
    poll['city'] = message.text
    bot.send_message(message.from_user.id, 'Укажите количество отелей')
    bot.register_next_step_handler(message, get_number_hotels)


def get_number_hotels(message):  # получаем количество отелей
    print(message.text)
    number_hotels = message.text
    if type(number_hotels) == int:
        answer = InlineKeyboardMarkup()
        btns = [InlineKeyboardButton(text=value, callback_data=key) for key, value in ANSWER.items()]
        answer.row(btns[0], btns[1])
        msg = bot.send_message(message.from_user.id, 'Показать фото?', reply_markup=answer)
        bot.register_next_step_handler(message, get_number_hotels)


# def get_number_hotels(message):  # получаем количество отелей
#     global number_hotels
#     number_hotels = message.text
#     bot.send_message(message.from_user.id, 'Укажите количество отелей')
#     bot.register_next_step_handler(message, get_number_hotels)
#
# f'Вы выбрали город {city} и количество отелей: {number_hotels}'