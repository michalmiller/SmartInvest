from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
import requests
from gui_config import RENDER_API

# הגדרה ידנית של כתובת השרת עבור אולמה בלבד
RENDER_API_OLAMA = "http://localhost:11434"

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

   # ...existing code...

    def ask_model(self):
        q = self.q_edit.toPlainText().strip()
        if not q:
            QMessageBox.information(self, "שימי לב", "נא להקליד שאלה.")
            return

        self.ask_btn.setEnabled(False)
        self.a_view.setPlainText("⏳ שואלת את המודל...")

        try:
            url = f"{RENDER_API_OLAMA}/api/generate"
            payload = {
                "model": "llama3",  # שנה לשם המודל שלך אם צריך
                "prompt": q
            }
            res = requests.post(url, json=payload, timeout=60)

            if res.status_code != 200:
                self.a_view.setPlainText(f"שגיאה ({res.status_code}) מהשרת.")
                return

            data = res.json()
            answer = data.get("response") or "❓ לא התקבלה תשובה."
            self.a_view.setPlainText(answer)

        except requests.exceptions.RequestException as e:
            self.a_view.setPlainText(f"שגיאת רשת: {e}")
        except Exception as e:
            self.a_view.setPlainText(f"שגיאה כללית: {e}")
        finally:
            self.ask_btn.setEnabled(True)
# ...existing code...