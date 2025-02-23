from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def set_balance_keyboard():
    markup = InlineKeyboardMarkup()
    set_balance_button = InlineKeyboardButton("Find out your balance", callback_data="set_balance")
    markup.add(set_balance_button)
    return markup
