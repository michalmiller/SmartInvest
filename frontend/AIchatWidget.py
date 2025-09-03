# AIchatWidget.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
import requests
from gui_config import RENDER_API

class AIchatWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("🤖 יועץ AI"))
        self.q_edit = QTextEdit()
        self.q_edit.setPlaceholderText("שאלי שאלה…")
        layout.addWidget(self.q_edit)

        self.ask_btn = QPushButton("שאלי")
        self.ask_btn.clicked.connect(self.ask_model)
        layout.addWidget(self.ask_btn)

        layout.addWidget(QLabel("תשובה:"))
        self.a_view = QTextEdit()
        self.a_view.setReadOnly(True)
        layout.addWidget(self.a_view)

def send_prompt(self):
    user_input = self.input_box.toPlainText().strip()
    if not user_input:
        return

    self.output_box.setPlainText("⏳ חושב...")

    try:
        res = requests.post(f"{RENDER_API}/ask", json={"prompt": user_input})
        res.raise_for_status()
        answer = res.json().get("answer", "❓ לא התקבלה תשובה.")
        self.output_box.setPlainText(answer)
    except Exception as e:
        self.output_box.setPlainText(f"שגיאה בתשובה: {e}")
