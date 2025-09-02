import sys
from PySide6.QtWidgets import QApplication
from login_window import LoginWindow
from app_main import AppMain 
def main():
    print("🚀 התחלת main()")
    app = QApplication(sys.argv)
    main_window = None

    def open_main_app(user):
            print(f"✅ open_main_app - {user}")
            global main_window
            main_window = AppMain(user)
            main_window.show()


    login = LoginWindow(on_login_success=open_main_app)
    print("🎬 מציגה את LoginWindow")

    login.show()
    
    try:
        with open("modern.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Failed to load stylesheet: {e}")
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except Exception:
            pass


    sys.exit(app.exec())
if __name__ == "__main__":
    main()
