import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import meal_tracker
from meal_tracker import load_meals
class MealTrackerTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.safe_foods = {
            "Breakfast": ["Bacon", "Eggs", "Bagel", "Croissant"],
            "Lunch/Dinner": ["Pizza", "Chicken Tenders", "Fries", "Mac and Cheese"]
        }

        self.selected_date = tk.StringVar()
        self.selected_date.set(datetime.now().strftime("%Y-%m-%d"))

        self.meal_entry = tk.StringVar()
        self.meal_type = tk.StringVar(value="Breakfast")

        ttk.Label(self, text="🍽️ Meal Tracker", style="Dark.TLabel", font=("Segoe UI", 14)).grid(row=0, column=0, columnspan=2, pady=(10, 5))

        ttk.Label(self, text="Meal:", style="Dark.TLabel").grid(row=1, column=0, sticky="e", padx=5)
        ttk.Entry(self, textvariable=self.meal_entry, width=30).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(self, text="Type:", style="Dark.TLabel").grid(row=2, column=0, sticky="e", padx=5)
        meal_type_dropdown = ttk.Combobox(self, textvariable=self.meal_type, values=["Breakfast", "Lunch", "Dinner", "Snack"])
        meal_type_dropdown.grid(row=2, column=1, padx=5, pady=2)
        self.meal_type.set("Breakfast")

        ttk.Button(self, text="Log Meal", command=self.log_meal, style="Dark.TButton").grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Label(self, text="Date:", style="Dark.TLabel").grid(row=4, column=0, sticky="e", padx=5)
        date_entry = ttk.Entry(self, textvariable=self.selected_date, width=12)
        date_entry.grid(row=4, column=1, padx=5, pady=2, sticky="w")

        ttk.Button(self, text="View Day", command=self.update_today_meals, style="Dark.TButton").grid(row=5, column=0, columnspan=2, pady=(5, 10))

        self.today_meals_listbox = tk.Listbox(self, height=6, width=45, bg="#1e1e1e", fg="white", selectbackground="#444444", activestyle="dotbox")
        self.today_meals_listbox.grid(row=6, column=0, columnspan=2, padx=10)

        delete_button = ttk.Button(self, text="Delete Selected", command=self.delete_selected, style="Dark.TButton")
        delete_button.grid(row=7, column=0, columnspan=2, pady=(5, 10))

        # 📝 Notes Section
        notes_label = tk.Label(self, text="📝 Nutrition Notes", font=("Segoe UI", 12), bg="#121212", fg="white")
        notes_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0))

        self.notes_text = tk.Text(self, height=5, wrap="word", font=("Segoe UI", 10),
                                  bg="#1e1e1e", fg="white", insertbackground="white")
        self.notes_text.grid(row=9, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="we")

        self.update_today_meals()
        self.load_notes()

    def log_meal(self):
        meal = self.meal_entry.get().strip().lower()
        meal_type_map = {
            "Breakfast": "breakfast",
            "Lunch": "lunch",
            "Dinner": "dinner",
            "Snack": "snack"
        }
        mtype = meal_type_map.get(self.meal_type.get(), "breakfast")
        date = self.selected_date.get()

        if not meal:
            messagebox.showwarning("Missing Input", "Please enter a meal.")
            return

        data = meal_tracker.load_meals()  # returns dict

        if date not in data:
            data[date] = {
                "breakfast": [],
                "lunch": [],
                "dinner": [],
                "snack": [],
                "notes": ""
            }

        if mtype not in data[date]:
            data[date][mtype] = []

        data[date][mtype].append(meal)
        meal_tracker.save_meals(data)

        self.save_notes()  # save notes if any changes
        self.update_today_meals()
        self.meal_entry.set("")

    def update_today_meals(self):
        date = self.selected_date.get()
        data = meal_tracker.load_meals()

        self.today_meals_listbox.delete(0, tk.END)

        if date in data:
            meals = data[date]
            # Show all meal categories except notes
            for category in ["breakfast", "lunch", "dinner", "snack"]:
                items = meals.get(category, [])
                for item in items:
                    self.today_meals_listbox.insert(tk.END, f"{category.title()}: {item}")
            if self.today_meals_listbox.size() == 0:
                self.today_meals_listbox.insert(tk.END, "No meals logged for this date.")
        else:
            self.today_meals_listbox.insert(tk.END, "No meals logged for this date.")

        self.load_notes()  # refresh notes for selected date

    def delete_selected(self):
        date = self.selected_date.get()
        selected_indices = self.today_meals_listbox.curselection()
        if not selected_indices:
            return

        data = meal_tracker.load_meals()

        if date not in data:
            return

        # We need to map the selected listbox item back to category + meal string
        # The format we inserted was: "Category: meal"
        meals_data = data[date]
        items_to_remove = []
        for idx in reversed(selected_indices):  # reverse to delete safely
            item_text = self.today_meals_listbox.get(idx)
            try:
                category, meal = item_text.split(": ", 1)
                category = category.lower()
                if category in meals_data and meal in meals_data[category]:
                    meals_data[category].remove(meal)
            except Exception:
                continue

        meal_tracker.save_meals(data)
        self.update_today_meals()
        self.save_notes()

    def save_notes(self):
        date = self.selected_date.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        data = meal_tracker.load_meals()
        if date not in data:
            data[date] = {
                "breakfast": [],
                "lunch": [],
                "dinner": [],
                "snack": [],
                "notes": ""
            }

        data[date]["notes"] = notes
        meal_tracker.save_meals(data)

    def load_notes(self):
        date = self.selected_date.get()
        data = meal_tracker.load_meals()
        self.notes_text.delete("1.0", tk.END)
        if date in data and "notes" in data[date]:
            self.notes_text.insert("1.0", data[date]["notes"])
