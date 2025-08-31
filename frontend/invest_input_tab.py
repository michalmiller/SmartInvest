# invest_input_tab.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QMessageBox, QDateEdit
)
from PySide6.QtCore import QDate, Signal
from PySide6.QtGui import QDoubleValidator
import requests
from gui_config import RENDER_API

class InvestInputTab(QWidget):
    investment_saved = Signal()  # ← סיגנל חדש

    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        layout = QVBoxLayout(self)

        self.asset_input = QLineEdit()

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("לדוגמה: 1000 או 1000.50")
        self.amount_input.setValidator(QDoubleValidator(0.0, 1e12, 2, self))

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

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

        self.submit_btn = QPushButton("📤 שלח השקעה")
        self.submit_btn.clicked.connect(self.send_data)
        layout.addWidget(self.submit_btn)

    def send_data(self):
        asset = self.asset_input.text().strip()
        category = self.category_input.text().strip()
        if not asset:
            QMessageBox.warning(self, "שגיאה", "אנא הזן שם נכס.")
            return

        try:
            amount = float(self.amount_input.text().strip())
            if amount <= 0:
                raise ValueError
        except Exception:
            QMessageBox.critical(self, "שגיאה", "אנא הכנס סכום תקין (לדוגמה 1000 או 1000.50).")
            return

        payload = {
            "asset": asset,
            "amount": amount,
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "risk": self.risk_input.currentText(),
            "category": category
        }

        self.submit_btn.setEnabled(False)
        try:
            res = requests.post(f"{RENDER_API}/invest/", json=payload, timeout=15)
            if res.status_code in (200, 201):
                QMessageBox.information(self, "הצלחה", "✅ ההשקעה נשמרה בהצלחה!")
                self.clear_fields()
                self.investment_saved.emit()  # ← מודיע לטאב השני לרענן
            else:
                body = res.text or ""
                QMessageBox.critical(self, "שגיאה", f"שגיאה בשמירה ({res.status_code}).\n{body[:400]}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "שגיאת רשת", f"בעיה בחיבור לשרת: {e}")
        finally:
            self.submit_btn.setEnabled(True)

    def clear_fields(self):
        self.asset_input.clear()
        self.amount_input.clear()
        self.category_input.clear()
        self.date_input.setDate(QDate.currentDate())
        self.risk_input.setCurrentIndex(0)
