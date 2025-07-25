import meal_tracker

# Log something
meal_tracker.log_meal("breakfast", "crispy bacon")
meal_tracker.log_meal("lunch", "pizza")
meal_tracker.log_meal("dinner", "french fries")

# View today's meals
print("Today's Meals:")
print(meal_tracker.view_today())
