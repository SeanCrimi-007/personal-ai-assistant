import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json, os
from datetime import datetime
import speech_recognition as sr
import pyttsx3

BG_COLOR = "#121212"
FG_COLOR = "#FFFFFF"
BUTTON_COLOR = "#1E1E1E"
HIGHLIGHT_COLOR = "#333333"

TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")
PRIORITY_ORDER = {"High": 1, "Normal": 2, "Low": 3}

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 180)

def speak(text):
    print("Assistant:", text)
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        speak("Listening for command...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        try:
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
        return ""

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def sort_tasks_by_priority(tasks):
    return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.get("priority", "Normal"), 2))

def sort_tasks_by_deadline(tasks):
    def parse_deadline(task):
        try:
            return datetime.strptime(task.get("deadline", "9999-12-31"), "%Y-%m-%d")
        except ValueError:
            return datetime.strptime("9999-12-31", "%Y-%m-%d")
    return sorted(tasks, key=parse_deadline)

class TaskManagerGUI:
    def __init__(self, parent_frame):
        self.frame = parent_frame
        self.frame.configure(bg=BG_COLOR)
        self.tasks = load_tasks()
        self.filtered_tasks = self.tasks
        self.build_gui()

    def build_gui(self):
        self.task_listbox = tk.Listbox(self.frame, width=50, height=10, font=("Arial", 12),
                                       bg=BG_COLOR, fg=FG_COLOR, selectbackground=HIGHLIGHT_COLOR,
                                       selectforeground=FG_COLOR)
        self.task_listbox.pack(pady=10)

        button_frame = tk.Frame(self.frame, bg=BG_COLOR)
        button_frame.pack()

        actions = [
            ("Add Task", self.add_task),
            ("Complete Task", self.complete_task),
            ("Remove Task", self.remove_task),
            ("Edit Task", self.edit_task),
            ("Quit", self.frame.quit if hasattr(self.frame, 'quit') else None)
        ]
        for i, (text, cmd) in enumerate(actions):
            if cmd:
                tk.Button(button_frame, text=text, command=cmd, bg=BUTTON_COLOR, fg=FG_COLOR,
                          activebackground=HIGHLIGHT_COLOR, activeforeground=FG_COLOR).grid(row=0, column=i, padx=5)

        tk.Button(button_frame, text="Sort by Priority", command=self.sort_by_priority,
                  bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR,
                  activeforeground=FG_COLOR).grid(row=1, column=0, padx=5)

        tk.Button(button_frame, text="Sort by Deadline", command=self.sort_by_deadline,
                  bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR,
                  activeforeground=FG_COLOR).grid(row=1, column=1, padx=5)

        filter_options = ["All", "Completed", "Incomplete"]
        self.filter_var = tk.StringVar(value="All")
        filter_menu = tk.OptionMenu(button_frame, self.filter_var, *filter_options, command=self.apply_filter)
        filter_menu.configure(bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR,
                              activeforeground=FG_COLOR, highlightthickness=0)
        filter_menu["menu"].config(bg=BUTTON_COLOR, fg=FG_COLOR)
        filter_menu.grid(row=1, column=2, padx=5)

        tk.Button(button_frame, text="Toggle Complete", command=self.toggle_task_completion,
                  bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR,
                  activeforeground=FG_COLOR).grid(row=1, column=3, padx=5)

        tk.Button(button_frame, text="🗣️ Voice Command", command=self.handle_voice_command,
                  bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR,
                  activeforeground=FG_COLOR).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="📢 Read All Tasks", command=self.read_all_tasks,
                  bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR,
                  activeforeground=FG_COLOR).grid(row=2, column=2, columnspan=2, pady=10)

        self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.filtered_tasks):
            status = "✅" if task.get("completed", False) else "❌"
            priority = task.get("priority", "Normal")
            deadline = task.get("deadline", "No deadline")
            self.task_listbox.insert(tk.END,
                f"{i + 1}. {task['description']} [Priority: {priority}] [Due: {deadline}] - {status}")

    def apply_filter(self, selected_filter):
        if selected_filter == "Completed":
            self.filtered_tasks = [t for t in self.tasks if t.get("completed")]
        elif selected_filter == "Incomplete":
            self.filtered_tasks = [t for t in self.tasks if not t.get("completed")]
        else:
            self.filtered_tasks = self.tasks
        self.update_task_listbox()

    def add_task(self):
        desc = simpledialog.askstring("Task", "Enter description:")
        if not desc: return
        priority = simpledialog.askstring("Priority", "Enter priority (Low, Normal, High):", initialvalue="Normal")
        deadline = simpledialog.askstring("Deadline", "Enter deadline (YYYY-MM-DD) or leave blank:")
        if deadline:
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid", "Deadline must be YYYY-MM-DD.")
                return
        else:
            deadline = "No deadline"
        self.tasks.append({"description": desc, "completed": False, "priority": priority or "Normal", "deadline": deadline})
        save_tasks(self.tasks)
        self.apply_filter(self.filter_var.get())

    def complete_task(self):
        self._mark_selected_task(True)

    def toggle_task_completion(self):
        self._toggle_selected_task()

    def remove_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            task = self.filtered_tasks[selection[0]]
            self.tasks.remove(task)
            save_tasks(self.tasks)
            self.apply_filter(self.filter_var.get())

    def edit_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            idx = self.tasks.index(self.filtered_tasks[selection[0]])
            new_desc = simpledialog.askstring("Edit Task", "New description:", initialvalue=self.tasks[idx]["description"])
            if new_desc:
                self.tasks[idx]["description"] = new_desc
                save_tasks(self.tasks)
                self.apply_filter(self.filter_var.get())

    def sort_by_priority(self):
        self.tasks = sort_tasks_by_priority(self.tasks)
        self.apply_filter(self.filter_var.get())

    def sort_by_deadline(self):
        self.tasks = sort_tasks_by_deadline(self.tasks)
        self.apply_filter(self.filter_var.get())

    def handle_voice_command(self):
        command = listen_command()
        if "add task" in command:
            desc = command.replace("add task", "").strip()
            if desc:
                self.tasks.append({"description": desc, "completed": False, "priority": "Normal", "deadline": "No deadline"})
                save_tasks(self.tasks)
                self.apply_filter(self.filter_var.get())
                speak(f"Task '{desc}' added.")
        elif "read" in command:
            self.read_all_tasks()
        elif "complete task" in command or "remove task" in command:
            speak("Please use the GUI to select the task for these commands.")
        elif "sort" in command:
            if "priority" in command: self.sort_by_priority()
            elif "deadline" in command: self.sort_by_deadline()
        else:
            speak("Command not recognized.")

    def read_all_tasks(self):
        if not self.tasks:
            speak("You have no tasks.")
            return
        for task in self.tasks:
            status = "completed" if task.get("completed") else "incomplete"
            speak(f"{task['description']}, priority {task['priority']}, due {task['deadline']}. This task is {status}.")

    def _mark_selected_task(self, complete=True):
        selection = self.task_listbox.curselection()
        if selection:
            idx = self.tasks.index(self.filtered_tasks[selection[0]])
            self.tasks[idx]["completed"] = complete
            save_tasks(self.tasks)
            self.apply_filter(self.filter_var.get())

    def _toggle_selected_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            idx = self.tasks.index(self.filtered_tasks[selection[0]])
            self.tasks[idx]["completed"] = not self.tasks[idx]["completed"]
            save_tasks(self.tasks)
            self.apply_filter(self.filter_var.get())
