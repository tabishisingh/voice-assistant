import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
from datetime import datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize the speech recognition
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return None
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            speak("There seems to be an issue with the speech recognition service.")
            return None

def tell_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"The current time is {current_time}")
def get_weather(city):
    api_key = "a6dc905e1d3632ff4af91642bde54a4c"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        speak(f"The current temperature in {city} is {temperature} degrees Celsius with {description}.")
    else:
        speak("City not found.")


def tell_date():
    today = datetime.today().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")

def set_reminder(reminder):
    # This is a simple reminder function
    speak(f"Reminder set for: {reminder}")

def search_web(query):
    speak("Searching the web for your query.")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Main loop for the assistant
def voice_assistant():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if not command:
            continue

        if "hello" in command:
            speak("Hello! How can I help you?")
        elif "time" in command:
            tell_time()
        elif "date" in command:
            tell_date()
        elif "weather" in command:
            speak("Which city?")
            city = listen()
            get_weather(city)
        elif "search" in command:
            speak("What would you like me to search for?")
            search_query = listen()
            if search_query:
                search_web(search_query)
        elif "remind me" in command:
            speak("What should I remind you about?") 
            reminder = listen()
            set_reminder(reminder)
        elif "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day!")
            break
        else:
            speak("I'm sorry, I didn't understand that command.")

if __name__ == "__main__":
    voice_assistant()
