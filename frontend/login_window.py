import json
import os
from typing import Callable, Any
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import requests

class LoginWindow(QWidget):
    def __init__(self, on_login_success: Callable[[Any], None]):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("התחברות למערכת")
        self.setFixedSize(300, 200)
        # לדוג' בקובץ הראשי או בכל חלון שתרצי
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("logo_temp.jpg").scaled(60, 60))
        self.logo.setObjectName("AppLogo")
        layout = QVBoxLayout()
        layout.addWidget(self.logo, alignment=Qt.AlignLeft | Qt.AlignTop)

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
        url = "http://www.michalmiller.somee.com/portfolio.json"
        try:
            response = requests.get(url, timeout=10)
            print(f"🔍 קוראת מתוך: {url}")

            if response.status_code != 200:
                print("❌ שגיאה בטעינה מהשרת:", response.status_code)
                return None

            data = response.json()
            print("📄 תוכן הקובץ:", data)

            # בדיקת המשתמשים מהשרת
            for user in data:
                print(f"בודקת: {user}")
                if user.get("username") == username and user.get("password") == password:
                    print("✅ משתמש תקף")
                    return user

            print("🚫 התחברות נכשלה")
            return None

        except Exception as e:
            print(f"❌ שגיאה כללית: {e}")
            return None


