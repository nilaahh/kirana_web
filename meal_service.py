from meal_ingredients_v2 import MEAL_INGREDIENTS

# ---------------------------------------------------
# 1️⃣ Get meal from local database ONLY
# ---------------------------------------------------

def get_meal_ingredients(meal_name):
    meal_name = meal_name.lower().strip()
    return MEAL_INGREDIENTS.get(meal_name, {"error": f"Meal '{meal_name}' not found"})

# ---------------------------------------------------
# 2️⃣ Grocery Formatter (Converts dictionary to readable text)
# ---------------------------------------------------
def format_grocery_list(ingredients):
    if not ingredients:
        return "No ingredients found."
    
    if "error" in ingredients:
        return ingredients["error"]

    lines = []
    for item, data in ingredients.items():
        qty = data.get("qty")
        unit = data.get("unit", "")

        if qty is not None:
            # If unit exists, format with it; otherwise just the number
            unit_str = f" {unit}" if unit else ""
            lines.append(f"• {item.title()}: {qty}{unit_str}")
        else:
            lines.append(f"• {item.title()}: As needed")

    return "\n".join(lines)


# ---------------------------------------------------
# 3️⃣ Main Logic: Combine Multiple Meals
# ---------------------------------------------------
def generate_combined_list(meal_input_string):
    """
    Takes a string like 'Pasta, Salad' and returns a single 
    summed-up list of ingredients.
    """
    meals = meal_input_string.split(",")
    master_list = {}

    for meal in meals:
        meal_name = meal.strip().lower()
        if not meal_name:
            continue
            
        ingredients = get_meal_ingredients(meal_name)

        # Skip if the meal is missing from the database
        if "error" in ingredients:
            print(f"Warning: {ingredients['error']}")
            continue

        # Merge these ingredients into the master list
        for item, data in ingredients.items():
            qty = data.get("qty", 0)
            unit = data.get("unit", "")

            if item in master_list:
                # Add to existing quantity if item already exists
                master_list[item]["qty"] += qty
            else:
                # Create new entry if item is new
                master_list[item] = {"qty": qty, "unit": unit}

    return format_grocery_list(master_list)


# --- EXAMPLE USAGE ---
if __name__ == "__main__":
    # Simulate a user entering multiple meals
    user_input = "Pasta, Chicken Salad, Pasta" 
    
    print("--- YOUR SHOPPING LIST ---")
    print(generate_combined_list(user_input))