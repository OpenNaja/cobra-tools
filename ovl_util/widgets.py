import contextlib
import logging
import webbrowser
import os
import sys
import re
import time
import subprocess  # used to launch a pip install process

"""
    Require Python >= 3.11
"""
if (sys.version_info.major, sys.version_info.minor) < (3, 11):
    logging.critical("Python 3.11 or later is required. Please update your Python installation.")
    time.sleep(60)

from abc import abstractmethod
from pkg_resources import packaging  # type: ignore
from pathlib import Path
from importlib.metadata import distribution, PackageNotFoundError
# Place typing imports after Python check
from typing import Any, AnyStr, Optional, Iterable, Callable, cast

from ovl_util.config import ANSI

"""
    Deals with missing packages and tries to install them from the tool itself.
"""

# raw_input returns the empty string for "enter"
def install_prompt(question):
    print(question)
    print(f"{ANSI.LIGHT_YELLOW}[Type y and hit Enter]{ANSI.END}{ANSI.LIGHT_GREEN}")
    yes = {'yes', 'y', 'ye'}
    choice = input().lower()
    if choice in yes:
        return True
    else:
        return False

# use pip to install a package
def pip_install(package):
    logging.info(f"Installing {package}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# use pip to install --update a package
def pip_upgrade(package):
    logging.info(f"Updating {package}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

missing = []
needs_update = []

with open("requirements.txt") as requirements:
    lines = requirements.read().splitlines()
    for line in lines:
        lib, op, version = re.split("(~=|==|>|<|>=|<=)", line)
        try:
            lib_dist = distribution(lib)
            if packaging.version.parse(lib_dist.metadata['Version']) < packaging.version.parse(version):
                logging.warning(f"{lib} is out of date.")
                # Append full line including ~= for pip upgrade command
                needs_update.append(line)
        except PackageNotFoundError:
            logging.error(f"{lib} not found.")
            # Append full line including ~= for pip install command
            missing.append(line)

ask_install = f"{ANSI.LIGHT_WHITE}Install the missing dependencies?{ANSI.END} (y/N)"
ask_upgrade = f"{ANSI.LIGHT_WHITE}Update the outdated dependencies?{ANSI.END} (y/N)"

if len(missing) and install_prompt(ask_install) == True:
    # upgrade pip then try installing the rest of packages
    pip_upgrade('pip')
    for package in missing:
        pip_install(package)

if len(needs_update) and install_prompt(ask_upgrade) == True:
    # upgrade pip then try updating the outdated packages
    pip_upgrade('pip')
    for package in needs_update:
        pip_upgrade(package)

""" End of installing dependencies """

try:
    from generated.formats.ovl import OvlFile, games
    from ovl_util.config import get_commit_str
    from ovl_util import config
    from root_path import root_dir

    from PyQt5 import QtGui, QtCore, QtWidgets
    from ovl_util import qt_theme, interaction
    import vdf

    games_list = [g.value for g in games]
except:
    logging.exception("Some modules could not be imported; make sure you install the required dependencies with pip!")
    time.sleep(15)

# Put used imports below try/except for typing purposes (to avoid `| Unbound` type unions)
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject, QDir, QRegularExpression,
                          QRect, QSize, QEvent, QTimer, QTimerEvent, QThread, QUrl,
                          QAbstractTableModel, QSortFilterProxyModel, QModelIndex, QItemSelection,
                          QAbstractAnimation, QParallelAnimationGroup, QPropertyAnimation)
from PyQt5.QtGui import (QBrush, QColor, QFont, QFontMetrics, QIcon, QPainter, QPen,
                         QStandardItemModel, QStandardItem,
                         QCloseEvent, QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent,
                         QFocusEvent, QMouseEvent, QPaintEvent, QResizeEvent, QWheelEvent)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QColorDialog, QFileDialog,
                             QAbstractItemView, QHeaderView, QTableView, QTreeView, QFileSystemModel,
                             QAction, QCheckBox, QComboBox, QDoubleSpinBox, QLabel, QLineEdit, QMenu, QMenuBar,
                             QMessageBox, QPlainTextEdit, QProgressBar, QPushButton, QStatusBar, QToolButton,
                             QFrame, QLayout, QGridLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy,
                             QStyleFactory, QStyleOptionViewItem, QStyledItemDelegate)

# Windows modules
try:
    import winreg
    WINDOWS = True
except:
    logging.warning("Required Windows modules missing; some features may not work.")
    WINDOWS = False

try:
    from qframelesswindow import FramelessMainWindow, StandardTitleBar
    FRAMELESS = True
except:
    FramelessMainWindow = QMainWindow
    StandardTitleBar = QWidget
    FRAMELESS = False

