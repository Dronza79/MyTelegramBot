import requests
from loader import BOT as bot
import telebot
from telebot import types

city = ''
number_hotels = 0

# bot.register_next_step_handler(call, callback=get_city)  # следующий шаг – функция get_name
# bot.send_message(call.from_user.id, text=result, reply_markup=return_main_menu)
@bot.message_handler(content_types=['text'])
def get_city(message):  # получаем фамилию
    if 'lowprice' == message:
        global city
        city = message.text
        bot.send_message(message.from_user.id, 'Укажите количество отелей')
        bot.register_next_step_handler(message, get_number_hotels)


def get_number_hotels(message):  # получаем фамилию
    global number_hotels
    number_hotels = message.text
    bot.send_message(message.from_user.id, 'Укажите количество отелей')
    bot.register_next_step_handler(message, get_number_hotels)

result = f'Вы выбрали город {city} и количество отелей: {number_hotels}'