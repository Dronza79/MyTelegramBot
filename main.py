from commands.loader import bot


if __name__ == '__main__':
    # try:
    bot.polling(none_stop=True, interval=0)
    # except Exception as exc:
    #     print('Ошибка:', exc)
