from telebot.types import ReplyKeyboardMarkup, KeyboardButton


class ReplyKeyboard:


    @staticmethod
    def get_main_keyboard() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            KeyboardButton("Balance"),
            KeyboardButton("History")
        )
        return keyboard


