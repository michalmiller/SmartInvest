import json
import os
from typing import Callable, Any
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)


class LoginWindow(QWidget):
    def __init__(self, on_login_success: Callable[[Any], None]):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("התחברות למערכת")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("שם משתמש")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("סיסמה")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("התחבר")
        self.login_button.clicked.connect(self.try_login)

        layout.addWidget(QLabel("התחברות ל-SmartInvest"))
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def try_login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        user = self.validate_user(username, password)
        if user:
            self.on_login_success(user)  # שליחה עם שם מלא
            self.close()
        else:
            QMessageBox.critical(self, "שגיאה", "שם משתמש או סיסמה שגויים")

    def validate_user(self, username, password):
        path =("C:\Users\מיכל מילר\Desktop\smartinvest\backend\storage\portfolio.json")
        print(f"🔍 קוראת מתוך: {path}")

        if not os.path.exists(path):
            print("❌ הקובץ לא קיים")
            return None

        with open(path, encoding="utf-8") as f:
            users = json.load(f)

        print("📄 תוכן הקובץ:", users)

        for user in users:
            print(f"בודקת: {user}")
            if user["username"] == username and user["password"] == password:
                print("✅ משתמש תקף")
                return user

        print("🚫 התחברות נכשלה")
        return None
