import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from theme import DARK_STYLE


def resource_path(relative_path):
    """
    Obtiene la ruta correcta tanto en desarrollo como en el .exe
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_styles(app):
    """
    Aplica SIEMPRE el tema oscuro.
    Si existe app.qss, se añade encima.
    """
    qss_path = resource_path("styles/app.qss")

    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(DARK_STYLE + "\n" + f.read())
    else:
        app.setStyleSheet(DARK_STYLE)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    load_styles(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
