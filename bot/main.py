"""bot/main.py

Main entry point for the PiggyPal Telegram bot.
Creates the bot instance, registers handlers,
and starts the long‑polling loop.
"""
import telebot

from bot.database import init_db
from bot.handlers import start, balance
from config.settings import BOT_TOKEN


class PiggyPalBot:
    def __init__(self, token: str):
        # Create a TeleBot instance using the token provided by BotFather.
        self.bot = telebot.TeleBot(token=token)
        # Current user balance stored in memory only.
        # TODO: replace this with persistent storage (e.g. PostgreSQL).
        self.current_balance = 0.00


    def register_handlers(self):
        balance_handler = balance.BalanceHandler(self.bot)
        start.register_handlers(self.bot, balance_handler)

    def run(self):
        # none_stop=True keeps the bot running even if a handler raises.
        self.bot.polling(none_stop=True)

if __name__ == '__main__':
    init_db()
    piggy_bot = PiggyPalBot(BOT_TOKEN)
    piggy_bot.register_handlers()
    piggy_bot.run()