import speech_recognition as sr
import pyttsx3
import psutil
import os
import socket
import platform
import subprocess
from win10toast import ToastNotifier

# Setup
recognizer = sr.Recognizer()
engine = pyttsx3.init()
toaster = ToastNotifier()

# Flag to control the listening loop
listening = True

def speak(text):
    print(f"[Bot 🧠]: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"[You 🗣️]: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None

# ---- ISSUE DETECTION ----

def check_disk_usage():
    usage = psutil.disk_usage('/')
    percent = usage.percent
    speak(f"Your disk is {percent}% full.")
    if percent > 85:
        speak("You should consider cleaning up files.")
    return percent

def check_ram():
    ram = psutil.virtual_memory()
    speak(f"RAM usage is at {ram.percent} percent.")
    if ram.percent > 90:
        speak("High RAM usage detected. Try closing unused applications.")
    return ram.percent

def check_cpu():
    cpu = psutil.cpu_percent(interval=1)
    speak(f"CPU usage is {cpu} percent.")
    if cpu > 85:
        speak("CPU usage is high. Consider restarting the system or checking for background apps.")
    return cpu

def check_network():
    try:
        socket.create_connection(("1.1.1.1", 53))
        speak("Internet connection is working.")
        return True
    except OSError:
        speak("No internet connection detected.")
        return False

def clear_temp():
    temp_dir = os.getenv('TEMP')
    count = 0
    try:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    count += 1
                except:
                    continue
        speak(f"Cleared {count} temporary files.")
        toaster.show_toast("ZeroLag AI", f"Cleaned {count} temp files.")
    except Exception as e:
        speak(f"Error clearing temp files: {e}")

def handle_command(command):
    if command is None:
        return

    if "hello" in command or "hi" in command:
        speak("Hi, I'm ZeroLag. How can I help you today?")

    elif "check system" in command or "diagnose" in command:
        speak("Okay, analyzing your system...")
        check_disk_usage()
        check_ram()
        check_cpu()
        check_network()

    elif "clean my pc" in command or "clear temp" in command:
        speak("Initiating cleanup...")
        clear_temp()

    elif "internet" in command or "network" in command:
        check_network()

    elif "cpu" in command:
        check_cpu()

    elif "ram" in command or "memory" in command:
        check_ram()

    elif "disk" in command or "storage" in command:
        check_disk_usage()

    elif "shutdown" in command:
        speak("Shutting down your PC.")
        os.system("shutdown /s /t 1")

    elif "restart" in command:
        speak("Restarting your PC.")
        os.system("shutdown /r /t 1")

    elif "stop" in command or "exit" in command:
        speak("Okay, I will stop listening now. Have a great day!")
        return "stop"

    else:
        speak("Sorry, I don't recognize this issue yet. Try asking differently.")

# ---- MAIN LOOP ----

def start_bot():
    global listening
    speak("Welcome! I am your system assistant. Say 'check system' to begin diagnosis.")
    while listening:
        cmd = listen_command()
        if cmd:
            result = handle_command(cmd)
            if result == "stop":
                listening = False
                break

if __name__ == "__main__":
    start_bot()
