import logging
import webbrowser
import os
import re
import html
import time
import threading
import abc
from collections import deque
from abc import abstractmethod
from pathlib import Path
from dataclasses import dataclass, field

from ovl_util import auto_updater  # pyright: ignore  # noqa: F401
from ovl_util import logs
from ovl_util.config import Config, ImmediateSetting, RestartSetting

from typing import Any, AnyStr, Union, Optional, Iterable, Callable, cast, NamedTuple, Literal
from textwrap import dedent
from modules.formats.shared import DummyReporter
from modules.walker import valid_packages
from generated.formats.ovl import games

import gui
from gui import qt_theme
from gui.app_utils import *

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject, QDir, QFileInfo, QRegularExpression,
                          QRect, QRectF, QSize, QEvent, QTimer, QTimerEvent, QThread, QUrl, QMimeData,
                          QAbstractTableModel, QSortFilterProxyModel, QModelIndex, QItemSelection,
                          QAbstractAnimation, QParallelAnimationGroup, QPropertyAnimation, QChildEvent,
                          QAbstractListModel, QPersistentModelIndex, QItemSelectionModel, QVariant)
from PyQt5.QtGui import (QBrush, QColor, QFont, QFontMetrics, QIcon, QPainter, QPen, qRgba, QPainterPath, QLinearGradient,
                         QStandardItemModel, QStandardItem, QTextOption,
                         QCloseEvent, QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent, QShowEvent, QHideEvent,
                         QKeyEvent, QFocusEvent, QMouseEvent, QPaintEvent, QResizeEvent, QWheelEvent, QPalette)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QColorDialog, QFileDialog, QAbstractItemView, QToolTip,
                             QListView, QHeaderView, QTableView, QTreeView, QFileSystemModel, QStyle, QLayoutItem,
                             QAction, QCheckBox, QComboBox, QDoubleSpinBox, QLabel, QLineEdit, QMenu, QMenuBar,
                             QMessageBox, QTextEdit, QProgressBar, QPushButton, QStatusBar, QToolButton, QSpacerItem,
                             QFrame, QLayout, QGridLayout, QBoxLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy,
                             QSplitter, QToolBar, QWidgetAction, QTextBrowser, QProxyStyle, QStyleOption,
                             QStyleFactory, QStyleOptionViewItem, QStyledItemDelegate, QDialog, QDialogButtonBox)
from PyQt5.QtWinExtras import QWinTaskbarButton
from qframelesswindow import FramelessMainWindow, StandardTitleBar
from __version__ import VERSION, COMMIT_HASH


MAX_UINT = 4294967295
root_dir = Path(__file__).resolve().parent.parent

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

    def showEvent(self, event: QPaintEvent) -> None:
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


FilterFunc = Callable[[Any, str], bool]

class CustomSortFilterProxyModel(QSortFilterProxyModel):
    """
    Implements a QSortFilterProxyModel that allows for custom
    filtering. Add new filter functions using addFilterFunction().
    New functions should accept two arguments, the column to be
    filtered and the currently set filter string, and should
    return True to accept the row, False otherwise.
    Filter functions are stored in a dictionary for easy
    removal by key. Use the addFilterFunction() and
    removeFilterFunction() methods for access.
    The filterString is used as the main pattern matching
    string for filter functions. This could easily be expanded
    to handle regular expressions if needed.
    """

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.filterString = ''
        self.filterFunctions: dict[str, FilterFunc] = {}

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        # for whatever reason, probably due to data loss in casting, we must override this function
        # to allow for correct comparison of djb2 hashes
        return left.data() < right.data()

    def setFilterFixedString(self, text: str) -> None:
        """
        text : string
            The string to be used for pattern matching.
        """
        self.filterString = text.lower()
        self.invalidateFilter()

    def addFilterFunction(self, name: str, new_func: FilterFunc) -> None:
        """
        name : hashable object
            The object to be used as the key for
            this filter function. Use this object
            to remove the filter function in the future.
            Typically this is a self descriptive string.
        new_func : function
            A new function which must take two arguments,
            the row to be tested and the ProxyModel's current
            filterString. The function should return True if
            the filter accepts the row, False otherwise.
            ex:
            mesh.addFilterFunction(
                'test_columns_1_and_2',
                lambda r,s: (s in r[1] and s in r[2]))
        """
        self.filterFunctions[name] = new_func
        self.invalidateFilter()

    def removeFilterFunction(self, name: str) -> None:
        """
        name : hashable object

        Removes the filter function associated with name,
        if it exists.
        """
        if name in self.filterFunctions.keys():
            del self.filterFunctions[name]
            self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, _source_parent: QModelIndex) -> bool:
        """
        Reimplemented from base class to allow the use
        of custom filtering.
        """
        # The source mesh should have a method called row()
        # which returns the table row as a python list.
        model = cast(TableModel, self.sourceModel())
        tests = [func(model.row(source_row), self.filterString) for func in self.filterFunctions.values()]
        return False not in tests


class TableModel(QAbstractTableModel):
    member_renamed = pyqtSignal(str, str)
    value_edited = pyqtSignal(str, str, object)

    def __init__(self, header_names: list[str], ignore_types: list[str], editable_columns=("Name",)) -> None:
        super(TableModel, self).__init__()
        self._data: list[list[str]] = []
        self.header_labels = header_names
        self.ignore_types = ignore_types
        self.editable_columns = set(self.header_labels.index(n) for n in editable_columns)
        # self.member_renamed.connect(self.member_renamed_debug_print)

    @staticmethod
    def member_renamed_debug_print(a, b) -> None:
        print("renamed", a, b)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        color = ""
        file_row = self._data[index.row()]
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if len(file_row):
                return file_row[index.column()]

        # TODO: Remove some hardcoding surrounding File Type
        if "File Type" in self.header_labels:
            type_idx = self.header_labels.index("File Type")
            file_ext = file_row[type_idx]
            # if role == Qt.ItemDataRole.ForegroundRole:
            #     # if file_ext in self.ignore_types:
            #     return QColor(color)

            if role == Qt.ItemDataRole.DecorationRole:
                if index.column() == 0:
                    if len(file_row):
                        # remove the leading '.' from ext
                        return get_icon(file_ext[1:], color)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            # center align non-primary integer columns
            if index.column() > 0 and str(file_row[index.column()]).isnumeric():
                return Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter

        if role == Qt.ItemDataRole.ToolTipRole:
            if len(file_row) > 2:
                return file_row[2]

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.DisplayRole) -> bool:
        if index.isValid():
            if role == Qt.ItemDataRole.EditRole:
                row = index.row()
                column = index.column()
                old_value = self._data[row][column]
                # value has changed, gotta update it
                if old_value != value:
                    self._data[row][column] = value
                    if column == 0:
                        self.member_renamed.emit(old_value, value)
                    else:
                        self.value_edited.emit(self._data[row][0], self.header_labels[column], value)
                return True
        return False

    def row(self, row_index: int) -> Any:
        return self._data[row_index]

    def rowCount(self, _index: Optional[QModelIndex] = None) -> int:
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, _index: Optional[QModelIndex] = None) -> int:
        # The following takes the first elem-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self.header_labels)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.header_labels[section]
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        dtype = self._data[index.row()]
        drag_n_drop = Qt.ItemFlags(cast(Qt.ItemFlags, Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled))
        renamable = Qt.ItemFlags(cast(Qt.ItemFlags, Qt.ItemFlag.ItemIsEditable))
        state = Qt.ItemFlags(cast(Qt.ItemFlags, Qt.ItemFlag.NoItemFlags))
        if index.column() in self.editable_columns:
            state |= renamable
        if len(dtype) and dtype[1] not in self.ignore_types:
            state |= drag_n_drop
        return state


class SortableTable(QWidget):
    closed = pyqtSignal()

    def __init__(self, header_names: list[str], ignore_types: list[str], ignore_drop_type: str = "", opt_hide: bool = False, actions={}, editable_columns=("Name",)) -> None:
        super().__init__()
        self.table = TableView(header_names, ignore_types, ignore_drop_type, actions, editable_columns)
        self.filter_entry = IconEdit("filter", "Filter Files", callback=self.table.set_filter)
        self.filter_entry.setToolTip("Filter by name - only show items matching this name")

        self.show_hidden = QCheckBox("Show Hidden")
        if opt_hide:
            self.show_hidden.stateChanged.connect(self.toggle_show_hidden)
        else:
            self.show_hidden.hide()
        self.table.set_show_hidden_filter(True)  # set the show_hidden filter to hide invisible extensions
        self.filter_invert = IconButton("invert")
        self.filter_invert.setCheckable(True)
        self.filter_invert.setToolTip("Invert filtering - show hidden items, and vice versa")
        self.filter_invert.toggled.connect(self.toggle_invert)

        self.filter_clear = IconButton("clear_filter")
        self.filter_clear.setToolTip("Clear Filter")
        self.filter_clear.pressed.connect(self.clear_filter)

        # Button Row Setup
        self.button_count = 0
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_frame = QFrame()
        self.btn_frame.setLayout(self.btn_layout)

        filter_bar = FlowWidget(self)
        filter_bar_lay = FlowHLayout(filter_bar)
        filter_bar_lay.addWidget(self.filter_entry, hide_index=-1)
        filter_bar_lay.addWidget(self.filter_invert, hide_index=3)
        filter_bar_lay.addWidget(self.filter_clear, hide_index=5)
        filter_bar_lay.addWidget(self.show_hidden, hide_index=0)
        filter_bar_lay.setContentsMargins(0, 0, 0, 0)
        filter_bar.show()
        filter_bar.setMinimumWidth(self.filter_entry.minimumWidth())

        qgrid = QGridLayout()
        qgrid.addWidget(filter_bar, 0, 0, 1, 4)
        qgrid.addWidget(self.table, 2, 0, 1, 4)
        qgrid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(qgrid)
        self.grid = qgrid

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.closed.emit()
        super(SortableTable, self).closeEvent(a0)

    def set_data(self, data: Any) -> None:
        self.table.set_data(data)

    def clear_filter(self) -> None:
        self.filter_entry.entry.setText("")
        self.show_hidden.setChecked(False)
        self.filter_invert.setChecked(False)
        self.table.clear_filter()

    def toggle_show_hidden(self, state: Qt.CheckState) -> None:
        self.table.set_show_hidden_filter(state != Qt.CheckState.Checked)

    def toggle_invert(self, checked: bool) -> None:
        self.table.inverted = checked
        self.table.update_filter_function()

    def add_button(self, btn) -> None:
        if not self.button_count:
            self.grid.addWidget(self.btn_frame, 1, 0, 1, 4)
        self.btn_layout.addWidget(btn)
        self.button_count += 1
        if isinstance(btn, SelectedItemsButton):
            btn.setDisabled(True)
            self.table.selectionModel().selectionChanged.connect(btn.setEnabledFromSelection)


class TableView(QTableView):
    files_dragged = pyqtSignal(list)
    files_dropped = pyqtSignal(list)
    file_selected = pyqtSignal(int)
    file_selected_count = pyqtSignal(int)
    file_double_clicked = pyqtSignal(list)

    def __init__(self, header_names: list[str], ignore_types: list[str], ignore_drop_type: str, actions={}, editable_columns=("Name",)) -> None:
        super().__init__()
        self.ignore_types = ignore_types
        self.header_names = header_names
        self.ignore_drop_type = ignore_drop_type
        self.actions = actions
        self.table_model = TableModel(header_names, ignore_types, editable_columns=editable_columns)
        self.proxy_model = CustomSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.table_model)
        self.proxy_model.setSortRole(Qt.ItemDataRole.UserRole)
        self.setModel(self.proxy_model)

        self.resizeColumnsToContents()
        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.verticalHeader().hide()
        self.setSelectionBehavior(self.SelectRows)

        self.setSortingEnabled(True)
        # sort by index; -1 means don't sort
        self.sortByColumn(-1, Qt.SortOrder.AscendingOrder)
        self.proxy_model.setFilterFixedString("")
        self.proxy_model.setFilterKeyColumn(0)
        self.inverted = False
        self.selectionModel().selectionChanged.connect(self.on_selectionChanged)
        self.doubleClicked.connect(self.on_double_click)

        # handle column width
        header = self.horizontalHeader()
        header.setStretchLastSection(True)

        # The number of selected items in the model
        self.selected_count = 0

    def on_selectionChanged(self, _selected: QItemSelection, _deselected: QItemSelection) -> None:
        self.selected = list(self.get_selected_line_indices())
        if self.selected:
            self.file_selected.emit(self.selected[-1])
        self.file_selected_count.emit(self.selected_count)

    def on_double_click(self, index: QModelIndex):
        row_i = self.proxy_model.mapToSource(index).row()
        self.file_double_clicked.emit(self.table_model._data[row_i])

    def update_filter_function(self) -> None:
        if self.inverted:
            self.proxy_model.addFilterFunction('name', lambda r, s: s not in r[0])
        else:
            self.proxy_model.addFilterFunction('name', lambda r, s: s in r[0])

    def set_filter(self, fixed_string: str) -> None:
        self.proxy_model.setFilterFixedString(fixed_string)
        self.update_filter_function()

    def set_show_hidden_filter(self, hide: bool) -> None:
        show_hidden_name = "show_hidden"
        if hide and "File Type" in self.header_names:
            ext_index = self.header_names.index("File Type")

            def show_hidden(r, s) -> bool:
                return r[ext_index] not in self.ignore_types

            self.proxy_model.addFilterFunction(show_hidden_name, show_hidden)
        else:
            self.proxy_model.removeFilterFunction(show_hidden_name)

    def clear_filter(self) -> None:
        self.proxy_model.setFilterFixedString("")
        self.sortByColumn(-1, Qt.SortOrder.AscendingOrder)

    def get_selected_line_indices(self) -> set[int]:
        indices = set(self.proxy_model.mapToSource(x).row() for x in self.selectedIndexes())
        self.selected_count = len(indices)
        return indices

    def get_selected_files(self) -> list[str]:
        # map the selected indices to the actual underlying data, which is in its original order
        return [self.table_model._data[x][0] for x in self.get_selected_line_indices()]

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()
        index = self.indexAt(event.pos())
        if index.isValid():
            row_ind = self.proxy_model.mapToSource(index).row()
            row = self.table_model._data[row_ind]
            if row:
                if self.actions:
                    for action, func in self.actions.items():
                        menu.addAction(action)
                    res = menu.exec_(event.globalPos())
                    if res in self.actions:
                        func = self.actions[res]
                        func(row)

    def get_files(self) -> list[str]:
        # returns the list of all file names
        return [x[0] for x in self.table_model._data]

    def startDrag(self, _supportedActions: (Qt.DropActions | Qt.DropAction)) -> None:
        """Emits a signal with the file names of all files that are being dragged"""
        # Disallow drops on self after drag has begun
        self.setAcceptDrops(False)
        # Drag only with LMB
        if QApplication.mouseButtons() & Qt.MouseButton.LeftButton:
            self.files_dragged.emit(self.get_selected_files())
        # Allow drops on self after drag has finished
        self.setAcceptDrops(True)

    def set_data(self, data) -> None:
        # Assure selectionChanged signal since reset bypasses this
        self.clearSelection()
        # Reset Model
        self.table_model.beginResetModel()
        self.table_model._data = data
        self.table_model.endResetModel()
        self.resizeColumnsToContents()

    def accept_ignore(self, e: QDropEvent) -> None:
        if not self.ignore_drop_type:
            e.accept()
            return
        path = e.mimeData().urls()[0].toLocalFile() if e.mimeData().hasUrls() else ""
        if not path.lower().endswith(f".{self.ignore_drop_type.lower()}"):
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        self.accept_ignore(event)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        self.accept_ignore(event)

    def dropEvent(self, event: QDropEvent) -> None:
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            self.files_dropped.emit([str(url.path())[1:] for url in urls])
            event.accept()


class SelectedItemsButton(QPushButton):
    """A QPushButton which is enabled only when items in a view are selected"""
    def __init__(self, parent: Optional[QWidget] = None, text: str = "", icon: Optional[QIcon] = None) -> None:
        if icon:
            super().__init__(icon, text, parent)
        else:
            super().__init__(text, parent)
        self.setStyleSheet("SelectedItemsButton:disabled { background-color: #252525; } ")

    def setEnabledFromSelection(self, selection: QItemSelection) -> None:
        self.setEnabled(selection.count() > 0)


class FlowWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.widgets: deque[QWidget] = deque()           # Visible widgets
        self.widgets_overflow: deque[QWidget] = deque()  # Hidden widgets
        self.perm_widgets: deque[QWidget] = deque()      # Permanently visible widgets
        self.flow_spacers: deque[QLayoutItem] = deque()  # Spacer widgets
        # Dummy widget to pad non-consecutive hide indices
        self.dummy = QWidget()
        self.dummy.setMaximumWidth(0)
        self.dummy.setHidden(True)
        self.dummy.setObjectName("dummy")

    def add_flow_widget(self, obj: QWidget, hide_index: int) -> None:
        """Sort children for flow"""
        if hide_index > -1 and hide_index < len(self.widgets):
            self.widgets.insert(hide_index, obj)
        elif hide_index > -1:
            # Handle non-consecutive hide indices
            for _ in range(0, hide_index - len(self.widgets)):
                self.widgets.append(self.dummy)
            self.widgets.append(obj)
        else:
            # Hide Index -1 is permanently visible
            self.perm_widgets.append(obj)

    def add_flow_item(self, obj: QLayoutItem) -> None:
        self.flow_spacers.append(obj)

    def remove_flow_widget(self, obj: QWidget) -> None:
        if obj in self.widgets:
            self.widgets.remove(obj)

    def remove_flow_item(self, obj: QLayoutItem) -> None:
        if obj in self.flow_spacers:
            self.flow_spacers.remove(obj)

    def do_flow_all(self, event: QResizeEvent, widgets: deque[QWidget]) -> None:
        for widget in widgets.copy():
            self.do_flow(event, widget)

    def do_flow(self, event: QResizeEvent, widget: QWidget) -> None:
        width = event.size().width()
        old_width = event.oldSize().width()
        growing = width >= old_width if old_width > -1 else False
        visible_count = 1 if widget.isVisible() else 0
        sibling_min_hint_width = 0
        spacer_width = 0
        total_width = 0
        spacing = self.layout().spacing()
        left_margin, _, right_margin, _ = self.layout().getContentsMargins()
        margins = left_margin + right_margin
        # Get spacer widths
        for spacer in self.flow_spacers:
            if isinstance(spacer, QSpacerItem) and spacer.sizeHint().width() > 0:
                spacer_width += spacer.sizeHint().width()
                visible_count += 1
        # Get sibling widget minimum widths
        for child in self.children():
            if isinstance(child, QWidget) and child != widget and child.isVisible():
                sibling_min_hint_width += child.minimumSizeHint().width()
                visible_count += 1
        # All visible widgets + spacing and margins
        total_width = widget.width() + sibling_min_hint_width + spacing * (visible_count - 1) + margins + spacer_width
        # Hide or show, and move the widget in or out of overflow
        if not growing and widget.isVisible() and width <= total_width:
            widget.hide()
            self.widgets_overflow.appendleft(self.widgets.popleft())
        elif growing and widget.isHidden() and total_width < width:
            widget.show()
            self.widgets.appendleft(self.widgets_overflow.popleft())

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Do flow on one or all widgets depending on oldSize() and growing/shrinking"""
        width = event.size().width()
        old_width = event.oldSize().width()
        if width < 0:
            return super().resizeEvent(event)
        growing = width >= old_width if old_width > -1 else False
        first_visible = self.widgets[0] if self.widgets else None
        first_hidden = self.widgets_overflow[0] if self.widgets_overflow else None
        current_item = first_visible if not growing else first_hidden
        if current_item:
            return self.do_flow(event, current_item) if old_width > -1 else self.do_flow_all(event, self.widgets)
        return super().resizeEvent(event)

    def compact_widgets(self) -> None:
        """Remove any empty spots from non-consecutive hide indices"""
        for widget in self.widgets.copy():
            if widget.objectName() == "dummy":
                self.widgets.remove(self.dummy)

    def show(self) -> None:
        self.compact_widgets()  # Ensures always runs
        return super().show()

    def showEvent(self, event: QShowEvent) -> None:
        """Send an initial QResizeEvent so that visibility is calculated on first show"""
        super().showEvent(event)
        self.resizeEvent(QResizeEvent(self.size(), QSize(-1, -1)))

    def sizeHint(self) -> QSize:
        """Return the minimumSizeHint so that splitter/window resizing is not blocked"""
        return self.minimumSizeHint()

    def minimumSizeHint(self) -> QSize:
        """Return the accumulated minimum widths of permanently visible widgets"""
        min_perm_width = 0
        for child in self.children():
            if isinstance(child, QWidget) and child in self.perm_widgets:
                min_perm_width += child.minimumSizeHint().width()
        min_size = super().minimumSizeHint()
        return QSize(min_perm_width, min_size.height())


class FlowHLayout(QHBoxLayout):
    """Layout for FlowWidget. Must be passed a `parent` FlowWidget."""
    def __init__(self, parent: FlowWidget) -> None:
        super().__init__(parent)
        self.parent_flow = parent

    def addWidget(self, widget: QWidget, stretch: int = 0,
                  alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignVCenter,
                  hide_index: int = -1) -> None:
        self.parent_flow.add_flow_widget(widget, hide_index)
        return super().addWidget(widget, stretch, alignment)

    def addItem(self, item: QLayoutItem) -> None:
        self.parent_flow.add_flow_item(item)
        return super().addItem(item)

    def removeWidget(self, widget: QWidget) -> None:
        self.parent_flow.remove_flow_widget(widget)
        return super().removeWidget(widget)

    def removeItem(self, item: QLayoutItem) -> None:
        self.parent_flow.remove_flow_item(item)
        return super().removeItem(item)


class IconButton(QPushButton):
    def __init__(self, icon_name: str, size: QSize = QSize(16, 16)) -> None:
        super().__init__(get_icon(icon_name), "")
        self.setFlat(True)
        self.setMouseTracking(True)
        self.setIconSize(size)
        self.setFixedSize(size)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # pal is only valid after getting it again from self
        self.setPalette(get_main_window().get_palette_from_cfg())
        color = self.palette().window().color()
        style = RF"""
            IconButton {{
                border: 1px solid transparent;
                padding: 0px;
                margin: 0px;
            }}
            IconButton:hover {{
                border: 1px solid {color.lighter(170).name()};
                background: {color.lighter(130).name()};
            }}
            IconButton:pressed {{
                background: {color.lighter(150).name()};
            }}
            IconButton:checked {{
                background: {color.lighter(200).name()};
            }}
        """
        self.setStyleSheet(style)


ToolbarItem = Union[QAction, QWidget]


class ToolbarSpacingProxyStyle(QProxyStyle):
    """
    A QProxyStyle that overrides the styling of toolbar widgets
    """
    def __init__(self, base_style: QStyle | str | None=None):
        super().__init__(base_style)
        self._spacing = 10  # Default spacing

    def set_toolbar_spacing(self, spacing: int) -> None:
        """Allows you to dynamically set the desired spacing."""
        self._spacing = spacing

    def pixelMetric(self, metric: QStyle.PixelMetric, option: QStyleOption | None=None,
                    widget: QWidget | None=None) -> int:
        """
        Custom pixel metric overrides
        """
        if metric == QStyle.PixelMetric.PM_ToolBarItemSpacing:
            return self._spacing

        return super().pixelMetric(metric, option, widget)


class OrientationToolBar(QToolBar):
    """
    A QToolBar that manages the visibility of its actions and widgets
    based on the toolbar's orientation.
    """

    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(title, parent)
        # This dictionary maps a QAction or QWidget to its visibility rule
        # The rule is a Qt.Orientations flag (e.g. Qt.Orientation.Horizontal)
        self._item_visibility: dict[ToolbarItem, Qt.Orientations] = {}
        # Store margins for each orientation, initializing with the current state.
        self._horizontal_margins = self.contentsMargins()
        self._vertical_margins = self.contentsMargins()

    def addOrientationAction(self, action: QAction, visibility: Qt.Orientations) -> None:
        """
        Adds a QAction that will only be visible in the specified orientations.
          Example: (Qt.Orientation.Horizontal | Qt.Orientation.Vertical)
        """
        super().addAction(action)
        self._item_visibility[action] = visibility
        self._updateItemVisibility(action)

    def addOrientationWidget(self, widget: QWidget, visibility: Qt.Orientations) -> None:
        """
        Adds a QWidget that will only be visible in the specified orientations.
        """
        widget_action = super().addWidget(widget)
        #widget_action.setPriority(QAction.Priority.LowPriority)
        self._item_visibility[widget_action] = visibility
        self._updateItemVisibility(widget_action)

    def addOrientationSeparator(self, visibility: Qt.Orientations) -> QAction:
        """
        Adds a separator that will only be visible in the specified orientations.
        """
        separator_action = super().addSeparator()
        self._item_visibility[separator_action] = visibility
        self._updateItemVisibility(separator_action)
        return separator_action

    def setOrientation(self, orientation: Qt.Orientation) -> None:
        """
        Overrides the parent method to apply custom visibility rules and to
        propagate the orientation change to any child that supports it.
        """
        # Let the parent class handle its own orientation change first
        super().setOrientation(orientation)
        # Iterate through all managed items to find child widgets
        for item_action in self._item_visibility.keys():
            if isinstance(item_action, QWidgetAction):
                # Retrieve the actual widget from the widget action
                child_widget = item_action.defaultWidget()
                # Check if the widget has a 'setOrientation' method
                if child_widget and hasattr(child_widget, 'setOrientation'):
                    child_widget.setOrientation(orientation)
        # Apply this toolbar's own visibility logic to its immediate items
        self._updateAllItemVisibility()
        # Apply the correct margins for the new orientation
        self._applyOrientationMargins()

    def setOrientationMargins(self,
                              horizontal: QtCore.QMargins | None = None,
                              vertical: QtCore.QMargins | None = None) -> None:
        """
        Sets the content margins to be used for each orientation.
        """
        if horizontal:
            self._horizontal_margins = horizontal
        if vertical:
            self._vertical_margins = vertical
        # Apply the correct margins immediately based on the current orientation
        self._applyOrientationMargins()

    def _applyOrientationMargins(self) -> None:
        """
        Applies the stored margins based on the current orientation.
        """
        if self.orientation() == Qt.Orientation.Horizontal:
            super().setContentsMargins(self._horizontal_margins)
        else:  # Qt.Orientation.Vertical
            super().setContentsMargins(self._vertical_margins)

    def setContentsMargins(self, *args, **kwargs) -> None:
        """
        The margins should only be set via setOrientationMargins().
        """
        pass


    def _updateAllItemVisibility(self) -> None:
        """
        Iterates through all tracked items and sets their visibility based on the toolbar's
        current orientation.
        """
        for item, visibility_rule in self._item_visibility.items():
            self._updateItemVisibility(item, visibility_rule)

    def _updateItemVisibility(self, item: ToolbarItem, visibility_rule: Qt.Orientations = None) -> None:
        """
        Updates the visibility of a single item.
        """
        if visibility_rule is None:
            visibility_rule = self._item_visibility.get(item)

        if not visibility_rule:
            return

        # Check if the item's visibility rule includes the current orientation
        is_visible = bool(self.orientation() & visibility_rule)
        item.setVisible(is_visible)

    def removeAction(self, action: QAction) -> None:
        """
        Overrides removeAction to clean up the item from the tracking dictionary.
        """
        if action in self._item_visibility:
            del self._item_visibility[action]
        super().removeAction(action)

    def childEvent(self, event: QChildEvent) -> None:
        """
        Overrides childEvent to catch when a widget is removed from the toolbar,
        ensuring it's also removed from the tracking dictionary.
        """
        if event.type() == QEvent.Type.ChildRemoved:
            child = event.child()
            if child in self._item_visibility:
                del self._item_visibility[child]
        super().childEvent(event)


class SnapCollapseWidget(QWidget):
    """
    A widget that contains a toolbar and content, designed to be used within a SnapCollapseSplitter.

    When the widget's size shrinks below a certain threshold in its primary
    orientation, the content widget is hidden. For horizontal orientation,
    the toolbar also switches from being above the content to being vertical.
    """
    snapped = pyqtSignal(bool)
    current_size = pyqtSignal(QSize)
    SNAP_THRESHOLD = 120

    def __init__(self, toolbar: QWidget=None, content: QWidget=None, orientation: Qt.Orientation=Qt.Orientation.Vertical,
                 threshold: int=SNAP_THRESHOLD, parent=None):
        super().__init__(parent)
        self._orientation = orientation
        self._toolbar = None
        self._content = None
        self._is_collapsed = False
        self._snap_threshold = threshold

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        if toolbar:
            self.set_toolbar(toolbar)
        if content:
            self.set_content(content)

    def set_toolbar(self, toolbar: QWidget):
        """Sets or replaces the toolbar widget."""
        # Remove and delete the existing toolbar, if any
        if self._toolbar:
            self._layout.removeWidget(self._toolbar)
            self._toolbar.deleteLater()

        self._toolbar = toolbar
        if self._toolbar:
            # Insert at top
            self._layout.insertWidget(0, self._toolbar)

    def set_content(self, content: QWidget):
        """Sets or replaces the content widget."""
        # Remove and delete the existing content, if any
        if self._content:
            self._layout.removeWidget(self._content)
            self._content.deleteLater()

        self._content = content
        if self._content:
            self._layout.addWidget(self._content)
            
            # Apply the size policy for collapsing
            if self._orientation == Qt.Orientation.Horizontal:
                self._content.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
            else:  # Vertical
                self._content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)

            # If the widget is already collapsed, hide the new content immediately
            if self.is_collapsed():
                self._content.hide()

    def is_collapsed(self) -> bool:
        return self._is_collapsed

    def resizeEvent(self, event):
        """The core logic for snapping is handled on resize"""
        super().resizeEvent(event)
        current_size = (
            self.width() if self._orientation == Qt.Orientation.Horizontal else self.height()
        )
        # Emit the signal every time the resize happens and we are under the threshold.
        # This allows the parent splitter to continuously enforce the snap.
        if current_size < self._snap_threshold:
            if not self._is_collapsed:
                self.collapse()
            else:
                # If already collapsed, still emit the signal so the splitter can enforce the size.
                self.snapped.emit(True)
        elif self._is_collapsed:
            self.expand()
        self.current_size.emit(self.size())

    def collapse(self):
        """Hides the content and updates the layout for the collapsed state."""
        self._is_collapsed = True
        self._content.hide()
        if self._orientation == Qt.Orientation.Horizontal and hasattr(self._toolbar, "setOrientation"):
            self._toolbar.setOrientation(Qt.Orientation.Vertical)

        self.snapped.emit(True)
        self.updateGeometry()

    def expand(self):
        """Shows the content and restores the layout for the expanded state."""
        self._is_collapsed = False
        self._content.show()
        if self._orientation == Qt.Orientation.Horizontal and hasattr(self._toolbar, "setOrientation"):
            self._toolbar.setOrientation(Qt.Orientation.Horizontal)

        self.snapped.emit(False)
        self.updateGeometry()

    def minimumSizeHint(self) -> QSize:
        """
        Calculates the minimum size hint for the parent QSplitter.
        """
        if self._is_collapsed:
            return self._toolbar.minimumSizeHint()
        # When expanded, the layout is always QVBoxLayout.
        # Therefore, the minimum size is the max of the children's widths and the sum of their heights.
        toolbar_hint = self._toolbar.minimumSizeHint()
        content_hint = self._content.minimumSizeHint()
        
        w = max(toolbar_hint.width(), content_hint.width())
        h = toolbar_hint.height() + content_hint.height()
        return QSize(w, h)


class SnapCollapseSplitter(QSplitter):
    """
    A QSplitter that properly handles SnapCollapseWidget children by actively
    enforcing their snapped (collapsed) state.
    """
    def __init__(self, orientation: Qt.Orientation, parent: QWidget | None = None):
        super().__init__(orientation, parent)
        self._snap_widgets = {}

    def addWidget(self, widget: QWidget):
        """
        Overrides addWidget to identify SnapCollapseWidgets and configure them.
        """
        super().addWidget(widget)
        if isinstance(widget, SnapCollapseWidget):
            index = self.indexOf(widget)
            self._snap_widgets[index] = widget
            self.setCollapsible(index, False)
            widget.snapped.connect(self._on_child_snapped)

    def _on_child_snapped(self, is_collapsed: bool):
        """
        When a child snaps collapsed, this slot enforces the splitter size,
        forcing the widget to its minimum and giving the extra space to another widget.
        """
        if not is_collapsed:
            return

        sender_widget = self.sender()
        if not isinstance(sender_widget, SnapCollapseWidget):
            return

        index = self.indexOf(sender_widget)
        current_sizes = self.sizes()
        if len(current_sizes) < 2 or index == -1:
            return

        min_hint = sender_widget.minimumSizeHint()
        min_size = min_hint.width() if self.orientation() == Qt.Orientation.Horizontal else min_hint.height()
        # If the widget already has a size smaller or equal to its minimum, do nothing
        # This check is to prevent recursive loops
        if current_sizes[index] <= min_size:
            return

        # Calculate the space to reclaim from the collapsed widget
        delta = current_sizes[index] - min_size
        new_sizes = list(current_sizes)
        new_sizes[index] = min_size
        # Find the largest non-collapsed widget to give the extra space to
        largest_widget_index = -1
        max_size = -1
        for i, size in enumerate(new_sizes):
            if i == index:
                continue
            widget = self.widget(i)
            # Don't give space to other collapsed widgets
            if isinstance(widget, SnapCollapseWidget) and widget.is_collapsed():
                continue
            if size > max_size:
                max_size = size
                largest_widget_index = i
        
        if largest_widget_index != -1:
            new_sizes[largest_widget_index] += delta
        else:
            # Fallback: if all other widgets are collapsed, give it to the first neighbor
            if index > 0:
                new_sizes[index - 1] += delta
            else:
                new_sizes[index + 1] += delta

        # Use a zero-delay QTimer to apply the sizes. This breaks potential
        # recursive event loops where setSizes -> resizeEvent -> snapped -> _on_child_snapped.
        QTimer.singleShot(0, lambda: self.setSizes(new_sizes))


class LogStatus(QWidget):
    """A log level icon, count for that log level, and optional last log text."""
    select_row = pyqtSignal(int)

    class Message(NamedTuple):
        row: int
        text: str

    def __init__(self, parent: Optional[QWidget] = None, level: str = "INFO",
                 color: str = "#ffcb44", show_msg: bool = False, max_msg_width: int = 400) -> None:
        super().__init__(parent)
        self.messages: deque[LogStatus.Message] = deque()
        self.show_msg: bool = show_msg
        self.max_msg_width: int = max_msg_width
        self.setFixedHeight(16)
        self.setContentsMargins(0, 0, 0, 0)
        # Icon and count
        self.count_box = QHBoxLayout()
        self.count_box.setSpacing(5)
        self.count_box.setContentsMargins(0, 0, 0, 0)
        # Icon
        self.count_btn = QPushButton(get_icon(level.lower()), "")
        self.count_btn.setFlat(True)
        self.count_btn.setFixedSize(16, 16)
        self.count_btn.setContentsMargins(0, 0, 0, 0)
        self.count_btn.setToolTip(f"{level.title()}s in the current file.")
        self.count_btn.setStatusTip(f"{level.title()}s in the current file.")
        self.count_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # Count
        self.count_lbl = QLabel("0")
        self.count_lbl.setContentsMargins(0, 0, 0, 0)
        self.count_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_lbl.setToolTip(f"{level.title()}s in the current file.")
        self.count_lbl.setStatusTip(f"{level.title()}s in the current file.")
        self.count_lbl.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.count_box.addWidget(self.count_btn)
        self.count_box.addWidget(self.count_lbl)
        # Next button and text
        self.next_box = QHBoxLayout()
        self.next_box.setSpacing(0)
        self.next_box.setContentsMargins(0, 0, 0, 0)
        # Next button
        self.next_btn = QPushButton(get_icon("jump", color=color), "", parent=self)
        self.next_btn.setFlat(True)
        self.next_btn.setVisible(False)
        self.next_btn.setStatusTip(f"Jump to next {level.title()}")
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        # Next text
        self.next_txt = QPushButton("", parent=self)
        self.next_txt.setVisible(False)
        self.next_txt.setStatusTip(f"Jump to next {level.title()}")
        self.next_txt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_box.addWidget(self.next_btn)
        if self.show_msg:
            self.next_txt.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            self.next_box.addWidget(self.next_txt)
        # TODO: Integrate with cfg palette
        bg = QApplication.palette().shadow().color()
        bg = bg.lighter(45)
        highlight = QColor(color)
        highlight = highlight.lighter(105)
        btn_style = RF"""
            QPushButton {{
                padding: 2px;
                margin: 0px;
                color: {color};
                border: none;
            }}
            QLabel {{
                padding: 0px;
                margin: 0px;
                color: {color};
                border: none;
            }}
        """
        next_btn_style = RF"""
            QPushButton {{
                padding: 2px;
                margin: 0px;
                color: {color};
                border: none;
                font: bold 12px "Hack, Consolas, monospace"; 
            }}
            QPushButton:hover {{
                color: {highlight.name()};
                background: {bg.name()};
                border: none;
            }}
        """
        self.count_btn.setStyleSheet(btn_style)
        self.count_lbl.setStyleSheet(btn_style)
        self.count_lbl.setFont(get_font("Hack, Consolas, monospace", 8))
        self.next_btn.setStyleSheet(next_btn_style)
        self.next_txt.setStyleSheet(next_btn_style)
        self.next_btn.clicked.connect(self.on_clicked)
        self.next_txt.clicked.connect(self.on_clicked)
        # Main layout
        self.status_box = QHBoxLayout(self)
        self.status_box.addLayout(self.count_box)
        self.status_box.addLayout(self.next_box)
        self.status_box.setContentsMargins(0, 0, 0, 0)

    @property
    def message_count(self) -> int:
        return len(self.messages)

    def setOrientation(self, orientation: Qt.Orientation):
        direction = (QHBoxLayout.Direction.LeftToRight if orientation == Qt.Orientation.Horizontal
                                else QHBoxLayout.Direction.TopToBottom)
        self.status_box.setDirection(direction)
        self.count_box.setDirection(direction)
        self.next_box.setDirection(direction)

        if orientation == Qt.Orientation.Horizontal:
            self.next_btn.setFixedHeight(16)
            self.next_txt.setFixedHeight(16)
            if self.show_msg:
                self.next_txt.setMaximumWidth(self.max_msg_width)
            else:
                self.next_txt.setMaximumWidth(0)
                self.next_btn.setFixedWidth(16)
            self.setFixedHeight(16)
        else:
            self.setMinimumHeight(32)
            self.setMaximumHeight(96)

    def set_show_message(self, show: bool) -> None:
        self.show_msg = show

    def add_message(self, row: int, msg: str) -> None:
        self.messages.append(LogStatus.Message(row, msg))
        self.update_text()

    def update_text(self) -> None:
        if self.message_count == 0:
            self.next_btn.setVisible(False)
            self.next_txt.setVisible(False)
            return self.count_lbl.setText("0")
        if self.show_msg:
            # Always show top of message deque
            self.next_txt.setText(f" {self.messages[0].text}")
            # TODO: Elision slightly cut off
            metrics = self.next_txt.fontMetrics()
            self.next_txt.setText(metrics.elidedText(self.next_txt.text(), Qt.TextElideMode.ElideRight, self.max_msg_width))
        if self.message_count < 100:
            self.count_lbl.setFont(get_font("Hack, Consolas, monospace", 8))
        else:
            self.count_lbl.setFont(get_font("Hack, Consolas, monospace", 7))
        self.next_btn.setVisible(True)
        self.next_txt.setVisible(True)
        self.next_btn.setToolTip(f"Jump to `{self.messages[0].text}`")
        self.next_txt.setToolTip(f"Jump to `{self.messages[0].text}`")
        self.count_lbl.setText(f"{self.message_count}")

    def on_clicked(self, _checked: bool) -> None:
        if self.message_count:
            self.select_row.emit(self.messages[0].row)
            self.messages.rotate(-1)
            self.update_text()

    def clear(self) -> None:
        self.messages.clear()
        self.update_text()


class LogViewDelegate(QStyledItemDelegate):
    FIXED_ROW_HEIGHT = 18
    ICON_AREA_WIDTH = 25
    TEXT_PADDING = 4
    ROW_FONT: QFont = get_font("Hack, Consolas, monospace", pixel_size=12, bold=True)
    HOVER_INDICATOR_SVG_NAME = "mouse_lmb"
    DETAIL_INDICATOR_SVG_NAME = "info_large"
    HOVER_INDICATOR_SVG_SIZE: QSize = QSize(16, 16)
    DETAIL_INDICATOR_SVG_SIZE: QSize = QSize(20, 20)
    HOVER_INDICATOR_TEXT = "Details "
    INDICATOR_SPACING = 4

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(-1, self.FIXED_ROW_HEIGHT + self.TEXT_PADDING)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        self.initStyleOption(option, index)

        painter.save()
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.HighQualityAntialiasing)

        # Data for the Row
        log_level = index.data(LogModel.LEVEL)
        bg_color = option.backgroundBrush.color()
        log_color = LogView.COLORS.get(log_level, option.palette.text().color())

        icon_pixmap = index.data(LogModel.ICON)
        row_txt_summary = str(index.data(LogModel.TEXT) or "")
        has_details = bool(index.data(LogModel.DETAIL))

        content_rect = option.rect.adjusted(
            self.TEXT_PADDING,       # Left padding from item edge
            self.TEXT_PADDING // 2,  # Top padding from item edge
            -self.TEXT_PADDING,      # Right padding from item edge
            -self.TEXT_PADDING // 2  # Bottom padding from item edge
        )
        # Effective vertical drawing area for text/indicator:
        drawing_y = content_rect.top()
        drawing_height = content_rect.height()
        # Define where text will start horizontally
        text_summary_start_x = option.rect.left() + self.ICON_AREA_WIDTH

        # Colored Gradients
        if content_rect.isValid():
            color = QColor(LogView.COLORS.get(index.data(LogModel.LEVEL), "#FFFFFF"))
            color.setAlpha(24)
            color2 = QColor(LogView.COLORS.get(index.data(LogModel.LEVEL), "#FFFFFF"))
            color2.setAlpha(16)

            if option.state & QtWidgets.QStyle.StateFlag.State_Selected:
                color.setAlpha(48)
                color2.setAlpha(32)
            elif option.state & QtWidgets.QStyle.StateFlag.State_MouseOver:
                color.setAlpha(8) 
                color2.setAlpha(0)

            expansion_pixels = 1
            gradient_fill_rect = QRectF(content_rect).adjusted(
                -expansion_pixels,
                -expansion_pixels,
                expansion_pixels,
                expansion_pixels
            )
            gradient_fill_rect = gradient_fill_rect.intersected(QRectF(option.rect))  # Constrain

            gradient = QLinearGradient(0, 0, 0, 1.0)  # Vertical gradient
            gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)
            gradient.setColorAt(0.0, color)
            gradient.setColorAt(1.0, color2)
            
            path = QPainterPath()
            path.addRoundedRect(gradient_fill_rect, 4, 4)
            painter.setPen(QPen(Qt.GlobalColor.transparent, 0))
            painter.setBrush(gradient)
            painter.drawPath(path)

        # Draw Icon
        icon_x_start = option.rect.left() + self.TEXT_PADDING
        if icon_pixmap and isinstance(icon_pixmap, QtGui.QPixmap):
            icon_y = drawing_y + (drawing_height - icon_pixmap.height()) // 2
            painter.drawPixmap(icon_x_start, icon_y, icon_pixmap)

        # Determine if hover indicator for details should be shown
        is_hovered = bool(option.state & QtWidgets.QStyle.StateFlag.State_MouseOver)
        hover_detail_indicator = has_details and is_hovered

        # To correctly elide log text
        indicator_block_width = 0
        # Draw Detail Indicators
        if hover_detail_indicator:
            # Font Metrics for log text elision
            details_txt_font: QFont = QFont(self.ROW_FONT)
            details_txt_font.setBold(False)
            indicator_icon_width = self.HOVER_INDICATOR_SVG_SIZE.width()
            details_txt = self.HOVER_INDICATOR_TEXT
            details_txt_font_metrics = QFontMetrics(details_txt_font)
            details_txt_width = details_txt_font_metrics.horizontalAdvance(details_txt)
            spacing_txt_inner = self.INDICATOR_SPACING // 2
            total_indicator_visual_width = details_txt_width + spacing_txt_inner + indicator_icon_width
            border_internal_padding = 2
            indicator_block_width = total_indicator_visual_width + (2 * border_internal_padding)
            # Icon
            indicator_pixmap = None
            try:
                indicator_icon: QIcon = get_icon(self.HOVER_INDICATOR_SVG_NAME, bg_color.name(), self.HOVER_INDICATOR_SVG_SIZE) 
                indicator_pixmap: QtGui.QPixmap = indicator_icon.pixmap(self.HOVER_INDICATOR_SVG_SIZE)
            except Exception as e:  # Catch if get_icon itself fails
                logging.error(f"Error getting icon '{self.HOVER_INDICATOR_SVG_NAME}': {e}")
                indicator_pixmap = None

            indicator_block_x_start = content_rect.right() - indicator_block_width

            # Ensure it doesn't overlap with where text summary is supposed to end
            if indicator_block_x_start < text_summary_start_x + self.INDICATOR_SPACING :  # Avoid overlap
                 indicator_block_x_start = text_summary_start_x + self.INDICATOR_SPACING

            # Draw the border
            border_draw_rect = QRect(
                indicator_block_x_start,
                drawing_y, 
                indicator_block_width,
                drawing_height 
            )
            indicator_bg_color = log_color
            indicator_border_color = QColor(log_color)
            indicator_border_color.setAlpha(192)
            painter.setPen(QPen(indicator_bg_color, 1)) 
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(border_draw_rect)  # 1px border just inside
            painter.fillRect(border_draw_rect, indicator_border_color)
            # Draw "Details "
            painter.setPen(bg_color)
            painter.setFont(details_txt_font)
            
            details_txt_draw_x = border_draw_rect.left() + border_internal_padding
            details_txt_rect = QRect(details_txt_draw_x + indicator_icon_width + spacing_txt_inner, drawing_y, details_txt_width, drawing_height)
            painter.drawText(details_txt_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, details_txt)

            if indicator_pixmap:
                arrow_y = drawing_y + (drawing_height - indicator_pixmap.height()) // 2
                painter.drawPixmap(details_txt_draw_x, arrow_y, indicator_pixmap)
        elif has_details:
            indicator_block_width = self.DETAIL_INDICATOR_SVG_SIZE.width() + self.INDICATOR_SPACING
            indicator_pixmap = None
            try:
                indicator_icon = get_icon(self.DETAIL_INDICATOR_SVG_NAME, log_color.name(), self.DETAIL_INDICATOR_SVG_SIZE) 
                indicator_pixmap = indicator_icon.pixmap(self.DETAIL_INDICATOR_SVG_SIZE)
            except Exception as e:
                logging.error(f"Error getting icon '{self.DETAIL_INDICATOR_SVG_NAME}': {e}")
                indicator_pixmap = None
            indicator_block_x_start = content_rect.right() - indicator_block_width
            if indicator_block_x_start < text_summary_start_x + self.INDICATOR_SPACING:
                 indicator_block_x_start = text_summary_start_x + self.INDICATOR_SPACING
            if indicator_pixmap:
                info_y = drawing_y + (drawing_height - indicator_pixmap.height()) // 2
                painter.drawPixmap(indicator_block_x_start, info_y, indicator_pixmap)

        # Calculate Text Summary Rect (respecting indicator)
        # Text ends before content_rect.right() or before the indicator if shown
        text_summary_end_x_limit = content_rect.right()
        if has_details:
            text_summary_end_x_limit -= indicator_block_width
        text_summary_available_width = text_summary_end_x_limit - text_summary_start_x
        text_summary_rect = QRect(
            text_summary_start_x,
            drawing_y,
            text_summary_available_width,
            drawing_height
        )

        # Draw Text Summary
        if row_txt_summary and text_summary_rect.width() > 0:
            text_color = None
            if option.state & QtWidgets.QStyle.StateFlag.State_Selected:
                text_color = log_color.lighter(120)
            else:
                text_color = log_color
            painter.setPen(text_color)
            painter.setFont(self.ROW_FONT)

            # Elide text based on the calculated text_summary_rect.width()
            summary_font_metrics = QFontMetrics(self.ROW_FONT)
            elided_text = summary_font_metrics.elidedText(row_txt_summary, Qt.TextElideMode.ElideRight, text_summary_rect.width())
            painter.drawText(text_summary_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, elided_text)

        painter.restore()


class LogListData(NamedTuple):
    level: str
    text: str
    html: str
    detail: str

    @staticmethod
    def from_str(text: str) -> 'LogListData':
        message, detail = text.split(logs.HtmlFormatter.eol, 1)
        level, plaintext, html = message.split(" | ", 2)
        return LogListData(level, plaintext, html, detail)


class LogModel(QAbstractListModel):
    number_fetched = pyqtSignal(int)
    resize_requested = pyqtSignal(int)

    TEXT = Qt.ItemDataRole.EditRole
    HTML = Qt.ItemDataRole.DisplayRole
    DETAIL = Qt.ItemDataRole.UserRole
    ICON = Qt.ItemDataRole.DecorationRole
    INFO = Qt.ItemDataRole.ToolTipRole
    LEVEL = Qt.ItemDataRole.WhatsThisRole
    TOGGLED = Qt.ItemDataRole.CheckStateRole

    def __init__(self, parent: QObject | None = None, batch_size=100) -> None:
        super().__init__(parent)
        self._row_count: int = 0
        self.log_data: list[LogListData] = list()
        self.batch_size = batch_size
        self.checks: dict[QPersistentModelIndex, Qt.CheckState] = {}

    def append(self, data: LogListData) -> None:
        self.log_data.append(data)

    def append_log_batch(self, data_list: list[LogListData]) -> None:
        self.log_data.extend(data_list)

    def clear(self) -> None:
        self.log_data.clear()
        self.removeRows(0, self.rowCount())
        self._row_count = 0

    @property
    def data_count(self) -> int:
        return len(self.log_data)

    def rowCount(self, _parent: QModelIndex = QModelIndex()) -> int:
        return self._row_count

    def setData(self, index: QModelIndex, value: Any, role: int = HTML) -> bool:
        if not index.isValid():
            return False
        if role == LogModel.TOGGLED:
            self.checks[QPersistentModelIndex(index)] = value
            return True
        return False

    def data(self, index: QModelIndex, role: int = HTML) -> Any:
        if not index.isValid():
            return None
        row = index.row()
        log = self.log_data[index.row()]
        if row < 0 or row >= self.data_count:
            return None
        if role == LogModel.HTML:
            return log.html
        elif role == LogModel.ICON:
            return get_icon(log.level).pixmap(16, 16)
        elif role == LogModel.DETAIL:
            return log.detail
        elif role == LogModel.TEXT:
            return log.text
        elif role == LogModel.INFO:
            return truncate_tooltip(f"{log.text}\n\n{dedent(log.detail).strip()}".strip(), line_count=100)
        elif role == LogModel.TOGGLED:
            return self.checks.get(QPersistentModelIndex(index), Qt.CheckState.Unchecked)
        elif role == LogModel.LEVEL:
            return log.level
        return QVariant()

    def canFetchMore(self, _index: QModelIndex | None = None) -> bool:
        return self._row_count < self.data_count

    def fetchMore(self, _index: QModelIndex | None = None) -> None:
        remainder = self.data_count - self._row_count
        fetched = min(self.batch_size, remainder)
        self.beginInsertRows(QModelIndex(), self._row_count, self._row_count + fetched)
        self._row_count += fetched
        self.endInsertRows()
        self.number_fetched.emit(fetched)

    def mimeData(self, indexes: Iterable[QModelIndex]) -> QMimeData:
        text = ""
        for index in indexes:
            text += f"{index.data(LogModel.LEVEL)} | {index.data(LogModel.TEXT)}"
            detail = index.data(LogModel.DETAIL)
            if detail:
                text += detail
            text += "\n"
        data = QMimeData()
        data.setText(text)
        return data

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlags(cast(Qt.ItemFlags,
                                 Qt.ItemFlag.ItemIsSelectable
                                 | Qt.ItemFlag.ItemIsEnabled))

    def on_rowSizeHintChanged(self, height: int) -> None:
        self.layoutChanged.emit()
        self.resize_requested.emit(height)


class LogView(QListView):
    toggle_detail = pyqtSignal()
    increment_error = pyqtSignal(int, str)
    increment_warning = pyqtSignal(int, str)

    FETCH_TIMER_INTERVAL = 250

    DEBUG_COLOR = "#808080"
    INFO_COLOR = "#ddd"
    SUCCESS_COLOR = "#2fff5d"
    WARNING_COLOR = "#ffcb44"
    ERROR_COLOR = "#e73f34"
    ERROR_COLOR_BRIGHT = "#e84b40"
    CRITICAL_COLOR = "#ff2e67"

    COLORS = {
        "DEBUG": QColor(DEBUG_COLOR),
        "INFO": QColor(INFO_COLOR),
        "SUCCESS": QColor(SUCCESS_COLOR),
        "WARNING": QColor(WARNING_COLOR),
        "ERROR": QColor(ERROR_COLOR),
        "CRITICAL": QColor(CRITICAL_COLOR),
    }

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.logger: LoggerWidget = parent
        self.on_detail = False
        self.setAcceptDrops(False)
        #self.setLayoutMode(QListView.LayoutMode.Batched)  # Flickers badly
        #self.setBatchSize(100)  # Flickers badly
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Ignored)
        self.setVerticalScrollMode(QListView.ScrollMode.ScrollPerItem)
        self.setDragEnabled(False)
        self.setMouseTracking(True)
        self.setAutoFillBackground(False)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyle(QStyleFactory.create('windows'))
        self.setUniformItemSizes(True)
        # pal is only valid after getting it again from self
        self.setPalette(get_main_window().get_palette_from_cfg())
        pal = self.palette()
        base_col = pal.base().color()
        text_col = pal.text().color()
        self.setStyleSheet(RF"""
            QListView {{
                border: 0px;
                padding-left: 1px;
                padding-top: 3px;
                background-color: {base_col.darker(110).name()};
                selection-background-color: transparent;
                outline: 0;
            }}
            QListView::item {{
                border: 1px solid transparent;
            }}
            QListView::item:selected {{
                background: {base_col.lighter(110).name()};
            }}
            QListView::item:selected:active {{
            }}
            QListView::item:hover {{
                background: {base_col.lighter(120).name()};
            }}
            QListView::item:focus {{
            }}
            QListView::item:selected:!active {{
            }}
            QListView > QToolTip {{font: bold 11px 'Hack, Consolas, monospace'; border: 1px solid white;}}
        """ + qt_theme.style_modern_scrollbar(handle_color=text_col.darker(300).name(),
                                              view_bg_color=base_col.darker(110).name()))
        # View model
        self.list_model = LogModel(self, batch_size=1000)
        self.setModel(self.list_model)
        self.list_model.number_fetched.connect(self.on_number_fetched)
        # Item delegate
        self.delegate = LogViewDelegate(self)
        self.setItemDelegate(self.delegate)

        # Timer for fetchMore
        self.fetchTimer = QTimer()
        self.fetchTimer.setInterval(self.FETCH_TIMER_INTERVAL)
        self.fetchTimer.setSingleShot(True)
        self.fetchTimer.timeout.connect(self.fetchMore)

        self._doFetches: bool = self.isVisible()  # Control fetching based on visibility
        if self.canFetch():  # Initial fetch if possible
            self.fetchTimer.start()
        self.list_model.number_fetched.connect(self.on_model_number_fetched)

    def _get_unhandled_item_count(self) -> int:
        """Helper to get the number of items in the model's store not yet in the view."""
        if not self.list_model:
            return 0
        return self.list_model.data_count - self.list_model.rowCount()

    @pyqtSlot(int)
    def set_fetch_interval(self, interval_ms: int):
        """Sets the interval for the timer that fetches from LogModel"""
        logging.debug(f"LogView: Setting fetch interval to {interval_ms}ms.")
        self._current_fetch_interval = interval_ms
        was_active = self.fetchTimer.isActive()
        if was_active:
            self.fetchTimer.stop()
        self.fetchTimer.setInterval(interval_ms)
        if was_active:  # If it was running, restart it to apply new interval for next timeout
            self.fetchTimer.start()
        # If it wasn't active, it will pick up the new interval when next started by startFetches.

    def append_log_batch(self, log_data_list: list[LogListData]) -> None:
        if self.logger.is_shutting_down or not log_data_list:
            return
        self.list_model.append_log_batch(log_data_list)
        if self.list_model.canFetchMore() and self.canFetch():
            self.startFetches()

    def clear(self) -> None:
        self.clearSelection()
        self.list_model.clear()

    def count(self) -> int:
        return self.list_model.data_count

    def fetched_count(self) -> int:
        """Items currently fetched and shown by the view"""
        return self.list_model.rowCount()

    def canFetch(self) -> bool:
        """Determines if fetching should occur (view is visible and allowed)."""
        return self._doFetches  # and self.isVisible()

    def startFetches(self) -> None:
        """Allow fetching of more data."""
        self._doFetches = True
        if self.list_model:  # and self.isVisible():
            # Before starting the timer loop, try an initial pull from handler
            # This makes it more responsive when there's already buffered data
            self._pull_logs()
            if self.list_model.canFetchMore():
                if not self.fetchTimer.isActive():
                    self.fetchTimer.start()

    def stopFetches(self) -> None:
        """Disallow fetching of more data."""
        self._doFetches = False
        if self.fetchTimer.isActive():
            self.fetchTimer.stop()

    def fetchMore(self) -> None:
        if self.logger.is_shutting_down:
            return
        self._pull_logs()
        if self.list_model and self.list_model.canFetchMore() and self.canFetch():
            if self.state() != self.State.EditingState:
                # Calls LogModel's fetchMore()
                # This internally calls begin/endInsertRows and emits number_fetched
                self.list_model.fetchMore()
            # After model fetch, check if there are more items for the next fetch
            if self.list_model.canFetchMore() and self.canFetch():
                self.fetchTimer.start()  # Schedule the next fetch iteration

    def _pull_logs(self):
        """Pulls logs from Handler's buffer and appends them to LogModel"""
        buffered_logs = self.logger.handler.get_and_clear_buffer()
        if buffered_logs:
            # Update LogStatus error/warning counts
            base_index_for_signals = self.list_model.data_count
            for i, data_item in enumerate(buffered_logs):
                if data_item.level in ("ERROR", "CRITICAL"):
                    self.increment_error.emit(base_index_for_signals + i, data_item.text)
                if data_item.level == "WARNING":
                    self.increment_warning.emit(base_index_for_signals + i, data_item.text)

            self.append_log_batch(buffered_logs)

    @pyqtSlot(int)
    def on_model_number_fetched(self, newly_fetched_count: int):
        """Slot for LogModel's number_fetched signal."""
        if newly_fetched_count > 0:
            self.scrollToBottom()

    def copy_selection(self) -> None:
        """Fill clipboard with log text for all selected items."""
        selection = self.selectedIndexes()
        if selection:
            mime_data = self.list_model.mimeData(selection)
            QApplication.clipboard().setMimeData(mime_data)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle Ctrl-C for log messages"""
        if event == QtGui.QKeySequence.Copy:
            self.copy_selection()
            return
        return super().keyPressEvent(event)

    def on_number_fetched(self, newly_fetched: int) -> None:
        """Scroll to bottom when new items are fetched, if appropriate."""
        if newly_fetched > 0:
            self.scrollToBottom()

    def hideEvent(self, event: QHideEvent) -> None:
        """Stop fetching data when the widget is hidden."""
        #self.stopFetches()
        super().hideEvent(event)

    def showEvent(self, event: QShowEvent) -> None:
        """Start fetching data when the widget is shown."""
        self.startFetches()
        super().showEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Ensure timer is stopped when the widget is closing"""
        if self.fetchTimer.isActive():
            self.fetchTimer.stop()
        super().closeEvent(event)


