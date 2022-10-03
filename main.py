from telebot import types
from API.bigText import DESCRIPTION, HELP_ANSWER, POLL_COMMAND
# import Commands
from loader import BOT as bot



@bot.message_handler(commands=['start'])
def process_start(message):
    bot.send_message(message.from_user.id, 'Привет\n'+DESCRIPTION)
    greeting = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Посмотреть помощь', callback_data='help')
    button2 = types.InlineKeyboardButton(text='Начать работу', callback_data='go')
    greeting.row(button1, button2)
    bot.send_message(message.from_user.id, text='Вы можете:', reply_markup=greeting)


@bot.callback_query_handler(func=lambda call: True)
def inline_menu(call):

    main_menu = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Дешёвые отели', callback_data='lowprice')
    button2 = types.InlineKeyboardButton(text='Дорогие отели', callback_data='highprice')
    button3 = types.InlineKeyboardButton(text='Лучшие предложения', callback_data='bestdeal')
    button4 = types.InlineKeyboardButton(text='Историю поиска', callback_data='history')
    main_menu.row(button1, button2).row(button3, button4)
    start_work = types.InlineKeyboardMarkup()
    start_work.add(types.InlineKeyboardButton(text='Начать работу', callback_data='go'))
    return_main_menu = types.InlineKeyboardMarkup()
    return_main_menu.add(types.InlineKeyboardButton(text='Вернутся в главное меню', callback_data='go'))

    if 'help' in call.data:
        bot.send_message(call.from_user.id, text=HELP_ANSWER, reply_markup=start_work)

    elif 'go' in call.data:
        bot.send_message(call.from_user.id, text='Выберите действие для просмотра:', reply_markup=main_menu)

    for poll in POLL_COMMAND:
        if poll in call.data:
            bot.send_message(call.from_user.id, text=POLL_COMMAND[poll], reply_markup=return_main_menu)
            break


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def text_command_chat(message):
    if 'lowprice' in message.text:
        bot.send_message(message.from_user.id, 'Производим поиск')


@bot.message_handler(commands=['help'])
def text_command_chat(message):
    helpkey = types.InlineKeyboardMarkup()
    helpkey.add(types.InlineKeyboardButton(text='Начать работу', callback_data='go'))
    bot.send_message(message.from_user.id, text=HELP_ANSWER, reply_markup=helpkey)




if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
