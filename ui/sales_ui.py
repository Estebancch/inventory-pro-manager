from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSpinBox, QFrame,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QCompleter, QLineEdit, QHeaderView
)
from PyQt6.QtCore import QDate, pyqtSignal, Qt
from database import Database
from ui.utils import apply_shadow


def formato_cop(valor: float) -> str:
    return f"${valor:,.0f}".replace(",", ".")


class SalesUI(QWidget):

    venta_realizada = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.productos = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(25)

        title = QLabel("Caja y Ventas")
        title.setObjectName("Title")
        layout.addWidget(title)

        # ===== FORMULARIO (TARJETA) =====
        form_frame = QFrame()
        form_frame.setObjectName("Card")
        apply_shadow(form_frame, blur_radius=20, x_offset=0, y_offset=6, color_alpha=60)
        
        form_layout = QHBoxLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(15)

        self.txt_qr = QLineEdit()
        self.txt_qr.setPlaceholderText("Escanear QR...")
        self.txt_qr.returnPressed.connect(self.buscar_por_qr)

        self.cb_productos = QComboBox()
        self.cb_productos.setEditable(True)
        self.cb_productos.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.cb_productos.currentIndexChanged.connect(self.actualizar_total)

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(1)
        self.spin_cantidad.setFixedSize(80, 40)
        self.spin_cantidad.valueChanged.connect(self.actualizar_total)

        self.lbl_total = QLabel("Total: $0")
        self.lbl_total.setObjectName("CardValue")
        self.lbl_total.setFixedWidth(180)
        self.lbl_total.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_vender = QPushButton("Procesar Venta")
        btn_vender.setProperty("class", "success")
        btn_vender.clicked.connect(self.vender)

        form_layout.addWidget(self.txt_qr, 2)
        form_layout.addWidget(QLabel("o Selección:"))
        form_layout.addWidget(self.cb_productos, 4)
        form_layout.addWidget(QLabel("Cant:"))
        form_layout.addWidget(self.spin_cantidad)
        form_layout.addWidget(self.lbl_total)
        form_layout.addWidget(btn_vender)

        layout.addWidget(form_frame)

        # ===== RECIENTES =====
        recent_layout = QHBoxLayout()
        lbl_recent = QLabel("Historial de Ventas")
        lbl_recent.setObjectName("Subtitle")
        
        btn_eliminar = QPushButton("Revertir venta")
        btn_eliminar.setProperty("class", "danger")
        btn_eliminar.clicked.connect(self.eliminar_venta)

        recent_layout.addWidget(lbl_recent)
        recent_layout.addStretch()
        recent_layout.addWidget(btn_eliminar)

        layout.addLayout(recent_layout)

        # ===== TABLA =====
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID Venta", "Producto", "Cantidad", "Total", "Fecha"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.table)

        self.load_ventas()

    def showEvent(self, event):
        self.load_productos()
        self.load_ventas()
        super().showEvent(event)

    def load_productos(self):
        self.productos = self.db.obtener_productos()
        self.cb_productos.clear()

        textos = []
        for p in self.productos:
            texto = f"{p[2]} | Stock: {p[4]} | Precio: {formato_cop(p[7])}"
            textos.append(texto)
            self.cb_productos.addItem(texto)

        completer = QCompleter(textos, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.cb_productos.setCompleter(completer)

        self.cb_productos.setCurrentIndex(-1)
        self.actualizar_total()

    def buscar_por_qr(self):
        codigo = self.txt_qr.text().strip()
        if not codigo:
            return

        for i, p in enumerate(self.productos):
            if p[1] == codigo:
                self.cb_productos.setCurrentIndex(i)
                self.spin_cantidad.setValue(1)
                self.txt_qr.clear()
                return

        QMessageBox.warning(self, "Error", "Producto no encontrado por QR")

    def producto_actual(self):
        idx = self.cb_productos.currentIndex()
        if idx < 0:
            return None
        return self.productos[idx]

    def actualizar_total(self):
        producto = self.producto_actual()
        if not producto:
            self.lbl_total.setText("Total: $0")
            return

        total = producto[7] * self.spin_cantidad.value()
        self.lbl_total.setText(f"Total: {formato_cop(total)}")

    def vender(self):
        producto = self.producto_actual()
        if not producto:
            QMessageBox.warning(self, "Error", "Seleccione o escanee un producto")
            return

        cantidad = self.spin_cantidad.value()
        fecha = QDate.currentDate().toString("yyyy-MM-dd")

        ok, resultado = self.db.vender_producto(
            qr_code=producto[1],
            producto_id=producto[0],
            cantidad=cantidad,
            fecha=fecha
        )

        if not ok:
            QMessageBox.warning(self, "Error", resultado)
            return

        self.load_productos()
        self.load_ventas()
        self.spin_cantidad.setValue(1)
        self.cb_productos.setCurrentIndex(-1)
        self.lbl_total.setText("Total: $0")

        self.venta_realizada.emit()

    def load_ventas(self):
        ventas = self.db.obtener_ventas()
        self.table.setRowCount(len(ventas))

        for row, v in enumerate(ventas):
            item_id = QTableWidgetItem(str(v[0]))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item_id)
            
            item_prod = QTableWidgetItem(v[1])
            item_prod.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, item_prod)
            
            item_cant = QTableWidgetItem(str(v[2]))
            item_cant.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, item_cant)
            
            item_total = QTableWidgetItem(formato_cop(v[3]))
            item_total.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, item_total)
            
            item_fecha = QTableWidgetItem(v[4])
            item_fecha.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, item_fecha)

    def eliminar_venta(self):
        fila = self.table.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Seleccione una venta")
            return

        venta_id = int(self.table.item(fila, 0).text())

        confirm = QMessageBox.question(
            self,
            "Confirmar",
            "¿Desea eliminar esta venta?\nEl stock será restaurado.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.db.eliminar_venta(venta_id)

        self.load_ventas()
        self.load_productos()
        self.venta_realizada.emit()
