from gpt_parser import interpret_command
import pyttsx3
import speech_recognition as sr
from task_manager import handle_command
import time

# Initialize text-to-speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Optional: Select a deeper or British male voice if available
for voice in voices:
    if "David" in voice.name or "UK English" in voice.name:
        engine.setProperty('voice', voice.id)
        break


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        speak("Listening.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            user_input = recognizer.recognize_google(audio)
            return user_input.lower()
        except sr.WaitTimeoutError:
            print("⏳ Listening timed out...")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            speak("Sorry, I didn't catch that.")
            return None
        except sr.RequestError as e:
            print(f"🔌 Could not request results; {e}")
            speak("There was a problem with the speech recognition service.")
            return None


if __name__ == "__main__":
    speak("Hello, I am your task assistant. What would you like me to do?")

    try:
        while True:
            user_input = listen()
            if not user_input:
                continue

            print(f"You said: {user_input}")
            command = interpret_command(user_input)
            if command.strip().lower().startswith("quit"):
                speak("Goodbye!")
                break
            response = handle_command(command)
            if response and response.lower() != "error":
                speak(response)
                print(f"Assistant: {response}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        speak("Shutting down. Goodbye.")
        time.sleep(1)
