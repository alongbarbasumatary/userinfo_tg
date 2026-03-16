import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask, request, jsonify

# --- Fetch environment variables ---
TOKEN = os.getenv('TELEGRAM_TOKEN')       # Telegram bot token
BOT_URL = os.getenv('BOT_URL')            # e.g., "https://yourapp.onrender.com"

# Flask app
app = Flask(__name__)

# --- Telegram Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    await update.message.reply_text(
        "Hello! I'm UserInfoBot. Forward a message to get detailed user information!"
    )

async def forward_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for forwarded messages"""
    if update.message.forward_from:
        user_info = (
            f"User Info:\n"
            f"Username: @{update.message.forward_from.username}\n"
            f"ID: {update.message.forward_from.id}"
        )
        await update.message.reply_text(user_info)
    else:
        await update.message.reply_text("No user info available.")

# --- Telegram Application ---
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.FORWARDED, forward_info))

# --- Flask route to receive Telegram updates ---
WEBHOOK_PATH = f"/webhook/{TOKEN}"

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    """Receive updates from Telegram and process them"""
    data = request.get_json(force=True)
    application.bot.process_update(Update.de_json(data, application.bot))
    return jsonify(ok=True)

# Health check route
@app.route('/')
def index():
    return "Bot is running!"

# --- Set webhook on startup ---
if __name__ == '__main__':
    if BOT_URL:
        webhook_url = f"{BOT_URL}{WEBHOOK_PATH}"
        application.bot.set_webhook(webhook_url)
        print(f"Webhook set to: {webhook_url}")
    else:
        print("Warning: BOT_URL not set. Webhook will not work.")

    # Start Flask server
    app.run(host='0.0.0.0', port=8080)
