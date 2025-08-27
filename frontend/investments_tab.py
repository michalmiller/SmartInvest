import requests
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView
)
from PySide6.QtGui import QPainter
from PySide6.QtCharts import (
    QChart, QChartView, QPieSeries,
    QBarSeries, QBarSet, QBarCategoryAxis
)


class InvestmentsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # כותרת
        self.layout.addWidget(QLabel("📋 השקעות נוכחיות"))

        # טבלה
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["נכס", "סכום", "תאריך", "סיכון", "קטגוריה"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        # אזור גרפים (אופקי)
        self.graphs_layout = QHBoxLayout()
        self.layout.addLayout(self.graphs_layout)

        # שליפת הנתונים
        self.load_data()

    def load_data(self):
        try:
            # השקעות
            res = requests.get("http://localhost:8000/invest/")
            data = res.json().get("investments", [])

            self.table.setRowCount(len(data))
            for row, item in enumerate(data):
                self.table.setItem(row, 0, QTableWidgetItem(str(item.get("asset", ""))))
                self.table.setItem(row, 1, QTableWidgetItem(str(item.get("amount", ""))))
                self.table.setItem(row, 2, QTableWidgetItem(str(item.get("date", ""))))
                self.table.setItem(row, 3, QTableWidgetItem(str(item.get("risk", ""))))
                self.table.setItem(row, 4, QTableWidgetItem(str(item.get("category", ""))))

            # גרף עוגה לפי קטגוריות
            res2 = requests.get("http://localhost:8000/invest/summary/")
            summary = res2.json().get("summary", {})

            series = QPieSeries()
            for category, count in summary.items():
                series.append(category, count)

            pie_chart = QChart()
            pie_chart.addSeries(series)
            pie_chart.setTitle("התפלגות לפי קטגוריות השקעה")
            pie_chart_view = QChartView(pie_chart)
            pie_chart_view.setRenderHint(QPainter.Antialiasing)

            # גרף עמודות לפי סיכון
            res3 = requests.get("http://localhost:8000/invest/risk-summary/")
            risk_data = res3.json().get("summary", {})

            risk_set = QBarSet("מספר השקעות")
            risk_set.append([
                risk_data.get("low", 0),
                risk_data.get("medium", 0),
                risk_data.get("high", 0)
            ])

            bar_series = QBarSeries()
            bar_series.append(risk_set)

            bar_chart = QChart()
            bar_chart.addSeries(bar_series)
            bar_chart.setTitle("התפלגות לפי רמת סיכון")
            axis = QBarCategoryAxis()
            axis.append(["נמוכה", "בינונית", "גבוהה"])
            bar_chart.createDefaultAxes()
            bar_chart.setAxisX(axis, bar_series)

            bar_chart_view = QChartView(bar_chart)
            bar_chart_view.setRenderHint(QPainter.Antialiasing)

            # הוספת שני הגרפים לפריסה אופקית
            self.graphs_layout.addWidget(pie_chart_view)
            self.graphs_layout.addWidget(bar_chart_view)

        except Exception as e:
            print("שגיאה בטעינת הנתונים:", str(e))
