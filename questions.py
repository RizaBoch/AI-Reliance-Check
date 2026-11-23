
# QUICK CHECK — QUESTIONS 1–5

QUICK_CHECK = [
    {
        "question": "How often do you use generative AI tools (such as ChatGPT, Gemini, or Claude)?",
        "options": [
            "Several times a day",
            "Once a day",
            "A few times a week",
            "Rarely",
            "Never"
        ]
    },
    {
        "question": "What do you usually use AI for? (Select all that apply.)",
        "options": [
            "Studying or learning",
            "Writing or editing",
            "Searching for explanations or information",
            "Generating ideas",
            "Planning or making decisions",
            "Coding or solving problems"
        ],
        "multiple": True
    },
    {
        "question": "When do you usually open AI while completing a task?",
        "options": [
            "Before I start",
            "After trying independently",
            "When I get stuck",
            "Only to check my work",
            "I usually don't use AI"
        ]
    },
    {
        "question": "Approximately how much of your work do you usually complete with AI assistance?",
        "options": [
            "None",
            "1–25%",
            "26–50%",
            "51–75%",
            "76–100%"
        ]
    },
    {
        "question": "What is your main reason for using AI?",
        "options": [
            "To save time",
            "To understand something difficult",
            "To improve my work",
            "Because I don't know how to start",
            "Because using AI has become a habit",
            "Other"
        ]
    }
]


# HABIT CHECK — QUESTIONS 6–16
# Scale: 1 = Strongly disagree, 5 = Strongly agree

HABIT_CHECK = [
    "When I receive a difficult task, using AI is one of the first solutions that comes to mind.",

    "I feel that AI is always available whenever I need help with a task.",

    "I find it difficult to start certain tasks without asking AI for help.",

    "I ask AI for answers before trying to solve problems independently.",

    "I use AI to generate ideas instead of thinking of my own ideas first.",

    "I rely on AI to explain information that I could try to understand independently.",

    "I use AI to make decisions that I could make on my own.",

    "I feel uncomfortable when I cannot use AI for a task I normally complete with its help.",

    "I often accept AI-generated answers without checking them carefully.",

    "I can complete most tasks that I usually do with AI without its assistance.",

    "I have used AI so much that I would feel something was missing if I could no longer use it."
]


# POST-REFLECTION — QUESTIONS 17–19

POST_REFLECTION = [
    {
        "question": "After completing this bot, do you have a better understanding of how much you rely on AI?",
        "options": [
            "Yes, much better",
            "Yes, somewhat better",
            "No change",
            "No, I am still unsure"
        ]
    },
    {
        "question": "Did the bot help you recognize any AI-use habits that you had not noticed before?",
        "options": [
            "Yes, several",
            "Yes, one or two",
            "No, I was already aware of my habits",
            "No, I did not understand my results"
        ]
    },
    {
        "question": "After completing the challenges, are you more likely to try solving a task independently before using AI?",
        "options": [
            "Definitely yes",
            "Probably yes",
            "Not sure",
            "Probably not",
            "Definitely not"
        ]
    }
]


# USER FEEDBACK — QUESTION 20

FEEDBACK_QUESTION = (
    "What did you think about the bot? "
    "Was anything confusing, unhelpful, or difficult to use? "
    "What would you improve?"
)
