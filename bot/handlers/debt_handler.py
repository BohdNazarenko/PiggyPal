from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot.database import DataBase, DebtRepository
from bot.keyboards.reply import ReplyKeyboard


class DebtHandler:

    def __init__(self, bot):
        self.bot = bot
        self.db = DataBase()
        self._register_handlers()
        self._pending: dict[int, dict] = {}
        self.debt_repo = DebtRepository(self.db)

    def _register_handlers(self):
        @self.bot.message_handler(func=lambda m: m.text == "Debt")
        def start_debt_flow(message: Message):
            chat_id = message.chat.id
            self._pending[chat_id] = {}

            debtors = self.debt_repo.list_debtors()
            keyboard = InlineKeyboardMarkup()

            for index, name in enumerate(debtors):
                keyboard.add(InlineKeyboardButton(
                    text=name,
                    callback_data=f"debt_exist_{index}"
                ))
            keyboard.add(InlineKeyboardButton(
                text="Add new debtor",
                callback_data="debt_new"
            ))

            self.bot.send_message(
                chat_id,
                "Select an existing debtor or add a new one:",
                reply_markup=keyboard
            )

        @self.bot.callback_query_handler(func=lambda c: c.data.startswith("debt_exist_") or c.data == "debt_new")
        def on_debtor_choice(call: CallbackQuery):
            chat_id = call.message.chat.id
            data = call.data

            if data == "debt_new":
                self.bot.send_message(chat_id, "Enter the new debtor's name:")
                self.bot.register_next_step_handler(call.message, process_name)
            else:
                index = int(data.split("_")[-1])
                name = self.debt_repo.list_debtors()[index]
                self._pending.setdefault(chat_id, {})["name"] = name
                self.bot.send_message(chat_id, f"Debtor: {name}\nEnter debt amount:")
                self.bot.register_next_step_handler(call.message, process_amount)

        def process_name(message: Message):
            chat_id = message.chat.id
            name = message.text.strip()
            self._pending[chat_id]["name"] = name
            self.bot.send_message(chat_id, f"Name set: {name}\nEnter debt amount:")
            self.bot.register_next_step_handler(message, process_amount)

        def process_amount(message: Message):
            chat_id = message.chat.id
            text = message.text.replace(',', '.')
            try:
                amount = float(text)
            except ValueError:
                return self.bot.send_message(
                    chat_id,
                    "Invalid amount. Please enter a number:"
                )
            self._pending[chat_id]["amount"] = amount
            self.bot.send_message(chat_id, "Enter purpose of the debt:")
            self.bot.register_next_step_handler(message, process_purpose)

        def process_purpose(message: Message):
            chat_id = message.chat.id

            purpose = message.text.strip()
            data = self._pending.pop(chat_id, {})
            name = data.get("name")
            amount = data.get("amount")
            debt_id = self.debt_repo.add_debt(name=name, debt_count=amount, purpose=purpose or None)
            self.bot.send_message(
                chat_id,
                f"Debt #{debt_id} saved:\n"
                f"• Debtor: {name}\n"
                f"• Amount: {amount:.2f}\n"
                f"• Purpose: {purpose}",
                reply_markup=ReplyKeyboard.get_main_keyboard()
            )



def debt_register_handlers(bot):
    DebtHandler(bot)
