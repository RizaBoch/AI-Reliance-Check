
def generate_reflection(data):
    habit = data.get("habit_answers", [])
    quick = data.get("quick_answers", {})
    ai = data.get("ai_followup_answers", [])
    ai_free = data.get("ai_free_followup_answers", [])

    messages = [
        "🪞 YOUR PERSONAL AI RELIANCE REFLECTION\n",
        "Your answers suggest the following patterns "
        "in how you experience and use generative AI.\n"
    ]

    # Habit Check positions:
    # 0=Q6, 1=Q7, ..., 10=Q16

    if len(habit) == 11:

        # Automatic consultation
        if habit[0] >= 4 or habit[3] >= 4:
            messages.append(
                "🔄 Automatic AI consultation\n"
                "You reported that AI often comes to mind "
                "early when solving problems. Consider "
                "trying your own approach before opening AI.\n"
            )

        # Perceived availability
        if habit[1] >= 4:
            messages.append(
                "📱 AI availability\n"
                "You see AI as a readily available source "
                "of help. Accessibility can be useful, "
                "but availability does not always mean "
                "you need assistance.\n"
            )

        # Difficulty working independently
        if habit[2] >= 4:
            messages.append(
                "🧩 Starting independently\n"
                "You sometimes find it difficult to "
                "begin tasks without AI. Try writing "
                "down your first idea before asking "
                "AI for suggestions.\n"
            )

        # Cognitive offloading
        if any(habit[i] >= 4 for i in [4, 5, 6]):
            messages.append(
                "🧠 Cognitive offloading\n"
                "You reported using AI for activities "
                "such as generating ideas, understanding "
                "information, or making decisions. "
                "Consider which parts you want to "
                "practice independently.\n"
            )

        # Discomfort without AI
        if habit[7] >= 4 or habit[10] >= 4:
            messages.append(
                "💭 Feelings about AI access\n"
                "You reported that being unable to use "
                "AI could feel uncomfortable or leave "
                "something missing. This may be worth "
                "reflecting on, without assuming it "
                "indicates dependency.\n"
            )

        # Checking answers
        if habit[8] >= 4:
            messages.append(
                "🔍 Checking AI-generated answers\n"
                "You sometimes accept AI answers without "
                "carefully checking them. Try verifying "
                "important information with reliable "
                "sources.\n"
            )

        # Independent capability
        if habit[9] >= 4:
            messages.append(
                "💪 Independent work\n"
                "You believe you can complete many "
                "AI-assisted tasks independently. "
                "This is a useful ability to maintain.\n"
            )

    # Quick Check: timing of AI consultation
    if quick.get(2) == "Before I start":
        messages.append(
            "⏱️ When you consult AI\n"
            "You usually open AI before starting a task. "
            "You could experiment with spending five "
            "minutes thinking independently first.\n"
        )

    # AI Challenge responses:
    # [used AI, difficulty, confidence]
    if len(ai) == 3 and len(ai_free) == 3:
        ai_difficulty = int(ai[1])
        ai_confidence = int(ai[2])

        free_difficulty = int(ai_free[0])
        free_confidence = int(ai_free[1])
        desire = int(ai_free[2])

        messages.append(
            "⚖️ YOUR CHALLENGE EXPERIENCE\n"
            f"AI Challenge difficulty: {ai_difficulty}/5\n"
            f"AI Challenge confidence: {ai_confidence}/5\n"
            f"AI-Free difficulty: {free_difficulty}/5\n"
            f"AI-Free confidence: {free_confidence}/5\n"
            f"Desire to use AI: {desire}/5\n"
        )

        if ai[0] == "No":
            messages.append(
                "You reported completing the first "
                "challenge without AI, even though "
                "AI use was permitted.\n"
            )

        if free_difficulty > ai_difficulty:
            messages.append(
                "You rated the AI-Free Challenge as "
                "more difficult. Remember that the "
                "tasks covered different topics, "
                "so this difference cannot be "
                "attributed to AI use alone.\n"
            )

        elif free_difficulty < ai_difficulty:
            messages.append(
                "You rated the AI-Free Challenge as "
                "easier. Task familiarity and topic "
                "differences may have influenced "
                "your experience.\n"
            )

        if desire >= 4:
            messages.append(
                "You experienced a strong desire "
                "to consult AI during the independent "
                "challenge. Consider what made you "
                "want to use it.\n"
            )

    messages.append(
        "🌱 FINAL THOUGHT\n"
        "The goal is not to stop using AI completely. "
        "Instead, think about when AI genuinely helps "
        "you and when you might benefit from trying "
        "something independently first.\n\n"
        "This reflection is based on self-reported "
        "answers and is not a validated psychological "
        "assessment."
    )

    return "\n".join(messages)
