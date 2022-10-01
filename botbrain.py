import telebot
from telebot import types
import json

with open('token.txt', 'r') as file:
    token = file.read()
# print(token)
bot = telebot.TeleBot(token)

discription = "Это Telegram-бот для анализа сайта Hotels.com и поиска подходящих пользователю отелей"

@bot.message_handler(commands=['start'])
def process_start(message):
    bot.send_message(message.from_user.id, 'Привет')
    bot.send_message(message.from_user.id, discription)
    menu1 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Да', callback_data='yes')
    button2 = types.InlineKeyboardButton(text='Нет', callback_data='no')
    menu1.row(button1, button2)
    bot.send_message(message.chat.id, text='Продолжим?...', reply_markup=menu1)

@bot.callback_query_handler(func=lambda call: True)
def work_menu(call):
    if 'no' in call.data:
        bot.ban_chat_member(call.message.chat, call.message.from_user)

bot.polling(none_stop=True, interval=0)


# if __name__ == '__main__':

