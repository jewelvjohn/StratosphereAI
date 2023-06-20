import sys
import time

from userInterface import MainWindow
from PySide6.QtWidgets import QApplication

from speechToText import STT
from textToSpeech import TTS

# app = QApplication(sys.argv)
# window = MainWindow(app)
# window.show()
# app.exec()

while True:
    choice = input("choice (L/R): ")

    if choice == "L":
        stt = STT()
        stt.listen()
        
    elif choice == "R":
        text = input("Enter the input: ")
        with open('files\\input.jwl', 'w') as f:
            f.write(text)

        tts = TTS(1, 150)
        tts.speak()

    else :
        print("Invalid input!, try again...")