MAX_UINT = 4294967295
myFont = QFont()
myFont.setBold(True)


def startup(cls):
    app_qt = QApplication([])
    win = cls()
    win.show()

    # style
    if not win.cfg.get("light_theme", False):
        app_qt.setStyle(QStyleFactory.create('Fusion'))
        app_qt.setPalette(qt_theme.dark_palette)
        app_qt.setStyleSheet("QToolTip { color: #ffffff; background-color: #353535; border: 1px solid white; }")
    app_qt.exec_()
    config.save_config(win.cfg)

def vbox(parent, grid):
    """Adds a grid layout"""
    # vbox = QVBoxLayout()
    # vbox.addLayout(grid)
    # vbox.addStretch(1.0)
    # vbox.setSpacing(0)
    # vbox.setContentsMargins(0,0,0,0)
    parent.setLayout(grid)

ICON_CACHE = {"no_icon": QIcon()}
def get_icon(name) -> QIcon:
    if name in ICON_CACHE:
        return ICON_CACHE[name]
    for ext in (".png", ".svg"):
        fp = os.path.join(root_dir, f'icons/{name}{ext}')
        if os.path.isfile(fp):
            ICON_CACHE[name] = QIcon(fp)
            return ICON_CACHE[name]
    return ICON_CACHE["no_icon"]


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

    def __init__(self, header_names: list[str], ignore_types: list[str]) -> None:
        super(TableModel, self).__init__()
        self._data: list[list[str]] = []
        self.header_labels = header_names
        self.ignore_types = ignore_types
        # self.member_renamed.connect(self.member_renamed_debug_print)

    @staticmethod
    def member_renamed_debug_print(a, b) -> None:
        print("renamed", a, b)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        file_row = self._data[index.row()]
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if len(file_row):
                return self._data[index.row()][index.column()]

        # TODO: Remove some hardcoding surrounding File Type
        if "File Type" in self.header_labels:
            type_idx = self.header_labels.index("File Type")
            if role == Qt.ItemDataRole.ForegroundRole:
                if len(file_row) and file_row[type_idx] in self.ignore_types:
                    return QColor('grey')

            if role == Qt.ItemDataRole.DecorationRole:
                if index.column() == 0:
                    if len(file_row):
                        # remove the leading '.' from ext
                        return get_icon(file_row[type_idx][1:])

        if role == Qt.ItemDataRole.TextAlignmentRole:
            # center align non-primary integer columns
            if index.column() > 0 and str(file_row[index.column()]).isnumeric():
                return Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.DisplayRole) -> bool:
        if index.isValid():
            if role == Qt.ItemDataRole.EditRole:
                row = index.row()
                column = index.column()
                old_value = self._data[row][column]
                # value has changed, gotta update it
                if old_value != value:
                    self._data[row][column] = value
                    self.member_renamed.emit(old_value, value)
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
        d_n_d = Qt.ItemFlags(cast(Qt.ItemFlags, Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled | Qt.ItemFlag.ItemIsSelectable))
        renamable = Qt.ItemFlags(cast(Qt.ItemFlags, Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled))
        state = Qt.ItemFlags(cast(Qt.ItemFlags, Qt.ItemFlag.NoItemFlags))
        if index.column() == 0:
            state |= renamable
        if len(dtype) and dtype[1] not in self.ignore_types:
            state |= d_n_d
        return state


