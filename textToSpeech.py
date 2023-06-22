# import os
import pyttsx3

class TTS():
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, input, voice_id, rate):

        # if os.path.exists("files\\input.jwl"):
        #     file = open("files\\input.jwl", 'r')
        #     input = file.read()
        # 
        # else:
        #     print("Failed to read input file!")
        #     input = "Sorry I can't hear you"
            
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice_id].id)
        self.engine.setProperty('rate', rate)
        self.engine.save_to_file(input, "files\\output.wav")
        self.engine.say(input)
        self.engine.runAndWait()