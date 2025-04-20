from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineKeyboard:
    """
    Namespace‑style container for inline keyboard builders.
    Each method returns a ready‑to‑use InlineKeyboardMarkup.
    """

    @staticmethod
    def set_start_balance() -> InlineKeyboardMarkup:

        markup = InlineKeyboardMarkup()

        markup.add(
            InlineKeyboardButton(
                "Set your starting balance",
                callback_data="set_balance"
            )
        )

        return markup
