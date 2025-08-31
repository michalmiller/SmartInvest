# search_tab.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QMessageBox
)
import requests
from gui_config import RENDER_API


class SearchTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # שדה חיפוש
        layout.addWidget(QLabel("🔍 חפש נכס:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("הקלד שם נכס או סימול…")
        layout.addWidget(self.search_input)

        # כפתור חיפוש
        self.search_button = QPushButton("חפש")
        self.search_button.clicked.connect(self.perform_search)
        layout.addWidget(self.search_button)

        # טבלת תוצאות
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["נכס", "סכום", "תאריך", "סיכון", "קטגוריה"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.results_table)

    def perform_search(self):
        query = self.search_input.text().strip()
        self.results_table.setRowCount(0)

        if not query:
            return

        try:
            res = requests.get(f"{RENDER_API}/search/", params={"query": query}, timeout=10)

            if res.status_code != 200:
                QMessageBox.warning(self, "שגיאה", f"שגיאה בקריאת הנתונים ({res.status_code}).")
                return

            payload = res.json() or {}
            data = payload.get("results", [])
            if not isinstance(data, list):
                data = []

            if not data:
                QMessageBox.information(self, "אין תוצאות", f"לא נמצאו תוצאות ל: {query}")
                return

            # מילוי טבלה
            self.results_table.setRowCount(len(data))
            for row, item in enumerate(data):
                self.results_table.setItem(row, 0, QTableWidgetItem(str(item.get("asset", ""))))

                # עיצוב סכום יפה אם אפשר
                amount = item.get("amount", "")
                try:
                    amount = float(amount)
                    amount_str = f"₪{amount:,.2f}"
                except Exception:
                    amount_str = str(amount)
                self.results_table.setItem(row, 1, QTableWidgetItem(amount_str))

                self.results_table.setItem(row, 2, QTableWidgetItem(str(item.get("date", ""))))
                self.results_table.setItem(row, 3, QTableWidgetItem(str(item.get("risk", ""))))
                self.results_table.setItem(row, 4, QTableWidgetItem(str(item.get("category", ""))))

        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "שגיאת רשת", str(e))
        except Exception as e:
            QMessageBox.critical(self, "שגיאה", f"שגיאה בחיפוש: {e}")
