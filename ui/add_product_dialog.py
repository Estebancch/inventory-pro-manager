from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class AddProductDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar producto")
        self.setFixedWidth(450)

        main_layout = QVBoxLayout(self)

        # ===== FORMULARIO =====
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignHCenter)

        # 🔹 QR (IDENTIFICADOR)
        self.txt_qr = QLineEdit()
        self.txt_qr.setPlaceholderText("Escanee el QR del producto")
        self.txt_qr.setClearButtonEnabled(True)

        # 🔹 DATOS DEL PRODUCTO
        self.txt_nombre = QLineEdit()
        self.spin_stock = QSpinBox()
        self.spin_stock_min = QSpinBox()
        self.spin_precio_compra = QDoubleSpinBox()
        self.spin_precio_venta = QDoubleSpinBox()
        self.txt_proveedor = QLineEdit()

        # ===== LIMITES =====
        self.spin_stock.setMaximum(100_000)
        self.spin_stock_min.setMaximum(100_000)
        self.spin_precio_compra.setMaximum(1_000_000)
        self.spin_precio_venta.setMaximum(1_000_000)

        self.spin_precio_compra.setDecimals(2)
        self.spin_precio_venta.setDecimals(2)

        # ===== CAMPOS =====
        form.addRow("QR del producto:", self.txt_qr)
        form.addRow("Nombre:", self.txt_nombre)
        form.addRow("Stock inicial:", self.spin_stock)
        form.addRow("Stock mínimo:", self.spin_stock_min)
        form.addRow("Precio compra:", self.spin_precio_compra)
        form.addRow("Precio venta:", self.spin_precio_venta)
        form.addRow("Proveedor:", self.txt_proveedor)

        main_layout.addLayout(form)

        # ===== BOTONES =====
        btns = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setProperty("class", "success")
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setProperty("class", "danger")

        btn_guardar.clicked.connect(self.validar_y_guardar)
        btn_cancelar.clicked.connect(self.reject)

        btns.addStretch()
        btns.addWidget(btn_guardar)
        btns.addWidget(btn_cancelar)

        main_layout.addLayout(btns)

    # -------------------------------------------------

    def validar_y_guardar(self):
        if not self.txt_qr.text().strip():
            QMessageBox.warning(self, "Error", "Debe escanear el QR del producto")
            return

        if not self.txt_nombre.text().strip():
            QMessageBox.warning(self, "Error", "El nombre del producto es obligatorio")
            return

        self.accept()

    # -------------------------------------------------

    def get_data(self):
        return {
            "qr_code": self.txt_qr.text().strip(),
            "nombre": self.txt_nombre.text().strip().upper(),
            "stock": self.spin_stock.value(),
            "stock_min": self.spin_stock_min.value(),
            "precio_compra": self.spin_precio_compra.value(),
            "precio_venta": self.spin_precio_venta.value(),
            "proveedor": self.txt_proveedor.text().strip().upper(),
        }