class SortableTable(QWidget):
    def __init__(self, header_names, ignore_types, ignore_drop_type="", opt_hide=False):
        super().__init__()
        self.table = TableView(header_names, ignore_types, ignore_drop_type)
        self.filter_entry = LabelEdit("Filter")
        self.filter_entry.entry.textChanged.connect(self.table.set_filter)
        self.hide_unused = QCheckBox("Hide unextractable files")
        if opt_hide:
            self.hide_unused.stateChanged.connect(self.toggle_hide)
        else:
            self.hide_unused.hide()
        self.rev_search = QCheckBox("Exclude Search")
        self.rev_search.stateChanged.connect(self.toggle_rev)
        self.clear_filters = QPushButton("Clear")
        self.clear_filters.pressed.connect(self.clear_filter)

        # Button Row Setup
        self.button_count = 0
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_frame = QFrame()
        self.btn_frame.setLayout(self.btn_layout)

        qgrid = QGridLayout()
        qgrid.addWidget(self.filter_entry, 0, 0, )
        qgrid.addWidget(self.hide_unused, 0, 1, )
        qgrid.addWidget(self.rev_search, 0, 2, )
        qgrid.addWidget(self.clear_filters, 0, 3, )
        qgrid.addWidget(self.table, 2, 0, 1, 4)
        qgrid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(qgrid)
        self.grid = qgrid

    def set_data(self, data):
        self.table.set_data(data)

    def clear_filter(self, ):
        self.filter_entry.entry.setText("")
        self.hide_unused.setChecked(False)
        self.rev_search.setChecked(False)
        self.table.clear_filter()

    def toggle_hide(self, state):
        self.table.set_ext_filter(self.hide_unused.isChecked())

    def toggle_rev(self, state):
        if self.rev_search.isChecked():
            self.table.rev_check = True
            self.table.update_filter_function()
        else:
            self.table.rev_check = False
            self.table.update_filter_function()

    def add_button(self, btn):
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

    def __init__(self, header_names: list[str], ignore_types: list[str], ignore_drop_type: str) -> None:
        super().__init__()
        self.ignore_types = ignore_types
        self.header_names = header_names
        self.ignore_drop_type = ignore_drop_type
        self.table_model = TableModel(header_names, ignore_types)
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
        self.rev_check = False
        self.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        # handle column width
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        # The number of selected items in the model
        self.selected_count = 0

    def on_selectionChanged(self, _selected: QItemSelection, _deselected: QItemSelection) -> None:
        self.selected = list(self.get_selected_line_indices())
        if self.selected:
            self.file_selected.emit(self.selected[-1])
        self.file_selected_count.emit(self.selected_count)

    def update_filter_function(self) -> None:
        if self.rev_check:
            self.proxy_model.addFilterFunction('name', lambda r, s: s not in r[0])
        else:
            self.proxy_model.addFilterFunction('name', lambda r, s: s in r[0])

    def set_filter(self, fixed_string: str) -> None:
        self.proxy_model.setFilterFixedString(fixed_string)
        self.update_filter_function()

    def set_ext_filter(self, hide: bool) -> None:
        ext_filter_name = "ext_filter"
        if hide and "File Type" in self.header_names:
            def ext_filter(r, s):
                return r[self.header_names.index("File Type")] not in self.ignore_types

            self.proxy_model.addFilterFunction(ext_filter_name, ext_filter)
        else:
            self.proxy_model.removeFilterFunction(ext_filter_name)

    def clear_filter(self) -> None:
        # self.proxy_model.setFilterFixedString("")
        self.proxy_model.setFilterFixedString("")
        self.sortByColumn(-1, Qt.SortOrder.AscendingOrder)

    def get_selected_line_indices(self) -> set[int]:
        indices = set(self.proxy_model.mapToSource(x).row() for x in self.selectedIndexes())
        self.selected_count = len(indices)
        return indices

    def get_selected_files(self) -> list[str]:
        # map the selected indices to the actual underlying data, which is in its original order
        return [self.table_model._data[x][0] for x in self.get_selected_line_indices()]

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

    def setEnabledFromSelection(self, selection: QItemSelection):
        self.setEnabled(selection.count() > 0)


class QTextEditLogger(logging.Handler, QObject):
    """Text field to hold log information."""
    appendPlainText = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget]) -> None:
        super().__init__()
        QObject.__init__(self, parent)
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.appendPlainText.connect(self.widget.appendPlainText)

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        self.appendPlainText.emit(msg)


class LabelEdit(QWidget):
    def __init__(self, name, ):
        QWidget.__init__(self, )
        self.label = QLabel(name)
        self.entry = QLineEdit()
        vbox = QHBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.entry)
        vbox.setContentsMargins(0, 0, 0, 0)
        # vbox.addStretch(1)
        self.setLayout(vbox)


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
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

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
        elidedText = metrics.elidedText(text, Qt.TextElideMode.ElideRight, self.lineEdit().width())
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

    def depth(self, idx: QModelIndex) -> int:
        """Depth of the file or directory in the filesystem"""
        level = 0
        index = idx
        while index.parent().isValid():
            level += 1
            index = index.parent()
        return level

    def set_max_depth(self, depth: int) -> None:
        """Set max subfolder depth. 0 depth = ovldata root folders only."""
        self.max_depth = depth

    def update_root(self, idx: QModelIndex) -> None:
        """Update root index and store base depth for ovldata subfolder"""
        self.root_idx = idx
        self.root_depth = self.depth(idx)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == QFileSystemModel.Roles.FileIconRole:
            name = index.data()
            _, ext = os.path.splitext(name)
            if ext:
                return get_icon(ext[1:])
            return get_icon("dir")
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

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        """Sort how QFileSystemModel sorts"""
        model = cast("OvlDataFilesystemModel", self.sourceModel())
        return model.fileInfo(left).isDir() and not model.fileInfo(right).isDir()

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


class OvlDataTreeView(QTreeView):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)


