from telebot.types import Message
from bot.keyboards.inline import set_balance_keyboard


def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        bot.send_message(
            message.chat.id,
            f"Hello, {message.from_user.first_name}! 🎉. Enter your balance to start tracking:",
            reply_markup=set_balance_keyboard())
