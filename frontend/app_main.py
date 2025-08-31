# app_main.py
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from AIchatWidget import AIchatWidget
from invest_input_tab import InvestInputTab
from investments_tab import InvestmentsTab
from search_tab import SearchTab

class AppMain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartInvest")

        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        layout.addWidget(tabs)

        self.ai_tab = AIchatWidget()
        self.input_tab = InvestInputTab()
        self.list_tab = InvestmentsTab()
        self.search_tab = SearchTab()

        tabs.addTab(self.ai_tab, "🤖 יועץ AI")
        tabs.addTab(self.input_tab, "➕ הוספת השקעה")
        tabs.addTab(self.list_tab, "📋 השקעות נוכחיות")
        tabs.addTab(self.search_tab, "🔍 חיפוש")

        # ← חיבור: אחרי שמירה, לרענן את טבלת ההשקעות
        self.input_tab.investment_saved.connect(self.list_tab.refresh_data)
