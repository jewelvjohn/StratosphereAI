import sys
from textToSpeech import TTS
from speechToText import STT
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, 
                               QTextEdit, QHBoxLayout, QVBoxLayout, 
                               QPushButton)

from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.resize(640, 480)
        self.setWindowTitle("Stratosphere AI")
        self.setStyleSheet("QWidget {background: rgb(40, 40, 40);}")

        input_label = QLabel("INPUT")
        input_label.setStyleSheet(
                                    """
                                    QLabel
                                    {
                                        color: #CCCCCC; 
                                        font-size: 15px; 
                                        font-weight: 850;
                                        background-color: #333333;
                                        border-radius: 5px;
                                        padding: 8px 8px;
                                    }
                                    """
                                )
        input_label.setAlignment(Qt.AlignCenter)

        self.input_textbox = QTextEdit()
        self.input_textbox.setStyleSheet(
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
        
        listen_button = QPushButton("LISTEN")
        listen_button.clicked.connect(self.run_stt)
        listen_button.setStyleSheet(
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
        
        output_label = QLabel("OUTPUT")
        output_label.setStyleSheet(
                                    """
                                    QLabel
                                    {
                                        color: #CCCCCC; 
                                        font-size: 15px; 
                                        font-weight: 850;
                                        background-color: #333333;
                                        border-radius: 5px;
                                        padding: 8px 8px;
                                    }
                                    """
                                )
        output_label.setAlignment(Qt.AlignCenter)
        
        self.output_textbox = QTextEdit()
        self.output_textbox.setStyleSheet(
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

        run_button = QPushButton("RUN")
        run_button.clicked.connect(self.run_ai)
        run_button.setStyleSheet(
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

        main_layout = QVBoxLayout()
        main_layout.addWidget(input_label)
        main_layout.addWidget(self.input_textbox)
        main_layout.addWidget(listen_button)
        main_layout.addWidget(output_label)
        main_layout.addWidget(self.output_textbox)
        main_layout.addWidget(run_button)

        self.setLayout(main_layout)

    def run_ai(self):
        input = self.input_textbox.toPlainText()
        self.run_tts(input)

    def run_stt(self):
        self.input_textbox.setText("Say Something...")
        stt = STT() 
        text = stt.listen()
        self.input_textbox.clear()
        self.input_textbox.setText(text)

    def run_tts(self, input):
        tts = TTS(1, 150)
        tts.save_to_file(input, "output.wav")

app = QApplication(sys.argv)
window = MainWindow(app)
window.show()
app.exec()