class GamesWidget(QWidget):
    """Installed games combo box with optional directory widget"""
    installed_game_chosen = pyqtSignal(str)
    dir_dbl_clicked = pyqtSignal(QModelIndex)
    file_dbl_clicked = pyqtSignal(QModelIndex)

    def __init__(self, parent: "MainWindow", filters: Optional[list[str]] = None,
                 game_chosen_fn: Optional[Callable] = None,
                 dir_dbl_click_fn: Optional[Callable] = None,
                 file_dbl_click_fn: Optional[Callable] = None) -> None:
        super().__init__(parent)
        self.cfg: dict[str, Any] = parent.cfg
        if filters is None:
            filters = ["*.ovl",]

        self.entry = CleverCombo(self, options=[])
        self.entry.setEditable(False)
        self.set_data(self.cfg["games"].keys())

        self.add_button = QPushButton("+")
        self.add_button.setMaximumWidth(20)

        vbox = QHBoxLayout(self)
        vbox.addWidget(self.entry)
        vbox.addWidget(self.add_button)
        # vbox.addWidget(self.delete_button)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.setToolTip("Select game for easy access below")
        
        self.entry.textActivated.connect(self.game_chosen)
        self.add_button.clicked.connect(self.add_installed_game)

        self.model = OvlDataFilesystemModel()
        self.model.setNameFilters(filters)
        self.model.setNameFilterDisables(False)

        self.dirs = OvlDataTreeView()
        self.dirs.setModel(self.model)
        self.dirs.setColumnHidden(1, True)
        self.dirs.setColumnHidden(2, True)
        self.dirs.setColumnHidden(3, True)
        self.dirs.setExpandsOnDoubleClick(False)
        self.dirs.clicked.connect(self.item_clicked)
        self.dirs.doubleClicked.connect(self.item_dbl_clicked)

        self.dirs.header().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        self.dirs.model().sort(self.dirs.header().sortIndicatorSection(), self.dirs.header().sortIndicatorOrder())

        self.proxy = OvlDataFilterProxy(self)
        self.proxy.setSourceModel(self.model)
        self.dirs.setModel(self.proxy)

        self.dirs.setAnimated(False)
        self.dirs.setIndentation(12)
        self.dirs.setSortingEnabled(True)

        self.set_games()

        if game_chosen_fn is not None:
            self.installed_game_chosen.connect(game_chosen_fn)
        if dir_dbl_click_fn is not None:
            self.dir_dbl_clicked.connect(dir_dbl_click_fn)
        if file_dbl_click_fn is not None:
            self.file_dbl_clicked.connect(file_dbl_click_fn)

    def hide_official(self) -> None:
        self.proxy.setFilterRegularExpression(QRegularExpression("^((?!(Content|DLC|GameMain)).)*$",
                                                                 options=QRegularExpression.PatternOption.CaseInsensitiveOption))
    
    def hide_modded(self) -> None:
        self.proxy.setFilterRegularExpression(QRegularExpression("^.*(Content|GameMain|.*DLC).*$",
                                                                 options=QRegularExpression.PatternOption.CaseInsensitiveOption))

    def set_depth(self, depth: int) -> None:
        """Set max visible subfolder depth. Depth = 0 root folders in ovldata only."""
        self.proxy.set_max_depth(depth)

    def item_clicked(self, idx: QModelIndex) -> None:
        if not self.dirs.isExpanded(idx):
            self.dirs.expand(idx)
        else:
            self.dirs.collapse(idx)

    def item_dbl_clicked(self, idx: QModelIndex) -> None:
        try:
            idx = self.proxy.mapToSource(idx)
            model = cast(OvlDataFilesystemModel, idx.model())
            file_path = model.filePath(idx)
            # open folder in explorer
            if os.path.isdir(file_path):
                os.startfile(file_path)
                self.dir_dbl_clicked.emit(idx)
            # open in tool
            else:
                self.file_dbl_clicked.emit(idx)
        except:
            MainWindow.handle_error("Clicked dir failed, see log!")

    def game_chosen(self, current_game: str) -> None:
        """Run after choosing a game from dropdown of installed games"""
        self.cfg["current_game"] = current_game
        self.installed_game_chosen.emit(current_game)

    def ask_game_dir(self) -> str:
        """Ask the user to specify a game root folder"""
        return QFileDialog.getExistingDirectory(self, "Open game folder")

    def get_selected_game(self) -> str:
        return self.entry.currentText()

    def set_selected_game(self, current_game: str) -> bool:
        # if current_game hasn't been set (no config.json), fall back on currently selected game
        dir_game = self.cfg["games"].get(current_game, self.get_selected_game())
        # if current_game has been set, assume it exists in the games dict too (from steam)
        if dir_game:
            self.set_root(dir_game)
            self.set_selected_dir(self.cfg.get("last_ovl_in", None))
            self.entry.setText(current_game)
            if current_game in games_list:
                return True
        return False
    
    def set_root(self, dir_game: str) -> None:
        rt_index = self.model.setRootPath(dir_game)
        self.dirs.setRootIndex(self.proxy.mapFromSource(rt_index))
        self.proxy.update_root(self.dirs.rootIndex())

    def get_selected_dir(self) -> str:
        ind = self.dirs.currentIndex()
        file_path = self.model.filePath(ind)
        return file_path if os.path.isdir(file_path) else ""

    def set_selected_dir(self, dir_path: str) -> None:
        """Show dir_path in dirs"""
        try:
            ind = self.model.index(dir_path)
            self.dirs.setCurrentIndex(ind)
        except:
            MainWindow.handle_error("Setting dir failed, see log.")

    def add_installed_game(self) -> None:
        """Add a new game to the list of available games"""
        dir_game = self.ask_game_dir()
        if dir_game:
            # todo - try to find the name of the game by stripping usual suffixes, eg. "win64\\ovldata"
            current_game = os.path.basename(dir_game)
            # store this newly chosen game in cfg
            self.cfg["games"][current_game] = dir_game
            self.cfg["current_game"] = current_game
            # update available games
            self.set_data(self.cfg["games"].keys())

    def set_data(self, items: Iterable[str]) -> None:
        self.entry.clear()
        self.entry.addItems(sorted(set(items)))

    def set_filter(self, proxy_cls: type[OvlDataFilterProxy]) -> None:
        self.proxy = proxy_cls(self)
        self.proxy.setSourceModel(self.model)
        self.dirs.setModel(self.proxy)

    def set_games(self) -> None:
        self.cfg["games"].update(self.get_steam_games())
        self.set_data(self.cfg["games"].keys())

    def get_steam_games(self) -> dict[str, str]:
        try:
            # get steam folder from windows registry
            hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Valve\\Steam")
            steam_query = winreg.QueryValueEx(hkey, "InstallPath")
            # get path to steam games folder
            # C:\\Program Files (x86)\\Steam
            steam_path = steam_query[0]
            library_folders = {steam_path}
            vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
            # check if there are other steam library folders (eg. on external drives)
            try:
                v = vdf.load(open(vdf_path))
                for folder in v["libraryfolders"].values():
                    library_folders.add(folder["path"])
            except:
                logging.warning(
                    f"vdf not installed, can not detect steam games on external drives - run `pip install vdf`")

            # map all installed fdev game names to their path
            fdev_games = {}
            # list all games for each library folder
            for steam_path in library_folders:
                try:
                    apps_path = os.path.join(steam_path, "steamapps\\common")
                    # filter with supported fdev games
                    fdev_in_lib = [game for game in os.listdir(apps_path) if game in games_list]
                    # generate the whole path for each game, add to dict
                    # C:\Program Files (x86)\Steam\steamapps\common\Planet Zoo\win64\ovldata
                    fdev_games.update({game: os.path.join(apps_path, game, "win64\\ovldata") for game in fdev_in_lib})
                except FileNotFoundError as e:
                    logging.warning(e)
            logging.info(f"Found {len(fdev_games)} Cobra games from Steam")
            return fdev_games
        except:
            logging.exception(f"Getting installed games from steam folder failed")
            return {}


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
    def __init__(self, name: str, options: Iterable[str], editable: bool = True, activated_fn: Optional[Callable] = None) -> None:
        QWidget.__init__(self, )
        self.label = QLabel(name)
        self.entry = CleverCombo(self, options=options)
        self.entry.setEditable(editable)
        box = QHBoxLayout(self)
        box.addWidget(self.label)
        box.addWidget(self.entry)
        box.setContentsMargins(0, 0, 0, 0)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # # sizePolicy.setHeightForWidth(self.entry.sizePolicy().hasHeightForWidth())
        self.entry.setSizePolicy(sizePolicy)
        self.setSizePolicy(sizePolicy)

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

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

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


