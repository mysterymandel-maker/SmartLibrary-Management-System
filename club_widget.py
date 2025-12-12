from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QListWidget, QGroupBox, QMessageBox, QTextEdit, QLabel, QScrollArea)
from PyQt5.QtCore import Qt
from services.club_service import ClubService

class ClubWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.club_service = ClubService()
        self.setup_ui()
        self.refresh_clubs()

    def setup_ui(self):
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        # Content widget
        content = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QLabel("📚 Book Clubs")
        header.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #533483;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(header)
        
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # Left Panel: All Clubs & Create
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        
        # Create Club
        create_group = QGroupBox("➕ Create New Club")
        create_group.setStyleSheet("""
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
        
        create_form = QVBoxLayout()
        create_form.setSpacing(12)
        create_form.setContentsMargins(15, 15, 15, 15)
        
        self.club_name_input = QLineEdit()
        self.club_name_input.setPlaceholderText("Enter club name...")
        self.club_name_input.setMinimumHeight(40)
        
        self.club_desc_input = QTextEdit()
        self.club_desc_input.setPlaceholderText("Enter club description...")
        self.club_desc_input.setMaximumHeight(80)
        
        create_btn = QPushButton("✨ Create Club")
        create_btn.setMinimumHeight(40)
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #533483, stop:1 #e94560);
                font-weight: 700;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #6644aa, stop:1 #ff5577);
            }
        """)
        create_btn.clicked.connect(self.create_club)
        
        create_form.addWidget(self.club_name_input)
        create_form.addWidget(self.club_desc_input)
        create_form.addWidget(create_btn)
        create_group.setLayout(create_form)
        left_layout.addWidget(create_group)
        
        # All Clubs List
        list_group = QGroupBox("🌐 Available Clubs")
        list_group.setStyleSheet("""
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
        
        list_layout = QVBoxLayout()
        list_layout.setSpacing(10)
        list_layout.setContentsMargins(15, 15, 15, 15)
        
        self.clubs_list = QListWidget()
        self.clubs_list.setMinimumHeight(250)
        
        join_btn = QPushButton("➕ Join Selected Club")
        join_btn.setMinimumHeight(40)
        join_btn.setCursor(Qt.PointingHandCursor)
        join_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #00d9ff, stop:1 #0099cc);
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #00eeff, stop:1 #00aadd);
            }
        """)
        join_btn.clicked.connect(self.join_club)
        
        delete_club_btn = QPushButton("🗑️ Delete Selected Club")
        delete_club_btn.setMinimumHeight(40)
        delete_club_btn.setCursor(Qt.PointingHandCursor)
        delete_club_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #ff4444, stop:1 #cc0000);
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #ff5555, stop:1 #dd0000);
            }
        """)
        delete_club_btn.clicked.connect(self.delete_club)
        
        list_layout.addWidget(self.clubs_list)
        list_layout.addWidget(join_btn)
        list_layout.addWidget(delete_club_btn)
        list_group.setLayout(list_layout)
        left_layout.addWidget(list_group)
        
        layout.addLayout(left_layout)
        
        # Right Panel: My Clubs
        right_group = QGroupBox("⭐ My Clubs")
        right_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: 600;
                color: #e94560;
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
        
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(15, 15, 15, 15)
        
        self.my_clubs_list = QListWidget()
        self.my_clubs_list.setMinimumHeight(400)
        self.my_clubs_list.setStyleSheet("""
            QListWidget::item {
                padding: 10px;
                border-left: 4px solid #e94560;
                margin: 4px 0;
            }
        """)
        right_layout.addWidget(self.my_clubs_list)
        right_group.setLayout(right_layout)
        
        layout.addWidget(right_group)
        
        main_layout.addLayout(layout)
        
        content.setLayout(main_layout)
        scroll.setWidget(content)
        
        # Final layout
        final_layout = QVBoxLayout()
        final_layout.setContentsMargins(0, 0, 0, 0)
        final_layout.addWidget(scroll)
        self.setLayout(final_layout)

    def create_club(self):
        name = self.club_name_input.text().strip()
        desc = self.club_desc_input.toPlainText().strip()
        
        if not name:
            QMessageBox.warning(self, "⚠️ Validation Error", "Club name is required!")
            return
            
        success, res = self.club_service.create_club(name, desc, self.user_id)
        if success:
            QMessageBox.information(self, "✅ Success", f"Club '{name}' created successfully!")
            self.refresh_clubs()
            self.club_name_input.clear()
            self.club_desc_input.clear()
        else:
            QMessageBox.warning(self, "⚠️ Error", res)

    def join_club(self):
        current_item = self.clubs_list.currentItem()
        if not current_item:
             QMessageBox.warning(self, "⚠️ Error", "Please select a club to join")
             return
             
        # Extract ID from item text (simple hack: "ID: Name - Desc")
        text = current_item.text()
        try:
            club_id = int(text.split(":")[0])
        except:
            QMessageBox.warning(self, "⚠️ Error", "Invalid club selection")
            return
        
        success, msg = self.club_service.join_club(club_id, self.user_id)
        if success:
            QMessageBox.information(self, "✅ Success", msg)
            self.refresh_clubs()
        else:
             QMessageBox.warning(self, "⚠️ Error", msg)

    def refresh_clubs(self):
        self.clubs_list.clear()
        self.my_clubs_list.clear()
        
        all_clubs = self.club_service.get_all_clubs()
        for club in all_clubs:
            # club: id, name, desc, owner_name
            self.clubs_list.addItem(f"{club[0]}: 📚 {club[1]} - Created by {club[3]}")
            
        my_clubs = self.club_service.get_my_clubs(self.user_id)
        if my_clubs:
            for club in my_clubs:
                self.my_clubs_list.addItem(f"📖 {club[1]}")
        else:
            self.my_clubs_list.addItem("You haven't joined any clubs yet")
    
    def delete_club(self):
        """Delete a club with confirmation"""
        current_item = self.clubs_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "⚠️ Error", "Please select a club to delete")
            return
        
        # Extract club ID and name from item text
        text = current_item.text()
        try:
            club_id = int(text.split(":")[0])
            club_name = text.split("📚")[1].split(" - ")[0].strip()
        except:
            QMessageBox.warning(self, "⚠️ Error", "Invalid club selection")
            return
        
        # Confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the club '{club_name}'?\n\nAll memberships will be removed.\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, msg = self.club_service.delete_club(club_id, self.user_id)
            if success:
                QMessageBox.information(self, "✅ Success", msg)
                self.refresh_clubs()
            else:
                QMessageBox.warning(self, "⚠️ Error", msg)

