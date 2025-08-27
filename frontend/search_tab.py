# search_tab.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView
)
import requests


class SearchTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # שדה חיפוש
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("הקלד שם נכס או סימול...")
        layout.addWidget(QLabel("🔍 חפש נכס:"))
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
            res = requests.get("http://localhost:8000/search/", params={"query": query})
            data = res.json().get("results", [])
            if not data:
              from PySide6.QtWidgets import QMessageBox
              QMessageBox.information(self, "אין תוצאות", f"לא נמצאו תוצאות ל: {query}")
              return


            self.results_table.setRowCount(len(data))
            for row, item in enumerate(data):
                self.results_table.setItem(row, 0, QTableWidgetItem(item.get("asset", "")))
                self.results_table.setItem(row, 1, QTableWidgetItem(str(item.get("amount", ""))))
                self.results_table.setItem(row, 2, QTableWidgetItem(item.get("date", "")))
                self.results_table.setItem(row, 3, QTableWidgetItem(item.get("risk", "")))
                self.results_table.setItem(row, 4, QTableWidgetItem(item.get("category", "")))

        except Exception as e:
            self.results_table.setRowCount(0)
            print("שגיאה בחיפוש:", e)
