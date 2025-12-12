from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QFormLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from services.auth_service import AuthService
from ui.styles import get_login_stylesheet

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Library - Login")
        self.setFixedSize(450, 500)
        self.auth_service = AuthService()
        self.user_data = None
        self.setup_ui()
        self.setStyleSheet(get_login_stylesheet())

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Welcome Header
        welcome_label = QLabel("📚 Smart Library")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #e94560;
            margin-bottom: 10px;
        """)
        layout.addWidget(welcome_label)
        
        subtitle = QLabel("Welcome Back!")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: #b8b8b8;
            margin-bottom: 20px;
        """)
        layout.addWidget(subtitle)
        
        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Login Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        
        # Username
        username_label = QLabel("Username")
        username_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #ffffff;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(45)
        
        # Password
        password_label = QLabel("Password")
        password_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #ffffff;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setMinimumHeight(45)
        self.password_input.returnPressed.connect(self.handle_login)
        
        form_layout.addRow(username_label, self.username_input)
        form_layout.addRow(password_label, self.password_input)
        
        layout.addLayout(form_layout)
        
        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Login Button
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.setMinimumHeight(50)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        
        # Info text
        info_label = QLabel("Default credentials:\nLibrarian: admin/admin123\nMember: john/pass123")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("""
            font-size: 11px;
            color: #666666;
            margin-top: 20px;
            line-height: 1.5;
        """)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        user = self.auth_service.login(username, password)
        if user:
            self.user_data = user
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.\nPlease try again.")

    def get_user_data(self):
        return self.user_data
