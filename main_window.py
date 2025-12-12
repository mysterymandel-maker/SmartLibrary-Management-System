from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget, 
                             QLabel, QHBoxLayout, QPushButton, QFrame)
from PyQt5.QtCore import Qt
from ui.styles import get_header_label_style, get_secondary_button_style

class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle(f"Smart Library - {user_data['username']} ({user_data['role'].title()})")
        self.resize(1200, 800)
        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        main_widget.setLayout(layout)
        
        # Header
        header = QHBoxLayout()
        header.setSpacing(20)
        
        # Title with icon
        title = QLabel("📚 Smart Library")
        title.setStyleSheet(get_header_label_style())
        header.addWidget(title)
        
        header.addStretch()
        
        # User info with role badge
        role_color = "#e94560" if self.user_data['role'] == 'librarian' else "#00d9ff"
        user_info = QLabel(f"👤 {self.user_data['username']}")
        user_info.setStyleSheet(f"""
            font-size: 15px;
            font-weight: 600;
            color: {role_color};
            background: transparent;
            padding: 8px 15px;
            border: 2px solid {role_color};
            border-radius: 20px;
        """)
        header.addWidget(user_info)
        
        # Role badge
        role_badge = QLabel(self.user_data['role'].upper())
        role_badge.setStyleSheet(f"""
            font-size: 11px;
            font-weight: 700;
            color: #ffffff;
            background-color: {role_color};
            padding: 6px 12px;
            border-radius: 12px;
        """)
        header.addWidget(role_badge)
        
        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet(get_secondary_button_style())
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.close)
        header.addWidget(logout_btn)
        
        layout.addLayout(header)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #533483;
            border: none;
            height: 2px;
            margin: 10px 0;
        """)
        layout.addWidget(separator)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setContentsMargins(0, 10, 0, 0)
        layout.addWidget(self.tabs)
        
        self.setup_tabs()

    def setup_tabs(self):
        role = self.user_data['role']
        user_id = self.user_data['id']
        
        from ui.dashboard_widget import DashboardWidget
        from ui.book_management import BookManagementWidget
        from ui.catalog_widget import CatalogWidget
        from ui.loans_widget import LoansWidget
        from ui.club_widget import ClubWidget

        if role == 'librarian':
            self.dashboard_widget = DashboardWidget()
            self.book_mgmt_widget = BookManagementWidget()
            self.club_widget_lib = ClubWidget(user_id)
            
            self.add_tab(self.dashboard_widget, "Dashboard")
            self.add_tab(self.book_mgmt_widget, "Manage Books")
            self.add_tab(self.club_widget_lib, "Manage Clubs")
        
        elif role == 'member':
            self.catalog_widget = CatalogWidget(user_id)
            self.loans_widget = LoansWidget(user_id)
            self.club_widget_member = ClubWidget(user_id)
            
            self.add_tab(self.catalog_widget, "Book Catalog")
            self.add_tab(self.loans_widget, "My Loans")
            self.add_tab(self.club_widget_member, "Book Clubs")
        
        # Connect tab change to refresh data
        self.tabs.currentChanged.connect(self.on_tab_changed)

    def add_tab(self, widget, title):
        self.tabs.addTab(widget, title)
    
    def on_tab_changed(self, index):
        """Refresh widget data when tab is changed"""
        current_widget = self.tabs.widget(index)
        
        # Refresh data for widgets that have a refresh method
        if hasattr(current_widget, 'refresh_loans'):
            current_widget.refresh_loans()
        elif hasattr(current_widget, 'refresh_books'):
            current_widget.refresh_books()
        elif hasattr(current_widget, 'refresh_clubs'):
            current_widget.refresh_clubs()
        elif hasattr(current_widget, 'refresh_data'):
            current_widget.refresh_data()
