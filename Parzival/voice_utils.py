import pyttsx3
import speech_recognition as sr
import threading
from gpt_parser import interpret_command

# === TTS Setup ===
engine = pyttsx3.init()
engine.setProperty('rate', 180)
for voice in engine.getProperty('voices'):
    if "David" in voice.name or "UK English" in voice.name:
        engine.setProperty('voice', voice.id)
        break

recognizer = sr.Recognizer()

def speak(text):
    try:
        print(f"Assistant: {text}")
        engine.say(text)
        engine.runAndWait()
    except RuntimeError as e:
        if "run loop already started" in str(e):
            pass

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
        except sr.RequestError:
            speak("There was a problem with the speech recognition service.")
        return None

def handle_command(command):
    if "add task" in command:
        desc = command.replace("add task", "").strip()
        if desc:
            return f"Task added: {desc}"
        return "Please provide a task description."

    elif "remove all tasks" in command:
        return "Please use the task tab to remove tasks safely."

    return "Sorry, I didn't understand that command."

def run_voice_command(panel_ref):
    def thread_logic():
        user_input = listen()
        if user_input:
            panel_ref.input_entry.delete(0, "end")
            panel_ref.input_entry.insert(0, user_input)
            command = interpret_command(user_input)
            response = handle_command(command)
            if response:
                panel_ref._append_to_output(f"Assistant: {response}")
                speak(response)

    threading.Thread(target=thread_logic, daemon=True).start()