LOGGER_RIGHT = Qt.Orientation.Horizontal
LOGGER_BOTTOM = Qt.Orientation.Vertical

class LoggerWidget(SnapCollapseWidget):
    """Logger widget with colored and expandable list items.
    Supports both horizontal and vertical placement and communicates with
    QSplitter to adjust its contents accordingly.
    """
    log_level_changed = pyqtSignal(str)

    ROOT_PATH = Path(os.getcwd()).parent
    DETAIL_INDENT_HTML = '\u00A0\u00A0'
    DETAIL_VIEW_CSS_STYLE = R"""
        div, span {font-size: 12px; background: transparent; border: 0px;}
        .msg_DEBUG {color:#808080;}
        .msg_INFO {color:#ddd;}
        .msg_SUCCESS {color:#2fff5d;}
        .msg_WARNING {color:#ffc52f;}
        .msg_ERROR {color:#e73f34;}
        .msg_CRITICAL {color:#ff2e67;}
        .level {font-size: 1px; color: transparent; width: 0px; }

        .detail, .traceback {color: #ddd; margin-top: 4px; border: 0px;}
        .traceback {font-size: 12px; font-weight: bold;}
        .detail {font-size: 12px; font-weight: bold;}

        .trace {font-size: 12px;}
        .trace.caret {color:#e54873;}
        .trace.line {color:#31b6e2;}
        .trace.file {color:#e8c35e;}
        .trace.location {color:#76a342;}
        .trace.exception, .trace.message {color:#f34965;}
    """

    class ResizeRequest(NamedTuple):
        size: int
        expand_only: bool = True

    resize_requested = pyqtSignal(ResizeRequest)

    HANDLER_POLL_INTERVAL = 500

    class Handler(logging.Handler, QObject):

        def __init__(self, parent: QWidget | None) -> None:
            super().__init__()
            QObject.__init__(self, parent)
            self._buffer: list[LogListData] = []
            self._buffer_lock = threading.Lock()

        def emit(self, record: logging.LogRecord) -> None:
            try:
                if not hasattr(record, "details"):
                    record.__dict__["details"] = ""
                log_list_data = LogListData.from_str(logs.shorten_str(self.format(record)))
                with self._buffer_lock:
                    self._buffer.append(log_list_data)
            except Exception as e:
                # print(f"Error in LoggerWidget.Handler.emit: {e}")
                pass

        def has_buffered_logs(self) -> bool:
            with self._buffer_lock:
                return bool(self._buffer)
        
        def get_and_clear_buffer(self) -> list[LogListData] | None:
            """Called by LoggerWidget to get current buffer and clear it."""
            batch = None
            with self._buffer_lock:
                if self._buffer:
                    batch = list(self._buffer)
                    self._buffer.clear()
            return batch

        def clear(self) -> None:
            with self._buffer_lock:
                self._buffer.clear()

        def close(self) -> None:
            super().close()

    @dataclass
    class DetailsPaneSizes:
        height: int = 120
        width: int = 300
        height_trace: int = 250
        width_trace: int = 400

    ICON_BAR_SIZE: int = 18
    MIN_HEIGHT: int = 48
    MIN_WIDTH: int = 180

    def __init__(self, parent: 'MainWindow', orientation: Qt.Orientation) -> None:
        super().__init__(orientation=orientation, parent=parent)
        self.cfg: Config[str, Any] = parent.cfg
        self.handler = LoggerWidget.Handler(self)
        self.orientation = orientation
        self._is_shutting_down = False
        self._clear_logs = True
        self._is_details_trace = True

        self.setPalette(get_main_window().get_palette_from_cfg())

        # --- CONTENT SECTION ---
        # Logger list
        self.list_widget = LogView(self)
        if self.orientation == LOGGER_BOTTOM:
            self.list_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
            self.list_widget.setMinimumHeight(50)
        else:
            self.list_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
            self.list_widget.setMinimumWidth(100)
        self.list_widget.selectionModel().currentChanged.connect(self.on_log_selection_changed)
        # Detail Pane
        self.details_pane: QTextBrowser = self.create_detail_view()
        self._details_pane_shown = False
        self._details_pane_sizes = self.DetailsPaneSizes()
        QTimer.singleShot(0, lambda: self.close_detail_pane(init_mode=True))
        # Logger | Detail splitter
        self.log_display_splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self.log_display_splitter.addWidget(self.list_widget)
        self.log_display_splitter.addWidget(self.details_pane)
        self.log_display_splitter.setMinimumSize(0, 0)
        if self.orientation == LOGGER_BOTTOM:
            self.log_display_splitter.setOrientation(Qt.Orientation.Horizontal)
        else:
            self.log_display_splitter.setOrientation(Qt.Orientation.Vertical)
        self.log_display_splitter.setHandleWidth(6)
        self.log_display_splitter.setCollapsible(0, True)
        self.log_display_splitter.setCollapsible(1, True)
        self.log_display_splitter.splitterMoved.connect(self.on_detail_splitter_moved)
        # --- END CONTENT SECTION ---

        # --- TOOLBAR SECTION ---
        self.toolbar = OrientationToolBar("Logger Controls", self)
        self.toolbar.setObjectName("loggerToolbar")
        self.warnings = LogStatus(level="WARNING", color=LogView.WARNING_COLOR, parent=self)
        self.errors = LogStatus(level="ERROR", color=LogView.ERROR_COLOR_BRIGHT, show_msg=True, parent=self)
        if self.orientation == LOGGER_RIGHT:
            self.errors.set_show_message(False)
        # Connect warnings and errors
        self.warnings.select_row.connect(self.on_select_row)
        self.errors.select_row.connect(self.on_select_row)
        self.list_widget.increment_warning.connect(self.warnings.add_message)
        self.list_widget.increment_error.connect(self.errors.add_message)

        # Log level combo
        self.log_level_choice = LabelCombo("", ("DEBUG", "INFO", "WARNING", "ERROR"),
                                           editable=False, activated_fn=self.on_log_level_changed)
        self.log_level_choice.setToolTip("How much information is shown in the logger")
        self.log_level_choice.setStatusTip("Log Level")
        self.log_level_choice.label.setFixedWidth(1)
        self.log_level_choice.entry.setFont(get_font("Hack, Consolas, monospace", 8, bold=True))
        self.log_level_choice.entry.setContentsMargins(0, 0, 0, 0)
        self.log_level_choice.entry.setFixedHeight(16)
        self.log_level_choice.setParent(self)

        # Add them to the OrientationToolbar with visibility rules
        self.toolbar.addOrientationWidget(self.warnings, Qt.Orientation.Horizontal | Qt.Orientation.Vertical)
        self.toolbar.addOrientationWidget(self.errors, Qt.Orientation.Horizontal | Qt.Orientation.Vertical)
        # Add a spacer to push the log level combo to the right in horizontal mode
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.toolbar.addOrientationWidget(spacer, Qt.Orientation.Horizontal)
        self.toolbar.addOrientationWidget(self.log_level_choice, Qt.Orientation.Horizontal)
        self.toolbar.setOrientation(Qt.Orientation.Horizontal)
        #self.toolbar.setOrientationMargins(horizontal=QtCore.QMargins(5, 2, 0, 2), vertical=QtCore.QMargins(0, 5, 0, 0))
        self.toolbar.setStyle(ToolbarSpacingProxyStyle(QStyleFactory.create('Fusion')))
        self.set_toolbar(self.toolbar)
        self.set_content(self.log_display_splitter)
        # --- END TOOLBAR SECTION ---

        self._handler_poll_timer = QtCore.QTimer(self)
        self._handler_poll_timer.setInterval(self.HANDLER_POLL_INTERVAL)
        self._handler_poll_timer.timeout.connect(self.poll_log_handler)

        if parent.file_widget:
            parent.file_widget.file_begin_open.connect(self.clear)
        parent.set_log_level.connect(self.on_log_level_changed)

        #self.snapped.connect(lambda collapsed: self.set_logging_speed("slow" if collapsed else "normal"))

    def showEvent(self, event: QShowEvent) -> None:
        self._is_shutting_down = False
        if not self._handler_poll_timer.isActive():
            self._handler_poll_timer.start()
        super().showEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.shutdown()
        super().closeEvent(event)

    def clear(self) -> None:
        if self._clear_logs:
            self.handler.clear()
            self.list_widget.clear()
            self.details_pane.clear()
            self.close_detail_pane()
            self.reset_warnings()
            self.reset_errors()

    def shutdown(self) -> None:
        self.errors.close()
        self.warnings.close()
        self.log_display_splitter.close()
        self._is_shutting_down = True
        if self._handler_poll_timer.isActive():
            self._handler_poll_timer.stop()
        # Stop any immediate activity in children if necessary
        if self.list_widget:
            # list_widget's own closeEvent will handle its timer,
            # but we can tell it to stop fetching explicitly too.
            self.list_widget.stopFetches()

    @property
    def is_shutting_down(self) -> bool:
        return self._is_shutting_down

    def expand(self) -> None:
        super().expand()
        self.set_logging_speed("normal")

    def collapse(self) -> None:
        super().collapse()
        self.set_logging_speed("slow")

    def make_visible(self) -> None:
        """Resize the logger to ensure the log console can be visible at min dimensions"""
        if not self.log_display_splitter.isVisible():
            self.set_logging_speed("normal")
            size = 0
            if self.orientation == LOGGER_BOTTOM:
                size = self.MIN_HEIGHT
                self.resize(self.width(), size)
            else:
                size = self.MIN_WIDTH
                self.resize(size, self.height())
            self.resize_requested.emit(self.ResizeRequest(size=size+self.ICON_BAR_SIZE))

    def create_detail_view(self):
        pal = self.palette()
        base_col = pal.base().color()
        text_col = pal.text().color()

        detail_view = QTextBrowser(self)
        detail_view.setObjectName("LogDetailViewPane")
        detail_view.setReadOnly(True)
        detail_view.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        detail_view.setMinimumSize(0, 0)
        #if self.orientation == LOGGER_BOTTOM:
        #    detail_view.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Ignored)
        #else:
        #    detail_view.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.MinimumExpanding)

        detail_view.setStyleSheet(detail_view.styleSheet() + qt_theme.style_modern_scrollbar(handle_color=text_col.darker(300).name(),
                                              view_bg_color=base_col.darker(110).name(), track_color=base_col.name()))
        detail_view.setFont(get_font("Hack, Consolas, monospace", 9))
        # Apply the stylesheet to the document of the QTextEdit
        detail_view.document().setDefaultStyleSheet(self.DETAIL_VIEW_CSS_STYLE)
        detail_view.document().setDefaultFont(get_font("Hack, Consolas, monospace", 9))
        detail_view.setOpenLinks(False)  # Handle anchor clicks manually
        detail_view.anchorClicked.connect(self.on_detail_link_clicked)
        return detail_view

    @staticmethod
    def color_traceback(escaped_text: str) -> str:
        """Basic coloring for tracebacks"""
        # Traceback (most recent call last)
        text = re.sub(r"(?m)^(Traceback.*:)$", r"<span class='trace message'>\g<1></span>", escaped_text)
        # Exception
        text = re.sub(r"(?m)^([A-Za-z0-9_\.]+):\s(.*?)$", r"<span class='trace exception'>\g<1>: \g<2></span>", text)
        # Caret underlines
        text = re.sub(r"([\^]+)", r"<span class='trace caret'>\g<0></span>", text)
        # Line numbers
        text = re.sub(r",(\sline\s[0-9]+),", r",<span class='trace line'>\g<1></span>,", text)
        # Filepath
        text = re.sub(r"(File\s&quot;.*?&quot;),", r"<span class='trace file'>\g<1></span>", text)
        # Method name
        text = re.sub(r"(?m),\sin\s(.*?)$", r", in <span class='trace location'>\g<1></span>", text)
        return text

    def format_raw_detail(self, raw_detail_str: str) -> str:
        if not raw_detail_str:
            return ""

        output_html_lines = []
        is_trace = raw_detail_str.strip().startswith("Traceback")
        self._is_details_trace = is_trace
        if is_trace:
            # Regex to identify file paths and line numbers in traceback lines
            # Captures: (Full match of "File ... line ..."), (File "path"), (path_only), (line_num_digits)
            file_link_segment_pattern = re.compile(r"""
                (File\s+"([^"]+)"(?:,\s*line\s*([0-9]+))?) # Group 1: Full "File...line..." part
                                                           # Group 2: Path within quotes
                                                           # Group 3: Line number digits
            """, re.VERBOSE)
            self.details_pane.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
            self.details_pane.setWordWrapMode(QTextOption.WrapMode.NoWrap)
            for raw_line in raw_detail_str.splitlines():
                # Separate leading whitespace from the actual content of the raw_line
                indent_raw = ""
                line_raw = raw_line
                match_indent = re.match(r"^(\s*)(.*)$", raw_line)
                if match_indent:
                    indent_raw = match_indent.group(1)
                    line_raw = match_indent.group(2)

                indent_html = html.escape(indent_raw)
                if is_trace:
                    indent_html = indent_html.replace(' ', '\u00A0')
                # Try to find the "File...line..." segment
                match = file_link_segment_pattern.match(line_raw)

                final_line_html = ""
                if match:
                    link_raw = match.group(1)  # e.g., File "path.py", line 123
                    file_raw = match.group(2)  # e.g., path.py
                    line_number_raw = match.group(3) if match.group(3) else "1"

                    abs_filepath = (self.ROOT_PATH / file_raw).as_posix()
                    href = f"code-goto:{abs_filepath}:{line_number_raw}"
                    # Trailing text after link
                    trailing_raw = line_raw[len(link_raw):]
                    # Process and color the link
                    link_html = html.escape(link_raw).replace(' ', '\u00A0')
                    colored_link_html = self.color_traceback(link_html) if is_trace else link_html
                    # Escape and color trailing text
                    trailing_html = html.escape(trailing_raw).replace(' ', '\u00A0')
                    colored_trailing_html = self.color_traceback(trailing_html) if is_trace else trailing_html
                    # Final colored link
                    final_line_html = f'<a href="{href}">{colored_link_html}</a>{colored_trailing_html}'
                else:
                    # No "File..." found, color the whole line_raw
                    line_html = html.escape(line_raw).replace(' ', '\u00A0')
                    final_line_html = self.color_traceback(line_html)

                output_html_lines.append(self.DETAIL_INDENT_HTML + indent_html + final_line_html)
        else:
            self.details_pane.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
            self.details_pane.setWordWrapMode(QTextOption.WrapMode.WordWrap)
            for raw_line in raw_detail_str.splitlines():
                output_html_lines.append(url_to_html(raw_line))

        full_content_html = "<br>".join(output_html_lines)
        div_class = 'traceback' if is_trace else 'detail'

        return f"<div class='{div_class}'>{full_content_html}</div>"

    def log_splitter_sizes(self, total_size: int) -> tuple[int, int]:
        """Returns the size of each side of the logger/details splitter."""
        current_sizes = self.log_display_splitter.sizes()
        total_size = sum(current_sizes)
        if len(current_sizes) != 2:
            return total_size, total_size // 4

        detail_height = self._details_pane_sizes.height_trace if self._is_details_trace else self._details_pane_sizes.height
        detail_width = self._details_pane_sizes.width_trace if self._is_details_trace else self._details_pane_sizes.width
        detail_size = detail_height if self.orientation == LOGGER_RIGHT else detail_width
        list_size = total_size - detail_size

        min_log_list_size = 150  # Min width/height for the log list view
        if self.log_display_splitter.orientation() == Qt.Orientation.Vertical:
            min_log_list_size = 100  # Min height if details are below

        if list_size < min_log_list_size:
            list_size = min_log_list_size
            detail_size = total_size - list_size

        if detail_size < 50:  # Ensure detail pane is at least somewhat visible if opened
            detail_size = 50
            if total_size - detail_size < min_log_list_size :  # Check again if main list will be too small
                list_size = min_log_list_size
                detail_size = total_size - list_size
            if detail_size < 0:
                detail_size = 0

        return list_size, detail_size
    
    def set_log_splitter_sizes(self) -> None:
        current_sizes = self.log_display_splitter.sizes()
        total_size = sum(current_sizes)
        if len(current_sizes) == 2:
            list_size, detail_size = self.log_splitter_sizes(total_size)
            self.log_display_splitter.setSizes([list_size, detail_size])

    def open_detail_pane(self) -> None:
        if self._details_pane_shown:
            return

        current_sizes = self.log_display_splitter.sizes()
        if len(current_sizes) == 2:
            total_size = sum(current_sizes)
            if total_size == 0:  # Splitter not yet sized
                QTimer.singleShot(50, self.open_detail_pane)  # Try again shortly
                return
            
            list_size, detail_size = self.log_splitter_sizes(total_size)

            #logging.debug(f"Opening detail pane. Total size: {total_size}, List size: {list_size}, Detail size: {detail_size}")
            if detail_size > 0:  # Only set if detail has some size
                self.log_display_splitter.setSizes([list_size, detail_size])
                self._details_pane_shown = True
            else:  # Cannot open if no space for detail
                self.close_detail_pane()  # Ensure it's marked closed

    def close_detail_pane(self, init_mode: bool = False):
        if not self._details_pane_shown and not init_mode:
            return
        current_sizes = self.log_display_splitter.sizes()
        if len(current_sizes) == 2 and (current_sizes[1] > 0 or init_mode):
            #logging.debug(f"Closing detail pane. Current sizes: {current_sizes}")
            self.log_display_splitter.setSizes([current_sizes[0] + current_sizes[1], 0])
        self._details_pane_shown = False
        if not init_mode and self._details_pane_shown:
            self.details_pane.clear()

    @pyqtSlot(str)
    def on_log_level_changed(self, level: str) -> None:
        """Slot for log level set internally (combo box) or externally (initial value from cfg)"""
        # Show successes still for "WARNING"
        actual_level = level if level != "SUCCESS" else "WARNING"
        if level == "WARNING":
            actual_level = "SUCCESS"
        # Set internally
        self.handler.setLevel(actual_level)
        self.log_level_choice.entry.setText(level)
        # Inform listeners
        self.log_level_changed.emit(actual_level)

    @pyqtSlot(QModelIndex, QModelIndex)
    def on_log_selection_changed(self, current: QModelIndex, previous: QModelIndex) -> None:
        if not current.isValid():
            self.close_detail_pane()
            self.details_pane.clear()  # Clear on no selection
            return

        raw_detail_text = current.data(LogModel.DETAIL)
        if raw_detail_text:
            formatted_html = self.format_raw_detail(str(raw_detail_text))
            self.details_pane.setHtml(formatted_html)
            if self._details_pane_shown:
                self.set_log_splitter_sizes()
            else:
                self.open_detail_pane()
        else:
            self.details_pane.clear()
            self.close_detail_pane()  # Close if no details to show

    @pyqtSlot(int, int)
    def on_detail_splitter_moved(self, pos: int, index: int) -> None:
        sizes = self.log_display_splitter.sizes()
        if len(sizes) == 2:
            details_pane_current_size = sizes[1]
            # Define a threshold for when the pane is considered meaningfully open
            open_threshold = 20 
            if details_pane_current_size > open_threshold:
                self._details_pane_size = details_pane_current_size
                self._details_pane_shown = True
            else:
                self._details_pane_shown = False
                # If user drags it very small, consider it closed for next programmatic open.
                # but don't set _details_pane_size to this small value.

    @pyqtSlot()
    def poll_log_handler(self) -> None:
        """Periodically called by _handler_poll_timer to check for new logs."""
        # Tell LogView to start fetching if it's not already running its timer and if it's in a state to fetch.
        if self.list_widget.canFetch() and self.handler.has_buffered_logs():
            #print("LoggerWidget: Handler has buffered logs. Triggering LogView to fetch.")
            if not self.list_widget.fetchTimer.isActive():
                self.list_widget.fetchTimer.start()
        if not self._handler_poll_timer.isActive():
            self._handler_poll_timer.start()

    @pyqtSlot(str)
    def set_logging_speed(self, speed_mode: Literal["fast", "normal", "slow"]) -> None:
        # Define your intervals
        intervals = {
            "fast"  : {"handler_poll": 100,  "view_fetch": 50},
            "normal": {"handler_poll": 500,  "view_fetch": 250},
            "slow"  : {"handler_poll": 2000, "view_fetch": 1000}
        }
        selected_intervals = intervals.get(speed_mode.lower(), intervals["normal"])

        # Update Handler Poll Timer in LoggerWidget
        self._current_handler_poll_interval = selected_intervals["handler_poll"]
        was_active = self._handler_poll_timer.isActive()
        if was_active:
            self._handler_poll_timer.stop()
        self._handler_poll_timer.setInterval(self._current_handler_poll_interval)
        if was_active:
            self._handler_poll_timer.start()
        #print(f"LoggerWidget: Handler poll interval set to {self._current_handler_poll_interval}ms.")

        if self.list_widget:
            self.list_widget.set_fetch_interval(selected_intervals["view_fetch"])

    @pyqtSlot(QUrl)
    def on_detail_link_clicked(self, url: QUrl):
        if not (QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier):
            return 

        if url.scheme() == "code-goto":
            full_target_spec = url.toString().split("code-goto:", 1)[1]
            path_parts = full_target_spec.rsplit(':', 1)
            target_filepath_str = ""
            target_line_number = "1"  # Default line

            if len(path_parts) == 2 and path_parts[1].isdigit():
                target_filepath_str = path_parts[0]
                target_line_number = path_parts[1]
            else:
                target_filepath_str = full_target_spec

            # Normalize the filepath for the current OS
            system_specific_filepath = os.path.normpath(target_filepath_str)
            preferred = self.cfg.get("preferred_editor", "VS Code")
            # Sort the list to move the preferred editor to the front
            editors_to_try = sorted(self.cfg.preferred_editor.options, key=lambda editor: editor != preferred)
            editor_launched_successfully = False
            for editor_key in editors_to_try:
                if editor_key not in EDITOR_CONFIGS.keys():
                    continue
                # Make a copy to avoid modifying the global config
                config = EDITOR_CONFIGS[editor_key].copy()
                editor_launched_successfully = launch_editor(
                    config,
                    system_specific_filepath,
                    target_line_number
                )
                if editor_launched_successfully:
                    break

            # Final Check
            if not editor_launched_successfully:
                if hasattr(self.parent(), 'showerror'):
                    self.parent().showerror("Failed to open file in editor. Please check editor or PATH settings.")
        elif url.scheme() in ["http", "https"]:
            QtGui.QDesktopServices.openUrl(url)

    @pyqtSlot(int)
    def on_select_row(self, row: int) -> None:
        """Handle logger visibility and scrolling on Jump To Warning/Error"""
        if row >= self.list_widget.count():
            return
        # Ensure row to scroll to is fetched
        while row >= self.list_widget.fetched_count():
            self.list_widget.fetchMore()
        # Ensure logger is visible
        self.make_visible()
        self.open_detail_pane()
        # Ensure row is visible
        index = self.list_widget.model().index(row, 0)
        self.list_widget.setCurrentIndex(index)
        self.list_widget.selectionModel().select(index, QItemSelectionModel.SelectionFlag.ClearAndSelect)
        self.list_widget.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)

    def toggle_clear_logs(self, enabled: bool):
        self._clear_logs = enabled

    def reset_warnings(self) -> None:
        self.warnings.clear()

    def reset_errors(self) -> None:
        self.errors.clear()


