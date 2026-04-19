from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QLineEdit, QCheckBox, QLabel,
    QHeaderView, QFrame
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from database import Database
from ui.add_product_dialog import AddProductDialog
from ui.restock_dialog import RestockDialog
from ui.utils import apply_shadow


def format_cop(valor):
    try:
        valor = int(round(valor))
        return f"${valor:,}".replace(",", ".")
    except:
        return "$0"


class InventoryUI(QWidget):
    current_bg = "#1A1A1C"
    current_fg = "#E5E5EA"

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.selected_qr = None
        self.selected_nombre = None
        self.productos_cache = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(25)

        title = QLabel("Gestión de Inventario")
        title.setObjectName("Title")
        layout.addWidget(title)

        # ===== CONTROLES SUPERIORES (TARJETA) =====
        controls_frame = QFrame()
        controls_frame.setObjectName("Card")
        
        apply_shadow(controls_frame, blur_radius=20, x_offset=0, y_offset=6, color_alpha=60)
        
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setContentsMargins(25, 25, 25, 25)
        controls_layout.setSpacing(15)

        # Fila 1: Búsqueda y Botones de acción
        row1 = QHBoxLayout()
        
        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Buscar producto por nombre...")
        self.txt_buscar.setFixedWidth(300)
        self.txt_buscar.textChanged.connect(self.aplicar_filtros)

        self.chk_stock_bajo = QCheckBox("Solo stock bajo")
        self.chk_stock_bajo.stateChanged.connect(self.aplicar_filtros)

        btn_agregar = QPushButton("Agregar")
        btn_agregar.setProperty("class", "success")
        
        btn_restock = QPushButton("Reabastecer")
        btn_restock.setProperty("class", "primary")
        
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setProperty("class", "danger")

        row1.addWidget(self.txt_buscar)
        row1.addWidget(self.chk_stock_bajo)
        row1.addStretch()
        row1.addWidget(btn_agregar)
        row1.addWidget(btn_restock)
        row1.addWidget(btn_eliminar)

        # Fila 2: Lector QR
        row2 = QHBoxLayout()
        self.txt_qr = QLineEdit()
        self.txt_qr.setPlaceholderText("Escanear QR y presionar Enter...")
        self.txt_qr.returnPressed.connect(self.buscar_por_qr)
        
        lbl_qr = QLabel("Lector QR:")
        lbl_qr.setStyleSheet("font-weight: bold; color: #8E8E93;")
        
        row2.addWidget(lbl_qr)
        row2.addWidget(self.txt_qr)
        
        controls_layout.addLayout(row1)
        controls_layout.addLayout(row2)

        layout.addWidget(controls_frame)

        # ===== TABLA =====
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "QR", "Nombre", "Stock",
            "Stock Min", "Precio Venta", "Proveedor"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        
        # Ajuste de columnas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

        # ===== EVENTOS =====
        btn_agregar.clicked.connect(self.agregar_producto)
        btn_eliminar.clicked.connect(self.eliminar_producto)
        btn_restock.clicked.connect(self.reabastecer_stock)
        self.table.cellClicked.connect(self.seleccionar_producto)

        self.load_productos()

    def load_productos(self):
        self.productos_cache = self.db.obtener_productos()
        self.aplicar_filtros()

    def aplicar_filtros(self):
        texto = self.txt_buscar.text().lower()
        solo_bajo = self.chk_stock_bajo.isChecked()

        filtrados = []

        for p in self.productos_cache:
            nombre = p[2].lower()
            stock = p[4]
            stock_min = p[5]

            if texto and texto not in nombre:
                continue

            if solo_bajo and stock > stock_min:
                continue

            filtrados.append(p)

        self.cargar_tabla(filtrados)

    def cargar_tabla(self, productos):
        self.table.setRowCount(len(productos))
        self.selected_qr = None
        self.selected_nombre = None

        for row, p in enumerate(productos):
            stock_int = int(p[4]) if p[4] is not None else 0
            min_int = int(p[5]) if p[5] is not None else 0
            
            # Emoji indicador de severidad
            indicator_emoji = ""
            if stock_int == 0:
                indicator_emoji = "🔴 "
            elif stock_int <= min_int:
                indicator_emoji = "🟠 "

            item_qr = QTableWidgetItem(p[1])
            self.table.setItem(row, 0, item_qr)
            
            item_nombre = QTableWidgetItem(indicator_emoji + (p[2] or ""))
            item_nombre.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, item_nombre)
            
            # Formatear números centrado
            item_stock = QTableWidgetItem(str(p[4]))
            item_stock.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_min = QTableWidgetItem(str(p[5]))
            item_min.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.table.setItem(row, 2, item_stock)
            self.table.setItem(row, 3, item_min)
            
            item_precio = QTableWidgetItem(format_cop(p[7]))
            item_precio.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, item_precio)
            
            item_prov = QTableWidgetItem(p[8])
            item_prov.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 5, item_prov)

            # Colores dinámicos del FOREGROUND (El background choca con el Modo Claro nativo de Qt6)
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is None:
                    continue
                if stock_int == 0:
                    item.setForeground(QColor("#FF3B30")) # Texto Rojo en vez de fondo roto
                elif stock_int <= min_int:
                    item.setForeground(QColor("#FF9500")) # Texto Naranja

    def buscar_por_qr(self):
        qr = self.txt_qr.text().strip()
        if not qr:
            return

        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == qr:
                self.table.selectRow(row)
                self.seleccionar_producto(row, 0)
                self.txt_qr.clear()
                return

        QMessageBox.warning(self, "No encontrado", "QR no registrado")
        self.txt_qr.selectAll()

    def seleccionar_producto(self, row, col):
        self.selected_qr = self.table.item(row, 0).text()
        self.selected_nombre = self.table.item(row, 1).text()

    def agregar_producto(self):
        dialog = AddProductDialog()
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.db.agregar_producto(
                    data["qr_code"],
                    data["nombre"],
                    data["stock"],
                    data["stock_min"],
                    data["precio_compra"],
                    data["precio_venta"],
                    data["proveedor"]
                )
                self.load_productos()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def reabastecer_stock(self):
        if not self.selected_qr:
            QMessageBox.warning(self, "Error", "Seleccione un producto")
            return

        dialog = RestockDialog(self.selected_nombre)
        if dialog.exec():
            cantidad, precio_compra, precio_venta = dialog.get_data()

            ok = self.db.reabastecer_por_qr(
                self.selected_qr,
                cantidad,
                precio_compra if precio_compra > 0 else None,
                precio_venta if precio_venta > 0 else None
            )

            if not ok:
                QMessageBox.warning(self, "Error", "No se pudo reabastecer")

            self.load_productos()

    def eliminar_producto(self):
        if not self.selected_qr:
            QMessageBox.warning(self, "Error", "Seleccione un producto")
            return

        resp = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Seguro que desea eliminar el producto?\n\n{self.selected_nombre}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if resp != QMessageBox.StandardButton.Yes:
            return

        ok = self.db.eliminar_producto_por_codigo(self.selected_qr)

        if not ok:
            QMessageBox.warning(self, "Error", "No se pudo eliminar el producto")

        self.load_productos()
