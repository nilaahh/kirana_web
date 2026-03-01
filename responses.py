# disease_responses.py

DISEASE_RESPONSES = {
    "greeting": "Hello! I am your Kirana Health Assistant. Ask me about diet guidance for health conditions.",
    
    "diabetes": (
        "<b>Diabetes:</b><br>"
        " <u>Whole Grains:</u> Brown rice, quinoa, barley, steel-cut oats, whole wheat roti.<br>"
        " <u>Vegetables:</u> Spinach, broccoli, kale, bottle gourd, okra, zucchini, bell peppers.<br>"
        " <u>Fruits:</u> Papaya, guava, pomegranate, dragon fruit, watermelon (in moderation), pineapple (controlled portions).<br>"
        " <u>Proteins:</u> Tofu, paneer, lentils, chickpeas, boiled eggs, grilled chicken, fish (salmon).<br>"
        " <u>Healthy Fats:</u> Avocado, olive oil, flaxseed, walnuts, almonds, chia seeds, ghee (in moderation).<br>"
        " <u>Avoid:</u> White rice, maida, white bread, potato (excess), sweet corn (limit), refined sugar, sweets, sugary drinks.<br>"
        " <u>Tip:</u> Pair iron-rich meals with Vitamin C, eat fiber-rich foods, and stay active with daily walks."
    ),

    "hypertension": (
        "<b>Hypertension:</b><br>"
        " <u>Include:</u> Fruits & vegetables (spinach, kale, beetroot, bananas, strawberries), whole grains (brown rice, oats, whole-wheat bread/pasta), lean proteins (chicken, turkey, fish, beans), low-fat dairy (semi-skimmed milk, yogurt).<br>"
        " <u>Avoid/Limit:</u> Salty foods (processed meats, pickles, bread), sugary & fatty foods, excess alcohol, excess caffeine.<br>"
        " <u>Tip:</u> Be physically active, maintain healthy weight, stop smoking, and take medications as prescribed."
    ),

    "thyroid": (
        "<b>Thyroid:</b><br>"
        " <u>Iodine:</u> Iodized salt, seafood, dairy.<br>"
        " <u>Selenium:</u> Brazil nuts (1–2/day), seafood, eggs, sunflower seeds, lean meats.<br>"
        " <u>Zinc & Iron:</u> Oysters, red meat, poultry, lentils, beans, pumpkin seeds, spinach.<br>"
        " <u>Vitamin D & B12:</u> Fatty fish, fortified dairy/plant milk, eggs, mushrooms, animal products.<br>"
        " <u>Omega-3 & Anti-inflammatory:</u> Salmon, mackerel, sardines, walnuts, chia, flaxseeds.<br>"
        " <u>Fiber & Gut-Friendly:</u> Whole grains, legumes, fruits, vegetables, yogurt, kefir.<br>"
        " <u>Avoid:</u> High-dose iodine supplements, excess raw cruciferous veggies, processed soy (with meds), excessive fiber with meds, calcium/iron supplements with meds, processed foods, sugar, trans fats.<br>"
        " <u>Tip:</u> Separate fiber and supplements from thyroid medication timing; favor whole foods."
    ),

    "weight_gain": (
        "<b>Weight Gain:</b><br>"
        " <u>Protein:</u> Lean meats, fatty fish, eggs, dairy, lentils, chickpeas, tofu, quinoa.<br>"
        " <u>Healthy Fats:</u> Avocados, nuts, seeds, nut butters, olive/coconut oil.<br>"
        " <u>Complex Carbs:</u> Whole grains (quinoa, brown rice, oats), starchy vegetables (sweet potato, squash, potatoes), legumes.<br>"
        " <u>Snacks:</u> Greek yogurt with granola, protein smoothies, protein bars, trail mix, whole-grain crackers with hummus.<br>"
        " <u>Tip:</u> Eat frequent meals and snacks; pair protein, carbs, and healthy fats each meal."
    ),

    "weight_loss": (
        "<b>Weight Loss:</b><br>"
        " <u>Vegetables:</u> Salad greens, asparagus, carrots, tomatoes, broccoli, zucchini.<br>"
        " <u>Fruits:</u> Fresh, frozen, canned without syrup (blueberries, mango, peaches, mandarins).<br>"
        " <u>Whole Grains:</u> Whole-wheat bread/pasta, oatmeal, brown rice, whole-grain cereal.<br>"
        " <u>Protein & Dairy:</u> Lean meats, poultry, fish, beans, lentils, peas, low-fat/fat-free dairy, egg whites.<br>"
        " <u>Healthy Fats:</u> Nuts, seeds, olive oil, flaxseed, safflower oil. Limit saturated/trans fats.<br>"
        " <u>Sweets:</u> Occasional healthy treats like fruit with yogurt or small dark chocolate.<br>"
        " <u>Tip:</u> Focus on low-energy-dense foods to feel full on fewer calories."
    ),

    "cholesterol": (
        "<b>Cholesterol:</b><br>"
        " <u>Fruits & Vegetables:</u> Berries, grapes, pears, oranges, apples, tomatoes, yams, broccoli, cauliflower, celery, spinach, kale, squash, zucchini, eggplant, bell peppers.<br>"
        " <u>Whole Grains:</u> Oats, oat bran, quinoa, barley, wheat berries, flaxseed, polenta, millet, bulgur, whole-wheat bread/pasta.<br>"
        " <u>Lean Proteins & Legumes:</u> Skinless chicken/turkey, lean red meat, tofu, tempeh, seitan, lentils, beans.<br>"
        " <u>Nuts & Seeds:</u> Almonds, walnuts, chia seeds, flaxseeds (~2 oz/day).<br>"
        " <u>Dairy & Calcium:</u> Low-fat/reduced-fat milk, yogurt, cottage cheese, fortified plant-based milk.<br>"
        " <u>Omega-3 & Vitamin D:</u> Fatty fish, egg yolks.<br>"
        " <u>Avoid:</u> Fried foods, trans fats, high-fat processed meats, full-fat dairy, excess sugar, highly processed snacks.<br>"
        " <u>Tip:</u> Focus on fiber, heart-healthy fats, and lean protein."
    ),

    "anemia": (
        "<b>Anemia:</b><br>"
        " <u>Heme Iron:</u> Red meat (beef, lamb), liver, poultry, seafood (clams, oysters, tuna).<br>"
        " <u>Non-Heme Iron:</u> Spinach, lentils, beans, fortified cereals, dried fruits (raisins, apricots).<br>"
        " <u>Vitamin C Boosters:</u> Oranges, bell peppers, broccoli, tomatoes, kiwi, strawberries.<br>"
        " <u>Avoid with Iron Meals:</u> Calcium-rich dairy, tea, coffee, large high-fiber meals.<br>"
        " <u>Tip:</u> Pair iron sources with Vitamin C and separate iron meals from calcium or caffeine."
    ),

    "copd": (
        "<b>COPD:</b><br>"
        " <u>Complex Carbs:</u> Whole grains, whole grain bread/pasta, beans, lentils, starchy vegetables, fresh fruit.<br>"
        " <u>Fiber:</u> Beans, lentils, fruits, vegetables, nuts, seeds, oats. Aim 20–30g/day.<br>"
        " <u>Protein:</u> Meat, poultry, fish, eggs, nuts, seeds, legumes, tofu, cheese, milk.<br>"
        " <u>Healthy Fats:</u> Olive oil, avocado oil, fatty fish, avocados, nuts, seeds.<br>"
        " <u>Tip:</u> Eat small frequent meals, stay hydrated, and balance carbs, protein, and fats for weight goals."
    ),

    "unknown": "I'm not sure I understand. Please ask about diet-related health conditions like diabetes, hypertension, anemia, etc."
}
