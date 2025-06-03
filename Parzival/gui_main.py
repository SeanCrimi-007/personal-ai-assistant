import tkinter as tk
from tkinter import messagebox
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def refresh_listbox():
    task_listbox.delete(0, tk.END)
    for i, task in enumerate(tasks):
        status = "✅" if task["completed"] else "❌"
        task_listbox.insert(tk.END, f"{i+1}. {task['description']} - {status}")

def add_task():
    task_text = task_entry.get()
    if task_text:
        tasks.append({"description": task_text, "completed": False})
        save_tasks(tasks)
        refresh_listbox()
        task_entry.delete(0, tk.END)

def complete_task():
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        tasks[index]["completed"] = True
        save_tasks(tasks)
        refresh_listbox()

def delete_task():
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        tasks.pop(index)
        save_tasks(tasks)
        refresh_listbox()

# Initialize tasks
tasks = load_tasks()

# GUI setup
root = tk.Tk()
root.title("Task Assistant")

task_entry = tk.Entry(root, width=40)
task_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

add_btn = tk.Button(root, text="Add Task", command=add_task)
add_btn.grid(row=0, column=2, padx=10)

task_listbox = tk.Listbox(root, width=50, height=10)
task_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

complete_btn = tk.Button(root, text="Mark Completed", command=complete_task)
complete_btn.grid(row=2, column=0, pady=5)

delete_btn = tk.Button(root, text="Delete Task", command=delete_task)
delete_btn.grid(row=2, column=2, pady=5)

refresh_listbox()

root.mainloop()
