from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QPushButton
)

class RestockDialog(QDialog):
    def __init__(self, nombre_producto):
        super().__init__()
        self.setWindowTitle("Reabastecer stock")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"Producto: {nombre_producto}"))

        layout.addWidget(QLabel("Cantidad a agregar:"))
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(1)
        layout.addWidget(self.spin_cantidad)

        layout.addWidget(QLabel("Precio compra (opcional):"))
        self.spin_compra = QDoubleSpinBox()
        self.spin_compra.setMaximum(1_000_000)
        layout.addWidget(self.spin_compra)

        layout.addWidget(QLabel("Precio venta (opcional):"))
        self.spin_venta = QDoubleSpinBox()
        self.spin_venta.setMaximum(1_000_000)
        layout.addWidget(self.spin_venta)

        btn = QPushButton("Confirmar")
        btn.setProperty("class", "primary")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def get_data(self):
        return (
            self.spin_cantidad.value(),
            self.spin_compra.value(),
            self.spin_venta.value()
        )
