DARK_STYLE = """
/* Fuentes Globales */
QWidget {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 14px;
    color: #E5E5EA; 
}

/* Evitar el rectangulo raro de focus */
* {
    outline: none;
}

QMainWindow, QStackedWidget, QDialog {
    background-color: #000000; 
}

QFrame#Card, QFrame#Sidebar {
    background-color: #1A1A1C; 
    border-radius: 12px;
    border: 1px solid #2C2C2E;
}

QLabel#Title {
    font-size: 24px;
    font-weight: bold;
    color: #FFFFFF;
}
QLabel#Subtitle {
    font-size: 16px;
    font-weight: bold;
    color: #E5E5EA;
}
QLabel#CardValue {
    font-size: 26px;
    font-weight: bold;
    color: #FFFFFF;
}
QLabel#CardDesc {
    font-size: 13px;
    color: #8E8E93; 
    text-transform: uppercase;
}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #2C2C2E;
    color: #FFFFFF;
    border: 1px solid #3A3A3D;
    padding: 10px 14px;
    border-radius: 8px;
    selection-background-color: #0A84FF;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #0A84FF;
    background-color: #1A1A1C;
}

QComboBox QAbstractItemView {
    background-color: #1A1A1C;
    color: #FFFFFF;
    border: 1px solid #3A3A3D;
    selection-background-color: #2C2C2E;
    outline: none;
}

QPushButton {
    background-color: #2C2C2E;
    color: #FFFFFF;
    border: 1px solid #3A3A3D;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: bold;
    outline: none;
}
QPushButton:hover { background-color: #3A3A3D; }
QPushButton:pressed { background-color: #1A1A1C; }

QPushButton[class="sidebar_btn"] {
    background-color: transparent;
    border: none;
    text-align: left;
    padding: 12px 18px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 500;
    color: #8E8E93;
    outline: none;
}
QPushButton[class="sidebar_btn"]:hover {
    background-color: #2C2C2E;
    color: #FFFFFF;
}
QPushButton[class="sidebar_btn_active"] {
    background-color: #0A84FF; 
    color: #FFFFFF;
    border: none;
    text-align: left;
    padding: 12px 18px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: bold;
    outline: none;
}

QPushButton[class="primary"] { background-color: #0A84FF; color: #FFFFFF; border: none; }
QPushButton[class="primary"]:hover { background-color: #0076E5; }

QPushButton[class="success"] { background-color: #32D74B; color: #FFFFFF; border: none; }
QPushButton[class="success"]:hover { background-color: #28B93D; }

QPushButton[class="danger"] { background-color: #FF453A; color: #FFFFFF; border: none; }
QPushButton[class="danger"]:hover { background-color: #E0352A; }

QTableWidget {
    background-color: #1A1A1C;
    border: none;
    gridline-color: transparent;
    selection-background-color: #2C2C2E;
    selection-color: #FFFFFF;
    color: #E5E5EA;
    outline: none;
}
QTableWidget::item { border-bottom: 1px solid #2C2C2E; }
QTableWidget::item:selected { background-color: #2C2C2E; }

QHeaderView::section {
    background-color: transparent;
    color: #8E8E93;
    padding: 12px 6px;
    border: none;
    border-bottom: 2px solid #3A3A3D;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 12px;
}
QHeaderView { background-color: #1A1A1C; }

QScrollBar:vertical, QScrollBar:horizontal {
    border: none;
    background-color: transparent;
    width: 6px; height: 6px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background-color: #3A3A3D;
    border-radius: 3px;
}
QScrollBar::add-line, QScrollBar::sub-line { width: 0px; height: 0px; margin: 0px; padding: 0px; }

QMessageBox { background-color: #1A1A1C; }
QMessageBox QLabel { color: #FFFFFF; }
"""

LIGHT_STYLE = """
/* Fuentes Globales */
QWidget {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 14px;
    color: #1C1C1E; 
}

/* Evitar el rectangulo raro de focus */
* {
    outline: none;
}

QMainWindow, QStackedWidget, QDialog {
    background-color: #F2F2F7; /* Gris claro de fondo */
}

QFrame#Card, QFrame#Sidebar {
    background-color: #FFFFFF; /* Blanco puro para tarjetas */
    border-radius: 12px;
    border: 1px solid #E5E5EA;
}

QLabel#Title {
    font-size: 24px;
    font-weight: bold;
    color: #000000;
}
QLabel#Subtitle {
    font-size: 16px;
    font-weight: bold;
    color: #1C1C1E;
}
QLabel#CardValue {
    font-size: 26px;
    font-weight: bold;
    color: #000000;
}
QLabel#CardDesc {
    font-size: 13px;
    color: #8E8E93; 
    text-transform: uppercase;
}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #FFFFFF;
    color: #1C1C1E;
    border: 1px solid #C7C7CC;
    padding: 10px 14px;
    border-radius: 8px;
    selection-background-color: #0A84FF;
    selection-color: #FFFFFF;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #0A84FF;
    background-color: #FFFFFF;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    color: #1C1C1E;
    border: 1px solid #C7C7CC;
    selection-background-color: #F2F2F7;
    outline: none;
}

QPushButton {
    background-color: #E5E5EA;
    color: #1C1C1E;
    border: 1px solid #D1D1D6;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: bold;
    outline: none;
}
QPushButton:hover { background-color: #D1D1D6; }
QPushButton:pressed { background-color: #C7C7CC; }

QPushButton[class="sidebar_btn"] {
    background-color: transparent;
    border: none;
    text-align: left;
    padding: 12px 18px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 500;
    color: #8E8E93;
    outline: none;
}
QPushButton[class="sidebar_btn"]:hover {
    background-color: #F2F2F7;
    color: #1C1C1E;
}
QPushButton[class="sidebar_btn_active"] {
    background-color: #0A84FF; 
    color: #FFFFFF;
    border: none;
    text-align: left;
    padding: 12px 18px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: bold;
    outline: none;
}

QPushButton[class="primary"] { background-color: #0A84FF; color: #FFFFFF; border: none; }
QPushButton[class="primary"]:hover { background-color: #0076E5; }

QPushButton[class="success"] { background-color: #34C759; color: #FFFFFF; border: none; }
QPushButton[class="success"]:hover { background-color: #28B93D; }

QPushButton[class="danger"] { background-color: #FF3B30; color: #FFFFFF; border: none; }
QPushButton[class="danger"]:hover { background-color: #E0352A; }

QTableWidget {
    background-color: #FFFFFF;
    border: none;
    gridline-color: transparent;
    selection-background-color: #F2F2F7;
    selection-color: #1C1C1E;
    color: #1C1C1E;
    outline: none;
}
QTableWidget::item { border-bottom: 1px solid #E5E5EA; }
QTableWidget::item:selected { background-color: #F2F2F7; }

QHeaderView::section {
    background-color: transparent;
    color: #8E8E93;
    padding: 12px 6px;
    border: none;
    border-bottom: 2px solid #C7C7CC;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 12px;
}
QHeaderView { background-color: #FFFFFF; }

QScrollBar:vertical, QScrollBar:horizontal {
    border: none;
    background-color: transparent;
    width: 6px; height: 6px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background-color: #C7C7CC;
    border-radius: 3px;
}
QScrollBar::add-line, QScrollBar::sub-line { width: 0px; height: 0px; margin: 0px; padding: 0px; }

QMessageBox { background-color: #FFFFFF; }
QMessageBox QLabel { color: #1C1C1E; }
"""
