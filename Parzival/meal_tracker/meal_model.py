from .persistence import load_meals, save_meals
import datetime

SAFE_FOODS = {
    "breakfast": [
        "fried eggs", "scrambled eggs", "crispy bacon",
        "bacon egg and cheese", "cereal", "muffins", "croissants",
        "bagels", "english muffin with butter",
        "pancakes", "waffles", "french toast"
    ],
    "lunch_dinner": [
        "pizza", "cheesy breadsticks", "mozzarella sticks",
        "cheese quesadilla", "kraft mac and cheese",
        "crispy chicken tenders", "nuggets", "boneless wings",
        "french fries", "ensure shake"
    ]
}

def log_meal(category, food_item):
    date = str(datetime.date.today())
    meals = load_meals()

    if date not in meals:
        meals[date] = {"breakfast": [], "lunch": [], "dinner": [], "snack": [], "notes": ""}

    if category not in meals[date]:
        meals[date][category] = []

    meals[date][category].append(food_item)

    is_safe = food_item.lower() in SAFE_FOODS.get("breakfast", []) + SAFE_FOODS.get("lunch_dinner", [])
    print(f"Meal logged: {category} - {food_item} ({'safe' if is_safe else 'new/unsure'})")

    save_meals(meals)

def view_today():
    today = str(datetime.date.today())
    meals = load_meals()
    return meals.get(today, {})

def delete_meal(category, food_item, date=None):
    if date is None:
        date = str(datetime.date.today())

    meals = load_meals()
    if date in meals and category in meals[date]:
        if food_item in meals[date][category]:
            meals[date][category].remove(food_item)
            save_meals(meals)
            return True
    return False

def edit_meal(category, old_food, new_food, date=None):
    if date is None:
        date = str(datetime.date.today())

    meals = load_meals()
    if date in meals and category in meals[date]:
        try:
            idx = meals[date][category].index(old_food)
            meals[date][category][idx] = new_food
            save_meals(meals)
            return True
        except ValueError:
            return False
    return False
