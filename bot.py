
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
    MessageHandler,
    ContextTypes,
    filters,
)

from questions import (
    QUICK_CHECK,
    HABIT_CHECK,
    POST_REFLECTION,
    FEEDBACK_QUESTION,
)

from challenges import AI_CHALLENGE, AI_FREE_CHALLENGE
from feedback import generate_reflection


# -----------------------------------
# BOT CONFIGURATION
# -----------------------------------

load_dotenv(override=True)

TOKEN = os.getenv("BOT_TOKEN")


def make_keyboard(options, prefix):
    """Create one Telegram button per answer."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                str(option),
                callback_data=f"{prefix}:{i}"
            )
        ]
        for i, option in enumerate(options)
    ])


async def send_long_text(message, text):
    """Split long messages to fit Telegram limits."""
    while text:
        if len(text) <= 4000:
            await message.reply_text(text)
            break

        split_at = text.rfind("\n", 0, 4000)

        if split_at <= 0:
            split_at = 4000

        await message.reply_text(text[:split_at])
        text = text[split_at:].lstrip("\n")


# -----------------------------------
# START COMMAND
# -----------------------------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    # Clear answers from previous sessions
    context.user_data.clear()
    context.user_data["stage"] = "welcome"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🚀 Start Quick Check",
                callback_data="start_quick"
            )
        ]
    ])

    message = (
        "🤖 WELCOME TO AI RELIANCE CHECK!\n\n"
        "Do you use AI because you need it, or "
        "because using it has become a habit?\n\n"
        "This bot helps you explore your AI-use "
        "habits through questions and reasoning tasks.\n\n"
        "You will complete:\n"
        "1. Quick Check\n"
        "2. Habit Check\n"
        "3. AI Challenge\n"
        "4. AI-Free Challenge\n"
        "5. Personal Reflection\n"
        "6. Post-Reflection Questions\n"
        "7. Optional Feedback\n\n"
        "Your responses are kept temporarily "
        "during this session.\n\n"
        "This bot is for self-reflection, "
        "not psychological diagnosis.\n\n"
        "Ready to begin?"
    )

    await update.message.reply_text(
        message,
        reply_markup=keyboard
    )


# -----------------------------------
# QUICK CHECK
# -----------------------------------

async def show_quick_question(query, context):
    index = context.user_data["quick_index"]

    if index >= len(QUICK_CHECK):
        context.user_data["stage"] = "quick_complete"

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "➡️ Continue to Habit Check",
                    callback_data="start_habit"
                )
            ]
        ])

        await query.edit_message_text(
            "✅ Quick Check completed!\n\n"
            "You've answered all five questions.\n\n"
            "Next: Habit Check.",
            reply_markup=keyboard
        )
        return

    question = QUICK_CHECK[index]
    multiple = question.get("multiple", False)

    selected = context.user_data.get("quick_selected", [])

    buttons = []

    for i, option in enumerate(question["options"]):
        label = option

        if multiple and i in selected:
            label = "✅ " + option

        buttons.append([
            InlineKeyboardButton(
                label,
                callback_data=f"quick_answer:{index}:{i}"
            )
        ])

    if multiple:
        buttons.append([
            InlineKeyboardButton(
                "➡️ Done selecting",
                callback_data=f"quick_done:{index}"
            )
        ])

    text = (
        f"📝 QUICK CHECK — {index + 1}/5\n\n"
        f"{question['question']}"
    )

    if multiple:
        text += "\n\nSelect all that apply, then press Done."

    context.user_data["stage"] = "quick"

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# -----------------------------------
# HABIT CHECK
# -----------------------------------

async def show_habit_question(query, context):
    index = context.user_data["habit_index"]

    if index >= len(HABIT_CHECK):
        context.user_data["stage"] = "habit_complete"

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🚀 Continue to AI Challenge",
                    callback_data="start_ai"
                )
            ]
        ])

        await query.edit_message_text(
            "✅ Habit Check completed!\n\n"
            "You've answered all 11 statements.\n\n"
            "Next, you'll complete a reasoning "
            "task where AI use is allowed.",
            reply_markup=keyboard
        )
        return

    statement = HABIT_CHECK[index]

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                str(rating),
                callback_data=f"habit_answer:{index}:{rating}"
            )
            for rating in range(1, 6)
        ]
    ])

    text = (
        f"🧠 HABIT CHECK — Question {index + 6}/16\n\n"
        f"{statement}\n\n"
        "How much do you agree?\n\n"
        "1 — Strongly disagree\n"
        "2 — Disagree\n"
        "3 — Neither agree nor disagree\n"
        "4 — Agree\n"
        "5 — Strongly agree"
    )

    context.user_data["stage"] = "habit"

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


# -----------------------------------
# CHALLENGES
# -----------------------------------

def get_challenge(context):
    if context.user_data.get("challenge_type") == "ai":
        return AI_CHALLENGE

    return AI_FREE_CHALLENGE


async def show_challenge(query, context, kind):
    context.user_data["challenge_type"] = kind
    context.user_data["challenge_index"] = 0
    context.user_data["stage"] = "challenge_answer"

    challenge = get_challenge(context)

    text = (
        f"🤖 {challenge['title'].upper()}\n\n"
        f"Instructions:\n{challenge['instructions']}\n\n"
        f"Scenario:\n{challenge['scenario']}\n\n"
        f"Your task:\n{challenge['task']}\n\n"
        "✍️ Write your answer and send it "
        "as a Telegram message."
    )

    await query.edit_message_text(text)


async def show_challenge_followup(message, context):
    challenge = get_challenge(context)
    index = context.user_data["challenge_index"]

    if index >= len(challenge["followups"]):
        await finish_challenge(message, context)
        return

    item = challenge["followups"][index]

    keyboard = make_keyboard(
        item["options"],
        f"challenge_answer:{index}"
    )

    text = (
        f"📋 FOLLOW-UP QUESTION {index + 1}/3\n\n"
        f"{item['question']}"
    )

    if "scale" in item:
        text += f"\n\n{item['scale']}"

    context.user_data["stage"] = "challenge_followup"

    await message.reply_text(
        text,
        reply_markup=keyboard
    )


async def finish_challenge(message, context):
    kind = context.user_data["challenge_type"]

    if kind == "ai":
        context.user_data["stage"] = "ai_complete"

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "➡️ Continue to AI-Free Challenge",
                    callback_data="start_ai_free"
                )
            ]
        ])

        await message.reply_text(
            "✅ AI Challenge completed!\n\n"
            "Next, complete a similar reasoning task "
            "without using generative AI.",
            reply_markup=keyboard
        )

    else:
        context.user_data["stage"] = "challenges_complete"

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🪞 View My Reflection",
                    callback_data="show_reflection"
                )
            ]
        ])

        await message.reply_text(
            "✅ Both challenges completed!\n\n"
            "You can now review your AI-use habits "
            "and your experience during the tasks.",
            reply_markup=keyboard
        )


# -----------------------------------
# PERSONALIZED REFLECTION
# -----------------------------------

async def show_reflection(query, context):
    reflection = generate_reflection(context.user_data)

    context.user_data["stage"] = "reflection"

    await query.edit_message_text(
        "🪞 Your reflection is ready!"
    )

    await send_long_text(query.message, reflection)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➡️ Continue to Post-Reflection",
                callback_data="start_post"
            )
        ]
    ])

    await query.message.reply_text(
        "Would you like to reflect on what "
        "you learned from this experience?",
        reply_markup=keyboard
    )


# -----------------------------------
# POST-REFLECTION
# -----------------------------------

async def show_post_question(query, context):
    index = context.user_data["post_index"]

    if index >= len(POST_REFLECTION):
        context.user_data["stage"] = "post_complete"

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "💬 Continue to Feedback",
                    callback_data="start_feedback"
                )
            ]
        ])

        await query.edit_message_text(
            "✅ Post-Reflection completed!\n\n"
            "Thank you for reflecting on "
            "your experience.\n\n"
            "There is one optional feedback question left.",
            reply_markup=keyboard
        )
        return

    question = POST_REFLECTION[index]

    keyboard = make_keyboard(
        question["options"],
        f"post_answer:{index}"
    )

    context.user_data["stage"] = "post"

    await query.edit_message_text(
        f"💭 POST-REFLECTION — Question {index + 17}/19\n\n"
        f"{question['question']}",
        reply_markup=keyboard
    )


# -----------------------------------
# USER FEEDBACK
# -----------------------------------

async def show_feedback(query, context):
    context.user_data["stage"] = "feedback"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⏭️ Skip Feedback",
                callback_data="skip_feedback"
            )
        ]
    ])

    await query.edit_message_text(
        f"💬 QUESTION 20 — OPTIONAL FEEDBACK\n\n"
        f"{FEEDBACK_QUESTION}\n\n"
        "Type your feedback as a message, "
        "or press Skip Feedback.\n\n"
        "Your feedback will only be held "
        "temporarily in this bot session.",
        reply_markup=keyboard
    )


async def finish_bot(message, context):
    context.user_data["stage"] = "finished"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔄 Start Again",
                callback_data="restart"
            )
        ]
    ])

    await message.reply_text(
        "🎉 AI RELIANCE CHECK COMPLETED!\n\n"
        "Thank you for participating!\n\n"
        "Remember: AI can be a useful tool, "
        "but independent thinking is also important.\n\n"
        "The goal is to use AI intentionally "
        "rather than automatically.",
        reply_markup=keyboard
    )


# -----------------------------------
# HANDLE BUTTON CLICKS
# -----------------------------------

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    data = query.data
    stage = context.user_data.get("stage")

    # Start Quick Check
    if data == "start_quick":
        if stage != "welcome":
            return

        context.user_data["quick_index"] = 0
        context.user_data["quick_answers"] = {}
        context.user_data["quick_selected"] = []

        await show_quick_question(query, context)

    # Quick Check answer
    elif data.startswith("quick_answer:"):
        if stage != "quick":
            return

        _, q_index, option_index = data.split(":")
        q_index = int(q_index)
        option_index = int(option_index)

        if q_index != context.user_data["quick_index"]:
            return

        question = QUICK_CHECK[q_index]

        if not 0 <= option_index < len(question["options"]):
            return

        if question.get("multiple", False):
            selected = context.user_data["quick_selected"]

            if option_index in selected:
                selected.remove(option_index)
            else:
                selected.append(option_index)

            await show_quick_question(query, context)

        else:
            context.user_data["quick_answers"][q_index] = (
                question["options"][option_index]
            )

            context.user_data["quick_index"] += 1
            await show_quick_question(query, context)

    # Finish multiple-selection question
    elif data.startswith("quick_done:"):
        if stage != "quick":
            return

        q_index = int(data.split(":")[1])

        if q_index != context.user_data["quick_index"]:
            return

        question = QUICK_CHECK[q_index]

        if not question.get("multiple", False):
            return

        selected = context.user_data["quick_selected"]

        if not selected:
            await query.answer(
                "Please select at least one answer.",
                show_alert=True
            )
            return

        context.user_data["quick_answers"][q_index] = [
            question["options"][i]
            for i in sorted(selected)
        ]

        context.user_data["quick_selected"] = []
        context.user_data["quick_index"] += 1

        await show_quick_question(query, context)

    # Start Habit Check
    elif data == "start_habit":
        if stage != "quick_complete":
            return

        context.user_data["habit_index"] = 0
        context.user_data["habit_answers"] = []

        await show_habit_question(query, context)

    # Habit Check answer
    elif data.startswith("habit_answer:"):
        if stage != "habit":
            return

        _, q_index, rating = data.split(":")
        q_index = int(q_index)
        rating = int(rating)

        if q_index != context.user_data["habit_index"]:
            return

        if rating not in range(1, 6):
            return

        context.user_data["habit_answers"].append(rating)
        context.user_data["habit_index"] += 1

        await show_habit_question(query, context)

    # Start AI Challenge
    elif data == "start_ai":
        if stage != "habit_complete":
            return

        context.user_data["ai_followup_answers"] = []
        await show_challenge(query, context, "ai")

    # Start AI-Free Challenge
    elif data == "start_ai_free":
        if stage != "ai_complete":
            return

        context.user_data["ai_free_followup_answers"] = []
        await show_challenge(query, context, "ai_free")

    # Challenge follow-up answer
    elif data.startswith("challenge_answer:"):
        if stage != "challenge_followup":
            return

        _, q_index, option_index = data.split(":")
        q_index = int(q_index)
        option_index = int(option_index)

        if q_index != context.user_data["challenge_index"]:
            return

        challenge = get_challenge(context)
        item = challenge["followups"][q_index]

        if not 0 <= option_index < len(item["options"]):
            return

        answer = item["options"][option_index]

        if answer in ["1", "2", "3", "4", "5"]:
            answer = int(answer)

        kind = context.user_data["challenge_type"]

        if kind == "ai":
            context.user_data[
                "ai_followup_answers"
            ].append(answer)
        else:
            context.user_data[
                "ai_free_followup_answers"
            ].append(answer)

        context.user_data["challenge_index"] += 1

        await query.edit_message_reply_markup(
            reply_markup=None
        )

        await show_challenge_followup(
            query.message,
            context
        )

    # Personalized reflection
    elif data == "show_reflection":
        if stage != "challenges_complete":
            return

        await show_reflection(query, context)

    # Start Post-Reflection
    elif data == "start_post":
        if stage != "reflection":
            return

        context.user_data["post_index"] = 0
        context.user_data["post_answers"] = []

        await show_post_question(query, context)

    # Post-Reflection answer
    elif data.startswith("post_answer:"):
        if stage != "post":
            return

        _, q_index, option_index = data.split(":")
        q_index = int(q_index)
        option_index = int(option_index)

        if q_index != context.user_data["post_index"]:
            return

        question = POST_REFLECTION[q_index]

        if not 0 <= option_index < len(question["options"]):
            return

        context.user_data["post_answers"].append(
            question["options"][option_index]
        )

        context.user_data["post_index"] += 1

        await show_post_question(query, context)

    # Start optional feedback
    elif data == "start_feedback":
        if stage != "post_complete":
            return

        await show_feedback(query, context)

    # Skip feedback
    elif data == "skip_feedback":
        if stage != "feedback":
            return

        context.user_data["user_feedback"] = None

        await query.edit_message_reply_markup(
            reply_markup=None
        )

        await finish_bot(query.message, context)

    # Restart bot
    elif data == "restart":
        if stage != "finished":
            return

        context.user_data.clear()
        context.user_data["stage"] = "welcome"

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🚀 Start Quick Check",
                    callback_data="start_quick"
                )
            ]
        ])

        await query.edit_message_text(
            "🤖 Welcome back to AI Reliance Check!\n\n"
            "Ready to begin again?",
            reply_markup=keyboard
        )


# -----------------------------------
# HANDLE WRITTEN ANSWERS
# -----------------------------------

async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    stage = context.user_data.get("stage")
    text = update.message.text.strip()

    if not text:
        await update.message.reply_text(
            "Please enter a written response."
        )
        return

    # Written reasoning challenge response
    if stage == "challenge_answer":
        kind = context.user_data["challenge_type"]

        if kind == "ai":
            context.user_data["ai_challenge_answer"] = text
        else:
            context.user_data["ai_free_challenge_answer"] = text

        context.user_data["challenge_index"] = 0

        await update.message.reply_text(
            "✅ Your answer has been received!\n\n"
            "Now answer three short questions "
            "about your experience."
        )

        await show_challenge_followup(
            update.message,
            context
        )

    # Optional feedback response
    elif stage == "feedback":
        context.user_data["user_feedback"] = text

        await update.message.reply_text(
            "Thank you for your feedback!"
        )

        await finish_bot(update.message, context)

    else:
        await update.message.reply_text(
            "Please use the buttons to continue.\n\n"
            "Send /start if you want to restart."
        )


# -----------------------------------
# MAIN FUNCTION
# -----------------------------------

def main():
    if not TOKEN:
        raise ValueError(
            "BOT_TOKEN not found. Check your .env file."
        )

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    print("AI Reliance Check bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
