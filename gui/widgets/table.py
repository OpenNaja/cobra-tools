import fnmatch
from typing import Any, AnyStr, Union, Optional, Iterable, Callable, cast, NamedTuple, Literal

from gui.app_utils import *
from gui.widgets.input import IconButton, IconEdit, SelectedItemsButton
from gui.widgets.layout import FlowHLayout, FlowWidget

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject,
						  QAbstractTableModel, QSortFilterProxyModel, QModelIndex, QItemSelection)
from PyQt5.QtGui import (QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent)
from PyQt5.QtWidgets import (QWidget, QApplication, QAbstractItemView,
							 QTableView, QCheckBox, QFrame, QGridLayout, QHBoxLayout)



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
	"""A Qt model for displaying tabular data, derived from QAbstractTableModel.

	This model manages a list of lists, where each inner list represents a row.
	It is responsible for providing data, header labels, and visual roles
	(like icons and alignment) to a QTableView. It also handles data editing
	and emits signals (`member_renamed`, `value_edited`) when specific
	columns are modified.
	"""
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

	def append_rows(self, new_rows) -> None:
		self.beginInsertRows(QModelIndex(),
			len(self._data),
			len(self._data) + len(new_rows)-1
		)
		self._data.extend(new_rows)
		self.endInsertRows()

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


class TableView(QTableView):
	"""A customized QTableView for displaying, sorting, and filtering data.

	This view integrates a TableModel and a CustomSortFilterProxyModel to
	provide features like column sorting and dynamic filtering based on user
	input (including regex and wildcard matching). It is configured for
	row-based selection, drag-and-drop, and context menu actions. It emits
	various signals to communicate user interactions, such as row selection,
	double-clicks, and file drops.
	"""
	files_dragged = pyqtSignal(list)
	files_dropped = pyqtSignal(list)
	file_selected = pyqtSignal(int)
	file_selected_count = pyqtSignal(int)
	file_double_clicked = pyqtSignal(list)
	regex_error = pyqtSignal(bool)

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
		self.regex_enabled = False
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

	def set_regex_enabled(self, enabled: bool) -> None:
		"""Sets the filter mode to regex or wildcard and reapplies the filter."""
		self.regex_enabled = enabled
		self.update_filter_function()

	def update_filter_function(self) -> None:
		search_string = self.proxy_model.filterString
		# Reset UI error state
		self.regex_error.emit(False)
		if self.regex_enabled:
			if not search_string:
				# Empty regex
				filter_func = (lambda r, s: False) if self.inverted else (lambda r, s: True)
				self.proxy_model.addFilterFunction('name', filter_func)
				return
			try:
				# Valid regex
				compiled_regex = re.compile(search_string, re.IGNORECASE)
				if self.inverted:
					self.proxy_model.addFilterFunction('name', lambda r, s: not compiled_regex.search(r[0]))
				else:
					self.proxy_model.addFilterFunction('name', lambda r, s: bool(compiled_regex.search(r[0])))
			except re.error:
				# Invalid regex, apply a filter that hides all rows
				self.regex_error.emit(True)  # Show error in UI
				self.proxy_model.addFilterFunction('name', lambda r, s: False)
		else:
			# Wildcard search by default
			if self.inverted:
				self.proxy_model.addFilterFunction('name', lambda r, s: not fnmatch.fnmatch(r[0].lower(), f'*{s}*'))
			else:
				self.proxy_model.addFilterFunction('name', lambda r, s: fnmatch.fnmatch(r[0].lower(), f'*{s}*'))

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

	def append_rows(self, new_rows) -> None:
		self.table_model.append_rows(new_rows)
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


class SortableTable(QWidget):
	"""A complete table widget that combines a TableView with user-facing
	filter controls.

	This composite widget provides a full user interface for interacting with a
	sortable and filterable table. It includes a text input for filtering by
	name, a checkbox to toggle the visibility of hidden items, and buttons to
	clear the filter, invert the search, and enable regular expression
	matching. It also provides a dedicated area for action buttons that can
	operate on the table's selected items.
	"""
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

		self.filter_regex = IconButton("regex")
		self.filter_regex.setCheckable(True)
		self.filter_regex.setToolTip("Enable regular expression matching for the filter")
		self.filter_regex.toggled.connect(self.toggle_regex)
		self.table.regex_error.connect(self.set_filter_error_state)

		self.filter_clear = IconButton("clear_filter")
		self.filter_clear.setToolTip("Clear Filter")
		self.filter_clear.pressed.connect(self.clear_filter)

		# Button Row Setup
		self.button_count = 0
		self.btn_layout = QHBoxLayout()
		self.btn_layout.setContentsMargins(0, 0, 0, 0)
		self.btn_frame = QFrame(self)
		self.btn_frame.setLayout(self.btn_layout)

		filter_bar = FlowWidget(self)
		filter_bar_lay = FlowHLayout(filter_bar)
		filter_bar_lay.addWidget(self.filter_entry, hide_index=-1)
		filter_bar_lay.addWidget(self.filter_clear, hide_index=4)
		filter_bar_lay.addWidget(self.filter_regex, hide_index=3)
		filter_bar_lay.addWidget(self.filter_invert, hide_index=2)
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
		self.filter_regex.setChecked(False)
		self.set_filter_error_state(False)
		self.table.clear_filter()

	def set_filter_error_state(self, is_error: bool) -> None:
		"""Changes the filter entry's border color to indicate a regex error."""
		if is_error:
			self.filter_entry.entry.setStyleSheet("border: 1px solid red; border-radius: 2px;")
		else:
			self.filter_entry.entry.setStyleSheet("")

	def toggle_show_hidden(self, state: Qt.CheckState) -> None:
		self.table.set_show_hidden_filter(state != Qt.CheckState.Checked)

	def toggle_invert(self, checked: bool) -> None:
		self.table.inverted = checked
		self.table.update_filter_function()

	def toggle_regex(self, checked: bool) -> None:
		self.table.set_regex_enabled(checked)

	def add_button(self, btn) -> None:
		if not self.button_count:
			self.grid.addWidget(self.btn_frame, 1, 0, 1, 4)
		self.btn_layout.addWidget(btn)
		self.button_count += 1
		if isinstance(btn, SelectedItemsButton):
			btn.setDisabled(True)
			self.table.selectionModel().selectionChanged.connect(btn.setEnabledFromSelection)
