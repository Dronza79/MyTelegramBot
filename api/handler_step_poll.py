from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from loader import bot, history
from api.big_text import ANSWER
from api.handler_request_api_hotels import display_result_getting_list_hotels, give_list_photos_of_hotel


def get_min_and_max_value(message):
    string = message.text
    user = message.chat.id
    if not all([st.isdigit() for st in string.split()]):
        msg = bot.send_message(message.from_user.id, text='Ошибка: Неверный тип значений.\n(Ожидаются цифры).')
        bot.register_next_step_handler(msg, get_min_and_max_value)
        return
    try:
        min_p, max_p = string.split()
    except Exception:
        msg = bot.send_message(message.from_user.id, text='Ошибка: Неверное количество значений.\n(Ожидается два).')
        bot.register_next_step_handler(msg, get_min_and_max_value)
        return
    poll = history[user][len(history[user]) - 1]
    poll.price_min = min_p
    poll.price_max = max_p
    bot.send_message(message.from_user.id, 'Укажите количество отелей (не более 25)')
    bot.register_next_step_handler(message, get_number_hotels)


def get_number_hotels(message):  # получаем количество отелей
    number_hotels = message.text
    user = message.chat.id
    if not number_hotels.isdigit():
        msg = bot.send_message(message.from_user.id, text='Ошибка. Должна быть цифра')
        bot.register_next_step_handler(msg, get_number_hotels)
        return
    if int(number_hotels) > 25:
        msg = bot.send_message(message.from_user.id, text='Ошибка. Должно быть не более 25')
        bot.register_next_step_handler(msg, get_number_hotels)
        return
    poll = history[user][len(history[user]) - 1]
    poll.number_hotels = number_hotels
    choice = InlineKeyboardMarkup()
    btns = [InlineKeyboardButton(text=value, callback_data=key) for key, value in ANSWER.items()]
    choice.row(btns[0], btns[1])
    bot.send_message(message.from_user.id, 'Показать фото?', reply_markup=choice)


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'not'])
def get_answer(call):
    count = 0
    user = call.from_user.id
    poll = history[user][len(history[user]) - 1]
    if call.data == 'yes':
        msg = bot.send_message(call.from_user.id, text='Укажите количество (не более 10):')
        bot.register_next_step_handler(msg, get_photos)
    else:
        for hotel, string in display_result_getting_list_hotels(poll.city_id,
                                                                poll.number_hotels,
                                                                poll.sort_filter,
                                                                poll.price_min,
                                                                poll.price_max):
            bot.send_message(user, text=string, parse_mode='html')
        return_key = InlineKeyboardMarkup()
        return_key.add(InlineKeyboardButton(text='Главное меню', callback_data='go'))
        bot.send_message(user, text='Доклад закончил...', reply_markup=return_key)


def get_photos(message):
    num_foto = message.text
    user = message.from_user.id
    if not num_foto.isdigit():
        msg = bot.send_message(message.from_user.id, text='Ошибка: Неверный типа значений.\n(ожидается число)')
        bot.register_next_step_handler(msg, get_photos)
        return
    if int(num_foto) > 10:
        msg = bot.send_message(message.from_user.id, text='Ошибка: Неверное значение.\n(значение не более 10)')
        bot.register_next_step_handler(msg, get_photos)
        return
    poll = history[user][len(history[user]) - 1]
    for hotel, string in display_result_getting_list_hotels(poll.city_id,
                                                            poll.number_hotels,
                                                            poll.sort_filter,
                                                            poll.price_min,
                                                            poll.price_max):
        hotel_foto = give_list_photos_of_hotel(hotel, num_foto)
        print(f'{hotel}: {hotel_foto}')
        poll.list_foto[hotel] = hotel_foto
        if not hotel_foto:
            msg = bot.send_message(user, text=string)
            bot.send_message(user,
                             text='Фотографии загрузить не удалось',
                             reply_to_message_id=msg.message_id)
            continue
        list_foto = [InputMediaPhoto(foto) for foto in hotel_foto]
        msg = bot.send_message(user, text=string)
        bot.send_media_group(user, list_foto, reply_to_message_id=msg.id)
    return_key = InlineKeyboardMarkup()
    return_key.add(InlineKeyboardButton(text='Главное меню', callback_data='go'))
    bot.send_message(user, text='Доклад закончил...', reply_markup=return_key)
