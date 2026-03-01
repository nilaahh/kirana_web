from meal_ingredients_v2 import MEAL_INGREDIENTS

def get_suggestions(user_ingredients_str):
    # 1. Clean the user input (e.g., "Chicken, Onion" -> ["chicken", "onion"])
    user_has = [i.strip().lower() for i in user_ingredients_str.split(",") if i.strip()]
    
    if not user_has:
        return []

    suggestions = []

    # 2. Loop through your recipes
    for meal_name, recipe_dict in MEAL_INGREDIENTS.items():
        recipe_ingredients = list(recipe_dict.keys())
        total_needed = len(recipe_ingredients)
        
        # 3. Find matches
        matches = [i for i in recipe_ingredients if i in user_has]
        missing = [i for i in recipe_ingredients if i not in user_has]
        
        # 4. Calculate score
        score = (len(matches) / total_needed) * 100
        
        # 5. Only suggest if there is at least one match
        if len(matches) > 0:
            suggestions.append({
                "meal": meal_name.replace("_", " ").title(),
                "score": round(score),
                "matching_count": len(matches),
                "total_count": total_needed,
                "missing": [m.replace("_", " ").title() for m in missing]
            })

    # 6. Sort by highest score first
    return sorted(suggestions, key=lambda x: x['score'], reverse=True)