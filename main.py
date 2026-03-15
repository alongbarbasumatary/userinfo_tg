import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import Filter  # Updated import for Filters
from flask import Flask
import logging

# Fetch the bot's API token from the environment variable
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Create a Flask app to handle HTTP requests and use Flask as a web server
app = Flask(__name__)

# Log handler for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Hello! I'm UserInfoBot. Forward a message to get detailed user information!"
    )

# Define the function to handle forwarded messages and show user info
def forward_info(update: Update, context: CallbackContext) -> None:
    if update.message.forward_from:
        user_info = f"User Info:\nUsername: @{update.message.forward_from.username}\nID: {update.message.forward_from.id}"
        update.message.reply_text(user_info)
    else:
        update.message.reply_text("No user info available.")

# Main function to start the bot
def main():
    # Create the Updater with the bot token
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers for the commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filter.forwarded, forward_info))  # Updated Filters usage

    # Start the bot
    updater.start_polling()

# Create a route for the Flask app to keep it running
@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    # Use port 8080 to listen for requests from Render
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 8080, app)
    main()
