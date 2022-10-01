
@bot.message_handler(commands=['start'])
def process_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton(text='Выбери меня'))
    bot.send_message(message.chat.id, text='Нажми кнопку в меню', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def step1(message):
    menu1 = telebot.types.InlineKeyboardMarkup()
    menu1.add(telebot.types.InlineKeyboardButton(text='Первая кнопка', callback_data='first'))
    menu1.add(telebot.types.InlineKeyboardButton(text='Вторая кнопка', callback_data='second'))

    if message.text == 'Выбери меня':
        bot.send_message(message.chat.id, text='Нажми первую inline кнопку', reply_markup=menu1)

@bot.callback_query_handler(func=lambda call: True)
def step2(call):
    menu2 = telebot.types.InlineKeyboardMarkup()
    menu2.add(telebot.types.InlineKeyboardButton(text='Третья кнопка', callback_data='third'))
    menu2.add(telebot.types.InlineKeyboardButton(text='Четвертая кнопка', callback_data='fourth'))

    if call.data == 'first':
        bot.send_message(call.message.chat.id, 'Нажми третью кнопку', reply_markup=menu2)
    elif call.data == 'third':
        bot.send_message(call.message.chat.id, 'Конец')
