import openai
import requests

# Set your OpenAI API key here (keep it secret!)
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_weather(city):
    # Free weather API example (Open-Meteo, no API key needed)
    url = f'https://wttr.in/{city}?format=3'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "Sorry, I couldn't fetch the weather right now."
    except Exception as e:
        return "Error fetching weather: " + str(e)

def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=100
    )
    return response.choices[0].message['content'].strip()

def main():
    print("Ask me anything or type 'weather in <city>' to get the weather.")
    while True:
        user_input = input("You: ").strip().lower()
        if user_input in ['exit', 'quit', 'bye']:
            print("Assistant: Goodbye!")
            break
        elif user_input.startswith("weather in "):
            city = user_input.replace("weather in ", "")
            weather = get_weather(city)
            print("Assistant:", weather)
        else:
            answer = ask_openai(user_input)
            print("Assistant:", answer)

if __name__ == "__main__":
    main()