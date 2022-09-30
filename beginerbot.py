import botbrain
from telebot import types

# bot = botbrain.bot

def send_start_mess(bot):
    discription = "Это Telegram-бот для анализа сайта Hotels.com и поиска подходящих пользователю отелей"

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.from_user.id, 'Привет')
        bot.send_message(message.from_user.id, discription)
        bot.send_message(message.from_user.id, 'продолжим?...')
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)


