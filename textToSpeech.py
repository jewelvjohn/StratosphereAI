import pyttsx3

class TTS():
    def __init__(self, voice_id, rate):
        self.engine = pyttsx3.init()

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice_id].id)
        self.engine.setProperty('rate', rate)

    def save_to_file(self, input, output):
        self.engine.save_to_file(input, output)
        self.engine.say(input)
        self.engine.runAndWait()