import sounddevice as sd
import faster_whisper as fw
import pyttsx3
import numpy as np

engine = pyttsx3.init()                                                             # Object creating for AI voice
input_Device = sd.query_devices()                                                   # Object creating for Voice input
model = fw.WhisperModel("base.en", device = "cpu", compute_type = "int8")           # Whisper Model

# Input device function

def sound_Input():
    print(input_Device)
    print(sd.default.device)
# sound_Input()

# Voice recording function

def record(duration, channels = 1, dtype = 'float32', samplerate = 16000):
    print(f"Recording for {duration} seconds")
    voice_input = sd.rec(int(samplerate * duration), samplerate = samplerate, channels = channels, dtype = dtype)
    sd.wait()
    return voice_input
#recording = record(duration = 5)
#print(type(recording), recording.shape, recording.dtype, len(recording))
#print(np.abs(recording).max())

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

speak("Hello")

# While loop to keep the AI running

while True:
    input("Press Enter to talk: ")
    heard = listen()
    if not heard:
        print("Didnt catch that")
        continue
    print(heard)
    if "shut down" in heard:
        break

            