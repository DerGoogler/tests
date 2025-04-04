import telebot
import json
import os

# Retrieve environment variables
TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
FILE_PATH = os.getenv('FILE_PATH')
JSON_BUTTONS_PATH = os.getenv('JSON_BUTTONS_PATH')
TEXT_MESSAGE_PATH = os.getenv('TEXT_MESSAGE_PATH')

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Function to send a file with buttons and a message
def send_file_with_buttons(channel_id, file_path, json_buttons_path, text_message_path):
    # Read the buttons from the JSON file
    with open(json_buttons_path, 'r') as f:
        buttons_data = json.load(f)
    
    # Create InlineKeyboardMarkup for buttons
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for button in buttons_data:
        button_obj = telebot.types.InlineKeyboardButton(text=button['text'], callback_data=button['callback_data'])
        markup.add(button_obj)
    
    # Read the message from the text file
    with open(text_message_path, 'r') as f:
        message = f.read().strip()

    # Send the file along with the buttons and message
    with open(file_path, 'rb') as file:
        bot.send_photo(
            chat_id=channel_id,
            photo=file,
            caption=message,
            reply_markup=markup
        )

# Call the function
send_file_with_buttons(CHANNEL_ID, FILE_PATH, JSON_BUTTONS_PATH, TEXT_MESSAGE_PATH)
