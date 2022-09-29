import telebot
import beginerbot

with open('token.txt', 'r') as file:
    token = file.read()

bot = telebot.TeleBot(token)

beginerbot.start_message(message=None)

bot.polling(none_stop=True, interval=0)


# if __name__ == '__main__':

