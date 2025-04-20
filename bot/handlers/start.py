from telebot.types import Message
from bot.keyboards import inline


class StartHandler:

    def __init__(self, bot):
        self.bot = bot
        self.register()


    def register(self):

        @self.bot.message_handler(commands=['start'])
        def start(message: Message):
            self.bot.send_message(
                message.chat.id,
                f"Hello, {message.from_user.first_name}! 🎉. Enter your balance to start tracking:",
                reply_markup = inline.InlineKeyboard.set_start_balance()
            )

def register_handlers(bot):
    StartHandler(bot)