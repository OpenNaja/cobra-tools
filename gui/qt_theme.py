
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
    "dark": dark_palette
}
