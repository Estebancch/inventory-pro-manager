from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

def apply_shadow(widget, blur_radius=25, x_offset=0, y_offset=8, color_alpha=120):
    """
    Aplica una sombra suave y profesional a un widget PyQt6 para dar
    efecto de elevación (Glass/Material Design).
    """
    # PREVENIR EL BUG DE SHADOW LEAK SOBRE LOS TEXTOS EN STARTUP:
    widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setOffset(x_offset, y_offset)
    shadow.setColor(QColor(0, 0, 0, color_alpha))
    widget.setGraphicsEffect(shadow)
