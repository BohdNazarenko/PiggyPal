"""bot/main.py

Main entry point for the PiggyPal Telegram bot.
Creates the bot instance, registers handlers,
and starts the long‑polling loop.
"""
import telebot

from bot.database import init_db
from bot.handlers import start_handler, balance_handler, add_actions, expenses_handler, incomes_handler, debt_handler, \
    goal_handler
from bot.handlers.goal_handler import goal_register_handler
from bot.handlers.incomes_handler import income_register_handler
from config.settings import BOT_TOKEN


class PiggyPalBot:
    def __init__(self, token: str):
        # Create a TeleBot instance using the token provided by BotFather.
        self.bot = telebot.TeleBot(token=token)
        # Current user balance stored in memory only.
        # TODO: replace this with persistent storage (e.g. PostgreSQL).
        self.current_balance = 0.00


    def register_handlers(self):
        balance_handler.register_handlers(self.bot)
        start_handler.register_handlers(self.bot, balance_handler)
        add_actions.register_handlers(self.bot)
        expenses_handler.expenses_register_handlers(self.bot)
        incomes_handler.income_register_handler(self.bot)
        debt_handler.debt_register_handlers(self.bot)
        goal_handler.goal_register_handler(self.bot)


    def run(self):
        # none_stop=True keeps the bot running even if a handler raises.
        self.bot.polling(none_stop=True)

if __name__ == '__main__':
    init_db()
    piggy_bot = PiggyPalBot(BOT_TOKEN)
    piggy_bot.register_handlers()
    piggy_bot.run()