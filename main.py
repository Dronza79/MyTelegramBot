from telebot.types import Message, BotCommand, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
# from collections.abc import Collection

from API.bigText import DESCRIPTION, HELP_ANSWER, GEN_KEYB
from Commands import lowprice
from loader import BOT as bot


@bot.message_handler(commands=['start'])
def process_start(message: BotCommand) -> None:
    """
    Оформление приветственного меню с возможностью выбора одного из двух действий:
    - просмотра помощи по командам чата
    - приступить к работе бота

    :param message: команда инициализации бота (/start)
    :return: None
    """
    bot.send_message(message.from_user.id, 'Привет\n'+DESCRIPTION)
    greeting = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Посмотреть помощь', callback_data='help')
    button2 = InlineKeyboardButton(text='Начать работу', callback_data='go')
    greeting.row(button1, button2)
    bot.send_message(message.from_user.id, text='Вы можете:', reply_markup=greeting)


@bot.message_handler(commands=['help'])
def text_command_chat(message):
    helpkey = InlineKeyboardMarkup()
    helpkey.add(InlineKeyboardButton(text='Начать работу', callback_data='go'))
    bot.send_message(message.from_user.id, text=HELP_ANSWER, reply_markup=helpkey)


@bot.callback_query_handler(func=lambda call: True)
def inline_menu(call):

    main_menu = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in GEN_KEYB.items()]
    main_menu.row(buttons[0], buttons[1]).row(buttons[2], buttons[3])
    start_work = InlineKeyboardMarkup()
    start_work.add(InlineKeyboardButton(text='Начать работу', callback_data='go'))
    return_main_menu = InlineKeyboardMarkup()
    return_main_menu.add(InlineKeyboardButton(text='Вернутся в главное меню', callback_data='go'))

    if 'help' in call.data:
        bot.send_message(call.from_user.id, text=HELP_ANSWER, reply_markup=start_work)

    elif 'go' in call.data:
        bot.send_message(call.from_user.id, text='Выберите действие для просмотра:', reply_markup=main_menu)

    elif 'lowprice' in call.data:
        msg = bot.send_message(call.from_user.id, text='Укажите город для поиска')
        bot.register_next_step_handler(msg, lowprice.get_city)  # следующий шаг – функция get_started


# @bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
# def text_command_chat(message):
#     if 'lowprice' in message.text:
#         bot.send_message(message.from_user.id, 'Производим поиск')




if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
