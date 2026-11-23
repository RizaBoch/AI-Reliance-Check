
AI_CHALLENGE = {
    "title": "AI Challenge",
    "instructions": (
        "You may use AI to complete this task."
    ),
    "scenario": (
        "A university wants to replace some traditional "
        "lectures with recorded video lessons. "
        "Supporters argue that students will have more "
        "flexibility, while opponents believe that "
        "students will lose opportunities to ask "
        "questions and interact with instructors."
    ),
    "task": (
        "Give two advantages and two disadvantages "
        "of this change. Then explain whether you "
        "would recommend it and why."
    ),
    "followups": [
        {
            "question": "Did you use AI for this task?",
            "options": ["Yes", "No"]
        },
        {
            "question": "How difficult was the task?",
            "options": ["1", "2", "3", "4", "5"],
            "scale": "1 = Very easy; 5 = Very difficult"
        },
        {
            "question": "How confident are you in your answer?",
            "options": ["1", "2", "3", "4", "5"],
            "scale": "1 = Not confident; 5 = Very confident"
        }
    ]
}


AI_FREE_CHALLENGE = {
    "title": "AI-Free Challenge",
    "instructions": (
        "Complete this task independently without "
        "using generative AI."
    ),
    "scenario": (
        "A university wants to replace some printed "
        "textbooks with digital learning materials. "
        "Supporters argue that digital materials are "
        "more convenient and easier to update, while "
        "opponents believe that students may become "
        "distracted and have difficulty studying "
        "from screens."
    ),
    "task": (
        "Give two advantages and two disadvantages "
        "of this change. Then explain whether you "
        "would recommend it and why."
    ),
    "followups": [
        {
            "question": "How difficult was the task?",
            "options": ["1", "2", "3", "4", "5"],
            "scale": "1 = Very easy; 5 = Very difficult"
        },
        {
            "question": "How confident are you in your answer?",
            "options": ["1", "2", "3", "4", "5"],
            "scale": "1 = Not confident; 5 = Very confident"
        },
        {
            "question": "How strongly did you want to use AI?",
            "options": ["1", "2", "3", "4", "5"],
            "scale": "1 = Not at all; 5 = Very strongly"
        }
    ]
}
