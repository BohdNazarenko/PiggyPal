"""bot/main.py

Main entry point for the PiggyPal Telegram bot.
Creates the bot instance, registers handlers,
and starts the long-polling loop.
"""
import logging
import signal
import sys

import telebot

from bot.database import init_db
from bot.database.db import DataBase
from bot.handlers import (
    balance_handler,
    menu_handler,
    expenses_handler,
    incomes_handler,
    debt_handler,
    goal_handler,
)
from config.settings import BOT_TOKEN

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)


class PiggyPalBot:
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token=token)
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Graceful shutdown on Ctrl+C."""
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)

    def _shutdown(self, signum, frame):
        logger.info("Shutting down bot...")
        self.bot.stop_polling()
        DataBase.close_pool()
        logger.info("Bot stopped gracefully")
        sys.exit(0)

    def register_handlers(self):
        balance_handler.register_handlers(self.bot)
        menu_handler.register_handlers(self.bot)
        expenses_handler.expenses_register_handlers(self.bot)
        incomes_handler.income_register_handler(self.bot)
        debt_handler.debt_register_handlers(self.bot)
        goal_handler.goal_register_handler(self.bot)

    def run(self):
        logger.info("Bot started polling...")
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    init_db()
    logger.info("Database initialized")

    piggy_bot = PiggyPalBot(BOT_TOKEN)
    piggy_bot.register_handlers()
    logger.info("Handlers registered")

    piggy_bot.run()
