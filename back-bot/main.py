import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SECRET_KEY")
frontUrl = os.getenv("FRONT_URL")
client = telebot.TeleBot(TOKEN)

client.set_my_commands([
    telebot.types.BotCommand("start", "start of the bot."),
    telebot.types.BotCommand("auction", "auction of the channels and chat's."),
    telebot.types.BotCommand("create_auction", "Create auction of your channel."),
    telebot.types.BotCommand("quit", "Leave all ongoing commands.")
])
# States

# Store user states (optional, you can use a database for better scalability)
user_states = {}

# Function to set user state
def set_user_state(user_id, state):
    user_states[user_id] = state

# Function to get user state
def get_user_state(user_id):
    return user_states.get(user_id)

# commands
@client.message_handler(commands=["start"])
def start_command(message):
    client.send_message(message.chat.id, "Hello! To create your auction you can use command - /create_auction\nTo check all active auctions command - /auction")
@client.message_handler(commands=["auction"])
def auction_command(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    WebApp = telebot.types.WebAppInfo(frontUrl)
    markup.add(telebot.types.InlineKeyboardButton(text="See all auctions", web_app=WebApp))
    client.send_message(message.chat.id, "See all auctions.", reply_markup=markup)

@client.message_handler(commands=["create_auction"])
def create_auction_command(message):
    client.send_message(message.chat.id, "You want to create auction? Let's start. Please add me to your channel and make me admin. Then send me the link of your channel.")

@client.message_handler(commands=["quit"])
def quit_command(message):
    reset_user_state(message.chat.id)
    client.send_message(message.chat.id, "You have left all ongoing commands.")

# Callbacks


client.infinity_polling()