import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import random
import json
import os
import time
from googletrans import Translator
from googlesearch import search  # Import Google Search Functionality
import openai  
from bs4 import BeautifulSoup  # Needed for web scraping
import openpyxl
import openwakeword

# Set your OpenAI API key here
OPENAI_API_KEY = "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"

# Initialize wake word model
wake_word_model = openwakeword.Model()

recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()

def text_input():
    command = input("Enter text command (or leave empty to use microphone): ")
    return command.strip()

def speak(text, lang="en"):
    """ Converts text to speech based on detected language """
    print(f"SophieAI: {text}")  # Show response in console
    engine = pyttsx3.init("sapi5")  # Use "sapi5" for Windows, "nsss" for Mac
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Ensure voice is set
    engine.say(text)
    engine.runAndWait()


def listen():
    """ Listens to user speech and detects language """
    with sr.Microphone() as source:
        print("listening...")
        speak("i am Listening sir")
        recognizer.adjust_for_ambient_noise(source, duration=1) # Adjusted for duration
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="hi-en")  # Detects both English & Hindi
        print(f"You: {command}")
        return command
    except sr.UnknownValueError:
        return "I didn't understand that sir"
    except sr.RequestError:
        return "Speech service is down"
    
# 🔹 **Wake Word Detection Loop**
print("Listening for wake word ")



# Set your password here
PASSWORD = "98897"  # Change this to your desired password

# Ask for the password at the start
attempts = 5
while attempts > 0:
    user_input = input("Enter password to start Sophie: ")
    if user_input == PASSWORD:
        speak("Access granted! Starting Sophie...")
        break
    else:
        attempts -= 1
        speak(f"Incorrect password! {attempts} attempts left.")

    if attempts == 0:
        speak("Too many incorrect attempts. Exiting...")
        time.sleep(2)
        exit()

print("I am  is online.")
speak("Hello sir""! I am Sophie, a super advanced artificial intelligence designed by Shreyank Mishra.")

# Ask user for interaction mode
mode = ""
while mode not in ["voice", "text", "both"]:
    mode = input("How do you want to interact sir? (voice/text/both): ").strip().lower()

print(f"I will run in {mode} mode.")
speak(f"I will run in {mode} mode.")

speak("so what is in your mind today sir?")

MEMORY_FILE = "E:\\SophieAI\\memory.json"

def load_memory():
    """ Load stored memory (conversation history & last topic) """
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Corrupt memory file detected. Resetting memory...")
            return {"conversations": [], "last_topic": None}
    return {"conversations": [], "last_topic": None}

def save_memory(memory):
    """ Save memory to file """
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

memory = load_memory()

    
def chat_with_gpt(prompt):
    openai.api_key = OPENAI_API_KEY  # Set API key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response["choices"][0]["message"]["content"]
        return response_text

    except Exception as e:
        return f"Error: {str(e)}"


        return response_text

    except Exception as e:
        return f"Error: {str(e)}"    

    
def process_command(command):
    command = command.lower()

    if command in ["goodbye", "quit", "exit"]:
        print("Sophie: Goodbye! sir ")
        speak("Goodbye sir! Have a great day!")
        exit()

    elif "open notepad" in command:
        os.system("notepad")
        return "Opening Notepad."

    elif "open calculator" in command:
        os.system("calc")
        return "Opening Calculator."

    elif "open chrome" in command:
        os.system("start chrome")
        return "Opening Google Chrome."

    elif "shutdown" in command:
        os.system("shutdown /s /t 5")
        return "Shutting down your computer."

    elif "restart" in command:
        os.system("shutdown /r /t 5")
        return "Restarting your computer."

    else:
        return "unknown"



def google_search(query):
    """ Searches Google and returns the first relevant result along with a summary. """
    try:
        search_results = list(search(query, num=3, stop=3, pause=2))  # Get top 3 results

        if search_results:
            first_result = search_results[0]
            response = f"I found this on Google: {first_result}"
            
            # Fetch webpage content (optional, if you want Sophie to summarize)
            page_summary = fetch_summary(first_result)  

            return response, page_summary
        else:
            return "I couldn't find anything relevant on Google.", None
    except Exception as e:
        return f"I couldn't retrieve search results right now. Error: {str(e)}", None


def fetch_summary(url):
    """ Fetches and summarizes webpage content from a URL (requires BeautifulSoup). """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Extract first few paragraphs
        paragraphs = soup.find_all("p")
        summary = " ".join([p.get_text() for p in paragraphs[:3]])  # Get first 3 paragraphs
        
        if not summary.strip():
            return "I found a link but couldn't summarize it."

        return summary
    except Exception as e:
        return f"Failed to fetch details. Error: {str(e)}"

    
import openpyxl  # Ensure Excel support

def execute_python_code(code, file_name):
    """Executes dynamically generated Python code for Excel tasks."""
    try:
        # Define allowed globals (Prevent dangerous operations)
        safe_globals = {"openpyxl": openpyxl, "__builtins__": {}}
        
        # Inject file name into code (if needed)
        code = code.replace("your_excel_file.xlsx", file_name)

        exec(code, safe_globals)  # Execute safely
        speak("Excel file has been modified successfully.")

    except Exception as e:
        speak(f"An error occurred while processing the Excel file: {str(e)}")




