from telebot.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.database import DataBase, ExpensesRepository, CategoryRepository, CategoryTypeRepository, BalanceRepository
from bot.keyboards.reply import ReplyKeyboard


class ExpensesHandler:

    def __init__(self, bot):
        self.bot = bot
        self.db = DataBase()
        self.balance_repo = BalanceRepository(self.db)
        self.category_type_repo = CategoryTypeRepository(self.db)
        self.category_repo = CategoryRepository(self.db)
        self.expense_repo = ExpensesRepository(self.db)
        self._pending = {}
        self._register_handlers()

    def _register_handlers(self):

        @self.bot.message_handler(func=lambda message: message.text == "Expense")
        def choose_category_type(message: Message):

            chat_id = message.chat.id
            self._pending[chat_id] = {}

            types = self.category_type_repo.list_all()
            keyboard = InlineKeyboardMarkup()
            for t in types:
                keyboard.add(InlineKeyboardButton(
                    text=f"{t['category_type_id']}. {t['category_type']}",
                    callback_data=f"exp_type_{t['category_type_id']}"
                ))
            self.bot.send_message(
                message.chat.id,
                "Select a category type:",
                reply_markup=keyboard
            )

        @self.bot.callback_query_handler(func=lambda c: c.data.startswith("exp_type_"))
        def on_type_selected(call: CallbackQuery):
            type_id = int(call.data.split("_")[-1])
            chat_id = call.message.chat.id

            self._pending[chat_id] = {"type_id": type_id}

            categories = self.category_repo.list_by_type(type_id)
            keyboard = InlineKeyboardMarkup()

            for category in categories:
                keyboard.add(InlineKeyboardButton(
                    text=f"{category['category']}",
                    callback_data=f"exp_category_{category['category_id']}"
                ))
            self.bot.send_message(
                chat_id,
                "Now select a specific category:",
                reply_markup=keyboard
            )

        @self.bot.callback_query_handler(func=lambda c: c.data.startswith("exp_category_"))
        def on_category_selected(call: CallbackQuery):
            categ_id = int(call.data.split("_")[-1])
            chat_id = call.message.chat.id

            self._pending.setdefault(chat_id, {})["category_id"] = categ_id

            self.bot.send_message(chat_id, "Enter the expense amount:")

            self.bot.register_next_step_handler(call.message, process_amount)


        def process_amount(message: Message):
            chat_id = message.chat.id
            text = message.text.replace(",", ".")
            try:
                amount = float(text)
            except ValueError:
                return self.bot.send_message(
                    chat_id,
                    "Invalid amount. Please enter a number:"
                )

            data = self._pending.pop(chat_id, {})
            categ_id = data.get("category_id")
            if not categ_id:
                return self.bot.send_message(
                    chat_id,
                    "Category lost. Please start over with Add Expense.",
                    reply_markup=ReplyKeyboard.get_main_keyboard()
                )

            exp_id = self.expense_repo.add_expense(user_id=chat_id, category_id=categ_id, amount=amount)
            new_balance = self.balance_repo.update_balance(chat_id, -amount)

            self.bot.send_message(
                chat_id,
                f"✅ Expense #{exp_id} saved: {amount:.2f} zł\n"
                f"💰 New balance: {new_balance:.2f} zł",
                reply_markup=ReplyKeyboard.get_main_keyboard()
            )


def expenses_register_handlers(bot):
    ExpensesHandler(bot)


