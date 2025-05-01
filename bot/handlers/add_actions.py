from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.reply import ReplyKeyboard


class AddHandler:

    def __init__(self, bot):
        self.bot = bot
        self._register()


    def _register(self):
        @self.bot.message_handler(func=lambda m: m.text == "Add")
        def on_add(message: Message):

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.row(
                KeyboardButton("Expense"),
                KeyboardButton("Income")
            )
            keyboard.row(
                KeyboardButton("Debt"),
                KeyboardButton("Goal")
            )
            keyboard.row(
                KeyboardButton("Back to Menu")
            )

            self.bot.send_message(
                message.chat.id,
                "What would you like to add?",
                reply_markup=keyboard
            )

        @self.bot.message_handler(func=lambda m: m.text =="Back to Menu")
        def on_back(message: Message):
            self.bot.send_message(
                message.chat.id,
                "Back to main menu:",
                reply_markup=ReplyKeyboard.get_main_keyboard()
            )


def register_handlers(bot):
    AddHandler(bot)