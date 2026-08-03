from openwakeword.model import Model
import pyaudio, numpy as np
import speech_recognition as sr
import pyttsx3
import requests
import webbrowser as wb
#import os
import subprocess
import ollama
from pydantic import BaseModel
import pywhatkit as pk
import datetime as dt
import os
import time


class Intent(BaseModel):
    Intent: str
    Target: str | None = None
    Location: str | None = None
    Query: str | None = None
    Confidence: float


listener = sr.Recognizer()


def listen():
    try:
        source = sr.Microphone()
        with source:
            print("🎤 Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)
            audio = listener.listen(source, timeout=10)
            command = listener.recognize_whisper(audio, model="base", language="english")
            command = command.lower().strip()
            if not command:
                return None
            else:
                print(f"🧠 Heard: {command}")
                return command
    except sr.WaitTimeoutError:
        return None
    except Exception as e:
        print(f"❌ Listening Error: {e}")
        return None

def speak(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 150)
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[Speech Error] {e}")

def wake():
    oww = Model(wakeword_models=["hey_celebi.onnx"], inference_framework="onnx")

    pa = pyaudio.PyAudio()
    stream = pa.open(rate=16000, channels=1, format=pyaudio.paInt16,
                    input=True, frames_per_buffer=1280)

    print("Listening for 'hey celebi'...")
    while True:
        audio = np.frombuffer(stream.read(1280), dtype=np.int16)
        score = oww.predict(audio)["hey_celebi"]
        if score > 0.3:
            return "hey celebi"

def ollama_():
    models = requests.get(
    "http://localhost:11434/api/tags"
    ).json()["models"]
    model_names=[model["name"] for model in models]
    user_model = model_names[0]
    # no_of_models=len(model_names)
    # n=1
    # for i in model_names:
    #         print(f"{n}) {i}")
    #         n+=1
    #
    # index=int(input("Select the index number of the model you want to use: "))
    # if index>0 and index<=no_of_models:
    #     user_model=model_names[index-1]
    #     print(f"You selected {user_model}")
    #     return user_model
    # else:
    #     print("Invalid index number")
    #     exit()
    return user_model

def get_intent(command):
    try:
        response = ollama.chat(
        model="gemma3:4b",
        messages=[
            { "role": "user",
                "content":"""
                You are Celebi's intent classifier.
    
                Your job is to understand the user's request.
                
                Always return ONLY valid JSON.
                
                The JSON must contain:
                
                {
                    "intent":"",
                    "target":"",
                    "query":"",
                    "location":"",
                    "confidence":0
                }
                
                Rules:
                
                1. If the user wants to open an application:
                intent = "open_application"
                
                Examples:
                Open Firefox
                Open VS Code
                
                2. If the user wants to search something:
                
                intent = "search_web"
                
                target = website if mentioned
                
                query = search text
                
                Examples:
                
                Search bitcoin on YouTube
                
                ↓
                
                {
                "intent":"search_web",
                "target":"YouTube",
                "query":"bitcoin",
                "confidence":0.99
                }
                
                Search Kali Linux
                
                ↓
                
                {
                "intent":"search_web",
                "target":"Google",
                "query":"Kali Linux",
                "confidence":0.99
                }
                
                3. If user wants music
                
                intent="play_music"
                
                target="Spotify"
                
                query="Arijit Singh"
                
                4. Never leave target or query empty if they exist.
            """
            },
            {
                "role": "user",
                "content": command
            }
        ],
        format=Intent.model_json_schema(),
        options={
            "temperature": 0
        }
        )
        print(type(response.message.content))
        intent = Intent.model_validate_json(response.message.content)

        return intent
    except Exception as e:
        print("ERROR:", e)

def open_application(app):
    web_apps = {
        "youtube": "https://www.youtube.com",
        "gpt": "https://www.chatgpt.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "google": "https://www.google.com",
        "instagram": "https://www.instagram.com",
        "gmail": "https://www.gmail.com",
        "outlook": "https://www.outlook.com",
        "github": "https://www.github.com",
        "spotify":"https://www.spotify.com",

    }

    if app in web_apps:
        wb.open(web_apps[app])
        speak(f"Opening {app}")
    else:
        result = subprocess.run(["which", app], capture_output=True, text=True)
        if result.returncode == 0:
            subprocess.Popen([app])
            speak(f"Opening {app}")
        else:
            speak("Sorry boss, I couldn't find that app.")

def send_whatapp_message():
    country_code=input("country code of receiver : ").strip()
    mobile_number=input("mobile number of receiver : ").strip()
    message=input("message : ")
    hour=int(input("hour : "))
    minute=int(input("minute : "))
    number=country_code+mobile_number
    pk.sendwhatmsg(number,message,hour,minute,25)

import urllib.parse
import webbrowser

def search_web(target, query):
    search_urls = {

        "youtube":
            "https://www.youtube.com/results?search_query={}",

        "google":
            "https://www.google.com/search?q={}",

        "github":
            "https://github.com/search?q={}",

        "reddit":
            "https://www.reddit.com/search/?q={}",

        "spotify":
            "https://open.spotify.com/search/{}"

    }

    target = target.lower()

    if target not in search_urls:
        target = "google"

    query = urllib.parse.quote(query)

    url = search_urls[target].format(query)

    webbrowser.open(url)

def search_image(query):
    query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?tbm=isch&q={query}"
    webbrowser.open(url)

def processing_cmd(intent,target,query,location):
    try:
        if "open_application" == intent:
            open_application(target)
            speak(f"opening {target}.")
        elif "search_web" == intent :
            search_web(target,query)
            speak(f"Searching for {query} in {target}.")
        elif "search_image" == intent:
            search_image(query)
            speak(f"showing images of {query}.")
        elif "get_time" == intent:
            current_time = dt.datetime.now().strftime("%I:%M %p")
            print(f"🕒 {current_time}")
            speak(f"The time is {current_time}")
        elif "play_music" == intent:
            speak(f"Playing {query} on YouTube.")
            pk.playonyt(query)
        elif "shutdown" == intent:
            speak("shutting down , Goodbye boss.")
            pk.shutdown(1)
        elif "restart" == intent:
            speak("Restarting boss.")
            os.system("shutdown -r -f -t 0")
        elif "send_whatsapp_message" == intent:
            send_whatapp_message()
        elif "exit" == intent:
            speak("Goodbye boss.")
        else:
            speak("Sorry boss, I didn’t catch that.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("👋 Stopped by user.")
        speak("Voice assistant stopped.")
def run(result):
    processing_cmd(
        result.intent,
        result.target,
        result.query,
        result.location
    )