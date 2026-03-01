# nutrition_calc.py

from nutrition_data import INGREDIENT_RULES
from meal_ingredients_v2 import MEAL_INGREDIENTS

IDEAL_WEEKLY = {
    "carb": 20,
    "protein": 20,
    "fat": 15,
    "fiber": 15
}


def analyze_family_balance(meals, day_person_lookup):

    totals = {
        "carb": 0.0,
        "protein": 0.0,
        "fat": 0.0,
        "fiber": 0.0
    }

    total_person_count = 0   # ✅ correct normalization base

    for meal in meals:

        meal_list = [m.strip() for m in meal.meal_name.split(",")]
        meal_day = meal.day
        persons = day_person_lookup.get(meal_day, 1)

        if not persons or persons <= 0:
            persons = 1

        total_person_count += persons

        for meal_name in meal_list:

            meal_ingredients = MEAL_INGREDIENTS.get(meal_name, {})
            if not isinstance(meal_ingredients, dict):
                continue

            for ingredient, data in meal_ingredients.items():

                if not isinstance(data, dict):
                    continue

                qty = data.get("qty", 0)
                if not qty:
                    continue

                category = INGREDIENT_RULES.get(ingredient.lower())

                if category in totals:
                    totals[category] += float(qty) * persons

    # Avoid division by zero
    if total_person_count == 0:
        total_person_count = 1

    # ✅ Proper per-person weekly average
    for key in totals:
        totals[key] = round(totals[key] / total_person_count, 2)

    percentages = {}

    for nutrient in totals:
        ideal_value = IDEAL_WEEKLY.get(nutrient, 1)
        percentages[nutrient] = round(
            (totals[nutrient] / ideal_value) * 100,
            1
        )

    recommendations = generate_recommendations(percentages)

    return {
        "summary": totals,
        "percentages": percentages,
        "recommendations": recommendations
    }


def generate_recommendations(percentages):

    recommendations = []

    for nutrient, percent in percentages.items():

        if percent < 70:
            recommendations.append(
                f"{nutrient.capitalize()} intake is LOW. "
                f"Increase foods rich in {nutrient}."
            )

        elif percent > 130:
            recommendations.append(
                f"{nutrient.capitalize()} intake is HIGH. "
                f"Consider reducing excess {nutrient}-rich foods."
            )

        else:
            recommendations.append(
                f"{nutrient.capitalize()} intake is within healthy range."
            )

    return recommendations