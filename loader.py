import os

import telebot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

__token = os.environ.get("TOKEN")
RapidAPI_Key = os.environ.get("RapidAPI_Key")


BOT = telebot.TeleBot(__token)

history = dict()
