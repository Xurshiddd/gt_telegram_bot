import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Your bot token
TOKEN = "7708841747:AAHTsvP6ANk9Z2mJ-rOSyteFuUja3fIhdl8"  # Replace with your actual bot token

# Admin ID (should be an integer, not a string)
admin_id = 898426931

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Dictionary to hold the message IDs for replies
pending_replies = {}


# Define the start handler
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == admin_id:
        bot.send_message(message.chat.id, "Assalomu alaykum Admin")
    else:
        bot.send_message(message.chat.id,
                         "Assalomu alaykum Murojat botga Hush kelibsiz, qanday savol va takliflaringiz bor?")

@bot.callback_query_handler(func=lambda call: call.data.startswith('reply_'))
def handle_reply_button(call):
    user_id = call.data.split('_')[1]
    pending_replies[call.message.chat.id] = user_id  # Store the user ID to reply to
    bot.send_message(call.message.chat.id, "Javobni yozing va jo'nating.")

    # Remove the reply button after it is clicked by editing the message
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)


@bot.message_handler(func=lambda message: message.chat.id == admin_id)
def handle_admin_reply(message):
    if admin_id in pending_replies:
        user_id = pending_replies[admin_id]
        bot.send_message(user_id, message.text)  # Send the reply to the user
        bot.send_message(admin_id, "Javobingiz yuborildi!")  # Notify the admin that the reply was sent
        del pending_replies[admin_id]  # Remove the entry after replying
    else:
        # If no pending reply, we can ignore or send a message indicating that there is no ongoing conversation.
        bot.send_message(admin_id, "Siz hech kimga javob yozmadingiz javob yozish uchun savol tagidagi Javob yozish tugmasini bosing agar bu tugma bo'lmasa savollarga javob berib bo'lingan.")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.chat.id != admin_id:
        keyboard = InlineKeyboardMarkup()
        reply_button = InlineKeyboardButton("Javob berish", callback_data=f"reply_{message.chat.id}")
        keyboard.add(reply_button)
        bot.send_message(admin_id, f"{message.chat.first_name}: {message.text}", reply_markup=keyboard)
        bot.reply_to(message, f"{message.chat.first_name} murojatingiz qabul qilindi, mutaxassisning javobini kuting!")


bot.polling()
