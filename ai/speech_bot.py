# ai/speech_bot.py
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

# Function to speak back to the user
def speak(text):
    print(f"🤖 Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to listen to microphone input
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Say something like 'clean my system'")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print("🗣️ You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your connection.")
        return ""

# Sample command handler (to be called from main.py)
def handle_voice_commands():
    while True:
        command = listen()

        if "clean my system" in command:
            speak("Starting cleanup now.")
            try:
                from fixer import background_cleaner
                background_cleaner()
                speak("Cleanup completed successfully.")
            except Exception as e:
                print(f"❌ Error during cleanup: {e}")
                speak("There was an error during cleanup.")

        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

        elif command:
            speak("I heard you say " + command + ". But I don't know what to do with that.")
