import pickle
import os
import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from loader import bot, history
from data_base import class_comands


def get_history():
    if not history:
        if os.path.isfile('../data_base/history.pickle'):
            with open('../data_base/history.pickle', 'rb') as f:
                try:
                    data = pickle.load(f)
                except Exception as exc:
                    print(exc)
                    data = history.copy()
            return data
    data = history.copy()
    return data


def display_history(message):
    print(message)
    user = message.chat.id
    data = get_history()
    find_history = data.get(user)
    if not find_history:
        return_key = InlineKeyboardMarkup()
        return_key.add(InlineKeyboardButton(text='Главное меню', callback_data='go'))
        bot.send_message(user, text='Историю вашего поиска найти не удалось.', reply_markup=return_key)
        return
    cnt = 1
    for action in find_history:
        hotels = ''
        for htl in action.list_foto.values():
            hotels += ' - ' + htl[0] + '\n'
        report = (f'<b>{cnt} действие\n{"*" * 50}\n</b>'
                  f'{time.strftime("%c", time.localtime(action.date))}\n'
                  f'Команда: {action}\nГород: {action.city.capitalize()}'
                  f'Количество отелей: {action.number_hotels}\nСписок отелей:\n{hotels}')
        cnt += 1
        bot.send_message(user, text=report, parse_mode='html')
    return_key = InlineKeyboardMarkup()
    return_key.add(InlineKeyboardButton(text='Главное меню', callback_data='go'))
    bot.send_message(user, text='Доклад закончил', reply_markup=return_key)


