import json
from collections import Counter


def load_ingredient_tags():
    with open("meal_ingredients.json", "r") as f:
        return json.load(f)

def detect_unhealthy_patterns(meals: list[list[str]]) -> list[str]:
    warnings = []
    ingredient_tags = load_ingredient_tags()

    # meals is already [["rice","oil"], ["burger"]]

    all_ingredients = []
    for meal in meals:
        all_ingredients.extend(meal)

    ingredient_count = Counter(all_ingredients)
    for ingredient, count in ingredient_count.items():
        if count > 3:
            warnings.append(
                f"'{ingredient}' is consumed too frequently this week."
            )
            break

    return warnings
