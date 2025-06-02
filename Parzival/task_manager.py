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

tasks = load_tasks()
for idx, task in enumerate(tasks, start=1):
    print(f"{idx}. {task['description']} - {'✔️' if task['completed'] else '❌'}")
def handle_command(command):
    parts = command.split(maxsplit=1)
    action = parts[0]

    if action == "add" and len(parts) > 1:
        task = {"description": parts[1], "completed": False}
        tasks.append(task)
        save_tasks(tasks)
        return f"Task added: {task['description']}"

    elif action == "complete" and len(parts) > 1 and parts[1].isdigit():
        index = int(parts[1]) - 1
        if 0 <= index < len(tasks):
            tasks[index]["completed"] = True
            save_tasks(tasks)
            return f"Task {index + 1} marked as complete."
        else:
            return "Invalid task number."

    elif action == "remove" and len(parts) > 1 and parts[1].isdigit():
        index = int(parts[1]) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks(tasks)
            return f"Removed task: {removed['description']}"
        else:
            return "Invalid task number."

    elif action == "show":
        if not tasks:
            return "No tasks found."
        return "\n".join(
            [f"{i+1}. [{'✔' if t['completed'] else ' '}] {t['description']}" for i, t in enumerate(tasks)]
        )

    elif action == "quit":
        return "quit"

    else:
        return "Sorry, I didn't understand that."
