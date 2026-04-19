from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QPushButton, QLabel, QStackedWidget,
    QFrame
)
from PyQt6.QtCore import Qt
from config import APP_NAME
from ui.inventory_ui import InventoryUI
from ui.sales_ui import SalesUI
from ui.dashboard_ui import DashboardUI
from ui.utils import apply_shadow 
from theme import DARK_STYLE, LIGHT_STYLE
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True
        self.setWindowTitle("Sistema de Gestión de Inventario")
        self.setMinimumSize(1200, 750)

        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== SIDEBAR =====
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(240)
        
        apply_shadow(self.sidebar, blur_radius=30, x_offset=10, y_offset=0, color_alpha=120)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)
        sidebar_layout.setSpacing(15)

        title = QLabel("Inventario Pro")
        title.setObjectName("Title")

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_inventory = QPushButton("Inventario")
        self.btn_sales = QPushButton("Caja y Ventas")

        self.sidebar_btns = (self.btn_dashboard, self.btn_inventory, self.btn_sales)

        for btn in self.sidebar_btns:
            btn.setProperty("class", "sidebar_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_dashboard.setProperty("class", "sidebar_btn_active")

        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(40)
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_inventory)
        sidebar_layout.addWidget(self.btn_sales)
        self.btn_sales.clicked.connect(lambda: self.switch_page(2, self.sales_page))

        sidebar_layout.addStretch()

        self.btn_theme = QPushButton("☀️ Modo Claro")
        self.btn_theme.setProperty("class", "sidebar_btn")
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.clicked.connect(self.toggle_theme)
        sidebar_layout.addWidget(self.btn_theme)

        owner = QLabel("Sistema de Gestión\nVersión 1.0")
        owner.setStyleSheet("font-size: 11px; color: #8E8E93;")
        owner.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sidebar_layout.addWidget(owner)

        # ===== MAIN CONTENT =====
        content_wrapper = QWidget()
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(40, 40, 40, 40)

        # ===== PÁGINAS =====
        self.pages = QStackedWidget()
        self.dashboard_page = DashboardUI()
        self.inventory_page = InventoryUI()
        self.sales_page = SalesUI()

        # 🔥 ACTUALIZACIONES EN TIEMPO REAL
        self.sales_page.venta_realizada.connect(
            self.dashboard_page.load_dashboard
        )
        self.sales_page.venta_realizada.connect(
            self.inventory_page.load_productos
        )

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.inventory_page)
        self.pages.addWidget(self.sales_page)

        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0, self.dashboard_page))
        self.btn_inventory.clicked.connect(lambda: self.switch_page(1, self.inventory_page))
        self.btn_sales.clicked.connect(lambda: self.switch_page(2, self.sales_page))

        content_layout.addWidget(self.pages)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_wrapper, 1)

        self.setCentralWidget(container)
        self.pages.setCurrentWidget(self.dashboard_page)

    def showEvent(self, event):
        super().showEvent(event)
        # Hack para fixear el Bleed Ghosting del DropShadow 
        # recargando iterativamente el QSS cuando las geometrías existen:
        QTimer.singleShot(50, lambda: QApplication.instance().setStyleSheet(DARK_STYLE if self.is_dark_theme else LIGHT_STYLE))

    def switch_page(self, index, page):
        self.pages.setCurrentWidget(page)
        for i, btn in enumerate(self.sidebar_btns):
            if i == index:
                btn.setProperty("class", "sidebar_btn_active")
            else:
                btn.setProperty("class", "sidebar_btn")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        app = QApplication.instance()
        if self.is_dark_theme:
            app.setStyleSheet(DARK_STYLE)
            self.btn_theme.setText("☀️ Modo Claro")
        else:
            app.setStyleSheet(LIGHT_STYLE)
            self.btn_theme.setText("🌙 Modo Oscuro")
        
        # Refrescar tabla en ventana actual si se puede, no critico.
        self.dashboard_page.load_dashboard()
        self.inventory_page.load_productos()
        self.sales_page.load_ventas()

