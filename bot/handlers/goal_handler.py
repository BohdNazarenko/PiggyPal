from telebot.types import Message

from bot.database import DataBase, GoalRepository
from bot.keyboards.reply import ReplyKeyboard


class GoalHandler:

    def __init__(self, bot):
        self.bot = bot
        self.db = DataBase()
        self.goal_repo = GoalRepository(self.db)
        self._pending: dict[int, dict] = {}
        self._register_handlers()


    def _register_handlers(self):
        @self.bot.message_handler(func=lambda m: m.text == "Goal")
        def start_goal_flow(message: Message):
            chat_id = message.chat.id
            self._pending[chat_id] = {}
            self.bot.send_message(chat_id, "Enter goal name:")
            self.bot.register_next_step_handler(message, ask_price)

        def ask_price(message: Message):
            chat_id = message.chat.id
            name = message.text.strip()
            self._pending[chat_id]["name"] = name
            self.bot.send_message(chat_id, f"Name set to {name}. Enter price:")
            self.bot.register_next_step_handler(message, ask_description)

        def ask_description(message: Message):
            chat_id = message.chat.id
            text = message.text.replace(",", ".")
            try:
                price = float(text)
            except ValueError:
                return self.bot.send_message(chat_id, "Invalid price. Please enter a number:")
            self._pending[chat_id]["price"] = price
            self.bot.send_message(chat_id, "Enter goal description:")
            self.bot.register_next_step_handler(message, save_goal)

        def save_goal(message: Message):
            chat_id = message.chat.id
            description = message.text.strip() or None
            data = self._pending.pop(chat_id, {})
            name = data.get("name")
            price = data.get("price")
            goal_id = self.goal_repo.add_goal(user_id=chat_id, name=name, price=price, description=description)
            self.bot.send_message(
                chat_id,
                f"✅ Goal #{goal_id} saved:\n"
                f"• Name: {name}\n"
                f"• Price: {price:.2f}\n"
                f"• Description: {description or '-'}",
                reply_markup=ReplyKeyboard.get_main_keyboard()
            )

def goal_register_handler(bot):
    GoalHandler(bot)