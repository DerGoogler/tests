import telebot
import json
import argparse
import re

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Send a photo with inline buttons using Telegram bot.")
parser.add_argument('--token', required=True, help='Telegram Bot Token')
parser.add_argument('--channel_id', required=True, help='Target Channel ID')
parser.add_argument('--file_path', required=True, help='Path to the image file')
parser.add_argument('--buttons', required=True, help='JSON string representing the buttons')
parser.add_argument('--message', required=True, help='Text message as a string')

args = parser.parse_args()

# Initialize the bot
bot = telebot.TeleBot(args.token)

def escape_markdown_v2(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

# Function to send a file with buttons and a message
def send_file_with_buttons(channel_id, file_path, buttons_json, message):
    buttons_data = json.loads(buttons_json)
    
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for button in buttons_data:
        button_obj = telebot.types.InlineKeyboardButton(
            text=button['text'],
            url=button['url']
        )
        markup.add(button_obj)

    message_v2 = escape_markdown_v2(message)


    with open(file_path, 'rb') as file:
        bot.send_document(
            chat_id=channel_id,
            document=file,
            caption=message_v2,
            reply_markup=markup,
            parse_mode='MarkdownV2'
        )

# Call the function
send_file_with_buttons(args.channel_id, args.file_path, args.buttons, args.message)
