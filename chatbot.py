# chatbot.py

CONDITIONS = {
    "diabetes": ["diabetes", "diabetic", "blood sugar"],
    "hypertension": ["bp", "blood pressure", "hypertension"],
    "obesity": ["obese", "overweight", "weight loss"]
}

DIET_GUIDE = {
    "diabetes": {
        "avoid": [
            "Sugary foods",
            "Sugary drinks",
            "White rice and refined flour",
            "Deep-fried foods",
            "Processed snacks"
        ],
        "prefer": [
            "Whole grains",
            "High-fiber vegetables",
            "Lean protein (egg, fish, lentils)",
            "Healthy fats (nuts, seeds)"
        ]
    }
}


def detect_condition(message: str):
    message = message.lower()
    for condition, keywords in CONDITIONS.items():
        for word in keywords:
            if word in message:
                return condition
    return None


def generate_response(condition: str) -> str:
    guide = DIET_GUIDE[condition]

    response = f"Based on general dietary guidelines for {condition.capitalize()}:\n\n"
    response += "Foods to limit or avoid:\n"
    for item in guide["avoid"]:
        response += f"- {item}\n"

    response += "\nFoods to choose more often:\n"
    for item in guide["prefer"]:
        response += f"- {item}\n"

    response += "\n⚠️ This is general guidance, not medical advice."
    return response


def chatbot_reply(user_message: str) -> str:
    condition = detect_condition(user_message)

    if not condition:
        return (
            "I can help with diet guidance for conditions like:\n"
            "- Diabetes\n"
            "- Blood Pressure\n"
            "- Weight Management\n\n"
            "Please mention your condition."
        )

    return generate_response(condition)
