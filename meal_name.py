from meal_ingredients_v2 import MEAL_INGREDIENTS

def get_all_meal_names(search_query=None):
    # 1. Get all keys from your dictionary
    # Replace underscores with spaces and capitalize for the UI
    all_meals = [m.replace("_", " ").title() for m in MEAL_INGREDIENTS.keys()]
    all_meals.sort()

    # 2. If the user searched for something, filter the list
    if search_query:
        query = search_query.lower().strip()
        filtered_meals = [m for m in all_meals if query in m.lower()]
        return filtered_meals

    return all_meals