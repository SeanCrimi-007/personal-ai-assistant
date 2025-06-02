import pyjokes
import pyttsx3

def tell_a_joke():
    joke = pyjokes.get_joke()
    print("Here's a joke for you:")
    print(joke)

    engine = pyttsx3.init()
    engine.say(joke)
    engine.runAndWait()

tell_a_joke()
