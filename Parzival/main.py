import tkinter as tk
from tkinter import ttk
import pyttsx3
import speech_recognition as sr
import atexit
from task_manager import TaskManagerGUI
from gpt_parser import interpret_command
from ai_weather_panel import AIWeatherPanel
from icloud_sync import add_reminder
from meal_tracker_tab import MealTrackerTab

# Add a reminder 1 day from now
add_reminder("Review AI Assistant notes")

# ========== TTS Setup ==========
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 180)

# Optional: Choose a preferred voice
for voice in tts_engine.getProperty('voices'):
    if "David" in voice.name or "UK English" in voice.name:
        tts_engine.setProperty('voice', voice.id)
        break

# ========== Speech Recognition Setup ==========
recognizer = sr.Recognizer()

def speak(text):
    try:
        print(f"Assistant: {text}")
        tts_engine.say(text)
        tts_engine.runAndWait()
    except RuntimeError as e:
        if str(e) != 'run loop already started':
            raise

def listen():
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        speak("Listening.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            return recognizer.recognize_google(audio).lower()
        except sr.WaitTimeoutError:
            print("⏳ Listening timed out.")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            speak("There was a problem with the speech recognition service.")
        return None

# ========== Command Handling ==========
def handle_command(command):
    if "add task" in command:
        desc = command.replace("add task", "").strip()
        if desc:
            speak(f"Task added: {desc}")
            # Actual task addition is handled in the TaskManagerGUI via voice button
            return f"Task added: {desc}"
        return "Please provide a task description."

    elif "remove all tasks" in command:
        # Voice command for mass removal is not safe — skip for now
        return "Please use the task tab to remove tasks safely."

    return "Sorry, I didn't understand that command."

# ========== Cleanup ==========
@atexit.register
def cleanup():
    try:
        tts_engine.stop()
    except Exception:
        pass

# ========== GUI Setup ==========
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Parzival AI Assistant")
    root.geometry("700x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # 🍽 Meal Tracker Tab
    meal_tab = MealTrackerTab(notebook)
    notebook.add(meal_tab, text="Meal Tracker")

    # 🗂 Tasks Tab
    task_frame = tk.Frame(notebook, bg="#1e1e1e")
    TaskManagerGUI(task_frame)
    notebook.add(task_frame, text="🗂 Tasks")

    # 🌦 AI + Weather Tab
    weather_frame = AIWeatherPanel(notebook)
    notebook.add(weather_frame, text="🌦 AI + Weather")

    root.mainloop()
