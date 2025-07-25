from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def interpret_command(user_input):
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY is missing in your .env file.")
        return "error"

    system_prompt = """
    You are a personal task manager assistant. Interpret the user's input and respond in one of these formats:
    - add <task>
    - complete <task number>
    - remove <task number>
    - remove all
    - show
    - quit

    Examples:
    - "I need to buy groceries" → add buy groceries
    - "Mark task 2 as done" → complete 2
    - "Remove the third task" → remove 3
    - "Clear all tasks" → remove all
    - "Delete everything" → remove all
    - "Get rid of all my tasks" → remove all
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        print("⏱️ Groq API request timed out.")
        return "error"
    except requests.exceptions.RequestException as e:
        print(f"❌ Groq API error: {e}")
        return "error"
    except (KeyError, IndexError):
        print("⚠️ Unexpected Groq API response format.")
        return "error"
