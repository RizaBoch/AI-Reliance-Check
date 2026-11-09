
import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Load the token from the private .env file
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# Welcome message when the user sends /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🤖 Welcome to AI Reliance Check!\n\n"
        "Do you use AI because you need it, or because "
        "opening AI has become a habit?\n\n"
        "This bot helps you explore your AI-use habits "
        "through short questions and reasoning challenges.\n\n"
        "You will complete:\n"
        "1. Quick Check\n"
        "2. Habit Check\n"
        "3. AI Challenge\n"
        "4. AI-Free Challenge\n"
        "5. Personal Reflection\n"
        "6. Feedback\n\n"
        "This is a self-reflection tool, not a psychological diagnosis.\n\n"
        "Ready to begin?"
    )

    keyboard = [
        [InlineKeyboardButton(
            "🚀 Start Quick Check",
            callback_data="quick_check"
        )]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup
    )


# Respond when the user presses Start Quick Check
async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    if query.data == "quick_check":
        await query.edit_message_text(
            "📝 Quick Check\n\n"
            "This section explores how often you use AI "
            "and what you use it for.\n\n"
            "Questions will be added in the next step."
        )


def main():
    if not TOKEN:
        raise ValueError(
            "BOT_TOKEN not found. Check your .env file."
        )

    app = ApplicationBuilder().token(TOKEN).build()

    # Register the /start command
    app.add_handler(CommandHandler("start", start))

    # Register button clicks
    app.add_handler(CallbackQueryHandler(button_handler))

    print("AI Reliance Check bot is running...")

    # Keep the bot listening for Telegram messages
    app.run_polling()


if __name__ == "__main__":
    main()
