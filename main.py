import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QFont
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow
from ui.styles import get_app_stylesheet
from database.init_db import init_db

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Apply modern stylesheet
    app.setStyleSheet(get_app_stylesheet())
    
    # Set modern font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Ensure DB is initialized
    init_db()
    
    login = LoginDialog()
    if login.exec_() == LoginDialog.Accepted:
        user_data = login.get_user_data()
        window = MainWindow(user_data)
        window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
