import json
import os
from collections import Counter

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "data", "meal_ingredients.json")) as f:
    MEAL_INGREDIENTS = json.load(f)

with open(os.path.join(BASE_DIR, "data", "ingredient_nutrients.json")) as f:
    INGREDIENT_NUTRIENTS = json.load(f)


def analyze_nutrition(meal_names: list[str]) -> dict:
    nutrient_counter = Counter()

    for meal in meal_names:
        key = meal.lower()

        if key not in MEAL_INGREDIENTS:
            continue

        for ingredient in MEAL_INGREDIENTS[key]:
            nutrients = INGREDIENT_NUTRIENTS.get(ingredient, [])
            for n in nutrients:
                nutrient_counter[n] += 1

    summary = dict(nutrient_counter)

    recommendations = []

    if nutrient_counter["protein"] < 3:
        recommendations.append("Increase protein intake (eggs, dal, fish, chicken).")

    if nutrient_counter["fiber"] < 3:
        recommendations.append("Add more vegetables and fiber-rich foods.")

    if nutrient_counter["carb"] > nutrient_counter["protein"] * 2:
        recommendations.append("Reduce carb-heavy meals and balance with protein.")

    if not recommendations:
        recommendations.append("Your meals are nutritionally balanced. Good job.")

    return {
        "summary": summary,
        "recommendations": recommendations
    }