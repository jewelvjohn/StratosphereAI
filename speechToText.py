import speech_recognition as sr

class STT:
    def listen(self): 
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Speak something...")
            audio = r.listen(source)

        text = r.recognize_google(audio)
        print(text)

        # with open("files\\output.jwl", 'w') as f:
        #     f.write(text)

        return text