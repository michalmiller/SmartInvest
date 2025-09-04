from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from AIchatWidget import AIchatWidget
from invest_input_tab import InvestInputTab
from investments_tab import InvestmentsTab
from search_tab import SearchTab

class AppMain(QWidget):
    def __init__(self, user=None):
        super().__init__()
        self.user = user

        # כותרת חלון עם שם המשתמש אם קיים
        display_name = ""
        if isinstance(user, dict):
            display_name = user.get("full_name") or user.get("username") or ""
        title = "SmartInvest" if not display_name else f"SmartInvest – שלום, {display_name}"
        self.setWindowTitle(title)

        # יצירת layout ראשי אופקי
        main_layout = QVBoxLayout(self)

        # שורת לוגו בראש החלון
        logo_row = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(QPixmap("logo_temp.jpg"))
        logo.setFixedSize(60, 60)
        logo.setScaledContents(True)
        logo.setObjectName("AppLogo")
        logo_row.addWidget(logo, alignment=Qt.AlignLeft | Qt.AlignTop)
        logo_row.addStretch()
        main_layout.addLayout(logo_row)
        # שאר התוכן
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        self.ai_tab = AIchatWidget()
        self.input_tab = InvestInputTab()
        self.list_tab = InvestmentsTab()
        self.search_tab = SearchTab()

        tabs.addTab(self.ai_tab, "🤖 יועץ AI")
        tabs.addTab(self.input_tab, "➕ הוספת השקעה")
        tabs.addTab(self.list_tab, "📋 השקעות נוכחיות")
        tabs.addTab(self.search_tab, "🔍 חיפוש")

        try:
            self.input_tab.investment_saved.connect(self.list_tab.refresh_data)
        except Exception:
            pass