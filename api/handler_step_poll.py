from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from loader import bot, history
from api.big_text import ANSWER
from api.handler_request_api_hotels import display_result, give_list_foto


def get_number_hotels(message):  # получаем количество отелей
    number_hotels = message.text
    user = message.chat.id
    if not number_hotels.isdigit():
        msg = bot.send_message(message.from_user.id, text='Ошибка. Должна быть цифра')
        bot.register_next_step_handler(msg, get_number_hotels)
        return
    if int(number_hotels) > 5:
        msg = bot.send_message(message.from_user.id, text='Ошибка. Должно быть не более 5')
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
    user = call.from_user.id
    poll = history[user][len(history[user]) - 1]
    if call.data == 'yes':
        msg = bot.send_message(call.from_user.id, text='Укажите количество (не более 10):')
        bot.register_next_step_handler(msg, get_photos)
    else:
        for hotel, string in display_result(poll.city_id, poll.number_hotels, poll.sort_filter):
            bot.send_message(user, text=string)
        return_key = InlineKeyboardMarkup()
        return_key.add(InlineKeyboardButton(text='Главное меню', callback_data='go'))
        bot.send_message(user, text='Доклад закончил...', reply_markup=return_key)


def get_photos(message):
    num_foto = message.text
    user = message.from_user.id
    if not num_foto.isdigit():
        msg = bot.send_message(message.from_user.id, text='Ошибка. Должно быть число')
        bot.register_next_step_handler(msg, get_photos)
        return
    if int(num_foto) > 10:
        msg = bot.send_message(message.from_user.id, text='Ошибка. Число должно быть меньше или равно 10')
        bot.register_next_step_handler(msg, get_photos)
        return
    poll = history[user][len(history[user]) - 1]
    for hotel, string in display_result(poll.city_id, poll.number_hotels, poll.sort_filter):
        hotel_foto = give_list_foto(hotel, num_foto)
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
        bot.send_media_group(user, list_foto,
                             reply_to_message_id=msg.message_id,
                             allow_sending_without_reply=True)
    return_key = InlineKeyboardMarkup()
    return_key.add(InlineKeyboardButton(text='Главное меню', callback_data='go'))
    bot.send_message(user, text='Доклад закончил...', reply_markup=return_key)
