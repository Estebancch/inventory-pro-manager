import sqlite3
from config import DB_NAME


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_tables()

    # ================== TABLAS ==================

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            qr_code TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            categoria TEXT,
            stock INTEGER DEFAULT 0,
            stock_minimo INTEGER DEFAULT 0,
            precio_compra REAL DEFAULT 0,
            precio_venta REAL DEFAULT 0,
            proveedor TEXT,
            fecha_ingreso TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            total REAL NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )
        """)

        self.conn.commit()

    # ================== PRODUCTOS ==================

    def obtener_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        return self.cursor.fetchall()

    def obtener_producto_por_qr(self, qr_code):
        self.cursor.execute(
            "SELECT * FROM productos WHERE qr_code = ?", (qr_code,)
        )
        return self.cursor.fetchone()

    def obtener_producto_por_id(self, producto_id):
        self.cursor.execute(
            "SELECT * FROM productos WHERE id = ?", (producto_id,)
        )
        return self.cursor.fetchone()

    def agregar_producto(
        self, qr_code, nombre, stock,
        stock_minimo, precio_compra,
        precio_venta, proveedor
    ):
        if self.obtener_producto_por_qr(qr_code):
            raise ValueError("QR ya registrado")

        self.cursor.execute("""
        INSERT INTO productos
        (qr_code, nombre, categoria, stock, stock_minimo,
         precio_compra, precio_venta, proveedor, fecha_ingreso)
        VALUES (?, ?, '', ?, ?, ?, ?, ?, date('now'))
        """, (
            qr_code, nombre, stock,
            stock_minimo, precio_compra,
            precio_venta, proveedor
        ))

        self.conn.commit()

    def eliminar_producto(self, producto_id):
        self.cursor.execute(
            "DELETE FROM productos WHERE id = ?", (producto_id,)
        )
        self.conn.commit()

    # ✅ FIX CRASH INVENTARIO
    def eliminar_producto_por_codigo(self, qr_code):
        self.cursor.execute(
            "DELETE FROM productos WHERE qr_code = ?", (qr_code,)
        )

        if self.cursor.rowcount == 0:
            return False

        self.conn.commit()
        return True

    # ================== STOCK ==================

    def reabastecer_por_qr(
        self, qr_code, cantidad,
        precio_compra=None, precio_venta=None
    ):
        producto = self.obtener_producto_por_qr(qr_code)
        if not producto:
            return False

        producto_id = producto[0]

        if precio_compra is not None and precio_venta is not None:
            self.cursor.execute("""
                UPDATE productos
                SET stock = stock + ?,
                    precio_compra = ?,
                    precio_venta = ?
                WHERE id = ?
            """, (cantidad, precio_compra, precio_venta, producto_id))
        else:
            self.cursor.execute("""
                UPDATE productos
                SET stock = stock + ?
                WHERE id = ?
            """, (cantidad, producto_id))

        self.conn.commit()
        return True

    # ================== VENTAS ==================

    def vender_producto(self, qr_code, producto_id, cantidad, fecha):
        if qr_code:
            producto = self.obtener_producto_por_qr(qr_code)
        else:
            producto = self.obtener_producto_por_id(producto_id)

        if not producto:
            return False, "Producto no existe"

        producto_id = producto[0]
        stock_actual = producto[4]
        precio_venta = producto[7]

        if stock_actual < cantidad:
            return False, "Stock insuficiente"

        total = cantidad * precio_venta

        self.cursor.execute("""
        INSERT INTO ventas
        (producto_id, cantidad, precio_unitario, total, fecha)
        VALUES (?, ?, ?, ?, ?)
        """, (
            producto_id, cantidad,
            precio_venta, total, fecha
        ))

        self.cursor.execute("""
        UPDATE productos
        SET stock = stock - ?
        WHERE id = ?
        """, (cantidad, producto_id))

        self.conn.commit()
        return True, total

    # ✅ NUEVO: ELIMINAR VENTA + RESTAURAR STOCK
    def eliminar_venta(self, venta_id):
        self.cursor.execute("""
            SELECT producto_id, cantidad
            FROM ventas
            WHERE id = ?
        """, (venta_id,))
        venta = self.cursor.fetchone()

        if not venta:
            return False

        producto_id, cantidad = venta

        # restaurar stock
        self.cursor.execute("""
            UPDATE productos
            SET stock = stock + ?
            WHERE id = ?
        """, (cantidad, producto_id))

        # eliminar venta
        self.cursor.execute(
            "DELETE FROM ventas WHERE id = ?", (venta_id,)
        )

        # Reajustar el consecutivo de ID (sqlite auto-increment) 
        self.cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT COALESCE(MAX(id), 0) FROM ventas) WHERE name = 'ventas'")

        self.conn.commit()
        return True

    # ================== REPORTES ==================

    def obtener_ventas(self):
        self.cursor.execute("""
        SELECT v.id, COALESCE(p.nombre, 'PRODUCTO ELIMINADO'), v.cantidad, v.total, v.fecha
        FROM ventas v
        LEFT JOIN productos p ON p.id = v.producto_id
        ORDER BY v.id DESC
        """)
        return self.cursor.fetchall()

    def ventas_totales_por_fecha(self, fecha):
        self.cursor.execute("""
            SELECT SUM(total)
            FROM ventas
            WHERE fecha = ?
        """, (fecha,))
        res = self.cursor.fetchone()[0]
        return res if res else 0.0

    def ventas_totales_mes(self, mes, anio):
        self.cursor.execute("""
            SELECT SUM(total)
            FROM ventas
            WHERE strftime('%m', fecha) = ?
              AND strftime('%Y', fecha) = ?
        """, (f"{mes:02}", str(anio)))
        res = self.cursor.fetchone()[0]
        return res if res else 0.0

    def producto_mas_vendido_mes(self, mes, anio):
        self.cursor.execute("""
            SELECT COALESCE(p.nombre, 'PRODUCTO ELIMINADO'), SUM(v.cantidad) AS total
            FROM ventas v
            LEFT JOIN productos p ON p.id = v.producto_id
            WHERE strftime('%m', v.fecha) = ?
              AND strftime('%Y', v.fecha) = ?
            GROUP BY v.producto_id
            ORDER BY total DESC
            LIMIT 1
        """, (f"{mes:02}", str(anio)))
        return self.cursor.fetchone()
