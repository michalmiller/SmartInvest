import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QWidget, QVBoxLayout, QLabel
)
from AIchatWidget import AIChatWidget 
from invest_input_tab import InvestInputTab
from investments_tab import InvestmentsTab
from search_tab import SearchTab


class SmartInvestApp(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"SmartInvest – שלום {self.user['full_name']}")
        self.setGeometry(100, 100, 1000, 700)

        tabs = QTabWidget()
        tabs.addTab(self.investments_tab(), "📊 השקעות נוכחיות")
        tabs.addTab(self.input_tab(), "➕ הוספת השקעה")
        tabs.addTab(self.ai_tab(), "🤖 יועץ AI")
        tabs.addTab(self.search_tab(), "🔍 חיפוש נכסים")
        self.setCentralWidget(tabs)

    def investments_tab(self):
        return InvestmentsTab()

    def input_tab(self):
        return InvestInputTab()

    def ai_tab(self):
        return AIChatWidget()

    def search_tab(self):
        return SearchTab()



    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartInvestApp()
    window.show()
    sys.exit(app.exec())
