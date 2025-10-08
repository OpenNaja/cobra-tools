
import abc
from dataclasses import dataclass, field

from typing import Optional, Callable
from PyQt5.QtGui import (QShowEvent, QPalette)
from PyQt5.QtWidgets import (QWidget, QLabel, QMenu, QFrame, QHBoxLayout, QSizePolicy, QWidgetAction)

FILE_MENU = 'File'
VIEW_MENU = 'View'
EDIT_MENU = 'Edit'
UTIL_MENU = 'Util'
HELP_MENU = 'Help'
DEVS_MENU = 'Devs'

@dataclass
class BaseMenuItem(abc.ABC):
    """Abstract base class for all items that appear in a menu"""
    name: str = ""
    func: Optional[Callable] = None
    icon: str = ""
    tooltip: str = ""

@dataclass
class MenuItem(BaseMenuItem):
    """Represents a standard, clickable menu item"""
    shortcut: str = ""

@dataclass
class SubMenuItem(BaseMenuItem):
    """Represents an item that creates a submenu"""
    items: list[BaseMenuItem] = field(default_factory=list)

@dataclass
class CheckableMenuItem(MenuItem):
    """Represents a menu item that can be checked."""
    config_name: str = ""
    config_default: bool = True

@dataclass
class SeparatorMenuItem(BaseMenuItem):
    """Represents a separator line in a menu."""
    pass

class LabelSeparator(QWidget):
    """
    A custom QWidget to act as a separator with a label, for use in a QMenu.
    
    It consists of a small text label followed by a horizontal line that
    fills the remaining space.
    """
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self._palette_initialized = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 3, 8, 3)
        layout.setSpacing(8)

        # Create the label that will display the separator's text.
        self.label = QLabel(text)
        # Set a very small, bold font
        font = self.font()
        font.setPointSize(7)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)

        # Create a QFrame configured to look like a horizontal line.
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Plain)

        layout.addWidget(self.label)
        layout.addWidget(self.line)
        layout.setStretch(1, 1)
        self.setLayout(layout)

    def showEvent(self, event: QShowEvent) -> None:
        """
        Overrides showEvent to apply palette changes when the widget is about
        to be displayed, ensuring it has inherited the correct application style.
        """
        super().showEvent(event)
        if not self._palette_initialized:
            lbl_color = self.palette().color(QPalette.ColorRole.WindowText)
            sep_color = lbl_color.darker(150)

            line_palette = self.line.palette()
            line_palette.setColor(QPalette.ColorRole.WindowText, sep_color)
            line_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, sep_color)
            self.line.setPalette(line_palette)

            label_palette = self.label.palette()
            label_palette.setColor(QPalette.ColorRole.WindowText, lbl_color)
            label_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, lbl_color)
            self.label.setPalette(label_palette)
            self._palette_initialized = True


def add_label_separator(menu: QMenu, text: str) -> None:
    """
    A helper function to create and add a LabelSeparator to a QMenu.
    """
    separator_widget = LabelSeparator(text)

    widget_action = QWidgetAction(menu)
    widget_action.setDefaultWidget(separator_widget)
    widget_action.setEnabled(False)

    menu.addAction(widget_action)
