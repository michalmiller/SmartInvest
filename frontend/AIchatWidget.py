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

    def ask_model(self):
        q = self.q_edit.toPlainText().strip()
        if not q:
            QMessageBox.information(self, "שימי לב", "נא להקליד שאלה.")
            return

        self.ask_btn.setEnabled(False)
        try:
            url = f"{RENDER_API}/ask/"
            r = requests.get(url, params={"question": q}, timeout=30)
            if r.status_code != 200:
                QMessageBox.warning(self, "שגיאה", f"שגיאה מהשרת ({r.status_code}).")
                return
            data = r.json() or {}
            ans = data.get("answer_he") or data.get("answer") or ""
            self.a_view.setPlainText(ans)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "שגיאת רשת", str(e))
        finally:
            self.ask_btn.setEnabled(True)
