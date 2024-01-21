# pip install llama-cpp-python
import speech_recognition as sr
import pyttsx3 # may use tensorflowtts
# import asyncio 
from llama_cpp import Llama

class Assistant:
    start_phrase = ""
    stop_phrase = "go to sleep"
    recognizer = sr.Recognizer()
    active = True
    LLM = Llama(model_path="models/mistral-7b-instruct-v0.1.Q6_K.gguf") # Got Model From HuggingFace

    # Setup Speak Engine
    speak_engine = pyttsx3.init()

    def __init__(self, name="tracer") -> None:
        self.start_phrase = name
        self.setup_speak_engine()
        print("Successfully initialized new Assistant")

    def setup_speak_engine(self) -> None:
        self.speak_engine.setProperty('rate', 150)
        self.speak_engine.setProperty('volume', 1.0)
        voices = self.speak_engine.getProperty('voices')
        self.speak_engine.setProperty('voice', voices[0].id)

    # Access Microphone and get audio file in format of mp3
    def listen(self) -> object:
        microphone = sr.Microphone()
        with microphone as source:
            print("listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
            audio = self.recognizer.listen(source)
        return audio

    # Input audio and get text
    def speech_to_text(self, audio:object) -> str:
        try:
            text = self.recognizer.recognize_google(audio)
            # print(text)
        except sr.UnknownValueError:
            text = "unrecognizable"
            # print("Unknown value")
        return text.lower()

    # Input text and repeat the text
    def text_to_speech(self, text:str) -> None:
        self.speak_engine.say(text)
        self.speak_engine.runAndWait()
        self.speak_engine.stop()

    # Input text into large language model and return response
    def get_response(self, text:str) -> str:
        print("formulating response...\n")
        response = self.LLM(text, model="mistral")
        return response["choices"][0]["text"]

    # Just to make the code easier to read
    def respond(self, text:str):
        self.text_to_speech(text)

    # Clears command of anything that will confuse the LLM
    def clean_command(self, text:str) -> str:
        index = text.find(self.start_phrase)
        # if the command was valid
        if index != -1:
            cleaned_text = text[index + len(self.start_phrase):].strip() # return the following text after the start phrase with spaces stripped away
            return cleaned_text
        else:
            return text
        
    # Assistants response after cleaning and processing
    def process_command(self, command:str) -> None:
        if self.start_phrase in command:
            if self.stop_phrase in command:
                self.active = False
                self.respond("Understood. I hope I was of assistance. Have a great rest of your day!")
            else:
                cleaned_command = self.clean_command(command)
                response = self.get_response(cleaned_command)
                self.respond(response)

    # Run the assistant
    def start(self) -> None:
        
        self.respond("Hello, I am " + self.start_phrase + ", your personal assistant")
        self.respond("For privacy reasons, I will not be able to listen to your commands unless you say my activation phrase. hey " + self.start_phrase + ".")

        while self.active:
            audio = self.listen()
            command = self.speech_to_text(audio)
            self.process_command(command)



tracer = Assistant()
tracer.start()