class MatcolInfo:
    def __init__(self, attrib, tooltips={}):
        """attrib must be pyffi matcol InfoWrapper object"""
        self.attrib = attrib
        name = attrib.info_name.data
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._color = None
        self.setMaximumWidth(32)
        self.pressed.connect(self.onColorPicker)
        QDir.addSearchPath("icon", self.get_icon_dir())

    def get_icon_dir(self):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "icons")

    def setColor(self, color):
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

    def color(self):
        return self._color

    def onColorPicker(self):
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

    def setValue(self, c):
        self.setColor(QColor(c.r, c.g, c.b, c.a))

    def getValue(self, ):
        if self._color:
            print(self._color.getRgb())


class FileDirWidget(QWidget):
    dir_opened = pyqtSignal(str)
    filepath_changed = pyqtSignal(str, bool)

    def __init__(self, parent: QWidget, cfg: dict, type: str, ask_user: bool = True, editable: bool = False,
                 check_exists: bool = False, root: Optional[str] = None) -> None:
        super().__init__(parent)

        self.type = type
        self.root = root
        self.cfg = cfg
        self.cfg.setdefault(self.cfg_last_dir_open, "C:/")
        self.cfg.setdefault(self.cfg_last_dir_save, "C:/")
        self.cfg.setdefault(self.cfg_last_file_open, "C:/")

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
    def type_lower(self) -> str:
        return self.type.lower()

    @property
    def cfg_last_dir_open(self) -> str:
        return f"dir_{self.type_lower}s_in"

    @property
    def cfg_last_dir_save(self) -> str:
        return f"dir_{self.type_lower}s_out"

    @property
    def cfg_last_file_open(self) -> str:
        return f"last_{self.type_lower}_in"

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
        if self.filepath:
            self.dirty = dirty
            self.filepath_changed.emit(self.filepath, self.dirty)