while True:
    user_input = ""

    user_input = ""  # Reset user input each loop

    if mode in ["voice", "both"]:
        voice_input = listen()
        if voice_input not in ["I didn't understand that", "Speech service is down"]:
            user_input = voice_input  # Only use voice if it's valid

    if mode in ["text", "both"]:
        text_cmd = text_input().strip()
        if text_cmd:  # If text input is given, prioritize it over voice
            user_input = text_cmd  

    if not user_input:
        continue  # Skip if still empty

    user_input = user_input.lower()

    # Detect language
    detected_lang = "hi" if any(word in user_input for word in ["नमस्ते", "कैसे", "समय", "तारीख"]) else "en"

    if detected_lang == "hi":
        user_input = translator.translate(user_input, src="hi", dest="en").text  # Translate Hindi to English

    response = "Hmm... I don’t understand that yet."  # Default response

    audio_frame = wake_word_model.get_audio_frame()
    wake_detected = wake_word_model.predict(audio_frame)

    if wake_detected:
        print("Wake word detected! Sophie is now active.")
        speak("Yes sir, I'm listening.")
        command = listen()


    # ✅ **Detect Follow-up Questions Using Context**
    if user_input in ["tell me more", "explain more", "what else?", "और बताओ", "और जानकारी दो"]:
        if memory["last_topic"]:
            response = f"Sure! Here's more about {memory['last_topic']}."
        else:
            response = "I'm not sure what you're referring to."

    detected_excel_file = None
    if ".xlsx" in user_input or "excel file" in user_input:
        words = user_input.split()
        for word in words:
            if word.endswith(".xlsx"):
                detected_excel_file = word  # Get the file name
                break
        
        if detected_excel_file:
            response = chat_with_gpt(f"Write Python code to modify {detected_excel_file} as per this command: {user_input}")
            execute_python_code(response, detected_excel_file)
            speak("Excel modification completed.")
            continue  # Skip other processing


     # **Check if user wants to use GPT**  
    if user_input.startswith("gpt "):
        prompt = user_input.replace("gpt ", "", 1)  # Remove "GPT " from the command
        response = chat_with_gpt(prompt)
        speak(response)

    elif detected_excel_file:
        response = chat_with_gpt(f"Write Python code to: {user_input}")
        print("Sophie:", response)

    # ✅ **Emotional Responses**
    elif any(word in user_input for word in ["i'm sad", "feeling down", "depressed", "मैं उदास हूँ"]):
        response = "I'm here for you. You can talk to me anytime."

    elif any(word in user_input for word in ["i'm happy", "feeling great", "excited", "मैं खुश हूँ"]):
        response = "That's awesome! I'm happy for you!"

    elif any(word in user_input for word in ["i'm bored", "nothing to do", "बोर हो रहा हूँ"]):
        response = "You could listen to music, watch a movie, or learn something new!"

    # ✅ **News Feature (With Category Filters)**
    elif "news" in user_input:
        category = "general"
        if "business" in user_input:
            category = "business"
        elif "sports" in user_input:
            category = "sports"
        elif "international" in user_input:
            category = "general"
        elif "national" in user_input:
            category = "general"

        API_KEY = "your_newsapi_key_here"
        try:
            url = f"https://newsapi.org/v2/top-headlines?category={category}&language=en&apiKey={API_KEY}"
            news = requests.get(url).json()
            headlines = [article["title"] for article in news["articles"][:5]]
            response = "Here are the latest news headlines: " + ", ".join(headlines)
        except Exception as e:
            response = f"Could not fetch news at the moment. Error: {e}"

    # ✅ **Weather Feature**
    elif "weather" in user_input:
        API_KEY = "your_openweathermap_api_key_here"
        city = "your_city_here"
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            weather_data = requests.get(url).json()
            temperature = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            response = f"The current temperature in {city} is {temperature}°C with {description}."
        except Exception as e:
            response = f"I couldn't fetch the weather right now. Error: {e}"

    # ✅ **Open Applications**
    elif "open notepad" in user_input or "नोटपैड" in user_input:
        response = "Opening Notepad."
        os.system("notepad.exe")

    elif "open calculator" in user_input or "कैलकुलेटर" in user_input:
        response = "Opening Calculator."
        os.system("calc.exe")

    elif "open chrome" in user_input or "क्रोम" in user_input:
        response = "Opening Google Chrome."
        os.system("start chrome")

    elif "open file" in user_input or "फाइल" in user_input:
        response = "Opening your file."
        os.startfile("E:\\SophieAI\\yourfile.txt")

    # ✅ **Shutdown & Restart**
    elif "shutdown" in user_input or "बंद करें" in user_input:
        response = "Shutting down your computer."
        os.system("shutdown /s /t 5")

    elif "restart" in user_input or "पुनः आरंभ करें" in user_input:
        response = "Restarting your computer."
        os.system("shutdown /r /t 5")

    elif any(word in user_input for word in ["exit", "bye", "sleep", "so jao cyron", "बाहर निकलें"]):
        response = "Goodbye! Have a great day!"
        speak(response, detected_lang)
        break

    else:
        response = process_command(user_input)  # Try processing the command first

        if response == "unknown":
            response, summary = google_search(user_input)

            if summary:
                speak(summary)




    # ✅ **Save Last Topic & Conversation**
    memory["last_topic"] = user_input
    # Ensure 'conversations' exists in memory
if "conversations" not in memory:
    memory["conversations"] = []  # Create it if missing

# Now append conversation safely
memory["conversations"].append({"user": user_input, "sophie": response})

# Save back to memory.json
with open("memory.json", "w") as f:
    json.dump(memory, f, indent=4)

    memory["conversations"].append({"user": user_input, "sophie": response})
    if len(memory["conversations"]) > 10:
        memory["conversations"].pop(0)
    save_memory(memory)

    speak(response, detected_lang)