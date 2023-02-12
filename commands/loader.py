import os
import pickle
from datetime import datetime, timedelta

import telebot
from dotenv import load_dotenv, find_dotenv

from data_base import class_comands

load_dotenv(find_dotenv())

__token = os.environ.get("TOKEN")
RapidAPI_Key = os.environ.get("RapidAPI_Key")

bot = telebot.TeleBot(__token)


if os.path.isfile('data_base/history.pickle'):
    with open('data_base/history.pickle', 'rb') as f:
        try:
            history = pickle.load(f)
        except Exception:
            history = dict()
else:

    history = dict()


print(history)
