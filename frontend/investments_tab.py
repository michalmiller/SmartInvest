# investments_tab.py

import requests
from collections import Counter

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView
)
from PySide6.QtGui import QPainter
from PySide6.QtCharts import (
    QChart, QChartView, QPieSeries,
    QBarSeries, QBarSet, QBarCategoryAxis
)

from gui_config import RENDER_API


class InvestmentsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("📋 השקעות נוכחיות"))

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["נכס", "סכום", "תאריך", "סיכון", "קטגוריה"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.graphs_layout = QHBoxLayout()
        self.layout.addLayout(self.graphs_layout)

        self.load_data()

# ...existing code...
    def load_data(self):
        """טוען נתוני השקעות מ-Somee (קובץ JSON סטטי)."""
        try:
            res = requests.get("http://www.michalmiller.somee.com/investments.json", timeout=120)
            print(f"📡 Status: {res.status_code}")
            print(f"🔍 Response: {res.text}")

            if res.status_code != 200:
                self.table.setRowCount(0)
                self.clear_graphs()
                return

            data = res.json()  # אם הקובץ הוא רשימה של השקעות
            if not isinstance(data, list):
                data = []

            self.populate_table(data)
            self.create_charts(data)

        except requests.exceptions.RequestException as e:
            print(f"🌐 שגיאת רשת: {e}")
            self.table.setRowCount(0)
            self.clear_graphs()
        except Exception as e:
            print(f"💥 שגיאה בטעינה: {e}")
            self.table.setRowCount(0)
            self.clear_graphs()
# ...existing code...
    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for row, item in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(item.get("asset", ""))))

            # פורמט סכום
            try:
                amount = float(item.get("amount", 0))
                amount_str = f"₪{amount:,.2f}"
            except:
                amount_str = str(item.get("amount", ""))
            self.table.setItem(row, 1, QTableWidgetItem(amount_str))

            self.table.setItem(row, 2, QTableWidgetItem(str(item.get("date", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.get("risk", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(str(item.get("category", ""))))

    def create_charts(self, data):
        self.clear_graphs()
        if not data:
            return
        self.create_category_pie_chart(data)
        self.create_risk_bar_chart(data)

    def create_category_pie_chart(self, data):
        categories = [item.get("category", "אחר") for item in data]
        counts = Counter(categories)

        series = QPieSeries()
        for category, count in counts.items():
            series.append(f"{category} ({count})", count)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("התפלגות לפי קטגוריות השקעה")

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        self.graphs_layout.addWidget(chart_view)

    def create_risk_bar_chart(self, data):
        risks = [str(item.get("risk", "medium")).lower() for item in data]
        counts = Counter(risks)

        labels = ["low", "medium", "high"]
        hebrew = ["נמוכה", "בינונית", "גבוהה"]
        values = [counts.get(label, 0) for label in labels]

        bar_set = QBarSet("מספר השקעות")
        bar_set.append(values)

        series = QBarSeries()
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("התפלגות לפי רמת סיכון")
        chart.createDefaultAxes()

        axis = QBarCategoryAxis()
        axis.append(hebrew)
        chart.setAxisX(axis, series)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        self.graphs_layout.addWidget(chart_view)

    def clear_graphs(self):
        while self.graphs_layout.count():
            child = self.graphs_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def refresh_data(self):
        self.load_data()
