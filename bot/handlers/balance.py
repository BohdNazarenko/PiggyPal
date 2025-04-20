from telebot.types import CallbackQuery

from bot.keyboards.reply import get_balance_keyboard


class BalanceHandler:

    def __init__(self, bot):
        self.bot = bot
        self._balance: float = 0.0
        self._register()

    def _register(self):
        """All balance-related handlers."""

        @self.bot.callback_query_handler(func=lambda call: call.data == "set_balance")
        def set_balance(call: CallbackQuery):
            """Prompt user to enter the balance."""
            self.bot.send_message(call.message.chat.id, "Enter your current balance:")
            self.bot.register_next_step_handler(call.message, save_balance)


        @self.bot.message_handler(func=lambda message: message.text == "Balance")
        def check_balance(message):
            self.bot.send_message(
                message.chat.id,
                f"Your current balance is {self._balance} zloty"
            )


        def save_balance(message):
            """Save and confirm the balance input."""
            try:
                self._balance = round(float(message.text.replace(",", ".")), 2)

                self.bot.send_message(
                    message.chat.id,
                    f"Your balance is now {self._balance} zloty",
                    reply_markup=get_balance_keyboard()
                )
            except ValueError:
                self.bot.send_message(message.chat.id, "Error! Please enter a valid number.")
                self.bot.register_next_step_handler(message, save_balance)


def register_handlers(bot):
    BalanceHandler(bot)