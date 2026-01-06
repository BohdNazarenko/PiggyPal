from telebot.types import Message

from bot.database import DataBase, BalanceRepository, UserRepository
from bot.keyboards.reply import ReplyKeyboard


class BalanceHandler:

    def __init__(self, bot):
        self.bot = bot
        self.db = DataBase()
        self.user_repo = UserRepository(self.db)
        self.balance_repo = BalanceRepository(self.db)
        self._register()

    def _register(self):
        """All balance-related handlers."""

        @self.bot.message_handler(commands=['start'])
        def initial_balance(message: Message):
            user = message.from_user
            chat_id = message.chat.id

            # Create or update user in database
            self.user_repo.get_or_create(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )

            # Check if user already has a balance
            existing_balance = self.balance_repo.get_balance(chat_id)
            if existing_balance is not None:
                self.bot.send_message(
                    chat_id,
                    f"Welcome back, {user.first_name}! 👋\n"
                    f"Your current balance is {existing_balance:.2f} zloty",
                    reply_markup=ReplyKeyboard.get_main_keyboard()
                )
                return

            self.bot.send_message(
                chat_id,
                f"Hello, {user.first_name}! 🎉 "
                f"Enter your balance to start tracking:"
            )

            self.bot.register_next_step_handler(message, save_initial)

        def save_initial(message: Message):
            chat_id = message.chat.id
            text = message.text

            # If user sends a command, let command handlers process it
            if text.startswith("/"):
                return

            text = text.replace(",", ".")
            try:
                value = float(text)
            except ValueError:
                self.bot.send_message(chat_id, "Invalid number. Please enter a valid balance:")
                self.bot.register_next_step_handler(message, save_initial)
                return

            self.balance_repo.set_balance(chat_id, value)
            self.bot.send_message(
                chat_id,
                f"Your starting balance is now {value:.2f} zloty",
                reply_markup=ReplyKeyboard.get_main_keyboard()
            )

        @self.bot.message_handler(func=lambda message: message.text == "Balance")
        def check_balance(message):
            balance = self.balance_repo.get_balance(message.chat.id)
            if balance is None:
                self.bot.send_message(message.chat.id, "You don't have a balance yet. Use /start to set one.")
            else:
                self.bot.send_message(message.chat.id, f"Your current balance is {balance:.2f} zloty")


def register_handlers(bot):
    BalanceHandler(bot)
