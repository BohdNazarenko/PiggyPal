from telebot.types import ReplyKeyboardMarkup, KeyboardButton


class ReplyKeyboard:

    @staticmethod
    def get_main_keyboard() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(
            KeyboardButton("Balance"),
            KeyboardButton("History"),
        )
        keyboard.row(
            KeyboardButton("Add")
        )
        return keyboard
