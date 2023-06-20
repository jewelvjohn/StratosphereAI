import os
import pyttsx3

class TTS():
    def __init__(self, voice_id, rate):
        self.engine = pyttsx3.init()

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice_id].id)
        self.engine.setProperty('rate', rate)

    def speak(self):

        if os.path.exists("files\\input.jwl"):
            file = open("files\\input.jwl", 'r')
            input = file.read()
        
        else:
            print("Failed to read input file!")
            input = "Sorry I can't hear you"
            
        self.engine.save_to_file(input, "files\\output.wav")
        self.engine.say(input)
        self.engine.runAndWait()