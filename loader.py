import os
from datetime import datetime, timedelta

import telebot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

__token = os.environ.get("TOKEN")
RapidAPI_Key = os.environ.get("RapidAPI_Key")


bot = telebot.TeleBot(__token)

history = dict()

tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
next_day = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
