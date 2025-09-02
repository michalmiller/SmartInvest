import sys
from PySide6.QtWidgets import QApplication
from login_window import LoginWindow
from app_main import AppMain 
def main():
    app = QApplication(sys.argv)
    main_window = None

    def open_main_app(user):
            global main_window
            main_window = AppMain(user)
            main_window.show()


    login = LoginWindow(on_login_success=open_main_app)
    login.show()
    with open("modern.qss", "r", encoding="utf-8") as f:
         app.setStyleSheet(f.read())
         try:
              from dotenv import load_dotenv
              load_dotenv()
         except Exception:
          pass


    sys.exit(app.exec())
if __name__ == "__main__":
    main()