class LabelEdit(QWidget):
    def __init__(self, name, ):
        QWidget.__init__(self, )
        self.label = QLabel(name)
        self.label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        self.entry = QLineEdit()
        self.entry.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.entry.setTextMargins(3, 0, 3, 0)
        vbox = QHBoxLayout(self)
        vbox.addWidget(self.label)
        vbox.addWidget(self.entry)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)


class IconEdit(QWidget):

    search_text = pyqtSignal(str)

    def __init__(self, icon_name, default_str="", callback=None):
        QWidget.__init__(self, )
        self.label = QPushButton(get_icon(icon_name), "")
        self.label.setCheckable(False)
        self.label.setFlat(True)
        self.label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.entry = QLineEdit()
        self.entry.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        self.entry.setTextMargins(3, 0, 3, 0)
        vbox = QHBoxLayout(self)
        vbox.addWidget(self.label)
        vbox.addWidget(self.entry)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)
        self.entry.setMinimumWidth(140)
        self.entry.setPlaceholderText(default_str)
        self.setMinimumWidth(self.label.minimumWidth() + self.entry.minimumWidth())
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)

        if callback:
            self.typing_timer = QTimer()
            self.typing_timer.setSingleShot(True)
            self.typing_timer.timeout.connect(self.timer_up)
            self.entry.textChanged.connect(self.search_text_changed)
            self.search_text.connect(callback)

    def search_text_changed(self):
        # wait for 250 ms before
        self.typing_timer.start(250)

    def timer_up(self):
        # emit the text on the signal
        self.search_text.emit(self.entry.text())


