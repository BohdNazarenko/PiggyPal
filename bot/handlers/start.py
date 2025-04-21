from telebot.types import Message
from bot.handlers.balance import BalanceHandler


class StartHandler:

    def __init__(self, bot, balance_handler):
        self.bot = bot
        self.balance_handler = balance_handler
        self._register()


    def _register(self):

        @self.bot.message_handler(commands=['start'])
        def start(message: Message):
            self.bot.send_message(
                message.chat.id,
                f"Hello, {message.from_user.first_name}! 🎉. "
                f"Enter your balance to start tracking:"
            )

            self.bot.register_next_step_handler(message, self.balance_handler.save_balance)



def register_handlers(bot, balance_handler):
    StartHandler(bot, balance_handler)