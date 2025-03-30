import speech_recognition as sr
import webbrowser
import pyttsx3
import sys
import google.generativeai as genai

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id) 
engine.setProperty('rate', 140) 
engine.setProperty('volume', 1.0)

genai.configure(api_key="Your API-KEY")

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    """Process command with Gemini AI"""
    try:
        model_names = [
            'gemini-1.5-pro-latest',  
            'gemini-pro',            
            'models/gemini-pro'      
        ]
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"You are a ai assistant like alexa answer it only in text form no symbols and nothing, User: {command}",
                    generation_config={"max_output_tokens": 150}
                )
                return response.text
            except Exception:
                continue
                
        return "Sorry, I couldn't connect to the AI service."
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Sorry, I couldn't process that request."

def processCommand(command):
    """Process voice commands"""
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open github" in command:
        webbrowser.open("https://github.com")
        speak("Opening GitHub")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")
    elif "open chatgpt" in command:
        webbrowser.open("https://chatgpt.com")
        speak("Opening chatgpt")
    elif "shutdown" in command or "exit" in command or "close" in command or "terminate" in command:
        speak("Shutting down Jarvis. Goodbye!")
        sys.exit(0)
    else:
        response = aiProcess(command)
        print(response)
        speak(response)

if __name__ == "__main__":
    speak("Initializing Jarvis")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                
            word = recognizer.recognize_google(audio).lower()
            print(f"Heard: {word}")
            
            if "jarvis" in word:
                speak("Yes? How can I help you?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command)
                    
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.WaitTimeoutError:
            speak("Please speak your command briefly")
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry, I encountered an error")
