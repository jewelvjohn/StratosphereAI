import socket
import sys, os

from PySide6.QtCore import Qt, QThread, Signal

from PySide6.QtWidgets import (QApplication, QWidget, 
                               QLabel, QTextEdit, 
                               QHBoxLayout, QVBoxLayout, 
                               QPushButton)

from speechToText import STT
from textToSpeech import TTS
from chatbot.chat import Chatbot
from userInterface import MainWindow

# app = QApplication(sys.argv)
# window = MainWindow(app)
# window.show()
# app.exec()

class WorkerThread(QThread):
    refresh_log_trigger = Signal()
    refresh_status_trigger = Signal()
    disconnect_socket_trigger = Signal()

    def run(self):
        self.tts = TTS()
        self.stt = STT()

        self.connect_socket()
        while True:
            receivedData = self.sock.recv(1024).decode("UTF-8")
            print("Received data: " + receivedData)

            if receivedData == "[STT]":
                self.with_stt()

            elif "[SkipSTT]" in receivedData:
                text = receivedData.replace("[SkipSTT]",'')
                self.without_stt(text)

            elif receivedData == "[Disconnect]":
                self.disconnect_socket()
                break
        
        notification = "Closing socket thread!"
        self.update_status(notification)
        self.quit()

    #Chatbot related stuff...

    def chatbot(self, input: str):
        json_file = "chatbot\\intents.json"
        data_file = "chatbot\\data.pth"
        
        chat = Chatbot(json_file, data_file)
        response = chat.get_response(input)

        return response

    def with_stt(self):
        recognition = self.stt.listen()

        if(recognition != ""):
            notification = "Speech recognised"
            self.update_status(notification)

        player_speech = "[Player]: " + recognition
        self.update_log(player_speech)
        self.sent(player_speech)
        
        response = self.chatbot(recognition)

        bot_speech = "[Chatbot]: " + response + '\n'
        self.update_log(bot_speech)
        self.sent(bot_speech)

        self.tts.speak(response, 1, 150)
        self.sent("[Success]")


    def without_stt(self, recognition: str):

        player_speech = "[Player]: " + recognition
        self.update_log(player_speech)
        self.sent(player_speech)

        response = self.chatbot(recognition)

        bot_speech = "[Chatbot]: " + response + '\n'
        self.update_log(bot_speech)
        self.sent(bot_speech)

        self.tts.speak(response, 1, 150)
        self.sent("[Success]")


    #UI related stuff...

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

    #Socket related stuff...

    def sent(self, data: str):
        self.sock.sendall(data.encode("UTF-8"))

    def connect_socket(self):
        self.shutdownSocket = False

        host, port = "127.0.0.1", 25001
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        notification = "Connection successfully established!"
        self.update_status(notification)

    def stop_socket(self):
        self.sent("[Disconnect Request]")

    def disconnect_socket(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        
        notification = "Connection successfully closed!"
        self.update_status(notification)

class MainWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.clear_log_data()
        self.clear_status_data()

        self.initialize_ui()

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
        
        disconnect_button = QPushButton("DISCONNECT")
        disconnect_button.setFixedSize(130, 40)
        disconnect_button.clicked.connect(self.disconnect)
        disconnect_button.setStyleSheet(
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
        button_layout.addSpacing(20)
        button_layout.addWidget(disconnect_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(chat_header)
        main_layout.addWidget(self.chat_textbox)
        main_layout.addWidget(status_header)
        main_layout.addWidget(self.status_textbox)
        main_layout.addSpacing(10)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def initialize_worker(self):
        self.worker_thread = WorkerThread()
        self.worker_thread.refresh_log_trigger.connect(self.refresh_log)
        self.worker_thread.refresh_status_trigger.connect(self.refresh_status)
        self.worker_thread.disconnect_socket_trigger.connect(self.worker_thread.stop_socket)

    def clear_status_data(self):
        if os.path.isfile("files\\status.jwl"):
            os.remove("files\\status.jwl")

    def clear_log_data(self):
        if os.path.isfile("files\\log.jwl"):
            os.remove("files\\log.jwl")

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

    def update_log(self, text: str):
        file = open("files\\log.jwl", 'a')
        file.write('\n '+ text)
        file.close()

        self.refresh_log()

    def update_status(self, text: str):
        file = open("files\\status.jwl", 'a')
        file.write('\n '+ text)
        file.close()

        self.refresh_status()

    def connect(self):
        self.initialize_worker()

        notification = "Trying to connect..."
        self.update_status(notification)

        self.worker_thread.start()

    def disconnect(self):
        notification = "Trying to disconnect..."
        self.update_status(notification)

        self.worker_thread.disconnect_socket_trigger.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec()