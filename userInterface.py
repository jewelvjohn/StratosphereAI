from PySide6.QtWidgets import (QWidget, QLabel, 
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

        header = QLabel("STRATOSPHERE NPC")
        header.setStyleSheet(
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
        header.setAlignment(Qt.AlignCenter)

        self.textbox = QTextEdit()
        self.textbox.setStyleSheet(
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
        #listen_button.clicked.connect(self.listen)
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

        run_button = QPushButton("RESPOND")
        #run_button.clicked.connect(self.respond)
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
        main_layout.addWidget(header)
        main_layout.addWidget(self.textbox)
        main_layout.addWidget(listen_button)
        main_layout.addWidget(run_button)

        self.setLayout(main_layout)