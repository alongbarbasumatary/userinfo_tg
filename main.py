import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Fetch the Telegram bot token from environment variables
token = os.getenv('TELEGRAM_TOKEN')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I can show user info when you forward a message.')

def forward_info(update: Update, context: CallbackContext) -> None:
    if update.message.forward_from:
        user_info = f"User Info:\nUsername: @{update.message.forward_from.username}\nID: {update.message.forward_from.id}"
        update.message.reply_text(user_info)
    else:
        update.message.reply_text("No user info available.")

def main():
    updater = Updater(token)
    dispatcher = updater.dispatcher

    # Add handlers for the commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.forwarded, forward_info))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
