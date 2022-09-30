import telebot
from telebot import types

with open('token.txt', 'r') as file:
    token = file.read()
print(token)
bot = telebot.TeleBot(token)

discription = "Это Telegram-бот для анализа сайта Hotels.com и поиска подходящих пользователю отелей"


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Привет')
    bot.send_message(message.from_user.id, discription)
    markup = types.InlineKeyboardButton(resize_keyboard=True)
    item1 = types.KeyboardButton("да")
    item2 = types.KeyboardButton("Нет")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, 'продолжим?...', reply_markup=markup)


bot.polling(none_stop=True, interval=0)


# if __name__ == '__main__':

