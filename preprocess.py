import json
import re

INPUT_JSON = "data/test.json"
OUTPUT_JSON = "data/meal_ingredients.json"

def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalize(ing):
    REMOVE = [
        "fresh", "chopped", "sliced", "minced",
        "tablespoon", "teaspoon", "cup", "cups",
        "tbsp", "tsp"
    ]

    ing = clean(ing)
    for r in REMOVE:
        ing = ing.replace(r, "")
    return ing.strip()

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

meal_map = {}

# ---- KEY FIX: data is a DICT ----
for title, ingredients in data.items():
    title = clean(title)

    clean_ings = []
    for ing in ingredients:
        norm = normalize(ing)
        if len(norm) > 2:
            clean_ings.append(norm)

    if title and clean_ings:
        meal_map[title] = list(set(clean_ings))

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(meal_map, f, indent=2)

print(f"✅ Saved {len(meal_map)} meals")
