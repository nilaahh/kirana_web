from meal_service import get_meal_ingredients


def generate_weekly_grocery(meals, persons):
    grocery = {}

    for meal in meals:

        # Get string
        meal_string = meal.meal_name if hasattr(meal, "meal_name") else str(meal)

        # Split multiple meals
        meal_list = meal_string.split(",")

        for single_meal in meal_list:
            meal_name = single_meal.strip().lower()

            ingredients = get_meal_ingredients(meal_name)

            if "error" in ingredients:
                print(ingredients["error"])
                continue

            for item, data in ingredients.items():
                qty = data["qty"]
                unit = data["unit"]

                total_qty = float(qty) * persons

                if item not in grocery:
                    grocery[item] = {"qty": 0, "unit": unit}

                grocery[item]["qty"] += total_qty

    # Clean rounding
    for item in grocery:
        val = grocery[item]["qty"]
        val = round(val, 2)
        grocery[item]["qty"] = int(val) if val % 1 == 0 else val

    return grocery
