import logging
import webbrowser
import os
import re
import html
import abc
from collections import deque
from abc import abstractmethod
from pathlib import Path
from dataclasses import dataclass, field

from ovl_util import auto_updater  # pyright: ignore  # noqa: F401
from ovl_util import logs
from ovl_util.config import Config, ImmediateSetting, RestartSetting

from typing import Any, AnyStr, Union, Optional, Iterable, Callable, cast, NamedTuple
from textwrap import dedent
from modules.formats.shared import DummyReporter
from modules.walker import valid_packages

import gui
from gui import qt_theme
from gui.app_utils import *

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject, QDir, QFileInfo, QRegularExpression,
                          QRect, QRectF, QSize, QEvent, QTimer, QTimerEvent, QThread, QUrl, QMimeData,
                          QAbstractTableModel, QSortFilterProxyModel, QModelIndex, QItemSelection,
                          QAbstractAnimation, QParallelAnimationGroup, QPropertyAnimation,
                          QAbstractListModel, QPersistentModelIndex, QItemSelectionModel, QVariant)
from PyQt5.QtGui import (QBrush, QColor, QFont, QFontMetrics, QIcon, QPainter, QPen, qRgba, QPainterPath, QLinearGradient,
                         QStandardItemModel, QStandardItem, QTextDocument, QTextCursor, QTextOption, QTextDocumentFragment,
                         QCloseEvent, QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent, QShowEvent,
                         QKeyEvent, QFocusEvent, QMouseEvent, QPaintEvent, QResizeEvent, QWheelEvent)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QColorDialog, QFileDialog, QAbstractItemView,
                             QListView, QHeaderView, QTableView, QTreeView, QFileSystemModel, QStyle, QLayoutItem,
                             QAction, QCheckBox, QComboBox, QDoubleSpinBox, QLabel, QLineEdit, QMenu, QMenuBar,
                             QMessageBox, QTextEdit, QProgressBar, QPushButton, QStatusBar, QToolButton, QSpacerItem,
                             QFrame, QLayout, QGridLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy,
                             QSplitter,
                             QStyleFactory, QStyleOptionViewItem, QStyledItemDelegate, QDialog, QDialogButtonBox,
                             QFileIconProvider, QButtonGroup)
from PyQt5.QtWinExtras import QWinTaskbarButton
from qframelesswindow import FramelessMainWindow, StandardTitleBar
from __version__ import VERSION, COMMIT_HASH


MAX_UINT = 4294967295
root_dir = Path(__file__).resolve().parent.parent

FILE_MENU = 'File'
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


