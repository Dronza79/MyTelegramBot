from telebot.types import Message, BotCommand, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from api.big_text import DESCRIPTION, HELP_ANSWER, GEN_KEYB, ANSWER
import commands
from loader import bot


@bot.message_handler(commands=['start'])
def process_start(message: BotCommand) -> None:
    """
    Оформление приветственного меню с возможностью выбора одного из двух действий:
    - просмотра помощи по командам чата
    - приступить к работе бота

    :param message: команда инициализации бота (/start)
    :return: Команды кнопок Помощь, Начало работы
    """
    bot.send_message(message.from_user.id, 'Привет\n'+DESCRIPTION)
    greeting = InlineKeyboardMarkup()
    btns = [InlineKeyboardButton(text=GEN_KEYB[key], callback_data=key) for key in ['help', 'go']]
    greeting.row(btns[0], btns[1])
    bot.send_message(message.from_user.id, text='Вы можете:', reply_markup=greeting)


@bot.message_handler(commands=['help'])
def text_command_chat(message):
    helpkey = InlineKeyboardMarkup()
    helpkey.add(InlineKeyboardButton(text='Начать работу', callback_data='go'))
    bot.send_message(message.from_user.id, text=HELP_ANSWER, reply_markup=helpkey)


@bot.callback_query_handler(func=lambda call: call.data in ['go', 'help'])
def run_maim_menu(call):
    print(call.data)
        # return_main_menu = InlineKeyboardMarkup()
    # return_main_menu.add(InlineKeyboardButton(text='Вернутся в главное меню', callback_data='go'))

    if 'help' in call.data:
        start_work = InlineKeyboardMarkup()
        start_work.add(InlineKeyboardButton(text='Начать работу', callback_data='go'))
        bot.send_message(call.from_user.id, text=HELP_ANSWER, reply_markup=start_work)

    elif 'go' in call.data:
        main_menu = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(text=GEN_KEYB[key], callback_data=key) for key in [
            'lowprice', 'highprice', 'bestdeal', 'history'
        ]]
        main_menu.row(buttons[0], buttons[1]).row(buttons[2], buttons[3])
        bot.send_message(call.from_user.id, text='Выберите действие для просмотра:', reply_markup=main_menu)
