
from PyQt5 import QtGui

dark_palette = QtGui.QPalette()
WHITE =     QtGui.QColor(255, 255, 255)
BLACK =     QtGui.QColor(0, 0, 0)
RED =       QtGui.QColor(255, 0, 0)
PRIMARY =   QtGui.QColor(53, 53, 53)
SECONDARY = QtGui.QColor(35, 35, 35)
TERTIARY =  QtGui.QColor(42, 130, 218)
DISABLED =  QtGui.QColor(125, 125, 125)
dark_palette.setColor(QtGui.QPalette.ColorRole.Window,          PRIMARY)
dark_palette.setColor(QtGui.QPalette.ColorRole.WindowText,      WHITE)
dark_palette.setColor(QtGui.QPalette.ColorRole.Base,            SECONDARY)
dark_palette.setColor(QtGui.QPalette.ColorRole.AlternateBase,   PRIMARY)
dark_palette.setColor(QtGui.QPalette.ColorRole.ToolTipBase,     WHITE)
dark_palette.setColor(QtGui.QPalette.ColorRole.ToolTipText,     WHITE)
dark_palette.setColor(QtGui.QPalette.ColorRole.Text,            WHITE)
dark_palette.setColor(QtGui.QPalette.ColorRole.Button,          PRIMARY)
dark_palette.setColor(QtGui.QPalette.ColorRole.ButtonText,      WHITE)
dark_palette.setColor(QtGui.QPalette.ColorRole.BrightText,      RED)
dark_palette.setColor(QtGui.QPalette.ColorRole.Link,            TERTIARY)
dark_palette.setColor(QtGui.QPalette.ColorRole.Highlight,       TERTIARY)
dark_palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, BLACK)

dark_palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, DISABLED)
dark_palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, DISABLED)
dark_palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, DISABLED)
dark_palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Light, PRIMARY)

palettes: dict[str, QtGui.QPalette] = {
    "dark": dark_palette,
    "light": QtGui.QPalette()
}


def style_modern_scrollbar(handle_color: str, view_bg_color: str, track_color: str="transparent") -> str:
    return RF"""
        QScrollBar:vertical {{
            border: 0px solid transparent;
            background: {track_color};
            width: 13px;
            margin: 0px 0px 0px 0px;
            border-radius: 6px;
        }}
        QScrollBar:horizontal {{
            border: 0px solid transparent;
            background: {track_color};
            height: 13px;
            margin: 0px 0px 0px 0px;
            border-radius: 6px;
        }}
        QAbstractScrollArea::corner {{
            background: {track_color};
            border: none;
        }}
        QScrollBar::handle {{
            background: {handle_color};
            border: 3px solid {view_bg_color};
            border-radius: 6px;
        }}
        QScrollBar::handle:hover {{
            background: {QtGui.QColor(handle_color).lighter(140).name()};
        }}
        QScrollBar::handle:vertical {{
            min-height: 12px;
        }}
        QScrollBar::up-arrow:vertical, QScrollBar::up-arrow:horizontal {{
            border: 0px solid transparent;
            width: 0px;
            height: 0px;
        }}
        QScrollBar::down-arrow:vertical, QScrollBar::down-arrow:horizontal {{
            border: 0px solid transparent;
            width: 0px;
            height: 0px;
        }}
        QScrollBar::add-line:vertical {{
            border: 0px solid transparent;
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:vertical {{
            border: 0px solid transparent;
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }}
        QScrollBar::add-line:horizontal {{
            border: 0px solid transparent;
            width: 0px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:horizontal {{
            border: 0px solid transparent;
            width: 0 px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }}

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            border: 0px solid transparent;
            width: 0px;
            background: none;
        }}
    """
