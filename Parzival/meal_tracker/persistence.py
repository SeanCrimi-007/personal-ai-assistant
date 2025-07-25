import json
import os

MEAL_FILE = "meals.json"

def load_meals():
    if os.path.exists(MEAL_FILE):
        with open(MEAL_FILE, "r") as f:
            return json.load(f)
    return {}

def save_meals(meals):
    with open(MEAL_FILE, "w") as f:
        json.dump(meals, f, indent=4)
