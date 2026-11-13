# ECHO's brain.py 
# Replys start of slow as it has to load into the memory but after that it is fast and responsive.

from email.mime import text
import time
import ollama
import re

model = "llama3.2:3b"   # Current version of olllama that I am using 

MAX_TURNS = 8

SYSTEM_PROMPT = ("You are ECHO, a helpful assistant that can perform tasks and answer questions." 
    "You are a virtual assistant that can help with various tasks and assisting with daily activities. "
    "You are designed to be user-friendly and efficient."
)

_history = []           # Running conversation

def clean(text):
    
    # This function cleans the text by removing any extra spaces and new lines
    
    return re.sub(r"[*#`>]", "", text).strip()

def think(user_text):
    
    _history.append({"role": "user", "content": user_text})
    del _history[:-MAX_TURNS * 2]                                                   # Keep only the last MAX_TURNS messages in history  
   
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + _history
    
    start = time.perf_counter()
    try:
        response = ollama.chat(model = model, messages = messages)
    except Exception as e:
        _history.pop()                                                          # Remove the last user message if there's an error
        print(f"Error: {e}")
        return "Sorry, I encountered an error while processing your request."
    
    reply = clean(response["message"]["content"])
    
    print(f"[brain] replied in {time.perf_counter() - start:.1f}s")
    _history.append({"role": "assistant", "content": reply})
    return reply


if __name__ == "__main__":
    print("Type what you want to say to ECHO, or click enter on a blank line to quit.")
    while True:
        text = input("> . ".strip())
        if not text:
            break
        print(think(text))
    

    