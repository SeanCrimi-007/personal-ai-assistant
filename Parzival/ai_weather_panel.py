import tkinter as tk
from tkinter import scrolledtext
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import threading
from gpt_parser import interpret_command
from voice_utils import speak, listen, handle_command, run_voice_command
from tkinter import messagebox

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_weather(city):
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            return response.text
        else:
            return "Sorry, I couldn't fetch the weather."
    except Exception as e:
        return f"Error: {e}"

def ask_groq(prompt):
    if not GROQ_API_KEY:
        return "❌ GROQ_API_KEY is not set. Please check your .env file."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful and concise AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error contacting Groq: {e}"

class AIWeatherPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#1e1e1e")
        self.pack(fill="both", expand=True)

        self.output_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg="#121212", fg="#FFFFFF", font=("Arial", 11))
        self.output_area.pack(padx=10, pady=10, fill="both", expand=True)
        self.output_area.config(state=tk.DISABLED)

        self._append_to_output("🧠 Parzival: Hello! Ask me anything — like \"weather in New York\" or \"What's the time?\"")

        self.input_entry = tk.Entry(self, font=("Arial", 12), bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff")
        self.input_entry.pack(padx=10, pady=(0, 10), fill="x")
        self.input_entry.bind("<Return>", self.process_input)

        send_button = tk.Button(self, text="Ask", command=self.process_input_gui, bg="#333", fg="#fff")
        send_button.pack(pady=(0, 10))

        self.voice_button = tk.Button(self, text="🎙 Voice Command", command=self.voice_input_button)
        self.voice_button.pack(pady=10)

    def voice_input_button(self):
        run_voice_command(self)

    def process_input_gui(self):
        self.process_input(None)

    def process_input(self, event):
        user_input = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not user_input:
            return

        self._append_to_output(f"🧑‍💻 You: {user_input}")

        if user_input.lower().startswith("weather in "):
            city = user_input.split("weather in ", 1)[1]
            response = get_weather(city)
        elif user_input.lower() in ["what's the time", "whats the time", "what time is it", "tell me the time"]:
            now = datetime.now().strftime("%I:%M %p")
            response = f"The current time is {now}."
        else:
            response = ask_groq(user_input)

        if "error" in response.lower():
            self._append_to_output("⚠️ An error occurred. Please try again.")
        else:
            self._append_to_output(f"🤖 Parzival: {response}")
            speak(response)

    def _append_to_output(self, text):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, text + "\n\n")
        self.output_area.config(state=tk.DISABLED)
        self.output_area.see(tk.END)
