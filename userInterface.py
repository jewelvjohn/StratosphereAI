from PySide6.QtWidgets import (QWidget, QLabel, QTextEdit, 
                               QHBoxLayout, QVBoxLayout, 
                               QPushButton)

from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.resize(640, 640)
        self.setWindowTitle("Stratosphere AI")
        self.setStyleSheet("QWidget {background: rgb(40, 40, 40);}")

        self.acceptConnection = False

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
        connect_button.clicked.connect(parent.connect)
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

    def append_status(self, text):
        update = self.status_textbox.toPlainText() + '\n' + text
        self.status_textbox.setPlainText(update)

    def append_log(self, text):
        update = self.chat_textbox.toPlainText() + '\n' + text
        self.chat_textbox.setPlainText(update)