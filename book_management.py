from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QMessageBox, QSpinBox, QHeaderView, QGroupBox, QFormLayout, QScrollArea)
from PyQt5.QtCore import Qt
from services.library_service import LibraryService

class BookManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
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
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QLabel("📚 Book Management")
        header.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #e94560;
            margin-bottom: 10px;
        """)
        layout.addWidget(header)
        
        # Add Book Form (Card Style)
        form_group = QGroupBox("➕ Add New Book")
        form_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
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
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title input
        title_label = QLabel("Title:")
        title_label.setStyleSheet("font-weight: 600; color: #ffffff;")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter book title")
        self.title_input.setMinimumHeight(35)
        
        # Author input
        author_label = QLabel("Author:")
        author_label.setStyleSheet("font-weight: 600; color: #ffffff;")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Enter author name")
        self.author_input.setMinimumHeight(35)
        
        # ISBN input
        isbn_label = QLabel("ISBN:")
        isbn_label.setStyleSheet("font-weight: 600; color: #ffffff;")
        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("Enter ISBN (optional)")
        self.isbn_input.setMinimumHeight(35)
        
        # Copies input
        copies_label = QLabel("Copies:")
        copies_label.setStyleSheet("font-weight: 600; color: #ffffff;")
        self.copies_input = QSpinBox()
        self.copies_input.setRange(1, 100)
        self.copies_input.setValue(1)
        self.copies_input.setMinimumHeight(35)
        
        form_layout.addRow(title_label, self.title_input)
        form_layout.addRow(author_label, self.author_input)
        form_layout.addRow(isbn_label, self.isbn_input)
        form_layout.addRow(copies_label, self.copies_input)
        
        # Add button
        add_btn = QPushButton("➕ Add Book to Library")
        add_btn.setMinimumHeight(45)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #00d9ff, stop:1 #0099cc);
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #00eeff, stop:1 #00aadd);
            }
        """)
        add_btn.clicked.connect(self.add_book)
        form_layout.addRow("", add_btn)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Book List Header
        list_header_layout = QHBoxLayout()
        list_header = QLabel("📖 Current Library Collection")
        list_header.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
            margin-top: 10px;
        """)
        list_header_layout.addWidget(list_header)
        list_header_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setMinimumHeight(35)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_books)
        list_header_layout.addWidget(refresh_btn)
        
        layout.addLayout(list_header_layout)
        
        # Book List Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # Added one more column for delete
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "ISBN", "Available/Total", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setMinimumHeight(300)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        
        content.setLayout(layout)
        scroll.setWidget(content)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        isbn = self.isbn_input.text().strip()
        copies = self.copies_input.value()
        
        if not title or not author:
            QMessageBox.warning(self, "⚠️ Validation Error", "Title and Author are required fields!")
            return
            
        try:
            res = self.library_service.add_book(title, author, isbn, copies)
            if res:
                QMessageBox.information(self, "✅ Success", f"Book '{title}' added successfully with {copies} copies!")
                self.title_input.clear()
                self.author_input.clear()
                self.isbn_input.clear()
                self.copies_input.setValue(1)
                self.refresh_books()
            else:
                QMessageBox.warning(self, "⚠️ Error", "Failed to add book. Please try again.")
        except Exception as e:
            QMessageBox.critical(self, "❌ Error", f"An error occurred:\n{str(e)}")

    def refresh_books(self):
        books = self.library_service.get_all_books()
        self.table.setRowCount(len(books))
        for i, book in enumerate(books):
            # book: id, title, author, isbn, available, total
            self.table.setItem(i, 0, QTableWidgetItem(str(book[0])))
            self.table.setItem(i, 1, QTableWidgetItem(book[1]))
            self.table.setItem(i, 2, QTableWidgetItem(book[2]))
            self.table.setItem(i, 3, QTableWidgetItem(book[3]))
            
            # Availability with color coding
            availability = f"{book[4]}/{book[5]}"
            avail_item = QTableWidgetItem(availability)
            if book[4] == 0:
                avail_item.setForeground(Qt.red)
            elif book[4] < book[5] / 2:
                avail_item.setForeground(Qt.yellow)
            else:
                avail_item.setForeground(Qt.green)
            self.table.setItem(i, 4, avail_item)
            
            # Delete button
            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #ff4444, stop:1 #cc0000);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #ff5555, stop:1 #dd0000);
                }
            """)
            delete_btn.clicked.connect(lambda checked, b_id=book[0], b_title=book[1]: self.delete_book(b_id, b_title))
            self.table.setCellWidget(i, 5, delete_btn)
    
    def delete_book(self, book_id, book_title):
        """Delete a book with confirmation"""
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete '{book_title}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.library_service.delete_book(book_id)
            if success:
                QMessageBox.information(self, "✅ Success", message)
                self.refresh_books()
            else:
                QMessageBox.warning(self, "⚠️ Error", message)
