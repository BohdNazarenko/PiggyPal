import telebot

from config.settings import BOT_TOKEN

bot = telebot.TeleBot(token=BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello World!')

bot.polling()