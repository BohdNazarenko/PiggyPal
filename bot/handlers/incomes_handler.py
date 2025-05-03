from sqlalchemy.testing import lambda_combinations
from telebot.types import Message

from bot.database import DataBase, IncomesRepository, BalanceRepository
from bot.handlers.balance_handler import BalanceHandler
from bot.keyboards.reply import ReplyKeyboard


class IncomeHandler:

    def __init__(self, bot):
        self.bot = bot
        self.db = DataBase()
        self.balance_repo = BalanceRepository(self.db)
        self.incomes_repo = IncomesRepository(self.db)
        self._register_handlers()

    def _register_handlers(self):

        @self.bot.message_handler(func=lambda m: m.text == "Income")
        def ask_income_amount(message: Message):
            self.bot.send_message(
                message.chat.id,
                "Enter your income amount:"
            )

            self.bot.register_next_step_handler(message, process_amount)

        def process_amount(message: Message):
            chat_id = message.chat.id
            text = message.text.replace(",", ".")
            try:
                amount = float(text)
            except ValueError:
                return self.bot.send_message(
                    chat_id,
                    "Invalid number. Please enter a valid income amount:"
                )

            income_id = self.incomes_repo.add_income(chat_id, amount)

            new_balance = self.balance_repo.update_balance(chat_id, amount)

            self.bot.send_message(
                chat_id,
                f"Income #{income_id} recorded: {amount:.2f}",
                reply_markup=ReplyKeyboard.get_main_keyboard()
            )


def income_register_handler(bot):
    IncomeHandler(bot)
