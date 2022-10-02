import telebot
from telebot import types
from bigText import DISCRIPTION, HELP_ANSWER

with open('token.txt', 'r') as file:
    token = file.read()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def process_start(message):
    bot.send_message(message.from_user.id, 'Привет')
    bot.send_message(message.from_user.id, DISCRIPTION)
    greeting = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Посмотреть помощь', callback_data='help')
    button2 = types.InlineKeyboardButton(text='Начать работу', callback_data='go')
    greeting.row(button1, button2)
    bot.send_message(message.chat.id, text='Вы можете:', reply_markup=greeting)


@bot.callback_query_handler(func=lambda call: True)
def inline_menu(call):
    main_menu = types.InlineKeyboardMarkup()
    main_menu.add(types.InlineKeyboardButton(text='Посмотреть самые дешёвые отели', callback_data='lowprice'))
    main_menu.add(types.InlineKeyboardButton(text='Посмотреть самые дорогие отели', callback_data='highprice'))
    main_menu.add(types.InlineKeyboardButton(text='Подобрать отели по цене и расположению', callback_data='bestdeal'))
    main_menu.add(types.InlineKeyboardButton(text='Посмотреть свою историю поиска отелей', callback_data='history'))

    if 'help' in call.data:
        helpkey = types.InlineKeyboardMarkup()
        helpkey.add(types.InlineKeyboardButton(text='Начать работу', callback_data='go'))
        bot.send_message(call.from_user.id, text=HELP_ANSWER, reply_markup=helpkey)

    elif 'go' in call.data:
        bot.send_message(call.from_user.id, text='Выберите действие:', reply_markup=main_menu)

    if 'lowprice' in call.data:
        main_lp = types.InlineKeyboardMarkup()
        main_lp.add(types.InlineKeyboardButton(text='Вернутся  в главное меню', callback_data='go'))
        bot.send_message(call.from_user.id, text='Происходит поиск ДЕШЕВЫХ отелей...', reply_markup=main_lp)

    elif 'highprice' in call.data:
        main_hp = types.InlineKeyboardMarkup()
        main_hp.add(types.InlineKeyboardButton(text='Вернутся  в главное меню', callback_data='go'))
        bot.send_message(call.from_user.id, text='Происходит поиск ДОРОГИХ отелей...', reply_markup=main_hp)

    elif 'bestdeal' in call.data:
        main_lp = types.InlineKeyboardMarkup()
        main_lp.add(types.InlineKeyboardButton(text='Вернутся  в главное меню', callback_data='go'))
        bot.send_message(call.from_user.id, text='Происходит поиск ЛУЧШИХ отелей...', reply_markup=main_lp)

    elif 'history' in call.data:
        main_htry = types.InlineKeyboardMarkup()
        main_htry.add(types.InlineKeyboardButton(text='Вернутся  в главное меню', callback_data='go'))
        bot.send_message(call.from_user.id, text='Показываю историю поиска...', reply_markup=main_htry)



if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

