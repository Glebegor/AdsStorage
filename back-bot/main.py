import os
import telebot
import time
import asyncio
import sqlite3
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
user_states = {}

# Function to set user state
def set_user_state(user_id, state):
    user_states[user_id] = state

# Function to get user state
def get_user_state(user_id):
    return user_states.get(user_id)

def reset_user_state(user_id):
    if user_id in user_states:
        del user_states[user_id]

def is_bot_admin(message):
    try:
        channel_id = client.get_chat(message).id
        chat_member = client.get_chat_member(channel_id, client.get_me().id)
        if chat_member is None:
            return ""
        return channel_id
    except Exception as e:
        print("Error:", e)
        return ""

def create_auction_in_database(channel_link, description, min_bet_ton, create_data, end_data):
    with sqlite3.connect('main.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO auctions (channel_link, description, min_bet_ton, create_data, end_data) VALUES (?, ?, ?, ?, ?)",
                    (channel_link, description, min_bet_ton, create_data, end_data))
        con.commit()

@client.message_handler(commands=["start"])
def start_command(message):
    client.send_message(message.chat.id, "Hello! To create your auction you can use command - /create_auction\nTo check all active auctions command - /auction")

@client.message_handler(commands=["auction"])
def auction_command(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    WebApp = telebot.types.WebAppInfo(frontUrl)
    markup.add(telebot.types.InlineKeyboardButton(text="See all auctions", web_app=WebApp))
    client.send_message(message.chat.id, "See all auctions.", reply_markup=markup)

@client.message_handler(commands=["quit"])
def quit_command(message):
    reset_user_state(message.chat.id)
    client.send_message(message.chat.id, "You have left all ongoing commands.")

@client.message_handler(commands=["create_auction"])
def create_auction_command(message):
    client.send_message(message.chat.id, "You want to create an auction? Great! Let's start.\n\n"
                                          "Please add me to your channel and make me admin. Then send me the link of your channel (@name).")
    set_user_state(message.chat.id, "awaiting_channel_link")

# Function to handle the channel link and retrieve description
@client.message_handler(func=lambda message: get_user_state(message.chat.id) == "awaiting_channel_link")
def handle_channel_link(message):
    global description, min_bet_ton, auction_timer, channel_link
    channel_link = message.text  # Assuming the channel link is provided as text in the message
    chat_id = is_bot_admin(channel_link)
    if chat_id == "":
        client.send_message(message.chat.id, "I am not an admin in the channel or bad channel. Please add me as an admin and write correct channel, after try again.")
        return

    # Get channel description
    channel_info = client.get_chat(chat_id)
    description = channel_info.description

    # Now prompt the user for the auction timer
    client.send_message(message.chat.id, "Please provide the time of the auction in hours.")
    set_user_state(message.chat.id, "awaiting_auction_timer")

@client.message_handler(func=lambda message: get_user_state(message.chat.id) == "awaiting_auction_timer")
def handle_auction_timer(message):
    global auction_timer
    auction_timer = message.text
    client.send_message(message.chat.id, "Please provide the minimum bet TON count for the auction.")
    set_user_state(message.chat.id, "awaiting_min_bet_ton")

# Function to handle minimum bet TON count
@client.message_handler(func=lambda message: get_user_state(message.chat.id) == "awaiting_min_bet_ton")
def handle_min_bet_ton(message):
    global channel_link, description, min_bet_ton, auction_timer
    min_bet_ton = message.text

    # Get current timestamp
    current_time = int(time.time() * 1000)
    # Calculate end timestamp based on auction timer
    end_time = current_time + (int(auction_timer) * 60 * 60 * 1000)

    # Create auction data dictionary
    auction_data = {
        "channel_link": channel_link,
        "description": description,
        "min_bet_ton": min_bet_ton,
        "create_data": current_time,
        "end_data": end_time
    }

    # Insert auction data into database
    create_auction_in_database(auction_data["channel_link"], auction_data["description"], auction_data["min_bet_ton"], auction_data["create_data"], auction_data["end_data"])

    # Clear user state
    reset_user_state(message.chat.id)

    # Inform the user that the auction creation is complete
    client.send_message(message.chat.id, "Auction creation complete!")

client.polling(none_stop=True)
