def extract_ingredients(meal_names):
    """
    Converts meal names into ingredient lists.
    Example:
    ["Rice, Oil", "Burger"] → [["rice","oil"], ["burger"]]
    """
    meals = []
    for meal in meal_names:
        meals.append(
            [i.strip().lower() for i in meal.split(",") if i.strip()]
        )
    return meals
