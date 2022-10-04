import telebot

with open('API/secret_keys.txt', 'r') as file:
    data = file.readlines()

__token = data[0].strip()
RapidAPI_Key = data[1].strip()

BOT = telebot.TeleBot(__token)
