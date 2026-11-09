import os

from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from questions import QUICK_CHECK

load_dotenv(override=True)
TOKEN = os.getenv("BOT_TOKEN")


# Start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    keyboard = [
        [InlineKeyboardButton(
            "🚀 Start Quick Check",
            callback_data="start_quick"
        )]
    ]

    message = (
        "🤖 Welcome to AI Reliance Check!\n\n"
        "Do you use AI because you need it, or because "
        "using it has become a habit?\n\n"
        "This bot helps you reflect on your AI-use habits "
        "through questions and reasoning challenges.\n\n"
        "You'll complete:\n"
        "1. Quick Check\n"
        "2. Habit Check\n"
        "3. AI Challenge\n"
        "4. AI-Free Challenge\n"
        "5. Personal Reflection\n"
        "6. Feedback\n\n"
        "This is a self-reflection tool, not a diagnosis.\n\n"
        "Ready to begin?"
    )

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Display the current question
async def show_question(query, context):
    index = context.user_data["question_index"]

    if index >= len(QUICK_CHECK):
        await show_completion(query)
        return

    question = QUICK_CHECK[index]
    multiple = question.get("multiple", False)

    selected = context.user_data.get("selected", [])

    buttons = []

    for option_index, option in enumerate(question["options"]):
        label = option

        if multiple and option_index in selected:
            label = "✅ " + option

        buttons.append([
            InlineKeyboardButton(
                label,
                callback_data=f"answer_{option_index}"
            )
        ])

    if multiple:
        buttons.append([
            InlineKeyboardButton(
                "➡️ Done",
                callback_data="done_multiple"
            )
        ])

    text = (
        f"📝 Quick Check — Question {index + 1}/5\n\n"
        f"{question['question']}"
    )

    if multiple:
        text += "\n\nYou can select more than one answer."

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# Show the completion screen
async def show_completion(query):
    keyboard = [[
        InlineKeyboardButton(
            "➡️ Continue to Habit Check",
            callback_data="habit_check"
        )
    ]]

    await query.edit_message_text(
        "✅ Quick Check completed!\n\n"
        "Thank you for answering all five questions.\n\n"
        "Next is the Habit Check, where you'll reflect "
        "on how automatically you use AI.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Handle button clicks
async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "start_quick":
        context.user_data["question_index"] = 0
        context.user_data["answers"] = {}
        context.user_data["selected"] = []

        await show_question(query, context)

    elif data.startswith("answer_"):
        if "question_index" not in context.user_data:
            await query.edit_message_text(
                "Session expired. Send /start to begin again."
            )
            return

        index = context.user_data["question_index"]
        if index >= len(QUICK_CHECK):
            return

        question = QUICK_CHECK[index]

        try:
            option_index = int(data.split("_")[1])
        except (ValueError, IndexError):
            return

        if not 0 <= option_index < len(question["options"]):
            return

        if question.get("multiple", False):
            selected = context.user_data["selected"]

            if option_index in selected:
                selected.remove(option_index)
            else:
                selected.append(option_index)

            await show_question(query, context)

        else:
            context.user_data["answers"][index] = (
                question["options"][option_index]
            )

            context.user_data["question_index"] += 1
            context.user_data["selected"] = []

            await show_question(query, context)

    elif data == "done_multiple":
        index = context.user_data.get("question_index")

        if index is None or index >= len(QUICK_CHECK):
            return

        if not QUICK_CHECK[index].get("multiple", False):
            return

        selected = context.user_data.get("selected", [])

        if not selected:
            await query.answer(
                "Please select at least one option.",
                show_alert=True
            )
            return

        question = QUICK_CHECK[index]

        context.user_data["answers"][index] = [
            question["options"][i] for i in sorted(selected)
        ]

        context.user_data["question_index"] += 1
        context.user_data["selected"] = []

        await show_question(query, context)

    elif data == "habit_check":
        await query.edit_message_text(
            "🧠 Habit Check\n\n"
            "In this section, you'll answer 10 statements "
            "about your AI-use habits using a 1–5 scale.\n\n"
            "We'll implement this section next!"
        )


def main():
    if not TOKEN:
        raise ValueError(
            "BOT_TOKEN not found. Check your .env file."
        )

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("AI Reliance Check bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
