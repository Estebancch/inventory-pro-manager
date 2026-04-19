# 📦 Inventory Pro Manager - Gestión de Inventario

Aplicación de escritorio desarrollada en Python con PyQt6 para gestionar inventario, ventas y control básico financiero.  
Pensada como una solución simple para pequeños negocios.

## 🚀 Tecnologías utilizadas
- Python 3
- PyQt6 (interfaz gráfica)
- SQLite (base de datos local)

## ✨ Funcionalidades
- Gestión de productos (agregar, editar, eliminar)
- Control de stock
- Módulo de ventas con actualización automática del inventario
- Dashboard con resumen de ingresos
- Alertas cuando un producto tiene poco stock
- Modo claro y oscuro

## 🛠️ Instalación y ejecución

1. Clonar repositorio:
```bash
git clone https://github.com/Estebancch/inventory-pro-manager.git
cd inventory-pro-manager
```

2. Crear entorno virtual (opcional):
```bash
python -m venv .venv
```

3. Activar:
- **Windows:**
```bash
.venv\Scripts\activate
```
- **Linux/macOS:**
```bash
source .venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Ejecutar:
```bash
python app.py
```

*La base de datos SQLite se crea automáticamente al iniciar el proyecto.*

## 📁 Estructura del proyecto
```text
/
├── app.py
├── config.py
├── database.py
├── theme.py
└── ui/
    ├── add_product_dialog.py
    ├── dashboard_ui.py
    ├── inventory_ui.py
    ├── main_window.py
    ├── restock_dialog.py
    ├── sales_ui.py
    └── utils.py
```

## 🔒 Notas
- Se usa `.gitignore` para evitar subir la base de datos local.
- El sistema maneja validaciones básicas para evitar errores en datos.

## 📌 Nota
Proyecto personal enfocado en practicar desarrollo de aplicaciones de escritorio con interfaz gráfica y manejo de datos.

## 📩 Contacto
Si tienes alguna duda o sugerencia sobre este proyecto, puedes contactarme a través de mi perfil de GitHub.
