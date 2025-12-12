from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QLabel, QScrollArea)
from PyQt5.QtCore import Qt
from services.library_service import LibraryService

class CatalogWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.library_service = LibraryService()
        self.setup_ui()
        self.refresh_books()

    def setup_ui(self):
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        # Content widget
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QLabel("📖 Book Catalog")
        header.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #00d9ff;
            margin-bottom: 10px;
        """)
        layout.addWidget(header)
        
        # Search Bar
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        search_label = QLabel("🔍")
        search_label.setStyleSheet("font-size: 18px;")
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Title or Author...")
        self.search_input.setMinimumHeight(40)
        self.search_input.returnPressed.connect(self.search_books)
        search_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("Search")
        search_btn.setMinimumHeight(40)
        search_btn.setMinimumWidth(120)
        search_btn.setCursor(Qt.PointingHandCursor)
        search_btn.clicked.connect(self.search_books)
        search_layout.addWidget(search_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.setMinimumHeight(40)
        clear_btn.setMinimumWidth(100)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                border: 2px solid #0f3460;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border: 2px solid #533483;
            }
        """)
        clear_btn.clicked.connect(self.clear_search)
        search_layout.addWidget(clear_btn)
        
        layout.addLayout(search_layout)
        
        # Book Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "ISBN", "Available", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setMinimumHeight(400)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        
        content.setLayout(layout)
        scroll.setWidget(content)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def clear_search(self):
        self.search_input.clear()
        self.refresh_books()

    def search_books(self):
        term = self.search_input.text()
        if term:
            books = self.library_service.search_books(term)
        else:
            books = self.library_service.get_all_books()
        self.update_table(books)

    def refresh_books(self):
        books = self.library_service.get_all_books()
        self.update_table(books)

    def update_table(self, books):
        self.table.setRowCount(len(books))
        for i, book in enumerate(books):
            # book: id, title, author, isbn, available, total
            self.table.setItem(i, 0, QTableWidgetItem(str(book[0])))
            self.table.setItem(i, 1, QTableWidgetItem(book[1]))
            self.table.setItem(i, 2, QTableWidgetItem(book[2]))
            self.table.setItem(i, 3, QTableWidgetItem(book[3]))
            
            # Availability with color coding
            available_item = QTableWidgetItem(f"{book[4]} / {book[5]}")
            if book[4] > 0:
                available_item.setForeground(Qt.green)
            else:
                available_item.setForeground(Qt.red)
            self.table.setItem(i, 4, available_item)
            
            # Borrow button with styling
            borrow_btn = QPushButton("📚 Borrow")
            borrow_btn.setCursor(Qt.PointingHandCursor)
            if book[4] > 0:
                borrow_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                    stop:0 #00d9ff, stop:1 #0099cc);
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 16px;
                        font-weight: 600;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                    stop:0 #00eeff, stop:1 #00aadd);
                    }
                """)
                borrow_btn.clicked.connect(lambda checked, b_id=book[0]: self.borrow_book(b_id))
            else:
                borrow_btn.setEnabled(False)
                borrow_btn.setText("❌ Unavailable")
                borrow_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2a2a3e;
                        color: #666666;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 16px;
                    }
                """)
                
            self.table.setCellWidget(i, 5, borrow_btn)

    def borrow_book(self, book_id):
        success, message = self.library_service.borrow_book(self.user_id, book_id)
        if success:
            QMessageBox.information(self, "✅ Success", message)
            self.refresh_books()  # Refresh catalog
            # Emit signal or notify parent to refresh loans widget if needed
        else:
            QMessageBox.warning(self, "⚠️ Error", message)