class FileWidget(FileDirWidget):
    """An entry widget that starts a file selector when clicked and also accepts drag & drop.
    Displays the current file's basename.
    """
    file_opened = pyqtSignal(str)
    file_saved = pyqtSignal(str)

    def __init__(self, parent: QWidget, cfg: dict, type: str = "OVL", ask_user: bool = True, editable: bool = False,
                 check_exists: bool = False, root: Optional[str] = None) -> None:
        super().__init__(parent=parent, cfg=cfg, type=type, ask_user=ask_user,
                         editable=editable, check_exists=check_exists, root=root)

        self.icon.setToolTip("Click to select a file")
        self.entry.setToolTip(self.tooltip_str)

    @property
    def files_filter_str(self) -> str:
        return f"{self.type} files (*.{self.type_lower})"

    @property
    def tooltip_str(self) -> str:
        return f"Currently open {self.type} file: {self.filepath}" if self.filepath else f"Open {self.type} file"

    def is_open(self) -> bool:
        if self.filename or self.dirty:
            return True
        interaction.showwarning("You must open a file first!")
        return False

    def abort_open_new_file(self, new_filepath: str) -> bool:
        # only return True if we should abort
        if not self.ask_user:
            return False
        if self.filepath and self.dirty:
            msg = "Do you really want to load " + os.path.basename(
                new_filepath) + "? You will lose unsaved work on " + os.path.basename(self.filepath) + "!"
            return not interaction.showdialog(msg, title="Unsaved Changes", 
                                  buttons=(QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel))
        return False

    def open_file(self, filepath: str) -> bool:
        if not self.abort_open_new_file(filepath):
            self.set_file_path(filepath)
            self.cfg[self.cfg_last_dir_open] = self.dir
            self.cfg[self.cfg_last_file_open] = self.filepath
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
        if os.path.isfile(filepath):
            if os.path.splitext(filepath)[1].lower() in (f".{self.type_lower}",):
                return self.open_file(filepath)
            else:
                interaction.showwarning("Unsupported File Format")
        return False

    def accept_dir(self, dirpath: str) -> bool:
        # TODO: This is generally confusing for something named FileWidget
        #       although it is no longer hardcoded for OVL Tool
        if os.path.isdir(dirpath):
            return self.open_file(f"{dirpath}.{self.type_lower}")
        return os.path.isdir(dirpath)

    def dropEvent(self, event: QDropEvent) -> None:
        urls = self.get_files(event)
        if urls:
            filepath = str(urls[0].path())[1:]
            self.open_file(filepath)

    def ask_open(self) -> None:
        filepath = QFileDialog.getOpenFileName(
            self, f'Load {self.type}', self.cfg_path(self.cfg_last_dir_open), self.files_filter_str)[0]
        if filepath:
            self.open_file(filepath)

    def ask_open_dir(self) -> None:
        # TODO: This is generally confusing for something named FileWidget
        #       although it is no longer hardcoded for OVL Tool
        file_dir = QFileDialog.getExistingDirectory(directory=self.cfg_path(self.cfg_last_dir_open))
        if self.accept_dir(file_dir):
            self.dir_opened.emit(file_dir)

    def ask_save_as(self) -> None:
        """Saves file, always ask for file path"""
        if self.is_open():
            filepath = QFileDialog.getSaveFileName(
                self, f'Save {self.type}', self.cfg_path(self.cfg_last_dir_save), self.files_filter_str)[0]
            if filepath:
                self.cfg[self.cfg_last_dir_save], file_name = os.path.split(filepath)
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

    def __init__(self, parent: QWidget, cfg: dict, type: str = "DIR", ask_user: bool = True) -> None:
        super().__init__(parent=parent, cfg=cfg, type=type, ask_user=ask_user)

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


