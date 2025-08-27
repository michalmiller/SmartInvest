# invest_input_tab.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QMessageBox, QDateEdit
)
from PySide6.QtCore import QDate
import requests


class InvestInputTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        layout = QVBoxLayout(self)

        # שדות טופס
        self.asset_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.risk_input = QComboBox()
        self.risk_input.addItems(["low", "medium", "high"])
        self.category_input = QLineEdit()

        layout.addWidget(QLabel("נכס:"))
        layout.addWidget(self.asset_input)

        layout.addWidget(QLabel("סכום השקעה:"))
        layout.addWidget(self.amount_input)

        layout.addWidget(QLabel("תאריך השקעה:"))
        layout.addWidget(self.date_input)

        layout.addWidget(QLabel("רמת סיכון:"))
        layout.addWidget(self.risk_input)

        layout.addWidget(QLabel("קטגוריה:"))
        layout.addWidget(self.category_input)

        # כפתור שליחה
        self.submit_btn = QPushButton("📤 שלח השקעה")
        self.submit_btn.clicked.connect(self.send_data)
        layout.addWidget(self.submit_btn)

    def send_data(self):
        try:
            data = {
                "asset": self.asset_input.text().strip(),
                "amount": float(self.amount_input.text().strip()),
                "date": self.date_input.date().toString("yyyy-MM-dd"),
                "risk": self.risk_input.currentText(),
                "category": self.category_input.text().strip()
            }

            res = requests.post("http://localhost:8000/invest/", json=data)
            if res.status_code == 200:
                QMessageBox.information(self, "הצלחה", "✅ ההשקעה נשמרה בהצלחה!")
                self.clear_fields()
            else:
                QMessageBox.critical(self, "שגיאה", f"שגיאה בשמירה: {res.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "שגיאה", f"שגיאה: {str(e)}")

    def clear_fields(self):
        self.asset_input.clear()
        self.amount_input.clear()
        self.category_input.clear()
        self.date_input.setDate(QDate.currentDate())
        self.risk_input.setCurrentIndex(0)
