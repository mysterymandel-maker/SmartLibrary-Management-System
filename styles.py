"""
Centralized stylesheet for Smart Library application
Provides modern, visually stunning UI with dark theme and gradients
"""

def get_app_stylesheet():
    """Returns the main application stylesheet with modern dark theme"""
    return """
    /* Global Application Styles */
    QWidget {
        background-color: #1a1a2e;
        color: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
    }
    
    /* Main Window */
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #1a1a2e, stop:1 #16213e);
    }
    
    /* Tab Widget */
    QTabWidget::pane {
        border: 2px solid #0f3460;
        border-radius: 8px;
        background-color: rgba(15, 52, 96, 0.3);
        padding: 10px;
    }
    
    QTabBar::tab {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #0f3460, stop:1 #1a1a2e);
        color: #b8b8b8;
        padding: 12px 24px;
        margin-right: 4px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-weight: 500;
        min-width: 100px;
    }
    
    QTabBar::tab:selected {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #e94560, stop:1 #533483);
        color: #ffffff;
        font-weight: 600;
    }
    
    QTabBar::tab:hover:!selected {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #533483, stop:1 #0f3460);
        color: #ffffff;
    }
    
    /* Push Buttons */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #e94560, stop:1 #533483);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 13px;
        min-height: 20px;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #ff5577, stop:1 #6644aa);
        transform: translateY(-2px);
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #cc3344, stop:1 #442266);
    }
    
    QPushButton:disabled {
        background: #2a2a3e;
        color: #666666;
    }
    
    /* Line Edits */
    QLineEdit {
        background-color: rgba(255, 255, 255, 0.05);
        border: 2px solid #0f3460;
        border-radius: 6px;
        padding: 10px 15px;
        color: #ffffff;
        font-size: 13px;
        selection-background-color: #e94560;
    }
    
    QLineEdit:focus {
        border: 2px solid #e94560;
        background-color: rgba(255, 255, 255, 0.08);
    }
    
    QLineEdit:hover {
        border: 2px solid #533483;
    }
    
    /* Spin Box */
    QSpinBox {
        background-color: rgba(255, 255, 255, 0.05);
        border: 2px solid #0f3460;
        border-radius: 6px;
        padding: 8px 12px;
        color: #ffffff;
        font-size: 13px;
    }
    
    QSpinBox:focus {
        border: 2px solid #e94560;
    }
    
    QSpinBox::up-button, QSpinBox::down-button {
        background-color: #533483;
        border: none;
        border-radius: 3px;
        width: 20px;
    }
    
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {
        background-color: #e94560;
    }
    
    /* Table Widget */
    QTableWidget {
        background-color: rgba(15, 52, 96, 0.2);
        alternate-background-color: rgba(15, 52, 96, 0.3);
        border: 2px solid #0f3460;
        border-radius: 8px;
        gridline-color: #0f3460;
        color: #ffffff;
        selection-background-color: #533483;
    }
    
    QTableWidget::item {
        padding: 8px;
        border: none;
    }
    
    QTableWidget::item:selected {
        background-color: #533483;
        color: #ffffff;
    }
    
    QTableWidget::item:hover {
        background-color: rgba(83, 52, 131, 0.3);
    }
    
    QHeaderView::section {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #533483, stop:1 #0f3460);
        color: #ffffff;
        padding: 12px;
        border: none;
        font-weight: 600;
        font-size: 13px;
    }
    
    QHeaderView::section:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #e94560, stop:1 #533483);
    }
    
    /* Scroll Bars */
    QScrollBar:vertical {
        background-color: rgba(15, 52, 96, 0.2);
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #533483;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #e94560;
    }
    
    QScrollBar:horizontal {
        background-color: rgba(15, 52, 96, 0.2);
        height: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #533483;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #e94560;
    }
    
    QScrollBar::add-line, QScrollBar::sub-line {
        border: none;
        background: none;
    }
    
    /* Labels */
    QLabel {
        color: #ffffff;
        background: transparent;
    }
    
    /* Group Box */
    QGroupBox {
        background-color: rgba(15, 52, 96, 0.3);
        border: 2px solid #533483;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 20px;
        font-weight: 600;
        font-size: 14px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 5px 15px;
        color: #e94560;
        background-color: transparent;
    }
    
    /* List Widget */
    QListWidget {
        background-color: rgba(15, 52, 96, 0.2);
        border: 2px solid #0f3460;
        border-radius: 8px;
        padding: 8px;
        color: #ffffff;
    }
    
    QListWidget::item {
        padding: 10px;
        border-radius: 4px;
        margin: 2px 0;
    }
    
    QListWidget::item:selected {
        background-color: #533483;
        color: #ffffff;
    }
    
    QListWidget::item:hover {
        background-color: rgba(83, 52, 131, 0.3);
    }
    
    /* Message Box */
    QMessageBox {
        background-color: #1a1a2e;
    }
    
    QMessageBox QLabel {
        color: #ffffff;
        font-size: 13px;
    }
    
    QMessageBox QPushButton {
        min-width: 80px;
    }
    """

def get_login_stylesheet():
    """Returns stylesheet specifically for login dialog"""
    return """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #1a1a2e, stop:1 #16213e);
    }
    
    QLabel {
        color: #ffffff;
        background: transparent;
    }
    
    QLineEdit {
        background-color: rgba(255, 255, 255, 0.08);
        border: 2px solid #0f3460;
        border-radius: 8px;
        padding: 12px 15px;
        color: #ffffff;
        font-size: 14px;
        selection-background-color: #e94560;
    }
    
    QLineEdit:focus {
        border: 2px solid #e94560;
        background-color: rgba(255, 255, 255, 0.12);
    }
    
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #e94560, stop:1 #533483);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 15px;
        min-height: 25px;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #ff5577, stop:1 #6644aa);
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #cc3344, stop:1 #442266);
    }
    """

def get_card_style():
    """Returns style for card-like containers"""
    return """
        background-color: rgba(255, 255, 255, 0.05);
        border: 2px solid #0f3460;
        border-radius: 12px;
        padding: 20px;
    """

def get_header_label_style():
    """Returns style for header/title labels"""
    return """
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        background: transparent;
        padding: 10px;
    """

def get_secondary_button_style():
    """Returns style for secondary/logout buttons"""
    return """
        QPushButton {
            background-color: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border: 2px solid #533483;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #533483;
            border: 2px solid #e94560;
        }
    """

def get_success_button_style():
    """Returns style for success/positive action buttons"""
    return """
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #00d9ff, stop:1 #0099cc);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #00eeff, stop:1 #00aadd);
        }
    """

def get_danger_button_style():
    """Returns style for danger/delete buttons"""
    return """
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #ff4444, stop:1 #cc0000);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #ff5555, stop:1 #dd0000);
        }
    """
