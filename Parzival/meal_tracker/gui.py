import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .meal_model import log_meal, view_today, delete_meal, edit_meal

class MealTrackerTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.selected_date = tk.StringVar()
        self.selected_date.set(datetime.now().strftime("%Y-%m-%d"))

        self.meal_entry = tk.StringVar()
        self.meal_type = tk.StringVar(value="breakfast")

        ttk.Label(self, text="🍽️ Meal Tracker", style="Dark.TLabel", font=("Segoe UI", 14)).grid(row=0, column=0, columnspan=2, pady=(10, 5))

        ttk.Label(self, text="Meal:", style="Dark.TLabel").grid(row=1, column=0, sticky="e", padx=5)
        ttk.Entry(self, textvariable=self.meal_entry, width=30).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(self, text="Type:", style="Dark.TLabel").grid(row=2, column=0, sticky="e", padx=5)
        meal_type_dropdown = ttk.Combobox(self, textvariable=self.meal_type, values=["breakfast", "lunch", "dinner", "snack"])
        meal_type_dropdown.grid(row=2, column=1, padx=5, pady=2)

        ttk.Button(self, text="Log Meal", command=self.log_meal, style="Dark.TButton").grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Label(self, text="Date:", style="Dark.TLabel").grid(row=4, column=0, sticky="e", padx=5)
        date_entry = ttk.Entry(self, textvariable=self.selected_date, width=12)
        date_entry.grid(row=4, column=1, padx=5, pady=2, sticky="w")

        ttk.Button(self, text="View Day", command=self.update_today_meals, style="Dark.TButton").grid(row=5, column=0, columnspan=2, pady=(5, 10))

        self.today_meals_listbox = tk.Listbox(self, height=6, width=45, bg="#1e1e1e", fg="white", selectbackground="#444444", activestyle="dotbox")
        self.today_meals_listbox.grid(row=6, column=0, columnspan=2, padx=10)

        delete_button = ttk.Button(self, text="Delete Selected", command=self.delete_selected, style="Dark.TButton")
        delete_button.grid(row=7, column=0, columnspan=2, pady=(5, 10))

        # Notes section
        notes_label = tk.Label(self, text="📝 Nutrition Notes", font=("Segoe UI", 12), bg="#121212", fg="white")
        notes_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0))

        self.notes_text = tk.Text(self, height=5, wrap="word", font=("Segoe UI", 10),
                                  bg="#1e1e1e", fg="white", insertbackground="white")
        self.notes_text.grid(row=9, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="we")

        self.update_today_meals()
        self.load_notes()

    def log_meal(self):
        meal = self.meal_entry.get().strip().lower()
        mtype = self.meal_type.get().lower()
        date = self.selected_date.get()

        if not meal:
            messagebox.showwarning("Missing Input", "Please enter a meal.")
            return

        log_meal(mtype, meal)
        self.save_notes()
        self.update_today_meals()
        self.meal_entry.set("")

    def update_today_meals(self):
        date = self.selected_date.get()
        meals = view_today() if date == datetime.now().strftime("%Y-%m-%d") else None

        self.today_meals_listbox.delete(0, tk.END)

        data = meals if meals else load_meals()
        if date in data:
            day_meals = data[date]
            for category in ["breakfast", "lunch", "dinner", "snack"]:
                items = day_meals.get(category, [])
                for item in items:
                    self.today_meals_listbox.insert(tk.END, f"{category.title()}: {item}")
            if self.today_meals_listbox.size() == 0:
                self.today_meals_listbox.insert(tk.END, "No meals logged for this date.")
        else:
            self.today_meals_listbox.insert(tk.END, "No meals logged for this date.")

        self.load_notes()

    def delete_selected(self):
        date = self.selected_date.get()
        selected_indices = self.today_meals_listbox.curselection()
        if not selected_indices:
            return

        meals = load_meals()
        if date not in meals:
            return

        for idx in reversed(selected_indices):
            item = self.today_meals_listbox.get(idx)
            try:
                category, meal = item.split(": ", 1)
                category = category.lower()
                if category in meals[date] and meal in meals[date][category]:
                    meals[date][category].remove(meal)
            except Exception:
                continue

        save_meals(meals)
        self.update_today_meals()
        self.save_notes()

    def save_notes(self):
        date = self.selected_date.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        meals = load_meals()
        if date not in meals:
            meals[date] = {
                "breakfast": [],
                "lunch": [],
                "dinner": [],
                "snack": [],
                "notes": ""
            }

        meals[date]["notes"] = notes
        save_meals(meals)

    def load_notes(self):
        date = self.selected_date.get()
        meals = load_meals()
        self.notes_text.delete("1.0", tk.END)
        if date in meals and "notes" in meals[date]:
            self.notes_text.insert("1.0", meals[date]["notes"])
