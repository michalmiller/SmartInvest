# app_main.py
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from AIchatWidget import AIchatWidget

from invest_input_tab import InvestInputTab
from investments_tab import InvestmentsTab
from search_tab import SearchTab

class AppMain(QWidget):
    def __init__(self, user=None):   # ← היה: def __init__(self):
        super().__init__()
        self.user = user

        # כותרת חלון עם שם המשתמש אם קיים
        display_name = ""
        if isinstance(user, dict):
            display_name = user.get("full_name") or user.get("username") or ""
        title = "SmartInvest" if not display_name else f"SmartInvest – שלום, {display_name}"
        self.setWindowTitle(title)

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

        # אם הגדרת קודם רענון אוטומטי אחרי שמירה:
        try:
            self.input_tab.investment_saved.connect(self.list_tab.refresh_data)
        except Exception:
            pass
