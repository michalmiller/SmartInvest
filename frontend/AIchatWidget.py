# gui_app.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import requests

class AIChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartInvest - שאל את המודל")  # לא חובה
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("הזן את השאלה שלך:")
        layout.addWidget(self.label)

        self.input = QLineEdit()
        layout.addWidget(self.input)

        self.button = QPushButton("שאל")
        self.button.clicked.connect(self.ask_model)
        layout.addWidget(self.button)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

        self.setLayout(layout)

    def ask_model(self):
        question = self.input.text()
        if not question.strip():
            self.result.setPlainText("אנא הזן שאלה")
            return

        try:
            url = f"http://127.0.0.1:8000/ask/?question={question}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.result.setPlainText(data.get("answer_he", "[לא התקבלה תשובה]"))
            else:
                self.result.setPlainText(f"שגיאה: {response.status_code}")
        except Exception as e:
            self.result.setPlainText(f"שגיאה בחיבור לשרת: {str(e)}")
