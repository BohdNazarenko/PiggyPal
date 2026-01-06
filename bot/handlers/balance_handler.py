from telebot.types import Message

from bot.database import DataBase, BalanceRepository
from bot.keyboards.reply import ReplyKeyboard


class BalanceHandler:

    def __init__(self, bot):
        self.bot = bot
        self.db = DataBase()
        self.balance_repo = BalanceRepository(self.db)
        self._register()

    def _register(self):
        """All balance-related handlers."""

        @self.bot.message_handler(commands=['start'])
        def initial_balance(message: Message):
            self.bot.send_message(
                message.chat.id,
                f"Hello, {message.from_user.first_name}! 🎉. "
                f"Enter your balance to start tracking:"
            )

            self.bot.register_next_step_handler(message, save_initial)

        def save_initial(message: Message):
            chat_id = message.chat.id
            text = message.text.replace(",", ".")
            try:
                value = float(text)
            except ValueError:
                return self.bot.send_message(
                    chat_id,
                    "Invalid number. Please enter a valid balance:"
                )

            self.balance_repo.set_balance(chat_id, value)
            self.bot.send_message(
                chat_id,
                f"Your starting balance is now {value:.2f} zloty",
                reply_markup=ReplyKeyboard.get_main_keyboard()
            )

        @self.bot.message_handler(func=lambda message: message.text == "Balance")
        def check_balance(message):
            balance = self.balance_repo.get_balance(message.chat.id)
            self.bot.send_message(message.chat.id, f"Your current balance is {balance:.2f} zloty")


def register_handlers(bot):
    BalanceHandler(bot)