class MouseWheelGuard(QObject):
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        if isinstance(object, QWidget):
            if event.type() == QEvent.Type.Wheel:
                if object.focusPolicy() == Qt.FocusPolicy.WheelFocus:
                    event.accept()
                    return False
                else:
                    event.ignore()
                    return True
            if event.type() == QEvent.Type.FocusIn and object.focusPolicy() == Qt.FocusPolicy.StrongFocus:
                object.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
            if event.type() == QEvent.Type.FocusOut and object.focusPolicy() == Qt.FocusPolicy.WheelFocus:
                object.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        return super().eventFilter(object, event)


class ClickGuard(QObject):
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        if isinstance(object, QWidget):
            if event.type() == QEvent.Type.MouseButtonPress:
                event.ignore()
                return True

        return super().eventFilter(object, event)


class DragDropPassthrough(QObject):
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.parent_widget = parent

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        if object.parent() == self.parent_widget and isinstance(self.parent_widget, QWidget):
            # Due to confusing inheritance between these QEvents, use type() for typing constraint
            # event.type() will not narrow the type for type checkers
            if type(event) is QDragMoveEvent:
                self.parent_widget.dragMoveEvent(event)
                return True
            elif type(event) is QDragEnterEvent:
                self.parent_widget.dragEnterEvent(event)
                return True
            elif type(event) is QDragLeaveEvent:
                self.parent_widget.dragLeaveEvent(event)
                return True
            elif type(event) is QDropEvent:
                self.parent_widget.dropEvent(event)
                return True

        return super().eventFilter(object, event)


class CleverCombo(QComboBox):
    """"A combo box that supports setting content (existing or new)"""

    def __init__(self, parent: Optional[QWidget] = None,
                 options: Optional[Iterable[str]] = None, allow_scroll: bool = False) -> None:
        super().__init__(parent)
        # Allow scroll events before clicking
        self.allow_scroll = allow_scroll
        if not allow_scroll:
            self.installEventFilter(MouseWheelGuard(self))
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        if options is not None:
            self.addItems(options)

    def setText(self, txt: str) -> None:
        flag = Qt.MatchFlag.MatchFixedString
        indx = self.findText(txt, flags=flag)
        # add new item if not found
        if indx == -1:
            self.addItem(txt)
            indx = self.findText(txt, flags=flag)
        self.setCurrentIndex(indx)


class NoScrollDoubleSpinBox(QDoubleSpinBox):
    """A double spin box that does not allow scrolling to change values until clicked"""

    def __init__(self, parent: Optional[QWidget] = None, allow_scroll: bool = False) -> None:
        super().__init__(parent)
        # Allow scroll events before clicking
        self.allow_scroll = allow_scroll
        if not allow_scroll:
            self.installEventFilter(MouseWheelGuard(self))
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)


class CheckableComboBox(QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def __init__(self, parent: Optional[QObject] = None, height: int = 20) -> None:
            super().__init__(parent)
            self.height = height

        def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
            size = super().sizeHint(option, index)
            size.setHeight(self.height)
            return size

    def __init__(self, parent: Optional[QWidget] = None,
                 item_height: int = 20, allow_scroll: bool = False) -> None:
        super().__init__(parent)
        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        # Allow scroll events before clicking
        self.allow_scroll = allow_scroll
        if not allow_scroll:
            self.installEventFilter(MouseWheelGuard(self))
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # store current selection
        self.texts: list[str] = []

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate(height=item_height))

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        if object == self.lineEdit():
            if isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = cast(QStandardItemModel, self.model()).item(index.row())

                if item.checkState() == Qt.CheckState.Checked:
                    item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    item.setCheckState(Qt.CheckState.Checked)
                return True
        return False

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        # Recompute text to elide as needed
        self.updateText()

    def timerEvent(self, event: QTimerEvent) -> None:
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def showPopup(self) -> None:
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self) -> None:
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def updateText(self) -> None:
        self.texts = []
        model = cast(QStandardItemModel, self.model())
        for i in range(model.rowCount()):
            if model.item(i).checkState() == Qt.CheckState.Checked:
                self.texts.append(model.item(i).text())
        text = ", ".join(self.texts)

        if len(self.texts) < 1:
            text = 'All known types'

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.TextElideMode.ElideRight, self.lineEdit().contentsRect().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text: str, data: Any = None) -> None: # type: ignore[override]
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemFlags(cast(Qt.ItemFlags, Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)))
        item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        cast(QStandardItemModel, self.model()).appendRow(item)

    def addItems(self, texts: Iterable[str], datalist: Optional[list[Any]] = None) -> None: # type: ignore[override]
        for i, text in enumerate(texts):
            if datalist is None:
                self.addItem(text)
            else:
                try:
                    data = datalist[i]
                except (TypeError, IndexError):
                    data = None
                self.addItem(text, data)
        self.updateText()

    def currentData(self, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        # Return the list of selected items data
        res = []
        model = cast(QStandardItemModel, self.model())
        for i in range(model.rowCount()):
            if model.item(i).checkState() == Qt.CheckState.Checked:
                res.append(model.item(i).data(role))
        return res


class OvlDataFilterProxy(QSortFilterProxyModel):
    """Base proxy class for OvlManagerWidget directory model"""

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super(OvlDataFilterProxy, self).__init__(parent)
        self.setDynamicSortFilter(True)
        self.setRecursiveFilteringEnabled(True)
        self.max_depth: int = 255
        self.root_idx: Optional[QModelIndex] = None
        self.root_depth: int = 0
        # self.test_str = "Init"

    def depth(self, index: QModelIndex) -> int:
        """Depth of the file or directory in the filesystem"""
        level = 0
        while index.parent().isValid():
            level += 1
            index = index.parent()
        return level

    def set_max_depth(self, depth: int) -> None:
        """Set max subfolder depth. 0 depth = ovldata root folders only."""
        self.max_depth = depth

    def update_root(self, index: QModelIndex) -> None:
        """Update root index and store base depth for ovldata subfolder"""
        self.root_idx = index
        self.root_depth = self.depth(index)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == QFileSystemModel.Roles.FileIconRole:
            model = cast("OvlDataFilesystemModel", self.sourceModel())
            finfo = model.fileInfo(index)
            return get_icon(finfo.suffix() if finfo.isFile() else "dir")
        return super().data(index, role)

    def setSourceModel(self, sourceModel: "OvlDataFilesystemModel") -> None: # type: ignore[override]
        super().setSourceModel(sourceModel)
        self.update_root(sourceModel.index(0, 0))

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if self.depth(parent) > self.max_depth + self.root_depth:
            # Hide children if they are beyond the specified depth.
            return 0
        return super().rowCount(parent)

    def hasChildren(self, parent: QModelIndex = QModelIndex()) -> bool:
        if self.depth(parent) > self.max_depth + self.root_depth:
            # Hide children if they are beyond the specified depth.
            return False
        return super().hasChildren(parent)

    @staticmethod
    def _human_key(key):
        parts = re.split('(\d*\.\d+|\d+)', key)
        return tuple((e.swapcase() if i % 2 == 0 else float(e)) for i, e in enumerate(parts))

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        """Change how QFileSystemModel sorts"""
        model = cast("OvlDataFilesystemModel", self.sourceModel())
        # dir before file
        if model.fileInfo(left).isDir() and not model.fileInfo(right).isDir():
            return True
        # file after dir
        if model.fileInfo(right).isDir() and not model.fileInfo(left).isDir():
            return False
        # same types
        return self._human_key(model.fileInfo(left).fileName()) < self._human_key(model.fileInfo(right).fileName())

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        model = cast("OvlDataFilesystemModel", self.sourceModel())
        idx = source_parent.child(source_row, 0)

        regex = self.filterRegularExpression()
        if not regex.pattern():
            return True

        # Do not filter if root_depth hasn't been set or for folders before ovldata
        if self.root_depth == 0 or self.depth(idx) <= self.root_depth:
            return True

        return regex.match(model.filePath(idx)).hasMatch()


class OvlDataFilesystemModel(QFileSystemModel):

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

    def map_index(self, index: QModelIndex) -> QModelIndex:
        """Map to source if applicable"""
        model = index.model()
        if isinstance(model, OvlDataFilterProxy):
            index = model.mapToSource(index)
        return index

    def fileIcon(self, index: QModelIndex) -> QIcon:
        return super().fileIcon(self.map_index(index))

    def fileInfo(self, index: QModelIndex) -> QFileInfo:
        return super().fileInfo(self.map_index(index))

    def fileName(self, index: QModelIndex) -> str:
        return super().fileName(self.map_index(index))

    def filePath(self, index: QModelIndex) -> str:
        return super().filePath(self.map_index(index))


class OvlDataTreeView(QTreeView):
    dir_dbl_clicked = pyqtSignal(str)
    file_dbl_clicked = pyqtSignal(str)
    def __init__(self, parent: Optional[QWidget] = None, actions={}, filters=()) -> None:
        super().__init__(parent)
        self.actions = actions
        self.file_model = OvlDataFilesystemModel()
        self.file_model.setNameFilters(filters)
        self.file_model.setNameFilterDisables(False)
        self.proxy = OvlDataFilterProxy(self)
        self.proxy.setSourceModel(self.file_model)
        self.setModel(self.proxy)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
        self.setExpandsOnDoubleClick(False)

        self.header().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        self.model().sort(self.header().sortIndicatorSection(), self.header().sortIndicatorOrder())
        self.setAnimated(False)
        self.setIndentation(12)
        self.setSortingEnabled(True)

        self.clicked.connect(self.item_clicked)
        self.doubleClicked.connect(self.item_dbl_clicked)

    def item_clicked(self, idx: QModelIndex) -> None:
        if not self.isExpanded(idx):
            self.expand(idx)

    def item_dbl_clicked(self, idx: QModelIndex) -> None:
        try:
            file_path = self.file_model.filePath(idx)
            # open folder in explorer
            if os.path.isdir(file_path):
                os.startfile(file_path)
                self.dir_dbl_clicked.emit(file_path)
            # open in tool
            else:
                self.file_dbl_clicked.emit(file_path)
        except:
            logging.exception("Item double-click failed")

    def set_root(self, dir_game: str) -> None:
        root_index = self.file_model.setRootPath(dir_game)
        self.setRootIndex(root_index)
        self.proxy.update_root(self.rootIndex())

    def get_root(self) -> str:
        return self.file_model.rootPath()

    def set_selected_path(self, file_path: str) -> None:
        """Select file_path in dirs view"""
        try:
            self.setCurrentIndex(self.file_model.index(file_path))
        except:
            logging.exception("Setting dir failed")

    def get_selected_dir(self) -> str:
        file_path = self.file_model.filePath(self.currentIndex())
        # if a file is selected, get its containing dir
        return file_path if os.path.isdir(file_path) else os.path.dirname(file_path)

    def set_regex(self, regex):
        if regex:
            # expand to also filter folders have not been opened before - sometimes slow but easy
            self.expandAll()
        self.proxy.setFilterRegularExpression(QRegularExpression(regex,
                                                                 options=QRegularExpression.PatternOption.CaseInsensitiveOption))

    def map_index(self, index: QModelIndex) -> QModelIndex:
        """Map from source if applicable"""
        source_model = index.model()
        if isinstance(source_model, OvlDataFilesystemModel):
            model = cast(OvlDataFilterProxy, self.model())
            index = model.mapFromSource(index)
        return index

    def setCurrentIndex(self, index: QModelIndex) -> None:
        return super().setCurrentIndex(self.map_index(index))

    def setRootIndex(self, index: QModelIndex) -> None:
        return super().setRootIndex(self.map_index(index))

    def isIndexHidden(self, index: QModelIndex) -> bool:
        return super().isIndexHidden(self.map_index(index))

    def indexAbove(self, index: QModelIndex) -> QModelIndex:
        return super().indexAbove(self.map_index(index))

    def indexBelow(self, index: QModelIndex) -> QModelIndex:
        return super().indexAbove(self.map_index(index))

    def scrollTo(self, index: QModelIndex,
                 hint: QAbstractItemView.ScrollHint = QAbstractItemView.ScrollHint.EnsureVisible) -> None:
        return super().scrollTo(self.map_index(index), hint)

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()
        index = self.indexAt(event.pos())
        if index.isValid():
            if self.actions:
                menu.addSection("Batch Process")
                for action, func in self.actions.items():
                    menu.addAction(action)
                res = menu.exec_(event.globalPos())
                if res in self.actions:
                    func = self.actions[res]
                    func()


class GameSelectorWidget(QWidget):
    installed_game_chosen = pyqtSignal(str)
    def __init__(self, parent):
        super().__init__(parent)
        self.cfg: dict[str, Any] = parent.cfg
        self.games_list = [g.value for g in games]
        self.entry = CleverCombo(self, options=[])
        self.entry.setEditable(False)
        self.entry.setToolTip("Select game for easy access")

        self.play_button = QPushButton(get_icon("play"), "")
        self.play_button.setMaximumWidth(20)
        self.play_button.setToolTip("Run the currently selected game")
        self.play_button.setShortcut("CTRL+P")

        self.add_button = QPushButton(get_icon("bookmarks"), "")
        self.add_button.setMaximumWidth(20)
        self.add_button.setToolTip("Add a game from a folder to the list of games")

        vbox = QHBoxLayout(self)
        vbox.addWidget(self.entry)
        vbox.addWidget(self.play_button)
        vbox.addWidget(self.add_button)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.set_games()

        self.entry.textActivated.connect(self.game_chosen)
        self.add_button.clicked.connect(self.add_installed_game_manually)
        self.play_button.clicked.connect(self.run_selected_game)

    def set_data(self, available_games: dict) -> None:
        self.entry.clear()
        sorted_games = sorted(available_games.items())

        # Query the style for the pixel metric of a small icon
        style = self.entry.style()
        icon_size = style.pixelMetric(QStyle.PM_SmallIconSize)

        self.entry.clear()
        for game, ovldata in sorted_games:
            icon = get_exe_icon(game, get_exe_from_ovldata(ovldata), icon_size)
            if not icon.isNull():
                self.entry.addItem(icon, game)
            else:
                self.entry.addItem(game)
        # update currently selected item
        if sorted_games:
            # get the current game from cfg, and fall back to first of the list if needed
            current_game = self.cfg.get("current_game", sorted_games[0][0])
            self.entry.setText(current_game)

    def get_selected_game(self) -> str:
        return self.entry.currentText()

    def run_selected_game(self):
        selected_game = self.get_selected_game()
        launch_game(selected_game, self.cfg)

    def ask_game_dir(self) -> str:
        """Ask the user to specify a game root folder"""
        return QFileDialog.getExistingDirectory(self, "Open game folder")

    def set_games(self) -> None:
        if "games" not in self.cfg:
            self.cfg["games"] = {}
        self.cfg["games"].update(get_steam_games(self.games_list))
        self.set_data(self.cfg["games"])

    def game_chosen(self, game: str) -> None:
        """Run after choosing a game from dropdown of installed games"""
        self.cfg["current_game"] = game
        # only update the ovl game version choice if it is a valid game
        if game in self.games_list:
            self.installed_game_chosen.emit(game)

    def add_installed_game_manually(self) -> None:
        """Manually add a new game to the list of available games. Works for both game root or ovldata folders"""
        dir_game = self.ask_game_dir()
        if dir_game:
            dir_game = os.path.normpath(dir_game)
            # try to find the name of the game by stripping usual suffixes, eg. "win64\\ovldata"
            pattern = re.compile(r"\\win64\\ovldata", re.IGNORECASE)
            without_suffix = pattern.sub("", dir_game)
            current_game = os.path.basename(without_suffix)
            # suffix the dir without suffix again and store that if it exists
            added_suffix = os.path.join(without_suffix, "win64", "ovldata")
            if os.path.isdir(added_suffix):
                dir_game = added_suffix
            # store this newly chosen game in cfg
            self.cfg["games"][current_game] = dir_game
            # update available games
            self.set_data(self.cfg["games"])
            self.game_chosen(current_game)


class OvlSearchWidget(QWidget):
    search_content_clicked = pyqtSignal(str)
    def __init__(self, parent):
        super().__init__(parent)
        self.entry = QLineEdit("")
        self.entry.setPlaceholderText("Search Archives")
        self.button = QPushButton(get_icon("search"), "")
        for btn in (self.entry, self.button):
            btn.setToolTip("Search OVL archives for uses of this string")
        vbox = QHBoxLayout(self)
        vbox.addWidget(self.button)
        vbox.addWidget(self.entry)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.button.clicked.connect(self.search_button_clicked)
        self.entry.returnPressed.connect(self.search_button_clicked)
        self.entry.textChanged.connect(self.force_lowercase)

    def force_lowercase(self, text):
        self.entry.setText(text.lower())

    def search_button_clicked(self):
        search_txt = self.entry.text()
        if search_txt:
            self.search_content_clicked.emit(search_txt)


class OvlFilterWidget(QWidget):
    
    filter_regex = pyqtSignal(str)
    
    def __init__(self, parent):
        super().__init__(parent)
        self.filter_entry = IconEdit("filter", "Filter OVL Files", callback=self.set_filter)
        self.filter_entry.setToolTip("Filter by name - only show items matching this name")
        self.show_official_button = IconButton("ovl")
        self.show_modded_button = IconButton("modded")
        self.show_official_button.setCheckable(True)
        self.show_modded_button.setCheckable(True)
        self.show_official_button.setToolTip("Show official OVLs only")
        self.show_modded_button.setToolTip("Show modded OVLs only")

        self.show_official_button.toggled.connect(self.show_official_toggle)
        self.show_modded_button.toggled.connect(self.show_modded_toggle)
        
        vbox = QHBoxLayout(self)
        vbox.addWidget(self.show_official_button)
        vbox.addWidget(self.show_modded_button)
        vbox.addWidget(self.filter_entry)
        vbox.setContentsMargins(0, 0, 0, 0)

    def show_modded_toggle(self, checked: bool) -> None:
        if checked:
            self.filter_entry.entry.setText("")
            self.show_official_button.setChecked(False)
            self.filter_regex.emit(f"^((?!({'|'.join(valid_packages)})).)*$")
        else:
            self.filter_regex.emit("")

    def show_official_toggle(self, checked: bool) -> None:
        if checked:
            self.filter_entry.entry.setText("")
            self.show_modded_button.setChecked(False)
            self.filter_regex.emit(f"^.*({'|'.join(valid_packages)}).*$")
        else:
            self.filter_regex.emit("")

    def set_filter(self):
        filter_str = self.filter_entry.entry.text()
        if filter_str:
            # turn off the other filters if a filter search string was entered
            self.show_modded_button.setChecked(False)
            self.show_official_button.setChecked(False)
            # set filter function for search string
            self.filter_regex.emit(f"^.*({filter_str}).*$")
        else:
            self.filter_regex.emit("")


class OvlManagerWidget(QWidget):
    """Installed games combo box with optional search and directory widgets (caller has to add them to layout)"""
    def __init__(self, parent: "MainWindow",
                 filters: Optional[list[str]] = None,
                 game_chosen_fn: Optional[Callable] = None,
                 dir_dbl_click_fn: Optional[Callable] = None,
                 file_dbl_click_fn: Optional[Callable] = None,
                 search_content_fn: Optional[Callable] = None,
                 actions: dict = {}) -> None:
        super().__init__(parent)
        self.cfg: dict[str, Any] = parent.cfg

        self.game_choice = GameSelectorWidget(self)
        self.game_choice.installed_game_chosen.connect(self.set_selected_game)

        self.search = OvlSearchWidget(self)

        if filters is None:
            filters = ["*.ovl", ]
        self.dirs = OvlDataTreeView(actions=actions, filters=filters)

        self.filters = OvlFilterWidget(self)
        self.filters.filter_regex.connect(self.dirs.set_regex)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.search)
        vbox.addWidget(self.filters)
        vbox.addWidget(self.dirs)
        vbox.addWidget(self.game_choice)
        vbox.setContentsMargins(0, 0, 0, 0)

        if game_chosen_fn is not None:
            self.game_choice.installed_game_chosen.connect(game_chosen_fn)
        if dir_dbl_click_fn is not None:
            self.dirs.dir_dbl_clicked.connect(dir_dbl_click_fn)
        if file_dbl_click_fn is not None:
            self.dirs.file_dbl_clicked.connect(file_dbl_click_fn)
        if search_content_fn is not None:
            self.search.search_content_clicked.connect(search_content_fn)

    def set_selected_game(self, game: str = None):
        # if current_game hasn't been set (no config.json), fall back on currently selected game
        if not game:
            game = self.game_choice.get_selected_game()
        dir_game = self.cfg["games"].get(game, None)
        # if current_game has been set, assume it exists in the games dict too (from steam)
        if dir_game:
            self.dirs.set_root(dir_game)
            self.dirs.set_selected_path(self.cfg.get("last_ovl_in", None))
            self.game_choice.entry.setText(game)


