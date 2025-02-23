from bot.keyboards.reply import get_balance_keyboard

current_balance: float = 0.00

def register_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "set_balance")
    def set_balance(call):
        bot.send_message(call.message.chat.id, "Enter your current balance:")
        bot.register_next_step_handler(call.message, save_balance)


    @bot.message_handler(func=lambda message: message.text == "Balance")
    def check_balance(message):
        bot.send_message(message.chat.id, f"Your current balance is {current_balance} zloty")



    def save_balance(message):
        global current_balance
        try:
            current_balance = float(message.text.replace(",", "."))
            bot.send_message(message.chat.id, f"Your balance is now {round(current_balance, 2)} zloty",
                             reply_markup=get_balance_keyboard()
            )
        except ValueError:
            bot.send_message(message.chat.id, "Error! Please enter a valid number.")
            bot.register_next_step_handler(message, save_balance)
