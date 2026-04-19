from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem,
    QComboBox, QFrame, QGridLayout, QHeaderView
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from database import Database
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from ui.utils import apply_shadow


class DashboardUI(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(25)

        # ===== ENCABEZADO =====
        header_layout = QHBoxLayout()

        title = QLabel("Dashboard")
        title.setObjectName("Title")

        lbl_filter = QLabel("Periodo:")
        lbl_filter.setStyleSheet("font-weight: bold; color: #8E8E93;")

        self.cmb_filtro = QComboBox()
        self.cmb_filtro.addItems([
            "Todo",
            "Este mes",
            "Últimos 6 meses",
            "Último año"
        ])
        self.cmb_filtro.setFixedWidth(160)
        self.cmb_filtro.currentIndexChanged.connect(self.load_dashboard)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(lbl_filter)
        header_layout.addWidget(self.cmb_filtro)

        layout.addLayout(header_layout)

        # ===== TARJETAS RESUMEN =====
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(25)

        self.lbl_ventas_hoy = QLabel("0")
        self.lbl_ventas_mes = QLabel("0")
        self.lbl_producto_top = QLabel("Ninguno")

        cards_layout.addWidget(self.create_card("Ventas Hoy", self.lbl_ventas_hoy, ""))
        cards_layout.addWidget(self.create_card("Ventas del Mes", self.lbl_ventas_mes, ""))
        cards_layout.addWidget(self.create_card("Producto Top", self.lbl_producto_top, ""))

        layout.addLayout(cards_layout)

        # ===== TÍTULO DE RECIENTES =====
        lbl_recent = QLabel("Historial de Transacciones")
        lbl_recent.setObjectName("Subtitle")
        layout.addWidget(lbl_recent)

        # ===== TABLA =====
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Fecha", "Producto", "Cantidad", "Precio Unit.", "Total"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(False)  # Forzar grid invisible
        self.table.verticalHeader().setVisible(False)
        
        # Ajuste columnas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.table)

        self.load_dashboard()

    def create_card(self, title, value_label, icon):
        card = QFrame()
        card.setObjectName("Card")
        
        # Efecto 3D Real
        apply_shadow(card, blur_radius=30, x_offset=0, y_offset=10, color_alpha=60)
        
        clayout = QVBoxLayout(card)
        clayout.setContentsMargins(25, 25, 25, 25)
        
        top_layout = QHBoxLayout()
        lbl_title = QLabel(title)
        lbl_title.setObjectName("CardDesc")
        
        lbl_icon = QLabel(icon)
        lbl_icon.setStyleSheet("font-size: 18px;")
        
        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        top_layout.addWidget(lbl_icon)
        
        value_label.setObjectName("CardValue")
        value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        clayout.addLayout(top_layout)
        clayout.addSpacing(10)
        clayout.addWidget(value_label)
        
        return card

    # -------------------------------------------------

    def format_cop(self, value: float) -> str:
        return f"${int(value):,}".replace(",", ".")

    def load_dashboard(self):
        hoy = date.today()
        filtro = self.cmb_filtro.currentText()

        # ===== FECHA INICIO SEGÚN FILTRO =====
        fecha_inicio = None
        if filtro == "Este mes":
            fecha_inicio = hoy.replace(day=1)
        elif filtro == "Últimos 6 meses":
            fecha_inicio = hoy - relativedelta(months=6)
        elif filtro == "Último año":
            fecha_inicio = hoy - relativedelta(years=1)

        # ===== RESUMEN =====
        ventas_hoy = self.db.ventas_totales_por_fecha(hoy)
        self.lbl_ventas_hoy.setText(self.format_cop(ventas_hoy))

        ventas_mes = self.db.ventas_totales_mes(hoy.month, hoy.year)
        self.lbl_ventas_mes.setText(self.format_cop(ventas_mes))

        top = self.db.producto_mas_vendido_mes(hoy.month, hoy.year)
        if top:
            self.lbl_producto_top.setText(f"{top[0]}\n({top[1]} und)")
        else:
            self.lbl_producto_top.setText("Ninguno")

        # ===== TABLA =====
        ventas = self.db.obtener_ventas()

        ventas_filtradas = []
        for v in ventas:
            fecha_venta = datetime.strptime(v[4], "%Y-%m-%d").date()
            if fecha_inicio is None or fecha_venta >= fecha_inicio:
                ventas_filtradas.append(v)

        self.table.setRowCount(len(ventas_filtradas))

        for row, v in enumerate(ventas_filtradas):
            total = v[3] * v[2]
            
            # Crear items
            item_fecha = QTableWidgetItem(v[4])
            item_fecha.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item_fecha)
            
            item_prod = QTableWidgetItem(v[1])
            item_prod.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, item_prod)
            
            item_cant = QTableWidgetItem(str(v[2]))
            item_cant.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, item_cant)
            
            item_precio = QTableWidgetItem(self.format_cop(v[3]))
            item_precio.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, item_precio)
            
            item_total = QTableWidgetItem(self.format_cop(total))
            item_total.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, item_total)