class EditCombo(QWidget):
    entries_changed = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)
        self.add_button = QPushButton("+")
        self.add_button.setToolTip("Add Item")
        self.add_button.clicked.connect(self.add)
        self.delete_button = QPushButton("-")
        self.delete_button.setToolTip("Delete Item")
        self.delete_button.clicked.connect(self.delete)
        self.add_button.setMaximumWidth(20)
        self.delete_button.setMaximumWidth(20)
        self.entry = QComboBox()
        self.entry.setEditable(True)
        self.vbox = QHBoxLayout(self)
        self.vbox.addWidget(self.entry)
        self.vbox.addWidget(self.add_button)
        self.vbox.addWidget(self.delete_button)
        self.vbox.setContentsMargins(0, 0, 0, 0)

    @property
    def items(self):
        return [self.entry.itemText(i) for i in range(self.entry.count())]

    def add(self, _checked=False, text=None):
        name = self.entry.currentText() if text is None else text
        if name and name not in self.items:
            self.entry.addItem(name)
            self.entries_changed.emit(self.items)

    def delete(self):
        name = self.entry.currentText()
        if name:
            ind = self.entry.findText(name)
            self.entry.removeItem(ind)
            self.entries_changed.emit(self.items)

    def set_data(self, items):
        items = sorted(set(items))
        self.entry.clear()
        self.entry.addItems(items)


class RelativePathCombo(EditCombo):

    def __init__(self, parent, file_widget, dtype="OVL"):
        super().__init__(parent)
        self.file = file_widget
        self.dtype = dtype.lower()
        self.icon = QPushButton()
        self.icon.setIcon(get_icon("dir"))
        self.icon.setFlat(True)
        self.icon.setToolTip("Open OVL file to include")
        self.icon.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.icon.pressed.connect(self.ask_open)
        self.entry.setAcceptDrops(True)
        self.entry.dropEvent = self.dropEvent
        self.entry.dragMoveEvent = self.dragMoveEvent
        self.entry.dragEnterEvent = self.dragEnterEvent
        self.vbox.insertWidget(0, self.icon)

    @property
    def items(self) -> list[str]:
        return [os.path.normpath(self.entry.itemText(i)) for i in range(self.entry.count())]

    @property
    def root(self):
        return os.path.dirname(self.file.filepath)

    def relative_path(self, path):
        return os.path.normpath(os.path.relpath(path, self.root))

    def accept_file(self, filepath):
        if os.path.isfile(filepath):
            if os.path.splitext(filepath)[1].lower() in (f".{self.dtype}",):
                return True
        return False

    def decide_add(self, filepath):
        if self.accept_file(filepath):
            path = self.relative_path(filepath)
            self.add(text=path)
            self.entry.setCurrentIndex(self.items.index(path))

    def ask_open(self):
        if self.file.filepath:
            filepath, _ = QFileDialog.getOpenFileName(self, f'Choose {self.dtype}', self.root, f"{self.dtype} files (*.{self.dtype})")
            self.decide_add(filepath)

    def get_files(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            return urls

    def accept_ignore(self, event):
        if self.file.filepath and self.get_files(event):
            event.acceptProposedAction()
            self.setFocus(True)
            return
        event.ignore()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        self.accept_ignore(event)

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        self.accept_ignore(event)

    def dropEvent(self, event: QDropEvent) -> None:
        urls = self.get_files(event)
        if urls:
            self.decide_add(str(urls[0].path())[1:])


class LabelCombo(QWidget):
    def __init__(self, name: str, options: Iterable[str], editable: bool = True, changed_fn: Optional[Callable] = None,
                 activated_fn: Optional[Callable] = None) -> None:
        QWidget.__init__(self, )
        self.label = QLabel(name)
        self.entry = CleverCombo(self, options=options)
        self.entry.setEditable(editable)
        box = QHBoxLayout(self)
        box.addWidget(self.label)
        box.addWidget(self.entry)
        box.setContentsMargins(0, 0, 0, 0)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # # sizePolicy.setHeightForWidth(self.entry.sizePolicy().hasHeightForWidth())
        self.entry.setSizePolicy(sizePolicy)
        self.setSizePolicy(sizePolicy)

        if changed_fn is not None:
            self.entry.currentTextChanged.connect(changed_fn)
        if activated_fn is not None:
            self.entry.textActivated.connect(activated_fn)


class MySwitch(QPushButton):
    PRIMARY = QColor(53, 53, 53)
    SECONDARY = QColor(35, 35, 35)
    OUTLINE = QColor(122, 122, 122)
    TERTIARY = QColor(42, 130, 218)
    BLACK = QColor(0, 0, 0)
    WHITE = QColor(255, 255, 255)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(66)
        self.setMinimumHeight(22)

    def setValue(self, v):
        self.setChecked(v)

    def paintEvent(self, _event: QPaintEvent) -> None:
        label = "ON" if self.isChecked() else "OFF"
        bg_color = self.TERTIARY if self.isChecked() else self.PRIMARY

        radius = 10
        width = 32
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(self.SECONDARY)

        pen = QPen(self.WHITE)
        pen.setWidth(0)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2 * width, 2 * radius), radius, radius)
        painter.setBrush(QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2 * radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignmentFlag.AlignCenter, label)


class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)

        self.toggle_button = QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QFrame.Shape.NoFrame)

        pack_in_box(
            self.toggle_button,
            self.content_area
        )

        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    @pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            Qt.ArrowType.DownArrow if not checked else Qt.ArrowType.RightArrow
        )
        self.toggle_animation.setDirection(
            QAbstractAnimation.Direction.Forward
            if not checked
            else QAbstractAnimation.Direction.Backward
        )
        self.toggle_animation.start()

    def setLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
                self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(100)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(100)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


class MatcolFloatAttrib:
    def __init__(self, attrib, tooltips={}):
        """attrib must be pyffi matcol InfoWrapper object"""
        self.attrib = attrib
        name = attrib.attrib_name.data
        self.label = QLabel(name)

        self.data = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        buttons = [self.create_field(i) for i, v in enumerate(attrib.flags) if v]
        for button in buttons:
            layout.addWidget(button)
        self.data.setLayout(layout)
        # get tooltip
        tooltip = tooltips.get(name, "Undocumented attribute.")
        self.data.setToolTip(tooltip)
        self.label.setToolTip(tooltip)

    def create_field(self, ind):
        default = self.attrib.value[ind]

        def update_ind(v):
            # use a closure to remember index
            # print(self.attrib, ind, v)
            self.attrib.value[ind] = v

        # always float
        field = QDoubleSpinBox()
        field.setDecimals(3)
        field.setRange(-10000, 10000)
        field.setSingleStep(.05)
        field.valueChanged.connect(update_ind)

        field.setValue(default)
        field.setMinimumWidth(50)
        field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        field.setContentsMargins(0, 0, 0, 0)
        return field


class QColorButton(QPushButton):
    '''
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).
    '''

    colorChanged = pyqtSignal(object)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._color: QColor = QColor()
        self.setMaximumWidth(32)
        self.pressed.connect(self.onColorPicker)
        QDir.addSearchPath("icon", self.get_icon_dir())

    def get_icon_dir(self) -> str:
        return os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "icons")

    def setColor(self, color) -> None:
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)

        if self._color:
            self.setStyleSheet(f"""QColorButton {{
                background-color: {self._color.name(QColor.NameFormat.HexArgb)};
                border: 0px;
                min-width: 100px;
                min-height: 22px;
                border-radius: 3px;
            }}""")
        else:
            self.setStyleSheet("")

    def color(self) -> QColor:
        return self._color

    def onColorPicker(self) -> None:
        '''
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        '''
        dlg = QColorDialog(self)
        dlg.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if self._color:
            dlg.setCurrentColor(self._color)
        if dlg.exec_():
            self.setColor(dlg.currentColor())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            self.setColor(None)

        return super().mousePressEvent(event)

    def setValue(self, c) -> None:
        self.setColor(QColor(c.r, c.g, c.b, c.a))

    def getValue(self, ) -> None:
        if self._color:
            print(self._color.getRgb())


class FileDirWidget(QWidget):
    dir_opened = pyqtSignal(str)
    filepath_changed = pyqtSignal(str, bool)

    def __init__(self, parent: QWidget, cfg: dict, cfg_key: str, ask_user: bool = True, editable: bool = False,
                 check_exists: bool = False, root: Optional[str] = None) -> None:
        super().__init__(parent)
        self.mainWidget = parent
        self.ftype = cfg_key
        self.cfg_key = cfg_key.lower()
        self.root = root
        self.cfg = cfg
        self.cfg.setdefault(self.cfg_last_dir_open, "C:/")
        self.cfg.setdefault(self.cfg_last_dir_save, "C:/")
        self.cfg.setdefault(self.cfg_last_file_open, "C:/")
        self.cfg.setdefault(self.cfg_recent_files, [])

        self.ask_user = ask_user
        self.check_exists = check_exists
        self.filepath = ""
        self.basename = ""
        # Whether data associated with this filepath has been modified
        self.dirty = False

        self.icon = QPushButton(self)
        self.icon.setIcon(get_icon("dir"))
        self.icon.setFlat(True)
        self.entry = QLineEdit(self)
        self.entry.setDragEnabled(True)
        self.entry.setTextMargins(3, 0, 3, 0)
        self.editable = editable
        if editable:
            # Icon still clickable
            self.icon.clicked.connect(self.ask_open)
            self.entry.textChanged.connect(self.check_file)
        else:
            self.entry.setReadOnly(True)
            self.entry.installEventFilter(ClickGuard(self))
            self.icon.installEventFilter(ClickGuard(self))

        self.icon.installEventFilter(DragDropPassthrough(self))
        self.entry.installEventFilter(DragDropPassthrough(self))

        self.qgrid = QGridLayout()
        self.qgrid.setContentsMargins(0, 0, 0, 0)
        self.qgrid.addWidget(self.icon, 0, 0)
        self.qgrid.addWidget(self.entry, 0, 1)
        self.setLayout(self.qgrid)

    @property
    def filename(self) -> str:
        return self.basename

    @filename.setter
    def filename(self, filename: str) -> None:
        self.basename = filename

    @property
    def ftype_lower(self) -> str:
        return self.ftype.lower()

    @property
    def cfg_last_dir_open(self) -> str:
        return f"dir_{self.cfg_key}s_in"

    @property
    def cfg_last_dir_save(self) -> str:
        return f"dir_{self.cfg_key}s_out"

    @property
    def cfg_last_file_open(self) -> str:
        return f"last_{self.cfg_key}_in"

    @property
    def cfg_recent_files(self) -> str:
        return f"recent_{self.cfg_key}_in"

    def cfg_path(self, cfg_str: str) -> str:
        return self.cfg.get(cfg_str, "C://") if not self.root else self.root

    def get_files(self, event: QDropEvent) -> list[QUrl]:
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            return urls
        return []

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if self.get_files(event):
            event.acceptProposedAction()
            self.setFocus()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if self.get_files(event):
            event.acceptProposedAction()
            self.setFocus()

    def setText(self, text: str) -> None:
        self.entry.setText(text)
        # Keep front of path visible when small
        self.entry.setCursorPosition(0)

    def setPlaceholderText(self, text: str) -> None:
        self.entry.setPlaceholderText(text)

    def set_modified(self, dirty: bool) -> None:
        self.dirty = dirty
        if self.filepath:
            self.filepath_changed.emit(self.filepath, self.dirty)


