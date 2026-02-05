import json
import re
from collections import Counter

RULES_PATH = "data/meal_rules.json"


def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text.strip()


def generate_grocery_list(meal_names):
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        meal_rules = json.load(f)

    grocery = Counter()

    for meal in meal_names:
        meal_key = normalize(meal)

        if meal_key in meal_rules:
            for ingredient in meal_rules[meal_key]:
                grocery[ingredient] += 1
        else:
            grocery["unknown item"] += 1

    return dict(grocery)
