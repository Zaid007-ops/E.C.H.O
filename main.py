import sounddevice as sd
import faster_whisper as fw
import pyttsx3
import numpy as np
import random as rd
from datetime import datetime

engine = pyttsx3.init()                                                             # Object creating for AI voice
input_Device = sd.query_devices()                                                   # Object creating for Voice input
model = fw.WhisperModel("base.en", device = "cpu", compute_type = "int8")           # Whisper Model

# Input device function

def sound_Input():
    print(input_Device)
    print(sd.default.device)

# Voice recording function

def record(duration, channels = 1, dtype = 'float32', samplerate = 16000):
    print(f"Recording for {duration} seconds")
    voice_input = sd.rec(int(samplerate * duration), samplerate = samplerate, channels = channels, dtype = dtype)
    sd.wait()
    return voice_input


# Speak function for echo

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


# Transcribe what the user audio was and flatten the audio    

def listen():
    voice_input = record(duration = 5)
    audio = voice_input.flatten()
    
    segments, info = model.transcribe(audio, language = "en", vad_filter = True)
    
    empty_list = list()
    
    # For loop that returns the recording
    
    for transcript in segments:
        empty_list.append(transcript.text)
    transcribed_string = " ".join(empty_list).strip(" ").lower()
    return transcribed_string

# Command functions

def say_date():
    today = datetime.now().strftime(" %A %d %B , %H:%M")
    speak(f"Today is {today}")
    
def flip_coin():
    result = rd.choice(["heads", "tails"])
    speak(f"Flipping a coin, the result is {result}")

def led_off():
    print("Killing the lights")
    speak("Lights off")

def led_on():
    print("Lights turning on")
    speak("Light on")

# Dictionary to store the commands

commands = { "date": say_date, "flip a coin": flip_coin, "kill the lights": led_off, "lights on": led_on}

# While loop to keep the AI running

speak("Hello Boss")

# Handles function

def handles(text):
    text = text.lower()
    for word, action in commands.items():
        if word in text:
            action()
            return True
    return False
    


while True:
    # input("Press Enter to talk: ")
    heard = listen()
    if not heard:
        print("Didnt catch that")
        continue
    print(heard)
    if "shut down" in heard:
        break
    matched = handles(heard)
    if not matched:
        print("That command doesnt exist yet")