class FileWidget(FileDirWidget):
    """An entry widget that starts a file selector when clicked and also accepts drag & drop.
    Displays the current file's basename.
    """
    file_begin_open = pyqtSignal(str)
    file_opened = pyqtSignal(str)
    file_saved = pyqtSignal(str)

    def __init__(self, parent: QWidget, cfg: dict, ftype: str = "OVL", ask_user: bool = True, editable: bool = False,
                 check_exists: bool = False, root: Optional[str] = None) -> None:
        super().__init__(parent=parent, cfg=cfg, cfg_key=ftype, ask_user=ask_user,
                         editable=editable, check_exists=check_exists, root=root)

        self.icon.setToolTip("Click to select a file")
        self.entry.setToolTip(self.tooltip_str)

    @property
    def files_filter_str(self) -> str:
        return f"{self.ftype} files (*.{self.ftype_lower})"

    @property
    def tooltip_str(self) -> str:
        return f"Currently open {self.ftype} file: {self.filepath}" if self.filepath else f"Open {self.ftype} file"

    def is_open(self) -> bool:
        if self.filename or self.dirty:
            return True
        self.mainWidget.showwarning("You must open a file first!")
        return False

    def may_open_new_file(self, new_filepath: str) -> bool:
        if self.ask_user and self.filepath and self.dirty:
            msg = f"Do you want to discard unsaved work on {os.path.basename(self.filepath)} to open {os.path.basename(new_filepath)}?"
            return self.mainWidget.showdialog(msg, title="Unsaved Changes", buttons=(QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel))
        return True

    def open_file(self, filepath: str) -> bool:
        if self.may_open_new_file(filepath):
            self.file_begin_open.emit(filepath)
            self.set_file_path(filepath)
            self.cfg[self.cfg_last_dir_open] = self.dir
            self.cfg[self.cfg_last_file_open] = self.filepath
            recent_files = self.cfg[self.cfg_recent_files]
            if self.filepath in recent_files:
                recent_files.remove(self.filepath)
            recent_files.insert(0, self.filepath)
            while len(recent_files) > self.cfg.get("num_recent", 5):
                recent_files.pop(-1)
            self.file_opened.emit(filepath)
            return True
        return False

    def set_file_path(self, filepath: str) -> None:
        self.filepath = filepath
        self.dir, self.filename = os.path.split(filepath)
        self.setText(self.filename)
        self.check_file(self.filename)
        self.entry.setToolTip(self.tooltip_str)
        self.filepath_changed.emit(self.filepath, self.dirty)

    def check_file(self, name: str) -> None:
        if self.check_exists:
            is_file = Path(os.path.join(self.root if self.root else self.dir, name)).is_file()
            self.entry.setToolTip("" if is_file else "Warning: File does not exist. This is OK if the file is external/shared.")
            self.entry.setStyleSheet("" if is_file else "QLineEdit { color: rgba(168, 168, 64, 255); background-color: rgba(44, 44, 30, 255); }")

    def accept_file(self, filepath: str) -> bool:
        """Check if filepath exists and is of the expected file extension"""
        if os.path.isfile(filepath):
            ext = os.path.splitext(filepath)[1].lower()
            if ext == f".{self.ftype_lower}":
                return self.open_file(filepath)
            else:
                self.mainWidget.showwarning(f"Unsupported File Format '{ext}'")
        return False

    def accept_dir(self, dirpath: str) -> bool:
        """Check if dirpath exists"""
        return os.path.isdir(dirpath)

    def dropEvent(self, event: QDropEvent) -> None:
        urls = self.get_files(event)
        if urls:
            filepath = str(urls[0].path())[1:]
            self.open_file(filepath)

    def ask_open(self) -> None:
        filepath = self.get_open_file_name()
        if filepath:
            self.open_file(filepath)

    def get_open_file_name(self, title=None):
        title = title if title else f'Load {self.ftype}'
        filepath = QFileDialog.getOpenFileName(
            self, title, self.cfg_path(self.cfg_last_dir_open), self.files_filter_str)[0]
        return filepath

    def ask_open_dir(self) -> None:
        # TODO: This is generally confusing for something named FileWidget
        #       although it is no longer hardcoded for OVL Tool
        dirpath = QFileDialog.getExistingDirectory(directory=self.cfg_path(self.cfg_last_dir_open))
        if self.accept_dir(dirpath):
            self.dir_opened.emit(dirpath)
            # Store the parent directory so that the next File > New
            # opens in root to allow selection of sibling folders.
            self.cfg[self.cfg_last_dir_open], _ = os.path.split(dirpath)
            # just set the name, do not trigger a loading event
            self.set_file_path(f"{dirpath}.{self.ftype_lower}")

    def ask_save_as(self) -> None:
        """Saves file, always ask for file path"""
        if self.is_open():
            suggested_file_path = os.path.join(self.cfg_path(self.cfg_last_dir_save), self.filename)
            filepath = QFileDialog.getSaveFileName(
                self, f'Save {self.ftype}', suggested_file_path, self.files_filter_str)[0]
            if filepath:
                self.cfg[self.cfg_last_dir_save], _ = os.path.split(filepath)
                self.set_file_path(filepath)
                self.file_saved.emit(filepath)

    def ask_save(self) -> None:
        """Saves file, overwrite if path has been set, else ask"""
        if self.is_open():
            # do we have a filename already?
            if self.filepath:
                self.file_saved.emit(self.filepath)
            # nope, ask user - modified, but no file name yet
            else:
                self.ask_save_as()

    def mousePressEvent(self, _event: QMouseEvent) -> None:
        if not self.editable:
            self.ask_open()


# Creates a dir widget, same as file but for directories
class DirWidget(FileDirWidget):
    """An entry widget that starts a file selector when clicked and also accepts drag & drop.
    Displays the current file's basename.
    """

    def __init__(self, parent: QWidget, cfg: dict, cfg_key: str = "DIR", ask_user: bool = True) -> None:
        super().__init__(parent=parent, cfg=cfg, cfg_key=cfg_key, ask_user=ask_user)

    def open_dir(self, filepath: str) -> None:
        if not self.accept_dir(filepath):
            logging.warning(f"{filepath} could not be opened as a directory.")

    def ask_open_dir(self) -> None:
        filepath = QFileDialog.getExistingDirectory(directory=self.cfg_path(self.cfg_last_dir_open))
        if self.accept_dir(filepath):
            pass

    def accept_dir(self, dirpath: str) -> bool:
        if os.path.isdir(dirpath):
            self.filepath = dirpath
            self.cfg[self.cfg_last_dir_open], self.basename = os.path.split(dirpath)
            self.setText(dirpath)
            self.dir_opened.emit(dirpath)
            return True
        return False

    def dropEvent(self, event: QDropEvent) -> None:
        urls = self.get_files(event)
        if urls:
            filepath = str(urls[0].path())[1:]
            self.open_dir(filepath)

    def mousePressEvent(self, _event: QMouseEvent) -> None:
        self.ask_open_dir()


class StatusSpacer(QWidget):
    """Right aligns permanent status widgets to another widget by providing a dynamic,
    preferred-size space."""
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.widget: QWidget | None = None
        self._preferred_width = 0

    def sizeHint(self) -> QSize:
        """
        Overrides the default sizeHint to report our dynamic preferred width.
        """
        return QSize(self._preferred_width, super().sizeHint().height())

    def set_widget(self, widget: QWidget) -> None:
        """Connects to the signal that provides the width for alignment."""
        self.widget = widget
        if hasattr(widget, "current_size"):
            widget.current_size.connect(self.resize)

    def showEvent(self, a0):
        super().showEvent(a0)
        if self.widget:
            QTimer.singleShot(0, lambda: self.resize(self.widget.size()))

    def resize(self, size: Union[QSize, int] = QSize(-1, -1), _h: int = 0) -> None:
        """
        This slot receives the new size, updates the preferred width, and tells
        the layout to re-evaluate everything safely.
        """
        parent = self.parent()
        if isinstance(size, QSize) and isinstance(parent, QStatusBar):
            new_width = max(1, size.width() - 20)
            sibling_width = 0
            for item in parent.children():
                if isinstance(item, QWidget) and not isinstance(item, StatusSpacer) and item.isVisible():
                    sibling_width += item.width()

            # If no room, or LOGGER_BOTTOM, spacer will be 0 width
            if new_width + sibling_width >= parent.width():
                new_width = 0

            # Only update if the width has actually changed.
            if self._preferred_width != new_width:
                self._preferred_width = new_width
                # Invalidate the old size hint and trigger a layout update.
                # This asks the layout to recalculate without forcing a resize.
                self.updateGeometry()


class WalkerDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None, title: str = "", walk_dir: str = "") -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        # Directory selector
        self.dir_widget = DirWidget(self, {})
        self.dir_widget.entry.setMinimumWidth(480)
        if walk_dir:
            self.dir_widget.open_dir(walk_dir)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.dir_widget)

        # Empty options area for external use
        self.options = QGridLayout()
        vbox.addLayout(self.options)

        # Buttons bar
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        self.chk_ovls = QCheckBox("Extract OVLs")
        self.chk_ovls.setChecked(True)

        self.chk_official = QCheckBox("Official Only")
        self.chk_official.setChecked(True)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        hbox.addWidget(self.chk_ovls)
        hbox.addWidget(self.chk_official)
        hbox.addSpacerItem(QSpacerItem(1, 16, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed))
        hbox.addWidget(self.buttons)

    @property
    def walk_dir(self):
        return self.dir_widget.filepath

    def addWidget(self, widget: QWidget, row: int, column: int, rowSpan: int = 1, columnSpan: int = 1, alignment = Qt.Alignment()):
        """Add widget to options section of dialog"""
        self.options.addWidget(widget, row, column, rowSpan, columnSpan, alignment)


class TitleBar(StandardTitleBar):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        # Minimize Colors
        self.minBtn.setNormalColor(Qt.GlobalColor.white)
        self.minBtn.setHoverColor(Qt.GlobalColor.white)
        self.minBtn.setHoverBackgroundColor("#777")
        self.minBtn.setPressedColor(Qt.GlobalColor.white)
        # Maximize Colors
        self.maxBtn.setNormalColor(Qt.GlobalColor.white)
        self.maxBtn.setHoverColor(Qt.GlobalColor.white)
        self.maxBtn.setHoverBackgroundColor("#777")
        self.maxBtn.setPressedColor(Qt.GlobalColor.white)
        # Close Colors
        self.closeBtn.setNormalColor(Qt.GlobalColor.white)
        # Set NoTextInteraction to prevent dragability issues with HTML / rich text
        self.titleLabel.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        # Change iconLabel to QSvgWidget
        self.iconLabel = QtSvg.QSvgWidget(os.path.join(root_dir, f'icons/Cobra_Tools_Logo_24px.svg'), parent)
        self.iconLabel.setGeometry(6, 6, 24, 24)

    def setIcon(self, icon):
        """Overriding StandardTitleBar.setIcon since self.iconLabel widget was changed due to DPI issues."""
        pass


