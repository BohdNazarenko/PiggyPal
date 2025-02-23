import telebot

from bot.handlers import start, balance
from config.settings import BOT_TOKEN

bot = telebot.TeleBot(token=BOT_TOKEN)

start.register_handlers(bot)
balance.register_handlers(bot)

if __name__ == '__main__':
    current_balance = 0.00
    bot.polling(none_stop=True)

