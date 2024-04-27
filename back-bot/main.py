import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SECRET_KEY")
client = telebot.TeleBot(TOKEN)

client.set_my_commands([
    telebot.types.BotCommand("start", "start of the bot."),
    telebot.types.BotCommand("auction", "auction of the channels and chat's."),
    telebot.types.BotCommand("create_auction", "Create auction of your channel."),
])

# commands
@client.message_handler(commands=["start"])
def start_command(message):
    client.send_message(message.chat.id, "Hello! To create your auction you can use command - /create_auction\nTo check all active auctions command - /auction")
@client.message_handler(commands=["auction"])
def auction_command(message):
    markup = telebot.types.InlineKeyboardMarkup()
    WebApp = telebot.types.WebAppData("https://adsstorage.herokuapp.com/auctions")
    markup.add(telebot.types.InlineKeyboardButton("See all auctions", web_app=WebApp))
    client.send_message(message.chat.id, "See all auctions.", reply_markup=markup)

@client.message_handler(commands=["create_auction"])
def create_auction_command(message):
    client.send_message(message.chat.id, "Test create auction message.")

# Callbacks


client.infinity_polling()