class MainWindow(FramelessMainWindow):
    modified = pyqtSignal(bool)
    set_log_level = pyqtSignal(str)
    change_log_speed = pyqtSignal(str)  # Emits "fast", "normal", "slow"

    CANCEL_WAIT_MS = 2000

    def __init__(self, name: str, opts: 'gui.GuiOptions', central_widget: Optional[QWidget] = None) -> None:
        self.opts = opts
        if self.opts.frameless:
            FramelessMainWindow.__init__(self)
        else:
            from types import MethodType
            QMainWindow.__init__(self)
            FramelessMainWindow.resizeEvent = MethodType(QMainWindow.resizeEvent, self)
            FramelessMainWindow.nativeEvent = MethodType(QMainWindow.nativeEvent, self)

        self.wrapper_widget = QWidget(self)
        self.central_widget = QWidget(self) if central_widget is None else central_widget
        self.central_layout: QVBoxLayout = QVBoxLayout()
        self.main_content_widget: QWidget = QWidget(self)

        self.title_sep = " | "
        self.title_sep_colored = " <font color=\"#5f5f5f\">|</font> "
        if self.opts.frameless:
            self.setTitleBar(TitleBar(self))

        self.menu_bar = QMenuBar(self)
        self.menu_bar.setStyleSheet("QMenuBar {background: transparent;}")
        self.actions: dict[str, QAction] = {}

        self.name = name
        self.log_name = opts.log_name if opts.log_name else ""
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon(os.path.join(root_dir, f'icons/Cobra_Tools_Logo_24px.svg')))  # Do not cache with get_icon
        self._stdout_handler: logging.StreamHandler = logs.get_stdout_handler(opts.log_name)

        # Threadpool workers
        self.active_workers = set()
        self._current_batch_start_time: Optional[float] = None
        self._is_processing_worker_batch: bool = False

        self.file_widget: Optional[FileWidget] = None
        self.logger: Optional[LoggerWidget] = None
        self.log_splitter: Optional[QSplitter] = None

        self.taskbar_button = QWinTaskbarButton(self)
        self.taskbar_button.setWindow(self.windowHandle())
        self.taskbar_progress = self.taskbar_button.progress()
        self.taskbar_progress.setRange(0, 100)
        self.taskbar_progress.show()

        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 200, 15)
        self.progress.setTextVisible(True)
        self.progress.setMaximum(100)
        self.progress.setValue(0)

        self.status_bar = QStatusBar()
        self.version_info = QLabel(f"Version {VERSION} ({COMMIT_HASH})")
        self.version_info.setFont(QFont("Hack, Consolas, monospace", 8))
        self.version_info.setStyleSheet("color: #999")
        self.status_bar.addPermanentWidget(self.version_info)
        self.status_bar.addPermanentWidget(self.progress)
        self.status_bar.setContentsMargins(5, 0, 0, 0)
        self.setStatusBar(self.status_bar)
        self.progress.hide()

        self.status_timer = QTimer()
        self.status_timer.setSingleShot(True)
        self.status_timer.setInterval(6000)
        self.status_timer.timeout.connect(self.reset_progress)

        self.cfg: Config[str, Any] = Config(root_dir)
        self.cfg.load()

        if self.opts.frameless:
            # Frameless titlebar
            self.titleBar.raise_()

        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.setCentralWidget(self.central_widget)
        self.resize(*opts.size)

    def showEvent(self, a0: QShowEvent) -> None:
        """Post-init setup on show"""
        log_level = self.cfg.get("logger_level", "INFO")
        self.set_log_level.emit(log_level)
        super().showEvent(a0)

    def create_main_splitter(self, top_layout: QLayout, left_widget: QWidget, right_widget: QWidget,
                             sizes: list[int] = [200,400]) -> None:
        """Helper to create a basic layout with a top layout + a left/right splitter"""
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.addWidget(left_widget)
        self.main_splitter.addWidget(right_widget)
        self.main_splitter.setSizes(sizes)
        self.main_splitter.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        self.main_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.main_splitter.setObjectName("mainContentSplitter")
        if not left_widget.objectName():
            left_widget.setObjectName("mainContentLeft")
        if not right_widget.objectName():
            right_widget.setObjectName("mainContentRight")

        main_content_layout = QVBoxLayout()
        main_content_layout.addLayout(top_layout)
        main_content_layout.addWidget(self.main_splitter)
        main_content_layout.setObjectName("mainContentLayout")
        self.main_content_widget.setLayout(main_content_layout)
        self.main_content_widget.setObjectName("mainContentWidget")

        enable_logger = self.cfg.get("enable_logger_widget", True)
        if enable_logger:
            # Layout for Logger
            logger_orientation = LOGGER_BOTTOM if self.cfg.get("logger_orientation", "V") == "V" else LOGGER_RIGHT
            if logger_orientation == LOGGER_BOTTOM:
                self.main_content_widget.setContentsMargins(5, 0, 5, 5)
            else:
                self.main_content_widget.setContentsMargins(5, 0, 0, 0)
            self.layout_logger(self.main_content_widget, logger_orientation)
        else:
            # Layout for no Logger
            self.central_layout.addWidget(self.main_content_widget)

    def layout_logger(self, topleft: QWidget, orientation: Qt.Orientation) -> None:
        self.logger, self.log_splitter = self.make_logger_widget(topleft=topleft,
                                                                 orientation=orientation,
                                                                 log_level_changed_fn=self.on_log_level_changed,
                                                                 resize_requested_fn=self.resize_logger)
        self.log_splitter.setHandleWidth(8)
        self.central_layout.addWidget(self.log_splitter)
        # Hide at start if configured
        self.show_logger = self.cfg.get("show_logger_widget", True)
        if not self.show_logger:
            self.logger.close()
            # Ensure default size
            self.resize(*self.opts.size)

    def get_palette_from_cfg(self):
        theme_name = self.cfg.get("theme", "dark")
        palette = qt_theme.palettes.get(theme_name)
        return palette

    @property
    def stdout_handler(self) -> logging.StreamHandler | None:
        if not self._stdout_handler:
            self._stdout_handler = logs.get_stdout_handler(self.log_name)
        return self._stdout_handler

    @stdout_handler.setter
    def stdout_handler(self, handler: logging.StreamHandler) -> None:
        self._stdout_handler = handler

    def set_log_name(self, name: str) -> None:
        self.log_name = name

    @abstractmethod
    def open(self, filepath: str) -> None:
        pass

    @abstractmethod
    def open_dir(self, dirpath: str) -> None:
        pass

    @abstractmethod
    def save(self, filepath: str) -> None:
        pass

    def setCentralWidget(self, widget: QWidget, layout: Optional[QLayout] = None) -> None:
        if not layout:
            layout = self.central_layout
        frame = QFrame(self)
        frame.setMinimumHeight(32)
        frame.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        if self.opts.frameless:
            layout.addWidget(frame)
        layout.addWidget(self.menu_bar)
        layout.addWidget(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.wrapper_widget.setLayout(layout)
        super().setCentralWidget(self.wrapper_widget)

    def make_file_widget(self, ask_user: bool = True, ftype: str = "OVL", editable: bool = False,
                         check_exists: bool = False, root: Optional[str] = None) -> FileWidget:
        file_widget = FileWidget(self, self.cfg, ask_user=ask_user, ftype=ftype, editable=editable,
                                 check_exists=check_exists, root=root)

        self.modified.connect(file_widget.set_modified)

        file_widget.file_opened.connect(self.open)
        file_widget.dir_opened.connect(self.open_dir)
        file_widget.file_saved.connect(self.save)
        file_widget.filepath_changed.connect(self.set_window_filepath)

        return file_widget
    
    def style_logger_widget(self, logger: LoggerWidget, log_splitter: QSplitter):
        log_splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        log_splitter.setContentsMargins(0, 0, 0, 0)
        log_splitter.setCollapsible(0, True)
        log_splitter.setCollapsible(1, False)
        style = ""
        if logger.orientation == LOGGER_BOTTOM:
            style = R"""
                QSplitter::handle:vertical {
                    padding: 0px 0px 4px 0px;
                }
            """
            # Make MainWindow larger
            self.resize(self.opts.size.width, self.opts.size.height + self.opts.logger_height)
            log_splitter.setSizes([self.opts.size.height, self.opts.logger_height])
        elif logger.orientation == LOGGER_RIGHT:
            style = R"""
                QSplitter::handle:horizontal {
                    width: 5px; /* Make handle visible */
                }
            """
            # Make MainWindow larger
            self.resize(self.opts.size.width + self.opts.logger_width, self.opts.size.height)
            log_splitter.setSizes([self.opts.size.width, self.opts.logger_width])

        log_splitter.setStyleSheet(style)
        log_splitter.setStretchFactor(0, 1)
        log_splitter.setStretchFactor(1, 0)

    def make_logger_widget(self, topleft: QWidget, orientation: Qt.Orientation = LOGGER_BOTTOM,
                           sizes: tuple[int, int] = (600, 200),
                           log_level_changed_fn: Optional[Callable] = None,
                           resize_requested_fn: Optional[Callable] = None) -> tuple[LoggerWidget, QSplitter]:
        logger = LoggerWidget(self, orientation)
        logger.handler.setFormatter(logs.HtmlFormatter('%(levelname)s | %(message)s'))
        logger.handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(logger.handler)
        log_splitter = SnapCollapseSplitter(orientation)
        log_splitter.addWidget(topleft)
        log_splitter.addWidget(logger)

        self.change_log_speed.connect(logger.set_logging_speed)

        if log_level_changed_fn:
            logger.log_level_changed.connect(log_level_changed_fn)
        if resize_requested_fn:
            logger.resize_requested.connect(resize_requested_fn)

        self.style_logger_widget(logger, log_splitter)

        if not hasattr(self, "status_spacer"):
            self.status_spacer = StatusSpacer(self)
            # Keep status widgets right-aligned with main layout, ignoring logger.
            self.status_bar.addPermanentWidget(self.status_spacer)
            self.status_spacer.set_widget(logger)

        return logger, log_splitter

    def setWindowTitle(self, title: str = "", file: str = "", modified: bool = False) -> None:
        if not title:
            title = self.name
        if file:
            super().setWindowTitle(f"{title}{self.title_sep}{self.get_file_name(file, only_basename=True)}")
            file_color = ""
            file_color_end = ""
            if modified and self.opts.frameless:
                file_color = "<font color=\"#ffe075\">"
                file_color_end = "</font>"
            if self.opts.frameless:
                self.titleBar.titleLabel.setText(f"{title}{self.title_sep_colored}{file_color}{self.get_file_name(file)}{file_color_end}")
            return
        super().setWindowTitle(f"{title}")

    def set_window_filepath(self, file: str, modified: bool) -> None:
        self.setWindowTitle(file=file, modified=modified)

    def elide_dirs(self, filepath: str) -> str:
        path, file = os.path.split(filepath)
        filename, _ = os.path.splitext(file)
        subdirs = path.split("/")
        if len(subdirs) > 3:
            if filename == subdirs[-1]:
                return "/".join([subdirs[0], subdirs[1], subdirs[2], "...", file])
            else:
                return "/".join([subdirs[0], subdirs[1], "...", subdirs[-1], file])
        return filepath

    def get_file_name(self, filepath: str, only_basename: bool = False) -> str:
        filepath = Path(os.path.normpath(filepath)).as_posix()
        if not only_basename and "ovldata/" in filepath:
            return self.elide_dirs(filepath.split("ovldata/")[1])
        return os.path.basename(filepath)

    def set_file_modified(self, dirty: bool) -> None:
        self.modified.emit(dirty)

    def set_clean(self) -> None:
        self.set_file_modified(False)

    def set_dirty(self) -> None:
        self.set_file_modified(True)

    @property
    def file_menu_items(self) -> list[BaseMenuItem]:
        return [
            MenuItem("Open", self.file_widget.ask_open, shortcut="CTRL+O", icon="dir"),
            SubMenuItem("Open Recent", self.populate_recent_files, icon="recent"),
            SeparatorMenuItem(),
            MenuItem("Save", self.file_widget.ask_save, shortcut="CTRL+S", icon="save"),
            MenuItem("Save As", self.file_widget.ask_save_as, shortcut="CTRL+SHIFT+S", icon="save"),
            SeparatorMenuItem(),
            MenuItem("Exit", self.close, icon="exit")
        ]

    @property
    def view_menu_items(self) -> list[BaseMenuItem]:
        return [
            SeparatorMenuItem("Logger"),
            CheckableMenuItem("Show Logger",
                func=self.toggle_logger,
                tooltip="Display logger in the GUI",
                config_name="show_logger_widget",
                config_default=True
            ),
            CheckableMenuItem("Clear Logs",
                func=self.toggle_clear_logs,
                tooltip="Clear previous logs on File Open",
                config_name="clear_logs",
                config_default=True
            )
        ]

    @pyqtSlot(bool)
    def toggle_logger(self, checked: bool):
        if hasattr(self, "logger") and self.logger:
            if checked:
                self.logger.show()
            else:
                self.logger.close()

    @pyqtSlot(bool)
    def toggle_clear_logs(self, checked: bool):
        if hasattr(self, "logger") and self.logger:
            self.logger.toggle_clear_logs(checked)

    @property
    def help_menu_items(self) -> list[BaseMenuItem]:
        return [
            MenuItem("Show Commit on GitHub", self.open_repo, icon="github"),
            MenuItem("Report Bug on GitHub", self.report_bug, icon="report"),
            MenuItem("Read Wiki Documentation", self.online_support, icon="manual")
        ]

    def open_repo(self) -> None:
        webbrowser.open(f"https://github.com/OpenNaja/cobra-tools/tree/{COMMIT_HASH}", new=2)

    def report_bug(self) -> None:
        webbrowser.open("https://github.com/OpenNaja/cobra-tools/issues/new?assignees=&labels=&template=bug_report.md&title=", new=2)

    def online_support(self) -> None:
        webbrowser.open("https://opennaja.github.io/cobra-tools/", new=2)

    def build_menus(self, menu_layout: dict[str, list[BaseMenuItem]]) -> None:
        """
        Constructs the entire menu bar from a declarative dict of menu item objects
        """
        # Initialize
        self.menus: dict[str, QMenu] = {}
        self.actions: dict[str, QAction] = {}

        for menu_name, items_in_menu in menu_layout.items():
            # Create top-level menu
            parent_menu = self.menu_bar.addMenu(menu_name)
            if parent_menu is None:
                logging.error(f"Failed to create menu '{menu_name}'")
                continue
            self.menus[menu_name] = parent_menu
            # Build all items for that menu
            for item in items_in_menu:
                self._build_menu_item(parent_menu, item)

    def _build_menu_item(self, parent_menu: QMenu, item: BaseMenuItem) -> None:
        """Builds a single QAction, QMenu, or separator from a definition object"""
        if isinstance(item, SeparatorMenuItem):
            if item.name:
                add_label_separator(parent_menu, item.name)
            else:
                parent_menu.addSeparator()
        elif isinstance(item, SubMenuItem):
            submenu = parent_menu.addMenu(item.name)
            if submenu is None:
                logging.error(f"Failed to create submenu '{submenu}'")
                return
            self.menus[item.name] = submenu
            if item.icon:
                submenu.setIcon(get_icon(item.icon))
            # Connect func to the aboutToShow signal for dynamic menus
            if item.func:
                submenu.aboutToShow.connect(item.func)
            # Recursively build any statically defined sub-items
            for sub_item in item.items:
                self._build_menu_item(submenu, sub_item)
        elif isinstance(item, (MenuItem, CheckableMenuItem)):
            action = QAction(item.name, self)
            if item.icon:
                action.setIcon(get_icon(item.icon))
            if hasattr(item, 'shortcut') and item.shortcut:
                action.setShortcut(item.shortcut)
            if item.tooltip:
                parent_menu.setToolTipsVisible(True)
                action.setToolTip(item.tooltip)
            if item.func:
                if isinstance(item, MenuItem):
                    action.triggered.connect(item.func)
                else:
                    action.toggled.connect(item.func)
            if isinstance(item, CheckableMenuItem):
                action.setCheckable(True)
                if item.config_name:
                    config_setting = self.cfg.get(item.config_name, item.config_default)
                    if isinstance(config_setting, bool):
                        action.setChecked(config_setting)
                        action.toggled.connect(
                            # name kwarg for proper capture
                            lambda checked, name=item.config_name: self.cfg.update({name: checked})
                        )
            parent_menu.addAction(action)
            self.actions[item.name.lower()] = action

    def populate_recent_files(self):
        """
        Dynamically populates the 'Open Recent' submenu
        """
        recent_menu = self.menus.get("Open Recent")
        if not recent_menu:
            return
        recent_menu.clear()
        # Fetch from config only once
        recent_files_from_cfg = self.cfg.get(self.file_widget.cfg_recent_files, [])
        valid_files = [fp for fp in recent_files_from_cfg if os.path.isfile(fp)]
        # If stale paths were removed, update the configuration
        if len(valid_files) != len(recent_files_from_cfg):
            self.cfg[self.file_widget.cfg_recent_files] = valid_files
        # Add a placeholder if the list is empty
        if not valid_files:
            action = QAction("(No Recent Files)", self)
            action.setEnabled(False)
            recent_menu.addAction(action)
            return
        # Create recents
        for fp in valid_files:
            ext = os.path.splitext(fp)[1][1:]
            icon = get_icon(ext)
            file_name = self.get_file_name(fp)

            action = QAction(icon, file_name, self)
            action.setToolTip(fp)
            action.triggered.connect(lambda _checked, path=fp: self.file_widget.open_file(path))

            recent_menu.addAction(action)
        # Add a "Clear" action
        recent_menu.addSeparator()
        clear_action = QAction("Clear Recent Files", self)
        def clear_list():
            self.cfg[self.file_widget.cfg_recent_files] = []

        clear_action.triggered.connect(clear_list)
        recent_menu.addAction(clear_action)

    def handle_error(self, msg: str) -> None:
        """Warn user with popup msg and write msg + exception traceback to log"""
        logging.exception(msg)
        self.showerror(msg)

    def show_progress(self) -> None:
        self.progress.show()
        self.version_info.hide()

    def set_progress(self, value: int) -> None:
        self.progress.setValue(value)
        self.taskbar_progress.setValue(value)
        if self.progress.value() >= self.progress.maximum():
            self.status_timer.start()

    def set_progress_total(self, value: int) -> None:
        if self.progress.isHidden():
            self.show_progress()
        self.progress.setMaximum(value)
        self.taskbar_progress.setMaximum(value)

    def reset_progress(self) -> None:
        self.taskbar_progress.setValue(0)
        self.progress.setValue(0)
        self.progress.hide()
        self.status_bar.clearMessage()
        self.version_info.show()

    def set_progress_message(self, message: str) -> None:
        self.status_bar.showMessage(message, 0)

    def run_in_parallel(self, func: Callable, callbacks: Iterable = (), *args, **kwargs) -> None:
        pass

    def run_in_threadpool(self, func: Callable, callbacks: Iterable = (), *args, **kwargs) -> None:
        # print(f"Running '{func.__name__}' in threadpool")
        worker = WorkerRunnable(func, *args, **kwargs)
        worker.signals.error_msg.connect(self.showerror)
        worker.signals.finished.connect(self.choices_update)

        if not self.active_workers:  # If no workers are currently active, this is the start of a new batch
            self.enable_gui_options(False)
            if not self._is_processing_worker_batch:  # Ensure we only start timing once per batch
                logging.debug(f"Starting new worker batch with '{func.__name__}'")
                self._current_batch_start_time = time.perf_counter()
                self._is_processing_worker_batch = True

        for callback in callbacks:
            worker.signals.finished.connect(callback)

        def worker_cleanup_slot(worker_instance=worker, func_name=func.__name__):
            logging.debug(f"Worker for '{func_name}' signaled completion. Removing from active set.")
            if worker_instance in self.active_workers:
                self.active_workers.remove(worker_instance)
            else:
                logging.warning(f"Worker for '{func_name}' was not in active_workers set during cleanup")

            logging.debug(f"Active workers remaining: {len(self.active_workers)}")

            # Check if this was the last worker of the batch
            if not self.active_workers and self._is_processing_worker_batch:
                if self._current_batch_start_time:
                    elapsed_time = time.perf_counter() - self._current_batch_start_time
                    logging.debug(f"'{func_name}' finished in {elapsed_time:.4f} seconds")

                self.change_log_speed.emit("normal")
                self._is_processing_worker_batch = False
                self._current_batch_start_time = None

            self.enable_gui_options(True)

        # Connect the cleanup slot to run when the worker is done
        worker.signals.finished.connect(worker_cleanup_slot)

        self.active_workers.add(worker)
        logging.debug(f"Starting worker for '{func.__name__}'. Total active: {len(self.active_workers)}")
        self.threadpool.start(worker)
        self.enable_gui_options(False)

    def cancel_workers(self):
        """Worker thread cancellation and wait."""
        # Print used in case logging no longer available
        print("Signaling and waiting for worker threads...")
        if hasattr(self, 'active_workers') and self.active_workers:
            print(f"  Signaling {len(self.active_workers)} active worker(s) to cancel...")
            for worker_ref in list(self.active_workers):
                if hasattr(worker_ref, 'cancel'):
                    worker_ref.cancel()

        if hasattr(self, 'threadpool'):
            print(f"Waiting for QThreadPool to finish (max {self.CANCEL_WAIT_MS / 1000}s)...")
            all_threads_done = self.threadpool.waitForDone(self.CANCEL_WAIT_MS)
            if all_threads_done:
                print("QThreadPool.waitForDone() completed successfully.")
            else:
                print("  WARNING - QThreadPool.waitForDone() TIMED OUT. Some QRunnables may still be active.")
                if hasattr(self, 'active_workers') and self.active_workers:
                    lingering_tracked_workers = [getattr(w.func, '__name__', 'unknown_func') for w in self.active_workers]
                    print(f"  Tracked workers still in self.active_workers after timeout: {lingering_tracked_workers}")

    def enable_gui_options(self, enable=True):
        pass

    def choices_update(self):
        pass

    def closeEvent(self, event: QCloseEvent) -> None:
        # Dirty check
        if self.file_widget and self.file_widget.dirty:
            quit_msg = f"Quit? You will lose unsaved work on {os.path.basename(self.file_widget.filepath)}!"
            if not self.showconfirmation(quit_msg, title="Quit"):
                event.ignore()
                return
        # Cancel batch operations
        self.cancel_workers()
        # Close logger widget
        if self.logger:
            self.logger.close()
        # Close logging handlers
        self.close_logs()
        event.accept()
        # Last resort workaround for console hanging
        # NOTE: Left as documentation in case it happens again.
        #       Instead, ensure any unparented widgets are closed or made parented
        #QtCore.QCoreApplication.instance().quit()

    def resize_logger(self, request: LoggerWidget.ResizeRequest) -> None:
        if not hasattr(self, 'logger') or not hasattr(self, 'log_splitter'):
            return
        if not self.logger or not self.log_splitter:
            return

        if self.logger.orientation == LOGGER_BOTTOM:
            if request.size > 0:
                logger_size = request.size + LoggerWidget.ICON_BAR_SIZE
                current_sizes = self.log_splitter.sizes()
                if not request.expand_only or current_sizes[1] < logger_size:
                    self.log_splitter.setSizes([self.log_splitter.widget(0).height() - logger_size, logger_size])
            else:
                self.log_splitter.setSizes([self.opts.size.height, 0])
        else:
            if request.size > 0:
                logger_size = min(request.size, 400)
                current_sizes = self.log_splitter.sizes()
                if not request.expand_only or current_sizes[1] < logger_size:
                    self.log_splitter.setSizes([self.log_splitter.widget(0).width() - logger_size, logger_size])
            else:
                self.log_splitter.setSizes([self.opts.size.width, 0])

    def on_log_level_changed(self, level: str) -> None:
        if self.stdout_handler:
            self.stdout_handler.setLevel(level)
        level = level if level != "SUCCESS" else "WARNING"  # So SUCCESS is still shown at "WARNING" level
        self.cfg["logger_level"] = level

    def close_logs(self) -> None:
        if self.log_name:
            root_logger = logging.getLogger()
            handlers_to_process = []
            for handler in list(root_logger.handlers):
                # Identify LoggerWidget.Handler
                if self.logger and handler is self.logger.handler:
                    handlers_to_process.append(handler)
                # Identify LogBackupFileHandler
                elif isinstance(handler, logs.LogBackupFileHandler) and handler.name and handler.name == self.log_name:
                    handlers_to_process.append(handler)

            if not handlers_to_process:
                print("close_logs: No specific handlers (LoggerWidget.Handler, LogBackupFileHandler) found to remove.")

            for handler in reversed(handlers_to_process):
                handler_id_str = f"{type(handler).__name__} (name: {getattr(handler, 'name', 'N/A')}, id: {id(handler)})"
                try:
                    root_logger.removeHandler(handler)
                except Exception as e:
                    print(f"ERROR: Failed to remove handler {handler_id_str}: {e}")
                    # Continue to try closing it anyway
                try:
                    handler.close()
                except Exception as e:
                    print(f"ERROR: Exception during close() for handler {handler_id_str}: {e}")

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if not self.file_widget:
            return

        path = event.mimeData().urls()[0].toLocalFile() if event.mimeData().hasUrls() else ""
        if path.lower().endswith(f".{self.file_widget.ftype_lower}"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if not self.file_widget:
            return

        path = event.mimeData().urls()[0].toLocalFile() if event.mimeData().hasUrls() else ""
        if path:
            self.file_widget.open_file(path)

    def showdialog(self, info, title="", buttons=None, details=None):
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(info)
        msg.setWindowTitle(title)
        msg.setStandardButtons(msg.Ok if not buttons else buttons)
        if details:
            msg.setDetailedText(details)
        return msg.exec_() not in [msg.No, msg.Cancel]

    def showquestion(self, info, title=None, details=None):
        logging.debug(f"User Prompt: {info}")
        return self.showdialog(info, title="Question" if not title else title,
                        buttons=(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No), details=details)

    def showconfirmation(self, info, title=None, details=None):
        logging.debug(f"User Prompt: {info}")
        return self.showdialog(info, title="Confirm" if not title else title,
                        buttons=(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel), details=details)

    def showwarning(self, info, details=None):
        logging.debug(f"User Prompt: {info}")
        return self.showdialog(info, title="Warning", details=details)

    def showerror(self, info, details=None):
        logging.debug(f"User Prompt: {info}")
        return self.showdialog(info, title="Error", details=details)


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    - finished: No data
    - error:`tuple` (exctype, value, traceback.format_exc() )
    - result: `object` data returned from processing, anything
    - progress: `tuple` indicating progress metadata
    '''
    # result = pyqtSignal(object)
    # progress = pyqtSignal(tuple)
    finished = pyqtSignal()
    error_msg = pyqtSignal(str)


class WorkerRunnable(QtCore.QRunnable):

    def __init__(self, func: Callable, *args, **kwargs) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self._is_cancelled = False
        self.setAutoDelete(True)

    @pyqtSlot()
    def run(self) -> None:
        if self._is_cancelled:
            logging.info(f"Worker for {self.func.__name__} cancelled before execution.")
            self.signals.finished.emit()  # Still signal completion of the runnable
            return
        try:
            # Check if the target function can accept a cancellation check
            import inspect
            sig = inspect.signature(self.func)
            if 'cancellation_check' in sig.parameters:
                # If so, inject our cancellation check method
                self.kwargs['cancellation_check'] = lambda: self._is_cancelled
            self.func(*self.args, **self.kwargs)
        except Exception as err:
            # Check if cancellation happened and func perhaps raised an error because of it
            if self._is_cancelled:
                 logging.info(f"Worker for {self.func.__name__} errored, possibly due to cancellation: {err}")
            else:
                logging.exception(f"Threaded call of function '{self.func.__name__}()' errored!")
                #if not self._is_cancelled:
                self.signals.error_msg.emit(str(err))
        finally:
            self.signals.finished.emit()

    def cancel(self) -> None:
        logging.info(f"Cancel requested for worker: {getattr(self.func, '__name__', 'unknown_func')}")
        self._is_cancelled = True


class Reporter(DummyReporter, QObject):
    """A class wrapping the interaction between OvlFile and the UI"""
    warning_msg = pyqtSignal(tuple)  # type: ignore
    success_msg = pyqtSignal(str)  # type: ignore
    files_list = pyqtSignal(list)  # type: ignore
    included_ovls_list = pyqtSignal(list)  # type: ignore
    progress_percentage = pyqtSignal(int)  # type: ignore
    progress_total = pyqtSignal(int)  # type: ignore
    current_action = pyqtSignal(str)  # type: ignore


class ConfigWindow(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.cfg = main_window.cfg
        self.vlayout = QVBoxLayout()
        for cfg_key, cfg_manager in self.cfg.settings.items():
            def make_setter():
                # make local copies to avoid overriding them in the scope of the closure
                cfg_key2 = str(cfg_key)
                cfg_manager2 = cfg_manager

                def set_key(v):
                    # nonlocal cfg_key
                    cfg_manager2.update(self.cfg, cfg_key2, v)

                return set_key

            set_key = make_setter()
            c = LabelCombo(cfg_manager.name, [str(x) for x in cfg_manager.options],
                           editable=not bool(cfg_manager.options), activated_fn=set_key)
            c.setToolTip(cfg_manager.tooltip)
            c.entry.setText(str(self.cfg.get(cfg_key, cfg_manager.default)))
            if isinstance(cfg_manager, RestartSetting):
                c.entry.currentTextChanged.connect(self.needs_restart)
            # if isinstance(cfg_manager, ImmediateSetting):
            # 	logging.debug(f"Saved '{self.name}' after storing '{k}'")
            # 	self.cfg.save()
            self.vlayout.addWidget(c)
        self.setLayout(self.vlayout)

    def needs_restart(self):
        if self.main_window.showconfirmation(f"Close tools now and then manually restart to apply the changes", title="Restart Tools"):
            self.close()
            self.main_window.close()
        # just close the gui, actually restarting from code is hard


def get_main_window():
    for w in QtWidgets.qApp.topLevelWidgets():
        if isinstance(w, MainWindow):
            return w


def pack_in_box(*widgets, margins=(0, 0, 0, 0), layout=QtWidgets.QVBoxLayout):
    frame = QtWidgets.QWidget()
    box = layout()
    for w in widgets:
        box.addWidget(w)
    box.setContentsMargins(*margins)
    box.setSizeConstraint(layout.SizeConstraint.SetNoConstraint)
    frame.setLayout(box)
    return frame
