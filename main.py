import socket
import sys, os

from PySide6.QtCore import Qt, QThread, Signal

from PySide6.QtWidgets import (QApplication, QWidget, 
                               QLabel, QTextEdit, 
                               QHBoxLayout, QVBoxLayout, 
                               QPushButton)

from speechToText import STT
from textToSpeech import TTS
from userInterface import MainWindow

# app = QApplication(sys.argv)
# window = MainWindow(app)
# window.show()
# app.exec()

class WorkerThread(QThread):
    refresh_log_trigger = Signal()
    refresh_status_trigger = Signal()

    def run(self):
        tts = TTS()
        stt = STT()

        host, port = "127.0.0.1", 25001
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        notification = "Connection successfully established!"
        self.update_status(notification)

        while True:
            receivedData = self.sock.recv(1024).decode("UTF-8")
            print(receivedData)

            if(receivedData == "[Chatbot]"):
                
                recognition = stt.listen()

                if(recognition != ""):
                    notification = "Speech recognised"
                    self.update_status(notification)

                player_speech = "[Player]: " + recognition
                self.update_log(player_speech)

                bot_speech = "[Chatbot]: " + recognition
                self.update_log(bot_speech)

                tts.speak(recognition, 1, 150)
                self.sent(recognition)

    def update_log(self, text: str):
        file = open("files\\log.jwl", 'a')
        file.write('\n '+ text)
        file.close()

        self.refresh_log_trigger.emit()

    def update_status(self, text: str):
        file = open("files\\status.jwl", 'a')
        file.write('\n '+ text)
        file.close()

        self.refresh_status_trigger.emit()

    def sent(self, data: str):
        self.sock.sendall(data.encode("UTF-8"))

class MainWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.initialize_ui()
        self.worker_thread = WorkerThread()
        self.worker_thread.refresh_log_trigger.connect(self.refresh_log)
        self.worker_thread.refresh_status_trigger.connect(self.refresh_status)

    def initialize_ui(self):
        self.resize(640, 640)
        self.setWindowTitle("Stratosphere AI")
        self.setStyleSheet("QWidget {background: rgb(40, 40, 40);}")

        chat_header = QLabel("CHAT LOG")
        chat_header.setStyleSheet(
                                    """
                                    QLabel
                                    {
                                        color: #CCCCCC; 
                                        font-size: 15px; 
                                        font-weight: 850;
                                        padding: 8px 8px;
                                    }
                                    """
                                )
        chat_header.setAlignment(Qt.AlignCenter)

        status_header = QLabel("STATUS")
        status_header.setStyleSheet(
                                    """
                                    QLabel
                                    {
                                        color: #CCCCCC; 
                                        font-size: 15px; 
                                        font-weight: 850;
                                        padding: 8px 8px;
                                    }
                                    """
                                )
        status_header.setAlignment(Qt.AlignCenter)

        self.chat_textbox = QTextEdit()
        self.chat_textbox.setReadOnly(True)
        self.chat_textbox.setStyleSheet(
                                    """
                                    QTextEdit
                                    {
                                        background-color: #202020; 
                                        color: #CCCCCC; 
                                        border-radius: 10px; 
                                        padding: 8px 8px;
                                    }
                                    """
                                )

        self.status_textbox = QTextEdit()
        self.status_textbox.setReadOnly(True)
        self.status_textbox.setMaximumHeight(128)
        self.status_textbox.setStyleSheet(
                                    """
                                    QTextEdit
                                    {
                                        background-color: #151515; 
                                        color: #CCCCCC; 
                                        border-radius: 10px; 
                                        padding: 8px 8px;
                                    }
                                    """
                                )
        
        connect_button = QPushButton("CONNECT")
        connect_button.setFixedSize(130, 40)
        connect_button.clicked.connect(self.connect)
        connect_button.setStyleSheet(
                                    """
                                    QPushButton {
                                        font-size: 15px;
                                        font-weight: 800;
                                        background-color: #335033;
                                        border: 0px solid #555555;
                                        border-radius: 5px;
                                        color: #CCCCCC;
                                        padding: 8px 8px;
                                    }
                                    
                                    QPushButton:hover {
                                        background-color: #151515;
                                        border: 1px solid #555555;
                                    }
                                    
                                    QPushButton:pressed {
                                        background-color: #444444;
                                        border: 2px solid #777777;
                                    }
                                    """
                                )
        
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(connect_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(chat_header)
        main_layout.addWidget(self.chat_textbox)
        main_layout.addWidget(status_header)
        main_layout.addWidget(self.status_textbox)
        main_layout.addSpacing(10)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def status_data(self):
        if os.path.isfile("files\\status.jwl"):
            with open("files\\status.jwl", 'r') as file:
                data = file.read() 
            file.close()
            return data
        else:
            return ""
        
    def log_data(self):
        if os.path.isfile("files\\log.jwl"):
            with open("files\\log.jwl", 'r') as file:
                data = file.read() 
            file.close()
            return data
        else:
            return ""

    def refresh_status(self):
        text = self.status_data()
        self.status_textbox.setPlainText(text)

    def refresh_log(self):
        text = self.log_data()
        self.chat_textbox.setPlainText(text)

    def connect(self):
        notification = "Trying to connect..."
        file = open("files\\status.jwl", 'a')
        file.write(notification)
        self.refresh_status()

        self.worker_thread.start()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec()