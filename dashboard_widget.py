from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QGroupBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt
from services.library_service import LibraryService

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.library_service = LibraryService()
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        # Content widget
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QLabel("📊 Librarian Dashboard")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #e94560;
            margin-bottom: 10px;
        """)
        layout.addWidget(header)
        
        # Statistics Cards Row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(15)
        
        # Card 1: Total Books
        self.total_books_card = self.create_stat_card("📚", "Total Books", "0", "#e94560")
        stats_row.addWidget(self.total_books_card)
        
        # Card 2: Active Loans
        self.active_loans_card = self.create_stat_card("📖", "Active Loans", "0", "#00d9ff")
        stats_row.addWidget(self.active_loans_card)
        
        # Card 3: Total Members
        self.total_members_card = self.create_stat_card("👥", "Total Members", "0", "#533483")
        stats_row.addWidget(self.total_members_card)
        
        layout.addLayout(stats_row)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #533483;
            border: none;
            height: 2px;
            margin: 10px 0;
        """)
        layout.addWidget(separator)
        
        # Most Borrowed Books Section
        most_borrowed_group = QGroupBox("🏆 Most Borrowed Books")
        most_borrowed_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: 600;
                color: #00d9ff;
                border: 2px solid #533483;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 25px;
                background-color: rgba(15, 52, 96, 0.2);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 15px;
            }
        """)
        
        most_borrowed_layout = QVBoxLayout()
        most_borrowed_layout.setContentsMargins(15, 15, 15, 15)
        
        self.stats_list = QListWidget()
        self.stats_list.setMinimumHeight(250)
        self.stats_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 12px;
                margin: 4px 0;
                border-left: 4px solid #e94560;
            }
        """)
        most_borrowed_layout.addWidget(self.stats_list)
        
        most_borrowed_group.setLayout(most_borrowed_layout)
        layout.addWidget(most_borrowed_group)
        
        layout.addStretch()
        
        content.setLayout(layout)
        scroll.setWidget(content)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def create_stat_card(self, icon, title, value, color):
        """Create a modern statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(15, 52, 96, 0.4), 
                                            stop:1 rgba(26, 26, 46, 0.4));
                border: 2px solid {color};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        
        card_layout = QVBoxLayout()
        card_layout.setSpacing(10)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 36px;
            color: {color};
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("value_label")
        value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {color};
        """)
        value_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #b8b8b8;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)
        
        card.setLayout(card_layout)
        return card

    def refresh_data(self):
        stats = self.library_service.get_dashboard_stats()
        
        # Update stat cards
        # Note: You may need to add methods to get these stats from library_service
        # For now, we'll just update the most borrowed list
        
        self.stats_list.clear()
        
        if stats['most_borrowed']:
            for i, (book_title, count) in enumerate(stats['most_borrowed'], 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                self.stats_list.addItem(f"{medal}  {book_title} - Borrowed {count} times")
        else:
            self.stats_list.addItem("No borrowing activity yet")
        
        # Update card values (you can extend this with actual data)
        # For demonstration, showing placeholder logic
        try:
            all_books = self.library_service.get_all_books()
            total_books = len(all_books) if all_books else 0
            
            # Find and update the value label in total_books_card
            value_label = self.total_books_card.findChild(QLabel, "value_label")
            if value_label:
                value_label.setText(str(total_books))
        except:
            pass
