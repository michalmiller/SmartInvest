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
from collections import Counter


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
            # טעינת נתוני השקעות מ-Somee
            res = requests.get("http://michalmiller.somee.com/portfolio.json", 
                             timeout=10)
            
            if res.status_code == 200:
                data = res.json()
                
                # וידוא שהנתונים הם רשימה
                if not isinstance(data, list):
                    data = []
                    
                # מילוי הטבלה
                self.populate_table(data)
                
                # יצירת גרפים
                self.create_charts(data)
                
            else:
                print(f"שגיאה בקריאת הנתונים: {res.status_code}")
                # טבלה ריקה במקרה של שגיאה
                self.table.setRowCount(0)
                
        except requests.exceptions.RequestException as e:
            print(f"שגיאת רשת: {str(e)}")
            self.table.setRowCount(0)
        except Exception as e:
            print(f"שגיאה בטעינת הנתונים: {str(e)}")
            self.table.setRowCount(0)

    def populate_table(self, data):
        """מילוי הטבלה עם נתוני השקעות"""
        self.table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(item.get("asset", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(f"₪{item.get('amount', 0):,.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(str(item.get("date", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.get("risk", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(str(item.get("category", ""))))

    def create_charts(self, data):
        """יצירת גרפים על בסיס הנתונים"""
        # ניקוי גרפים קיימים
        self.clear_graphs()
        
        if not data:
            return
            
        # גרף עוגה לפי קטגוריות
        self.create_category_pie_chart(data)
        
        # גרף עמודות לפי רמת סיכון
        self.create_risk_bar_chart(data)

    def create_category_pie_chart(self, data):
        """יצירת גרף עוגה לפי קטגוריות"""
        # ספירת השקעות לפי קטגוריה
        categories = [item.get("category", "אחר") for item in data]
        category_counts = Counter(categories)
        
        series = QPieSeries()
        for category, count in category_counts.items():
            series.append(f"{category} ({count})", count)

        pie_chart = QChart()
        pie_chart.addSeries(series)
        pie_chart.setTitle("התפלגות לפי קטגוריות השקעה")
        pie_chart_view = QChartView(pie_chart)
        pie_chart_view.setRenderHint(QPainter.Antialiasing)

        self.graphs_layout.addWidget(pie_chart_view)

    def create_risk_bar_chart(self, data):
        """יצירת גרף עמודות לפי רמת סיכון"""
        # ספירת השקעות לפי רמת סיכון
        risks = [item.get("risk", "medium") for item in data]
        risk_counts = Counter(risks)
        
        risk_set = QBarSet("מספר השקעות")
        risk_labels = ["low", "medium", "high"]
        risk_hebrew = ["נמוכה", "בינונית", "גבוהה"]
        
        # הוספת נתונים לגרף
        risk_values = [risk_counts.get(risk, 0) for risk in risk_labels]
        risk_set.append(risk_values)

        bar_series = QBarSeries()
        bar_series.append(risk_set)

        bar_chart = QChart()
        bar_chart.addSeries(bar_series)
        bar_chart.setTitle("התפלגות לפי רמת סיכון")
        
        # יצירת ציר קטגוריות
        axis = QBarCategoryAxis()
        axis.append(risk_hebrew)
        bar_chart.createDefaultAxes()
        bar_chart.setAxisX(axis, bar_series)

        bar_chart_view = QChartView(bar_chart)
        bar_chart_view.setRenderHint(QPainter.Antialiasing)

        self.graphs_layout.addWidget(bar_chart_view)

    def clear_graphs(self):
        """ניקוי גרפים קיימים"""
        while self.graphs_layout.count():
            child = self.graphs_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def refresh_data(self):
        """רענון הנתונים (לקריאה חיצונית)"""
        self.load_data()