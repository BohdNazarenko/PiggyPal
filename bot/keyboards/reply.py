from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_balance_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Balance")
    keyboard.add(button)
    return keyboard
