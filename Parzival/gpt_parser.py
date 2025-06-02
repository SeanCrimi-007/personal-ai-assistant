from dotenv import load_dotenv
import os
import requests

load_dotenv()  # 👈 This loads variables from .env into os.environ

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def interpret_command(user_input):
    # same as before...
    # Construct the prompt to steer the model to format your commands
    system_prompt = """
You are a personal task manager assistant. Interpret the user's input and respond in one of these formats:
- add <task>
- complete <task number>
- remove <task number>
- show
- quit

Examples:
- "I need to buy groceries" → add buy groceries
- "Mark task 2 as done" → complete 2
- "Remove the third task" → remove 3
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        print(f"❌ API error: {response.status_code} - {response.text}")
        return "error"
