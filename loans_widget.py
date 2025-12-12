from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox, QLabel, QHBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt
from services.library_service import LibraryService
from datetime import datetime

class LoansWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.library_service = LibraryService()
        self.setup_ui()
        self.refresh_loans()

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
        header_layout = QHBoxLayout()
        header = QLabel("📚 My Active Loans")
        header.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #00d9ff;
            margin-bottom: 10px;
        """)
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setMinimumHeight(35)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_loans)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Loans table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Loan ID", "Book", "Borrowed Date", "Due Date", "Action"])
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

    def refresh_loans(self):
        loans = self.library_service.get_user_loans(self.user_id)
        self.table.setRowCount(len(loans))
        
        for i, loan in enumerate(loans):
            # loan: id, title, borrow_date, due_date
            self.table.setItem(i, 0, QTableWidgetItem(str(loan[0])))
            self.table.setItem(i, 1, QTableWidgetItem(loan[1]))
            self.table.setItem(i, 2, QTableWidgetItem(str(loan[2])))
            
            # Due date with color coding
            due_date_item = QTableWidgetItem(str(loan[3]))
            try:
                due_date = datetime.strptime(str(loan[3]), "%Y-%m-%d")
                if due_date < datetime.now():
                    due_date_item.setForeground(Qt.red)
                    due_date_item.setText(f"⚠️ {loan[3]} (OVERDUE)")
                else:
                    due_date_item.setForeground(Qt.green)
            except:
                pass
            self.table.setItem(i, 3, due_date_item)
            
            # Return button
            return_btn = QPushButton("✅ Return Book")
            return_btn.setCursor(Qt.PointingHandCursor)
            return_btn.setStyleSheet("""
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
            return_btn.clicked.connect(lambda checked, l_id=loan[0]: self.return_book(l_id))
            self.table.setCellWidget(i, 4, return_btn)

    def return_book(self, loan_id):
        success, message = self.library_service.return_book(loan_id)
        if success:
            QMessageBox.information(self, "✅ Success", message)
            self.refresh_loans()
        else:
            QMessageBox.warning(self, "⚠️ Error", message)