ButtonData = Iterable[tuple[QMenu, str, Callable[[], None], str, str]]

class MainWindow(FramelessMainWindow):
    modified = pyqtSignal(bool)

    def __init__(self, name: str, central_widget: Optional[QWidget] = None) -> None:
        FramelessMainWindow.__init__(self)

        self.wrapper_widget = QWidget(self)
        self.central_widget = QWidget(self) if central_widget is None else central_widget
        self.central_layout: QLayout = QVBoxLayout()

        self.title_sep = " | "
        self.title_sep_colored = " <font color=\"#5f5f5f\">|</font> "
        if FRAMELESS:
            self.setTitleBar(TitleBar(self))

        self.menu_bar = QMenuBar(self)
        self.actions: dict[str, QAction] = {}

        self.name = name
        self.setWindowTitle(name)
        self.setWindowIcon(get_icon("frontier"))

        self.file_widget: Optional[FileWidget] = None

        self.p_action = QProgressBar(self)
        self.p_action.setGeometry(0, 0, 200, 15)
        self.p_action.setTextVisible(True)
        self.p_action.setMaximum(100)
        self.p_action.setValue(0)
        self.dev_mode = os.path.isdir(os.path.join(root_dir, ".git"))
        dev_str = "DEV" if self.dev_mode else ""
        commit_str = get_commit_str()
        commit_str = commit_str.split("+")[0]
        self.statusBar = QStatusBar()

        self.version_info = QLabel(f"Version {commit_str}{dev_str}")
        self.version_info.setFont(QFont("Cascadia Code, Consolas, monospace"))
        self.version_info.setStyleSheet("color: #999")
        self.statusBar.addPermanentWidget(self.version_info)
        self.statusBar.addPermanentWidget(self.p_action)
        self.statusBar.setContentsMargins(5, 0, 0, 0)
        self.setStatusBar(self.statusBar)
        self.p_action.hide()

        self.status_timer = QTimer()
        self.status_timer.setSingleShot(True)
        self.status_timer.setInterval(3500)
        self.status_timer.timeout.connect(self.p_action.hide)
        self.status_timer.timeout.connect(self.version_info.show)

        self.cfg: dict[str, Any] = config.load_config()

        if FRAMELESS:
            # Frameless titlebar
            self.titleBar.raise_()

        self.setCentralWidget(self.central_widget)

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
        if FRAMELESS:
            layout.addWidget(frame)
        layout.addWidget(self.menu_bar)
        layout.addWidget(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.wrapper_widget.setLayout(layout)
        super().setCentralWidget(self.wrapper_widget)

    def make_file_widget(self, ask_user: bool = True, type: str = "OVL", editable: bool = False, 
                         check_exists: bool = False, root: Optional[str] = None) -> FileWidget:
        file_widget = FileWidget(self, self.cfg, ask_user=ask_user, type=type, editable=editable,
                                 check_exists=check_exists, root=root)

        self.modified.connect(file_widget.set_modified)

        file_widget.file_opened.connect(self.open)
        file_widget.dir_opened.connect(self.open_dir)
        file_widget.file_saved.connect(self.save)
        file_widget.filepath_changed.connect(self.set_window_filepath)

        return file_widget

    def setWindowTitle(self, title: str = "", file: str = "", modified: bool = False) -> None:
        if not title:
            title = self.name
        if file:
            super().setWindowTitle(f"{title}{self.title_sep}{self.get_file_name(file, only_basename=True)}")
            file_color = ""
            file_color_end = ""
            if modified and FRAMELESS:
                file_color = "<font color=\"#ffe075\">"
                file_color_end = "</font>"
            if FRAMELESS:
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
        if not only_basename and "ovldata/" in filepath:
            return self.elide_dirs(filepath.split("ovldata/")[1])
        return os.path.basename(filepath)
    
    def set_file_modified(self, dirty: bool) -> None:
        self.modified.emit(dirty)

    def report_bug(self) -> None:
        webbrowser.open("https://github.com/OpenNaja/cobra-tools/issues/new?assignees=&labels=&template=bug_report.md&title=", new=2)

    def online_support(self) -> None:
        webbrowser.open("https://github.com/OpenNaja/cobra-tools/wiki", new=2)

    def add_to_menu(self, button_data: ButtonData) -> None:
        for btn in button_data:
            self._add_to_menu(*btn)

    def _add_to_menu(self, submenu: QMenu, action_name: str, func: Callable[[], None], shortcut: str, icon_name: str, only_dev_mode=False) -> None:
        if only_dev_mode and not self.dev_mode:
            return
        action = QAction(action_name, self)
        if icon_name:
            icon = get_icon(icon_name)
            action.setIcon(icon)
        action.triggered.connect(func)
        if shortcut:
            action.setShortcut(shortcut)
        self.actions[action_name.lower()] = action
        submenu.addAction(action)

    @staticmethod
    def handle_error(msg: str) -> None:
        """Warn user with popup msg and write msg + exception traceback to log"""
        logging.exception(msg)
        interaction.showerror(msg)

    def show_progress(self) -> None:
        self.p_action.show()
        self.version_info.hide()

    def set_progress(self, value: int) -> None:
        if self.p_action.isHidden() and value > 0:
            self.show_progress()

        self.p_action.setValue(value)
        if self.p_action.value() >= self.p_action.maximum():
            self.status_timer.start()

    def update_progress(self, message: str, value: int = 100, vmax: int = 100) -> None:
        # avoid gui updates if the value won't actually change the percentage.
        # this saves us from making lots of GUI update calls that don't really
        # matter.
        percent = value
        if vmax > 100:
            percent = int((value / vmax) * 100)
            vmax = 100
        if percent > self.p_action.value():
            if self.p_action.maximum() != vmax:
                self.p_action.setMaximum(vmax)
            self.set_progress(percent)
            self.set_msg_temporarily(message)
            QApplication.instance().processEvents()

    def set_msg_temporarily(self, message: str) -> None:
        self.statusBar.showMessage(message, 3500)

    def run_threaded(self, func: Callable, *args, **kwargs) -> None:
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker(func, *args, **kwargs)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.error_msg.connect(interaction.showdialog)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.enable_gui_options(False)
        self.thread.finished.connect(self.enable_gui_options)
        self.thread.finished.connect(self.choices_update)

    def enable_gui_options(self, enable=True):
        pass

    def choices_update(self):
        pass

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.file_widget and self.file_widget.dirty:
            quit_msg = f"Quit? You will lose unsaved work on {os.path.basename(self.file_widget.filepath)}!"
            if not interaction.showconfirmation(quit_msg, title="Quit"):
                event.ignore()
                return
        event.accept()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if not self.file_widget:
            return

        path = event.mimeData().urls()[0].toLocalFile() if event.mimeData().hasUrls() else ""
        if path.lower().endswith(f".{self.file_widget.type_lower}"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if not self.file_widget:
            return

        path = event.mimeData().urls()[0].toLocalFile() if event.mimeData().hasUrls() else ""
        if path:
            self.file_widget.open_file(path)


class Worker(QObject):
    finished = pyqtSignal()
    error_msg = pyqtSignal(str)

    def __init__(self, func: Callable, *args, **kwargs) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        # mutex.lock()
        # func = getattr(self.thread().ovl_data, self.function_name)
        try:
            self.func(*self.args, **self.kwargs)
        except BaseException as err:
            logging.exception(f"Threaded call errored!")
            # self.error_msg.emit(f"ERROR - {err}")
            self.error_msg.emit(str(err))
        # mutex.unlock()
        self.finished.emit()


class Reporter(QObject):
    """A class wrapping the interaction between OvlFile and the UI"""
    warning_msg = pyqtSignal(tuple)  # type: ignore
    success_msg = pyqtSignal(str)  # type: ignore
    files_list = pyqtSignal(list)  # type: ignore
    included_ovls_list = pyqtSignal(list)  # type: ignore
    progress_percentage = pyqtSignal(int)  # type: ignore
    current_action = pyqtSignal(str)  # type: ignore

    def iter_progress(self, iterable, message):
        self.current_action.emit(message)
        self._percentage = 0
        v_max = len(iterable) - 1
        for i, item in enumerate(iterable):
            yield item
            if i and v_max:
                p = round(i / v_max * 100)
                if p != self._percentage:
                    self.progress_percentage.emit(p)
                    self._percentage = p
        msg = f"Finished {message}"
        self.current_action.emit(msg)
        # logging.success(msg)

    @contextlib.contextmanager
    def report_error_files(self, operation):
        error_files = []
        yield error_files
        if error_files:
            self.warning_msg.emit(
                (f"{operation} {len(error_files)} files failed - please check 'Show Details' or the log.",
                 "\n".join(error_files)))
        else:
            msg = f"{operation} succeeded"
            logging.success(msg)
            self.success_msg.emit(msg)