class LogStatus(QWidget):
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
        self.next_btn = QPushButton(get_icon("jump", color=color), "")
        self.next_btn.setFlat(True)
        self.next_btn.setVisible(False)
        self.next_btn.setStatusTip(f"Jump to next {level.title()}")
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        # Next text
        self.next_txt = QPushButton("")
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
                font: bold 12px "Consolas, monospace"; 
            }}
            QPushButton:hover {{
                color: {highlight.name()};
                background: {bg.name()};
                border: none;
            }}
        """
        self.count_btn.setStyleSheet(btn_style)
        self.count_lbl.setStyleSheet(btn_style)
        self.next_btn.setStyleSheet(next_btn_style)
        self.next_txt.setStyleSheet(next_btn_style)
        self.next_btn.clicked.connect(self.on_clicked)
        self.next_txt.clicked.connect(self.on_clicked)
        # Main layout
        self.hbox = QHBoxLayout(self)
        self.hbox.addLayout(self.count_box)
        self.hbox.addLayout(self.next_box)
        self.hbox.setContentsMargins(0, 0, 0, 0)

    @property
    def message_count(self) -> int:
        return len(self.messages)

    def layout_horizontal(self) -> None:
        self.next_btn.setFixedHeight(16)
        self.next_txt.setFixedHeight(16)
        if self.show_msg:
            self.next_txt.setMaximumWidth(self.max_msg_width)
        else:
            self.next_txt.setMaximumWidth(0)
            self.next_btn.setFixedWidth(16)
        self.setFixedHeight(16)
        self.hbox.setDirection(QHBoxLayout.Direction.LeftToRight)
        self.hbox.setSpacing(6)
        self.count_box.setDirection(QHBoxLayout.Direction.LeftToRight)
        self.next_box.setDirection(QHBoxLayout.Direction.LeftToRight)

    def layout_vertical(self) -> None:
        self.setFixedHeight(64)
        self.hbox.setDirection(QHBoxLayout.Direction.TopToBottom)
        self.hbox.setSpacing(6)
        self.count_box.setDirection(QHBoxLayout.Direction.TopToBottom)
        self.next_box.setDirection(QHBoxLayout.Direction.TopToBottom)

    def resize_max_msg_width(self, add_sub: int) -> None:
        """Increase/Decrease max message width with window"""
        # TODO: This wasn't quite working and is not currently called
        if self.show_msg:
            self.max_msg_width += add_sub
            self.next_txt.setMaximumWidth(self.max_msg_width)
            self.update_text()

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
            self.count_lbl.setFont(QFont("Consolas, monospace", 8))
        else:
            self.count_lbl.setFont(QFont("Consolas, monospace", 7))
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
    rowSizeHintChanged = QtCore.pyqtSignal(int)

    document_cache: dict[int, QTextDocument] = dict()

    HEIGHT = 18
    PAD = 4
    DETAIL_INDENT = '\u00A0\u00A0'
    DETAIL_OFFSET = HEIGHT
    ICON_COL_SIZE = 25

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.do_toggle = False
        self._style = R"""
            div, span {font-family: "Consolas, monospace"; font-size: 12px; background: transparent; border: 0px;}
            .msg_DEBUG {color:#808080;}
            .msg_INFO {color:#ddd;}
            .msg_SUCCESS {color:#2fff5d;}
            .msg_WARNING {color:#ffc52f;}
            .msg_ERROR {color:#e73f34;}
            .msg_CRITICAL {color:#ff2e67;}
            .level {font-size: 1px; color: transparent; width: 0px; }

            .detail, .traceback, .show, .hide {font-family: "Consolas, monospace"; color: #ddd; margin-top: 4px; border: 0px;}
            .traceback, .show, .hide {font-size: 11px;}
            .detail {font-size: 12px;}

            .trace {font-family: "Consolas, monospace"; font-size: 11px;}
            .trace.caret {color:#e54873;}
            .trace.line {color:#31b6e2;}
            .trace.file {color:#e8c35e;}
            .trace.location {color:#76a342;}
            .trace.exception, .trace.message {color:#f34965;}

            QTextBlock {font-family: "Consolas, monospace"; margin: 0px; padding: 0px; border: 0px;}
        """

    SHOW_CHAR = "\u2B9E"  # >  arrow
    HIDE_CHAR = "\u2B9F"  # \/ arrow
    SHOW_INFO = f"{SHOW_CHAR} Show Info"
    HIDE_INFO = f"{HIDE_CHAR} Hide Info"
    SHOW_TRACE = f"{SHOW_CHAR} Show Traceback"
    HIDE_TRACE = f"{HIDE_CHAR} Hide Traceback"

    @staticmethod
    def show_text(is_trace: bool) -> str:
        return f"{LogViewDelegate.SHOW_TRACE if is_trace else LogViewDelegate.SHOW_INFO}"

    @staticmethod
    def hide_text(is_trace: bool) -> str:
        return f"{LogViewDelegate.HIDE_TRACE if is_trace else LogViewDelegate.HIDE_INFO}"

    @staticmethod
    def color_traceback(text: str) -> str:
        """Basic coloring for tracebacks"""
        # Traceback (most recent call last)
        text = re.sub(r"(?m)^(Traceback.*:)$", r"<span class='trace message'>\g<1></span>", text)
        # ExceptionType: exception message
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

    def create_doc(self, option: QStyleOptionViewItem, index: QModelIndex) -> QTextDocument:
        """Create a QTextDocument for a logger item and cache it for repaints"""
        # Cache each row for repaints
        doc = None #self.document_cache.get(index.row(), None)
        if doc is None:
            doc = QTextDocument()
            opt = QTextOption()
            if not (option.features & QStyleOptionViewItem.ViewItemFeature.WrapText):
                opt.setWrapMode(QTextOption.WrapMode.NoWrap)
            doc.setDefaultStyleSheet(self._style)
            doc.setUndoRedoEnabled(False)
            doc.setDocumentMargin(0)
            doc.setUseDesignMetrics(True)
            doc.setTextWidth(option.rect.width() - self.ICON_COL_SIZE)
            doc.setDefaultTextOption(opt)

            detail = str(index.data(Qt.ItemDataRole.UserRole))
            is_trace = detail.startswith("\nTraceback")
            cursor = QTextCursor(doc)
            cursor.insertHtml(option.text)
            if detail:
                cursor.movePosition(QTextCursor.MoveOperation.End)
                cursor.insertBlock()  # Whitespace for Show/Hide line
                cursor.insertBlock()  # Block for Traceback/Info
                detail = self.color_traceback(html.escape(detail).replace(' ', '\u00A0'))
                if is_trace:
                    detail = detail.replace('\n', self.DETAIL_INDENT, 1)  # Replace first \n
                detail = detail.replace('\n', f'<br>{self.DETAIL_INDENT}')
                cursor.insertHtml(f"<div class='{'traceback' if is_trace else 'detail'}'>{detail}</div>")
                cursor.block().setVisible(False)
            #self.document_cache[index.row()] = doc
        return doc

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        """Render our logger widget item"""
        self.initStyleOption(option, index)
        painter.setFont(QFont("Consolas, monospace", 8))
        painter.setRenderHints(QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.Antialiasing)
        painter.save()
        option.features &= ~(QStyleOptionViewItem.ViewItemFeature.WrapText | QStyleOptionViewItem.ViewItemFeature.HasCheckIndicator)
        doc = self.create_doc(option, index)
        option.text = ""
        option.widget.style().drawControl(QtWidgets.QStyle.ControlElement.CE_ItemViewItem, option, painter, option.widget)

        detail = str(index.data(LogModel.DETAIL))
        if detail:
            # Detail block expand/collapse state
            toggled = False
            is_trace = detail.startswith("\nTraceback")
            # Entire list view item rect
            area = option.rect
            # Entire detail block
            detail_rect = QRect(area)
            detail_rect.setTop(area.top() + self.DETAIL_OFFSET)
            detail_rect.adjust(self.ICON_COL_SIZE, 0, -self.ICON_COL_SIZE, 0)
            # Show/Hide detail line
            show_detail_rect = QRect(detail_rect)
            show_detail_rect.setHeight(min(10, show_detail_rect.height()))
            # There is the space for Show/Hide detail, get index state
            if area.contains(show_detail_rect, proper=True):
                toggled = index.data(LogModel.TOGGLED) == Qt.CheckState.Checked
            # Is the detail block being hovered on
            on_detail = False
            widget = option.widget
            if type(widget) is LogView and (option.state & QStyle.StateFlag.State_MouseOver):
                position = widget.viewport().mapFromGlobal(QtGui.QCursor.pos())
                if detail_rect.contains(position):
                    on_detail = True
            # Draw mouseover highlight
            if on_detail and (option.state & QStyle.StateFlag.State_MouseOver):
                # Color for log level
                color = QColor(LogView.COLORS.get(index.data(LogModel.LEVEL), "#FFFFFF"))
                color.setAlpha(32)
                grad_rect = detail_rect if toggled else detail_rect
                gradient = QLinearGradient(0, 0, 0, 1.0)
                gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)
                gradient.setColorAt(0.0, color)
                if toggled:
                    color.setAlpha(0)
                gradient.setColorAt(1.0, color)
                path = QPainterPath()
                path.addRoundedRect(QRectF(grad_rect), 4, 4)
                painter.setPen(QPen(Qt.GlobalColor.transparent, 0))
                painter.setBrush(gradient)
                painter.drawPath(path)
            # Highlight Show/Hide text over entire detail block
            if (option.state & QStyle.StateFlag.State_MouseOver):
                if on_detail:
                    painter.setPen(QColor("#CCC"))
                else:
                    painter.setPen(QColor("#AAA"))
            else:
                painter.setPen(QColor("#999"))
            # Show/Hide Text
            text = self.show_text(is_trace) if not toggled else self.hide_text(is_trace)
            painter.drawText(show_detail_rect.adjusted(0, 3, 0, 3), Qt.AlignmentFlag.AlignVCenter, text)
            oldSize = self.sizeHint(option, index)
            if self.do_toggle and (option.state & (QStyle.StateFlag.State_HasFocus)):
                cursor = QTextCursor(doc)
                cursor.movePosition(QTextCursor.MoveOperation.End)
                cursor.block().setVisible(toggled)
                doc.markContentsDirty(cursor.block().position(), cursor.block().length())
                self.do_toggle = False
            # Update LogView layout
            if oldSize != self.sizeHint(option, index):
                self.rowSizeHintChanged.emit(min(300, int(doc.size().height())))

        painter.translate(option.rect.left() + self.ICON_COL_SIZE, option.rect.top() + self.PAD)
        doc.drawContents(painter, QRectF(0, 0, option.rect.width(), option.rect.height()))
        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        """Adjust the sizeHint for the QTextDocument"""
        self.initStyleOption(option, index)
        doc = self.create_doc(option, index)
        size = QSize(int(doc.idealWidth()), int(doc.size().height()) + self.PAD * 2)
        return size

    def on_toggle_detail(self) -> None:
        self.do_toggle = True

    def clear(self) -> None:
        self.document_cache.clear()


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
        self.log_data: deque[LogListData] = deque()
        self.batch_size = batch_size
        self.checks: dict[QPersistentModelIndex, Qt.CheckState] = {}

    def append(self, data: LogListData) -> None:
        self.log_data.append(data)

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
            return dedent(log.detail).strip()
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

    @staticmethod
    def get_plaintext(msg: str) -> str:
        return QTextDocumentFragment.fromHtml(msg).toPlainText()

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
        self.on_detail = False
        self.setAcceptDrops(False)
        #self.setLayoutMode(QListView.LayoutMode.Batched)  # Flickers badly
        #self.setBatchSize(100)  # Flickers badly
        self.setSelectionMode(QAbstractItemView.SelectionMode.ContiguousSelection)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        self.setVerticalScrollMode(QListView.ScrollMode.ScrollPerItem)
        self.setDragEnabled(False)
        self.setMouseTracking(True)
        self.setAutoFillBackground(False)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyle(QStyleFactory.create('windows'))
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
            QListView > QToolTip {{font: bold 11px 'Consolas, monospace'; border: 1px solid white;}}
        """ + qt_theme.style_modern_scrollbar(handle_color=text_col.darker(300).name(),
                                              view_bg_color=base_col.darker(110).name()))
        # View model
        self.list_model = LogModel(self, batch_size=1000)
        self.setModel(self.list_model)
        self.list_model.number_fetched.connect(self.on_number_fetched)
        self.list_model.resize_requested.connect(cast(LoggerWidget, parent).expand_for_detail)
        # Item delegate
        self.delegate = LogViewDelegate(self)
        self.setItemDelegate(self.delegate)
        self.delegate.rowSizeHintChanged.connect(self.list_model.on_rowSizeHintChanged)
        self.toggle_detail.connect(self.delegate.on_toggle_detail)
        # Timer for fetchMore
        self.fetchTimer = QTimer()
        self.fetchTimer.setInterval(250)
        self.fetchTimer.setSingleShot(True)
        self.fetchTimer.timeout.connect(self.fetchMore)
        self.fetchTimer.start()

    def append(self, data: LogListData) -> None:
        if data.level in ("ERROR", "CRITICAL"):
            self.increment_error.emit(self.list_model.data_count, data.text)
        if data.level == "WARNING":
            self.increment_warning.emit(self.list_model.data_count, data.text)
        self.list_model.append(data)
        # Always start fetch timer after an append
        self.fetchTimer.start()

    def clear(self) -> None:
        self.list_model.clear()
        self.delegate.clear()

    def count(self) -> int:
        return self.list_model.data_count

    def fetched_count(self) -> int:
        return self.list_model.rowCount()

    def fetchMore(self) -> None:
        if self.list_model.canFetchMore():
            if self.state() != self.State.EditingState:
                self.list_model.fetchMore()
            self.fetchTimer.start()

    def copy_selection(self) -> None:
        """Fill clipboard with log text for all selected items"""
        selection = self.selectedIndexes()
        if selection:
            data = self.list_model.mimeData(selection)
            QApplication.clipboard().setMimeData(data)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle Ctrl-C for log messages"""
        if event == QtGui.QKeySequence.Copy:
            self.copy_selection()
            return
        return super().keyPressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Handle hover state for detail blocks"""
        position = event.pos()
        index = self.indexAt(position)
        self.on_detail = False
        if index.data(LogModel.DETAIL):
            area = self.visualRect(index)
            detail_rect = QRect(area)
            detail_rect.setTop(area.top() + LogViewDelegate.DETAIL_OFFSET)
            detail_rect.adjust(LogViewDelegate.ICON_COL_SIZE, 0, -LogViewDelegate.ICON_COL_SIZE, 0)
            if detail_rect.height() > 10:
                # To make entire traceback clickable to toggle, do not set height
                #show_detail.setHeight(10)
                self.on_detail = detail_rect.contains(position)
                # Force repaint
                self.update(index)
        # Handle cursor on detail hover
        if self.on_detail:
            self.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.viewport().unsetCursor()
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Handle toggle state for detail blocks"""
        if event.button() == Qt.MouseButton.LeftButton and self.on_detail:
            position = event.pos()
            index = self.indexAt(position)
            # Toggle check state
            checked = self.list_model.data(index, LogModel.TOGGLED)
            if checked == Qt.CheckState.Checked:
                checked = Qt.CheckState.Unchecked
                self.setVerticalScrollMode(QListView.ScrollMode.ScrollPerItem)
            else:
                checked = Qt.CheckState.Checked
                self.setVerticalScrollMode(QListView.ScrollMode.ScrollPerPixel)
            # Set new check state
            self.list_model.setData(index, checked, LogModel.TOGGLED)
            # Inform listeners
            self.toggle_detail.emit()
            # Force repaint
            self.update(index)
        return super().mouseReleaseEvent(event)

    def on_number_fetched(self, _number: int) -> None:
        self.scrollToBottom()


class LoggerWidget(QWidget):
    """Logger widget with colored and expandable list items.
    Supports both horizontal and vertical placement and communicates with
    QSplitter to adjust its contents accordingly.
    """
    log_level_changed = pyqtSignal(str)
    current_size = pyqtSignal(QSize)


    class ResizeRequest(NamedTuple):
        size: int
        expand_only: bool = True


    resize_requested = pyqtSignal(ResizeRequest)


    class Handler(logging.Handler, QObject):
        append = pyqtSignal(LogListData)

        def __init__(self, parent: QWidget | None) -> None:
            super().__init__()
            QObject.__init__(self, parent)

        def emit(self, record: logging.LogRecord) -> None:
            # Supply an empty details string for logging calls that
            # do not include it (to avoid an exception)
            if not hasattr(record, "details"):
                record.__dict__["details"] = ""
            data = LogListData.from_str(logs.shorten_str(self.format(record)))
            self.append.emit(data)


    ICON_BAR_SIZE: int = 18
    MIN_HEIGHT: int = 48
    MIN_WIDTH: int = 180

    def __init__(self, parent: 'MainWindow', orientation: Qt.Orientation) -> None:
        super().__init__(parent)
        self.handler = LoggerWidget.Handler(self)
        self.list_widget = LogView(self)
        self.orientation = orientation
        self.splitter_moving = False
        if self.orientation == Qt.Orientation.Vertical:
            self.list_widget.setMinimumHeight(1)
        else:
            self.list_widget.setMinimumWidth(1)

        self.handler.append.connect(self.list_widget.append)

        self.warnings = LogStatus(level="WARNING", color=LogView.WARNING_COLOR)
        self.errors = LogStatus(level="ERROR", color=LogView.ERROR_COLOR_BRIGHT, show_msg=True)
        if self.orientation == Qt.Orientation.Horizontal:
            self.errors.set_show_message(False)
        # Connect warnings and errors
        self.warnings.select_row.connect(self.on_select_row)
        self.errors.select_row.connect(self.on_select_row)
        self.list_widget.increment_warning.connect(self.warnings.add_message)
        self.list_widget.increment_error.connect(self.errors.add_message)
        # Preserve Log checkbox
        self.preserve_log = QCheckBox("Preserve Log")
        self.preserve_log.setFont(QFont("Consolas, monospace", 8))
        self.preserve_log.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.preserve_log.setFixedHeight(16)
        # Log level combo
        self.log_level_choice = LabelCombo("", ("DEBUG", "INFO", "WARNING", "ERROR"),
                                           editable=False, activated_fn=self.on_log_level_changed)
        self.log_level_choice.setToolTip("How much information is shown in the logger")
        self.log_level_choice.setStatusTip("Log Level")
        self.log_level_choice.label.setFixedWidth(1)
        self.log_level_choice.entry.setFont(QFont("Consolas, monospace", 8))
        self.log_level_choice.entry.setContentsMargins(0, 0, 0, 0)
        self.log_level_choice.entry.setFixedHeight(16)
        # Logger toolbar
        self.menu_hor = FlowWidget(self)
        self.menu_hor_lay = FlowHLayout(self.menu_hor)
        self.menu_ver = QWidget(self)
        self.menu_ver_lay = QVBoxLayout(self.menu_ver)
        self.menu_spacer_hor = QSpacerItem(1, 16, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.menu_spacer_ver = QSpacerItem(16, 16, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding)
        # Vbox for toolbar when logger is collapsed in left position
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.menu_hor)
        self.vbox.addWidget(self.list_widget)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        # Hbox for toolbar in all other positions
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.menu_ver)
        self.hbox.addLayout(self.vbox)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        # Initial layout
        self.layout_logger_stats_hor()

        if parent.file_widget:
            parent.file_widget.file_opened.connect(self.clear)
        parent.set_log_level.connect(self.on_log_level_changed)

    def reset_warnings(self) -> None:
        self.warnings.clear()

    def reset_errors(self) -> None:
        self.errors.clear()

    def clear(self) -> None:
        # Do not preserve log
        if not self.preserve_log.isChecked():
            self.list_widget.clear()
        # Always reset values for the current file
        self.reset_warnings()
        self.reset_errors()

    def close(self) -> None:
        print("Close")
        super().close()

    def closeEvent(self, event: QCloseEvent) -> None:
        print("Close Event")
        super().closeEvent(event)

    def layout_logger_stats_hor(self) -> None:
        """Layout logger toolbar horizontally"""
        # Hide vertical widget and remove widgets from layout
        self.menu_ver.hide()
        self.menu_ver_lay.removeWidget(self.warnings)
        self.menu_ver_lay.removeWidget(self.errors)
        self.menu_ver_lay.removeItem(self.menu_spacer_ver)
        # Add left widgets
        self.menu_hor_lay.addWidget(self.warnings)
        self.menu_hor_lay.addWidget(self.errors)
        self.menu_hor_lay.addItem(self.menu_spacer_hor)
        # Add right Widgets
        self.menu_hor_lay.addWidget(self.preserve_log, alignment=Qt.AlignmentFlag.AlignRight, hide_index=3)
        self.menu_hor_lay.addWidget(self.log_level_choice, alignment=Qt.AlignmentFlag.AlignRight, hide_index=5)
        # Spacing, alignment, size policy for horizontal layout
        self.menu_hor_lay.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.menu_hor_lay.setSpacing(10)
        self.menu_hor.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        if self.orientation == Qt.Orientation.Vertical:
            self.menu_hor_lay.setContentsMargins(10, 0, 5, 0)
            self.menu_hor.setFixedHeight(self.ICON_BAR_SIZE)
        else:
            self.menu_hor_lay.setContentsMargins(5, 5, 5, 0)  # Extra space at top
            self.menu_hor.setFixedHeight(self.ICON_BAR_SIZE + 5)  # Accomodate extra space at top
        # Show and set LogStatus layout
        self.menu_hor.show()
        self.warnings.layout_horizontal()
        self.errors.layout_horizontal()

    def layout_logger_stats_ver(self) -> None:
        """Layout logger toolbar vertically"""
        # Hide horizontal widget and remove widgets from layout
        self.menu_hor.hide()
        self.menu_hor_lay.removeWidget(self.warnings)
        self.menu_hor_lay.removeWidget(self.errors)
        self.menu_hor_lay.removeItem(self.menu_spacer_hor)
        self.menu_hor_lay.removeWidget(self.preserve_log)
        self.menu_hor_lay.removeWidget(self.log_level_choice)
        self.menu_hor_lay.setContentsMargins(0, 0, 0, 0)
        # Add top widgets
        self.menu_ver_lay.addWidget(self.warnings)
        self.menu_ver_lay.addWidget(self.errors)
        self.menu_ver_lay.addItem(self.menu_spacer_ver)
        # Spacing, alignment, size policy for vertical layout
        self.menu_ver_lay.setContentsMargins(0, 5, 0, 0)
        self.menu_ver_lay.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.menu_ver.setLayout(self.menu_ver_lay)
        self.menu_ver.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.menu_ver.setFixedWidth(self.ICON_BAR_SIZE)
        # Show and set LogStatus layout
        self.menu_ver.show()
        self.warnings.layout_vertical()
        self.errors.layout_vertical()

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

    def resizeEvent(self, event: QResizeEvent) -> None:
        # Handle logger resizing from window instead of splitter handle
        if not self.splitter_moving:
            self.resize_logger(event.size().width(), event.size().height())
        # Inform listeners of current size
        self.current_size.emit(self.size())
        return super().resizeEvent(event)

    def on_splitterMoved(self, _pos: int = 0, _index: int = 0) -> None:
        """Slot for parent splitter's splitterMoved signal"""
        self.splitter_moving = True
        _x, _y, layout_width, layout_height = self.hbox.geometry().getRect()
        self.resize_logger(layout_width, layout_height)
        self.splitter_moving = False

    def resize_logger(self, layout_width: int, layout_height: int) -> None:
        """Handles splitter rubber banding and visibility of logger widgets based on available dimensions"""
        if self.orientation == Qt.Orientation.Vertical:
            if self.list_widget.isHidden() and layout_height >= self.MIN_HEIGHT or layout_height == 0:
                # Show and adjust sizing
                self.list_widget.show()
                self.preserve_log.show()
                self.hbox.setSpacing(4)
                self.menu_hor.setFixedHeight(20)
            elif layout_height < self.MIN_HEIGHT:
                # Hide and adjust sizing
                if not self.list_widget.isHidden():
                    self.list_widget.hide()
                    self.preserve_log.hide()
                    self.hbox.setSpacing(0)
                    self.menu_hor.setFixedHeight(16)
                # Keep logger at 0 below MIN_HEIGHT
                self.resize_requested.emit(self.ResizeRequest(size=0, expand_only=False))
        else:  # Horizontal
            if self.list_widget.isHidden() and (layout_width >= self.MIN_WIDTH + LoggerWidget.ICON_BAR_SIZE) or layout_width == 0:
                # Show and adjust sizing
                self.list_widget.show()
                if self.menu_hor.isHidden():
                    self.layout_logger_stats_hor()
                self.vbox.setContentsMargins(0, 0, 0, 0)
            elif self.list_widget.width() < self.MIN_WIDTH:
                # Hide and adjust sizing
                if not self.list_widget.isHidden():
                    self.list_widget.hide()
                    if self.menu_ver.isHidden():
                        self.layout_logger_stats_ver()
                    self.vbox.setContentsMargins(0, 0, 5, 0)
                # Keep logger at 0 below MIN_WIDTH
                self.resize_requested.emit(self.ResizeRequest(size=0, expand_only=False))

    def make_visible(self) -> None:
        """Resize the logger to ensure the log console can be visible at min dimensions"""
        if not self.list_widget.isVisible():
            size = 0
            if self.orientation == Qt.Orientation.Vertical:
                size = self.MIN_HEIGHT
                self.resize(self.width(), size)
            else:
                size = self.MIN_WIDTH
                self.resize(size, self.height())
            self.resize_requested.emit(self.ResizeRequest(size=size+self.ICON_BAR_SIZE))

    def expand_for_detail(self, height: int) -> None:
        """Auto increase logger dimensions for large detail texts"""
        self.resize_requested.emit(self.ResizeRequest(size=height))

    def on_select_row(self, row: int) -> None:
        """Handle logger visibility and scrolling on Jump To Warning/Error"""
        if row >= self.list_widget.count():
            return
        # Ensure row to scroll to is fetched
        while row >= self.list_widget.fetched_count():
            self.list_widget.fetchMore()
        # Ensure logger is visible
        self.make_visible()
        # Ensure row is visible
        index = self.list_widget.model().index(row, 0)
        self.list_widget.selectionModel().select(index, QItemSelectionModel.SelectionFlag.ClearAndSelect)
        self.list_widget.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)


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
    """Base proxy class for GamesWidget directory model"""

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

        regexp = self.filterRegularExpression()
        if not regexp.pattern():
            return True

        # Do not filter if root_depth hasn't been set or for folders before ovldata
        if self.root_depth == 0 or self.depth(idx) <= self.root_depth:
            return True

        return regexp.match(model.filePath(idx)).hasMatch()


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


class GamesWidget(QWidget):
    """Installed games combo box with optional search and directory widgets (caller has to add them to layout)"""
    installed_game_chosen = pyqtSignal(str)
    dir_dbl_clicked = pyqtSignal(str)
    file_dbl_clicked = pyqtSignal(str)
    search_content_clicked = pyqtSignal(str)

    def __init__(self, parent: "MainWindow",
                 games: Optional[list] = (),
                 filters: Optional[list[str]] = None,
                 game_chosen_fn: Optional[Callable] = None,
                 dir_dbl_click_fn: Optional[Callable] = None,
                 file_dbl_click_fn: Optional[Callable] = None,
                 search_content_fn: Optional[Callable] = None,
                 actions: dict = {}) -> None:
        super().__init__(parent)
        self.cfg: dict[str, Any] = parent.cfg
        self.games_list = games
        if filters is None:
            filters = ["*.ovl", ]

        self.entry = CleverCombo(self, options=[])
        self.entry.setEditable(False)
        self.entry.setToolTip("Select game for easy access")
        self.set_data(self.cfg["games"])

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

        self.search = QWidget()
        self.search_entry = QLineEdit("")
        self.search_entry.setPlaceholderText("Search Archives")
        self.search_button = QPushButton(get_icon("search"), "")
        # self.search_button.setMaximumWidth(20)
        self.search_button.clicked.connect(self.search_button_clicked)
        for btn in (self.search_entry, self.search_button):
            btn.setToolTip("Search OVL archives for uses of this string")
        vbox = QHBoxLayout(self.search)
        vbox.addWidget(self.search_button)
        vbox.addWidget(self.search_entry)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.entry.textActivated.connect(self.set_selected_game)
        self.play_button.clicked.connect(self.run_selected_game)
        self.add_button.clicked.connect(self.add_installed_game_manually)

        self.dirs = OvlDataTreeView(actions=actions, filters=filters)
        self.dirs.clicked.connect(self.item_clicked)
        self.dirs.doubleClicked.connect(self.item_dbl_clicked)

        self.filters = QWidget()
        self.filter_entry = IconEdit("filter", "Filter OVL Files", callback=self.set_filter)
        self.filter_entry.setToolTip("Filter by name - only show items matching this name")
        self.show_official_button = IconButton("ovl")
        self.show_modded_button = IconButton("modded")
        self.show_official_button.setCheckable(True)
        self.show_modded_button.setCheckable(True)
        self.show_official_button.toggled.connect(self.show_official_toggle)
        self.show_modded_button.toggled.connect(self.show_modded_toggle)
        self.show_official_button.setToolTip("Show official OVLs only")
        self.show_modded_button.setToolTip("Show modded OVLs only")

        vbox = QHBoxLayout(self.filters)
        vbox.addWidget(self.show_official_button)
        vbox.addWidget(self.show_modded_button)
        vbox.addWidget(self.filter_entry)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.set_games()

        if game_chosen_fn is not None:
            self.installed_game_chosen.connect(game_chosen_fn)
        if dir_dbl_click_fn is not None:
            self.dir_dbl_clicked.connect(dir_dbl_click_fn)
        if file_dbl_click_fn is not None:
            self.file_dbl_clicked.connect(file_dbl_click_fn)
        if search_content_fn is not None:
            self.search_content_clicked.connect(search_content_fn)
            self.search_entry.returnPressed.connect(self.search_button_clicked)
            self.search_entry.textChanged.connect(self.force_lowercase)

    def set_dirs_regexp(self, regexp):
        self.dirs.proxy.setFilterRegularExpression(QRegularExpression(regexp,
                                                                 options=QRegularExpression.PatternOption.CaseInsensitiveOption))

    def show_modded_toggle(self, checked: bool) -> None:
        if checked:
            self.filter_entry.entry.setText("")
            self.show_official_button.setChecked(False)
            self.set_dirs_regexp(f"^((?!({'|'.join(valid_packages)})).)*$")
        else:
            self.set_dirs_regexp("")

    def show_official_toggle(self, checked: bool) -> None:
        if checked:
            self.filter_entry.entry.setText("")
            self.show_modded_button.setChecked(False)
            self.set_dirs_regexp(f"^.*({'|'.join(valid_packages)}).*$")
        else:
            self.set_dirs_regexp("")

    def set_filter(self):
        filter_str = self.filter_entry.entry.text()
        if filter_str:
            # turn off the other filters if a filter search string was entered
            self.show_modded_button.setChecked(False)
            self.show_official_button.setChecked(False)
            # expand to also filter folders have not been opened before - sometimes slow but easy
            self.dirs.expandAll()
            # set filter function for search string
            self.set_dirs_regexp(f"^.*({filter_str}).*$")
        else:
            self.set_dirs_regexp("")

    def force_lowercase(self, text):
        self.search_entry.setText(text.lower())

    def search_button_clicked(self):
        search_txt = self.search_entry.text()
        if search_txt:
            self.search_content_clicked.emit(search_txt)

    def set_depth(self, depth: int) -> None:
        """Set max visible subfolder depth. Depth = 0 root folders in ovldata only."""
        self.dirs.proxy.set_max_depth(depth)

    def item_clicked(self, idx: QModelIndex) -> None:
        if not self.dirs.isExpanded(idx):
            self.dirs.expand(idx)

    def item_dbl_clicked(self, idx: QModelIndex) -> None:
        try:
            file_path = self.dirs.file_model.filePath(idx)
            # open folder in explorer
            if os.path.isdir(file_path):
                os.startfile(file_path)
                self.dir_dbl_clicked.emit(file_path)
            # open in tool
            else:
                self.file_dbl_clicked.emit(file_path)
        except:
            logging.exception("Item double-click failed")

    def game_chosen(self, game: str) -> None:
        """Run after choosing a game from dropdown of installed games"""
        self.cfg["current_game"] = game
        # only update the ovl game version choice if it is a valid game
        if game in self.games_list:
            self.installed_game_chosen.emit(game)

    def ask_game_dir(self) -> str:
        """Ask the user to specify a game root folder"""
        return QFileDialog.getExistingDirectory(self, "Open game folder")

    def get_selected_game(self) -> str:
        return self.entry.currentText()

    def set_selected_game(self, game: str = None):
        # if current_game hasn't been set (no config.json), fall back on currently selected game
        if not game:
            game = self.get_selected_game()
        dir_game = self.cfg["games"].get(game, None)
        # if current_game has been set, assume it exists in the games dict too (from steam)
        if dir_game:
            self.set_root(dir_game)
            self.set_selected_path(self.cfg.get("last_ovl_in", None))
            self.entry.setText(game)
            self.game_chosen(game)

    def run_selected_game(self):
        selected_game = self.get_selected_game()
        launch_game(selected_game, self.cfg)

    def set_root(self, dir_game: str) -> None:
        root_index = self.dirs.file_model.setRootPath(dir_game)
        self.dirs.setRootIndex(root_index)
        self.dirs.proxy.update_root(self.dirs.rootIndex())

    def get_root(self) -> str:
        return self.dirs.file_model.rootPath()

    def get_selected_dir(self) -> str:
        file_path = self.dirs.file_model.filePath(self.dirs.currentIndex())
        # if a file is selected, get its containing dir
        return file_path if os.path.isdir(file_path) else os.path.dirname(file_path)

    def set_selected_path(self, file_path: str) -> None:
        """Select file_path in dirs view"""
        try:
            self.dirs.setCurrentIndex(self.dirs.file_model.index(file_path))
        except:
            logging.exception("Setting dir failed")

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
            self.cfg["current_game"] = current_game
            # update available games
            self.set_data(self.cfg["games"])

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

    def set_games(self) -> None:
        self.cfg["games"].update(get_steam_games(self.games_list))
        self.set_data(self.cfg["games"])


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
        self.central_layout: QLayout = QVBoxLayout()

        self.title_sep = " | "
        self.title_sep_colored = " <font color=\"#5f5f5f\">|</font> "
        if self.opts.frameless:
            self.setTitleBar(TitleBar(self))

        self.menu_bar = QMenuBar(self)
        self.menu_bar.setStyleSheet("QMenuBar {background: transparent;}")
        self.actions: dict[str, QAction] = {}

        self.name = name
        self.log_name = ""
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon(os.path.join(root_dir, f'icons/Cobra_Tools_Logo_24px.svg')))  # Do not cache with get_icon
        self._stdout_handler: logging.StreamHandler | None = None

        self.file_widget: Optional[FileWidget] = None
        self.logger: Optional[LoggerWidget] = None
        self.log_splitter: Optional[QSplitter] = None
        self.logger_orientation: Qt.Orientation = Qt.Orientation.Vertical

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
        self.version_info.setFont(QFont("Consolas, monospace", 8))
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

    def layout_splitter(self, grid, left_frame, right_frame):
        # Setup Logger
        orientation = QtCore.Qt.Orientation.Vertical if self.cfg.get("logger_orientation",
                                                                     "V") == "V" else QtCore.Qt.Orientation.Horizontal
        self.show_logger = self.cfg.get("logger_show", True)

        self.file_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.file_splitter.addWidget(left_frame)
        self.file_splitter.addWidget(right_frame)
        self.file_splitter.setSizes([200, 400])
        self.file_splitter.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        self.file_splitter.setContentsMargins(0, 0, 0, 0)
        topleft = self.file_splitter
        if orientation == QtCore.Qt.Orientation.Vertical:
            self.file_splitter.setContentsMargins(5, 0, 5, 0)
            grid.setContentsMargins(5, 0, 5, 5)
            self.central_layout.addLayout(grid)
            self.central_layout.setSpacing(5)
        else:
            topleft = QtWidgets.QWidget()
            box = QtWidgets.QVBoxLayout()
            box.addLayout(grid)
            box.addWidget(self.file_splitter)
            topleft.setLayout(box)
        # Layout Logger
        if self.show_logger:
            self.layout_logger(topleft, orientation)
        else:
            self.central_layout.addWidget(topleft)

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

    def make_logger_widget(self, topleft: QWidget, orientation: Qt.Orientation = Qt.Orientation.Vertical,
                           sizes: tuple[int, int] = (600, 200),
                           log_level_changed_fn: Optional[Callable] = None,
                           resize_requested_fn: Optional[Callable] = None) -> tuple[LoggerWidget, QSplitter]:
        logger = LoggerWidget(self, orientation)
        logger.handler.setFormatter(logs.HtmlFormatter('%(levelname)s | %(message)s'))
        logger.handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(logger.handler)

        self.logger_orientation = orientation
        log_splitter = QSplitter(orientation)
        log_splitter.addWidget(topleft)
        log_splitter.addWidget(logger)
        log_splitter.setSizes(list(sizes))
        log_splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        log_splitter.setContentsMargins(0, 0, 0, 0)
        log_splitter.setCollapsible(1, False)
        if orientation == Qt.Orientation.Vertical:
            style = R"""
                QSplitter::handle:vertical {
                    padding: 0px 0px 4px 0px;
                }
            """
            log_splitter.setStyleSheet(style)

        log_splitter.splitterMoved.connect(logger.on_splitterMoved)

        if log_level_changed_fn:
            logger.log_level_changed.connect(log_level_changed_fn)
        if resize_requested_fn:
            logger.resize_requested.connect(resize_requested_fn)

        if self.logger_orientation == Qt.Orientation.Horizontal:
            # Make MainWindow larger by default
            self.resize(1024, 600)
            log_splitter.setSizes([700, 324])
            log_splitter.setStretchFactor(0, 1000)
            log_splitter.setStretchFactor(1, 1)
            # Keep status widgets right-aligned with main layout, ignoring logger.
            spacer = StatusSpacer(self)
            self.status_bar.addPermanentWidget(spacer)
            spacer.set_widget(logger)
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
                    config_setting = self.cfg.get(item.config_name, False)
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
        worker.signals.finished.connect(self.enable_gui_options)
        worker.signals.finished.connect(self.choices_update)
        for callback in callbacks:
            # print(f"connecting {callback}")
            worker.signals.finished.connect(callback)
        self.threadpool.start(worker)
        self.enable_gui_options(False)

    def enable_gui_options(self, enable=True):
        pass

    def choices_update(self):
        pass

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.file_widget and self.file_widget.dirty:
            quit_msg = f"Quit? You will lose unsaved work on {os.path.basename(self.file_widget.filepath)}!"
            if not self.showconfirmation(quit_msg, title="Quit"):
                event.ignore()
                return
        event.accept()
        self.close_logs()

    def layout_logger(self, topleft: QWidget, orientation: Qt.Orientation) -> None:
        self.logger, self.log_splitter = self.make_logger_widget(topleft=topleft,
                                                                 orientation=orientation,
                                                                 log_level_changed_fn=self.on_log_level_changed,
                                                                 resize_requested_fn=self.resize_logger)
        self.central_layout.addWidget(self.log_splitter)

    def resize_logger(self, request: LoggerWidget.ResizeRequest) -> None:
        if not hasattr(self, 'logger') or not hasattr(self, 'log_splitter'):
            return
        if not self.logger or not self.log_splitter:
            return

        if self.logger_orientation == Qt.Orientation.Vertical:
            if request.size > 0:
                logger_size = request.size + LoggerWidget.ICON_BAR_SIZE
                current_sizes = self.log_splitter.sizes()
                if not request.expand_only or current_sizes[1] < logger_size:
                    self.log_splitter.setSizes([self.log_splitter.widget(0).height() - logger_size, logger_size])
                    self.logger.on_splitterMoved()
            else:
                self.log_splitter.setSizes([400, 0])
        else:
            if request.size > 0:
                logger_size = min(request.size, 400)
                current_sizes = self.log_splitter.sizes()
                if not request.expand_only or current_sizes[1] < logger_size:
                    self.log_splitter.setSizes([self.log_splitter.widget(0).width() - logger_size, logger_size])
                    self.logger.on_splitterMoved()
            else:
                self.log_splitter.setSizes([800, 0])

    def on_log_level_changed(self, level: str) -> None:
        if self.stdout_handler:
            self.stdout_handler.setLevel(level)
        level = level if level != "SUCCESS" else "WARNING"  # So SUCCESS is still shown at "WARNING" level
        self.cfg["logger_level"] = level

    def close_logs(self) -> None:
        if self.log_name:
            removed_handlers: list[logging.Handler] = []
            for handler in logging.getLogger().handlers:
                if isinstance(handler, logs.LogBackupFileHandler) and handler.name and handler.name == self.log_name:
                    removed_handlers.append(handler)
                elif isinstance(handler, LoggerWidget) and isinstance(handler.parent(), MainWindow):
                    removed_handlers.append(handler)
            for handler in reversed(removed_handlers):
                logging.debug(f"Closing Log: {type(handler).__name__}: {handler.get_name() if handler.get_name() else handler}")
                logging.getLogger().removeHandler(handler)
                handler.close()

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
    finished = pyqtSignal()
    error_msg = pyqtSignal(str)

    def __init__(self, func: Callable, *args, **kwargs) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self) -> None:
        try:
            self.func(*self.args, **self.kwargs)
        except BaseException as err:
            logging.exception(f"Threaded call of function '{self.func.__name__}()' errored!")
            self.signals.error_msg.emit(str(err))
        finally:
            self.signals.finished.emit()


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


def pack_in_box(*widgets, margins=(0, 0, 0, 0)):
    frame = QtWidgets.QWidget()
    box = QtWidgets.QVBoxLayout()
    for w in widgets:
        box.addWidget(w)
    box.setContentsMargins(*margins)
    box.setSizeConstraint(QtWidgets.QVBoxLayout.SizeConstraint.SetNoConstraint)
    frame.setLayout(box)
    return frame
