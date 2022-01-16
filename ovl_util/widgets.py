import webbrowser
import os
from PyQt5 import QtGui, QtCore, QtWidgets

from ovl_util.interaction import showdialog
from ovl_util import config, qt_theme

MAX_UINT = 4294967295
myFont = QtGui.QFont()
myFont.setBold(True)


def startup(cls):
	appQt = QtWidgets.QApplication([])

	# style
	appQt.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
	appQt.setPalette(qt_theme.dark_palette)
	appQt.setStyleSheet("QToolTip { color: #ffffff; background-color: #353535; border: 1px solid white; }")

	win = cls()
	win.show()
	appQt.exec_()
	config.write_config("config.ini", win.cfg)


def abort_open_new_file(parent, newfile, oldfile):
	# only return True if we should abort
	if newfile == oldfile:
		return True
	if oldfile:
		qm = QtWidgets.QMessageBox
		return qm.No == qm.question(parent.parent, '', "Do you really want to load " + os.path.basename(
			newfile) + "? You will lose unsaved work on " + os.path.basename(oldfile) + "!", qm.Yes | qm.No)


def vbox(parent, grid):
	"""Adds a grid layout"""
	# vbox = QtWidgets.QVBoxLayout()
	# vbox.addLayout(grid)
	# vbox.addStretch(1.0)
	# vbox.setSpacing(0)
	# vbox.setContentsMargins(0,0,0,0)
	parent.setLayout(grid)


class CustomSortFilterProxyModel(QtCore.QSortFilterProxyModel):
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

	def __init__(self, parent=None):
		super(CustomSortFilterProxyModel, self).__init__(parent)
		self.filterString = ''
		self.filterFunctions = {}

	def lessThan(self, QModelIndex, QModelIndex_1):
		# for whatever reason, probably due to data loss in casting, we must override this function
		# to allow for correct comparison of djb hashes
		l = QModelIndex.data()
		r = QModelIndex_1.data()
		return l < r

	def setFilterFixedString(self, text):
		"""
		text : string
			The string to be used for pattern matching.
		"""
		self.filterString = text.lower()
		self.invalidateFilter()

	def addFilterFunction(self, name, new_func):
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

	def removeFilterFunction(self, name):
		"""
		name : hashable object

		Removes the filter function associated with name,
		if it exists.
		"""
		if name in self.filterFunctions.keys():
			del self.filterFunctions[name]
			self.invalidateFilter()

	def filterAcceptsRow(self, row_num, parent):
		"""
		Reimplemented from base class to allow the use
		of custom filtering.
		"""
		model = self.sourceModel()
		# The source mesh should have a method called row()
		# which returns the table row as a python list.
		tests = [func(model.row(row_num), self.filterString)
				 for func in self.filterFunctions.values()]
		return not False in tests


class TableModel(QtCore.QAbstractTableModel):
	member_renamed = QtCore.pyqtSignal(str, str)

	def __init__(self, data, header_names, ignore_types):
		super(TableModel, self).__init__()
		self._data = data
		self.header_labels = header_names
		self.ignore_types = ignore_types
		# self.member_renamed.connect(self.member_renamed_debug_print)

	@staticmethod
	def member_renamed_debug_print(a, b):
		print("renamed", a, b)

	def data(self, index, role):
		if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
			# See below for the nested-list data structure.
			# .row() indexes into the outer list,
			# .column() indexes into the sub-list
			return self._data[index.row()][index.column()]

		if role == QtCore.Qt.ForegroundRole:
			dtype = self._data[index.row()][1]
			if dtype in self.ignore_types:
				return QtGui.QColor('grey')

		if role == QtCore.Qt.DecorationRole:
			if index.column() == 0:
				dtype = self._data[index.row()][1]
				# remove the leading .
				return get_icon(dtype[1:])

		if role == QtCore.Qt.TextAlignmentRole:
			# right align hashes
			if index.column() == 2:
				return QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight

	def setData(self, index, value, role=QtCore.Qt.EditRole):
		if index.isValid():
			if role == QtCore.Qt.EditRole:
				row = index.row()
				column = index.column()
				old_value = self._data[row][column]
				# value has changed, gotta update it
				if old_value != value:
					self._data[row][column] = value
					self.member_renamed.emit(old_value, value)
				return True
		return False

	def row(self, row_index):
		return self._data[row_index]

	def rowCount(self, index):
		# The length of the outer list.
		return len(self._data)

	def columnCount(self, index):
		# The following takes the first sub-list, and returns
		# the length (only works if all rows are an equal length)
		return len(self._data[0])

	def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
		if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
			return self.header_labels[section]
		return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

	def flags(self, index):
		dtype = self._data[index.row()][1]
		if dtype in self.ignore_types:
			return QtCore.Qt.ItemIsDropEnabled
		else:
			# names
			if index.column() == 0:
				return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | \
					   QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEditable
			# other stuff, can't be edited
			else:
				return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | \
					   QtCore.Qt.ItemIsDropEnabled


class SortableTable(QtWidgets.QWidget):
	def __init__(self, header_names, ignore_types):
		super().__init__()
		self.table = TableView(header_names, ignore_types)
		self.filter_entry = LabelEdit("Filter:")
		self.filter_entry.entry.textChanged.connect(self.table.set_filter)
		self.hide_unused = QtWidgets.QCheckBox("Hide unextractable files")
		self.hide_unused.stateChanged.connect(self.toggle_hide)
		self.rev_search = QtWidgets.QCheckBox("Exclude Search")
		self.rev_search.stateChanged.connect(self.toggle_rev)
		self.clear_filters = QtWidgets.QPushButton("Clear")
		self.clear_filters.pressed.connect(self.clear_filter)
		qgrid = QtWidgets.QGridLayout()
		qgrid.addWidget(self.filter_entry, 0, 0, )
		qgrid.addWidget(self.hide_unused, 0, 1, )
		qgrid.addWidget(self.rev_search, 0, 2, )
		qgrid.addWidget(self.clear_filters, 0, 3, )
		qgrid.addWidget(self.table, 1, 0, 1, 4)
		qgrid.setContentsMargins(0, 0, 0, 0)
		self.setLayout(qgrid)

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


class TableView(QtWidgets.QTableView):
	files_dragged = QtCore.pyqtSignal(list)
	files_dropped = QtCore.pyqtSignal(list)
	file_selected = QtCore.pyqtSignal(int)

	def __init__(self, header_names, ignore_types):
		super().__init__()
		# list of lists
		# row first
		self.data = [[], ]
		self.ignore_types = ignore_types
		self.model = TableModel(self.data, header_names, ignore_types)
		# self.proxyModel = QSortFilterProxyModel()
		self.proxyModel = CustomSortFilterProxyModel()
		self.proxyModel.setSourceModel(self.model)
		self.proxyModel.setSortRole(QtCore.Qt.UserRole)
		self.setModel(self.proxyModel)

		self.resizeColumnsToContents()
		self.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.setDropIndicatorShown(True)
		self.verticalHeader().hide()
		self.setSelectionBehavior(self.SelectRows)

		self.setSortingEnabled(True)
		# sort by index; -1 means don't sort
		self.sortByColumn(-1, QtCore.Qt.AscendingOrder)
		self.proxyModel.setFilterFixedString("")
		self.proxyModel.setFilterKeyColumn(0)
		self.rev_check = False
		self.selectionModel().selectionChanged.connect(self.on_selectionChanged)

	def on_selectionChanged(self, selected, deselected):
		self.selected = list(self.get_selected_line_indices())
		if self.selected:
			self.file_selected.emit(self.selected[-1])

	def update_filter_function(self):
		if self.rev_check:
			self.proxyModel.addFilterFunction('name', lambda r, s: s not in r[0])
		else:
			self.proxyModel.addFilterFunction('name', lambda r, s: s in r[0])

	def set_filter(self, fixed_string):
		self.proxyModel.setFilterFixedString(fixed_string)
		self.update_filter_function()

	def set_ext_filter(self, hide):
		ext_filter_name = "ext_filter"
		if hide:
			def ext_filter(r, s):
				return r[1] not in self.ignore_types

			self.proxyModel.addFilterFunction(ext_filter_name, ext_filter)
		else:
			self.proxyModel.removeFilterFunction(ext_filter_name)

	def clear_filter(self, ):
		# self.proxyModel.setFilterFixedString("")
		self.proxyModel.setFilterFixedString("")
		self.sortByColumn(-1, QtCore.Qt.AscendingOrder)

	def get_selected_line_indices(self):
		return set(self.proxyModel.mapToSource(x).row() for x in self.selectedIndexes())

	def get_selected_files(self):
		# map the selected indices to the actual underlying data, which is in its original order
		return [self.model._data[x][0] for x in self.get_selected_line_indices()]

	def get_files(self):
		# returns the list of all file names
		return [x[0] for x in self.model._data]


	def startDrag(self, actions):
		"""Emits a signal with the file names of all files that are being dragged"""
		self.files_dragged.emit(self.get_selected_files())

	def set_data(self, data):
		if not data:
			data = [[], ]
		self.model.beginResetModel()
		self.model._data = data
		self.model.endResetModel()
		self.resizeColumnsToContents()

	def dragMoveEvent(self, e):
		e.accept()

	def dragEnterEvent(self, e):
		e.accept()

	@staticmethod
	def get_files_from_event(event):
		data = event.mimeData()
		urls = data.urls()
		if urls and urls[0].scheme() == 'file':
			return [str(url.path())[1:] for url in urls]

	def dropEvent(self, e):
		e.setDropAction(QtCore.Qt.CopyAction)
		self.files_dropped.emit(self.get_files_from_event(e))
		e.accept()


class LabelEdit(QtWidgets.QWidget):
	def __init__(self, name, ):
		QtWidgets.QWidget.__init__(self, )
		self.label = QtWidgets.QLabel(name)
		self.entry = QtWidgets.QLineEdit()
		vbox = QtWidgets.QHBoxLayout()
		vbox.addWidget(self.label)
		vbox.addWidget(self.entry)
		vbox.setContentsMargins(0, 0, 0, 0)
		# vbox.addStretch(1)
		self.setLayout(vbox)


class CleverCombo(QtWidgets.QComboBox):
	""""A combo box that supports setting content (existing or new), and a callback"""

	def __init__(self, options=[], link_inst=None, link_attr=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.addItems(options)
		self.link_inst = link_inst
		self.link_attr = link_attr
		if link_inst and link_attr:
			name = str(getattr(link_inst, link_attr))
			self.setText(name)
			self.currentIndexChanged.connect(self.update_name)

	def setText(self, txt):
		flag = QtCore.Qt.MatchFixedString
		indx = self.findText(txt, flags=flag)
		# add new item if not found
		if indx == -1:
			self.addItem(txt)
			indx = self.findText(txt, flags=flag)
		self.setCurrentIndex(indx)

	def update_name(self, ind):
		"""Change data on pyffi struct if gui changes"""
		setattr(self.link_inst, self.link_attr, self.currentText())


class EditCombo(QtWidgets.QWidget):
	entries_changed = QtCore.pyqtSignal(list)

	def __init__(self, parent):
		super().__init__(parent)
		self.main_window = parent
		self.add_button = QtWidgets.QPushButton("+")
		self.add_button.clicked.connect(self.add)
		self.delete_button = QtWidgets.QPushButton("-")
		self.delete_button.clicked.connect(self.delete)
		self.add_button.setMaximumWidth(20)
		self.delete_button.setMaximumWidth(20)
		self.entry = QtWidgets.QComboBox()
		self.entry.setEditable(True)
		vbox = QtWidgets.QHBoxLayout(self)
		vbox.addWidget(self.entry)
		vbox.addWidget(self.add_button)
		vbox.addWidget(self.delete_button)
		vbox.setContentsMargins(0, 0, 0, 0)

	@property
	def items(self):
		return [self.entry.itemText(i) for i in range(self.entry.count())]

	def add(self):
		name = self.entry.currentText()
		if name:
			self.entry.addItem(name)
			self.entries_changed.emit(self.items)

	def delete(self):
		name = self.entry.currentText()
		if name:
			ind = self.entry.findText(name)
			self.entry.removeItem(ind)
			self.entries_changed.emit(self.items)

	def set_data(self, items):
		items = set(items)
		self.entry.clear()
		self.entry.addItems(items)


class LabelCombo(QtWidgets.QWidget):
	def __init__(self, name, options, link_inst=None, link_attr=None):
		QtWidgets.QWidget.__init__(self, )
		# sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		# sizePolicy.setHorizontalStretch(0)
		# sizePolicy.setVerticalStretch(0)
		# sizePolicy.setHeightForWidth(self.entry.sizePolicy().hasHeightForWidth())
		# self.entry.setSizePolicy(sizePolicy)
		# self.entry.setMaxVisibleItems(10)
		self.label = QtWidgets.QLabel(name)
		self.entry = CleverCombo(options=options, link_inst=link_inst, link_attr=link_attr)
		self.entry.setEditable(True)
		vbox = QtWidgets.QHBoxLayout(self)
		vbox.addWidget(self.label)
		vbox.addWidget(self.entry)
		vbox.setContentsMargins(0, 0, 0, 0)


class MySwitch(QtWidgets.QPushButton):
	PRIMARY = QtGui.QColor(53, 53, 53)
	SECONDARY = QtGui.QColor(35, 35, 35)
	OUTLINE = QtGui.QColor(122, 122, 122)
	TERTIARY = QtGui.QColor(42, 130, 218)
	BLACK = QtGui.QColor(0, 0, 0)
	WHITE = QtGui.QColor(255, 255, 255)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setCheckable(True)
		self.setMinimumWidth(66)
		self.setMinimumHeight(22)

	def setValue(self, v):
		self.setChecked(v)

	def paintEvent(self, event):
		label = "ON" if self.isChecked() else "OFF"
		bg_color = self.TERTIARY if self.isChecked() else self.PRIMARY

		radius = 10
		width = 32
		center = self.rect().center()

		painter = QtGui.QPainter(self)
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		painter.translate(center)
		painter.setBrush(self.SECONDARY)

		pen = QtGui.QPen(self.WHITE)
		pen.setWidth(0)
		painter.setPen(pen)

		painter.drawRoundedRect(QtCore.QRect(-width, -radius, 2 * width, 2 * radius), radius, radius)
		painter.setBrush(QtGui.QBrush(bg_color))
		sw_rect = QtCore.QRect(-radius, -radius, width + radius, 2 * radius)
		if not self.isChecked():
			sw_rect.moveLeft(-width)
		painter.drawRoundedRect(sw_rect, radius, radius)
		painter.drawText(sw_rect, QtCore.Qt.AlignCenter, label)


class CollapsibleBox(QtWidgets.QWidget):
	def __init__(self, title="", parent=None):
		super().__init__(parent)

		self.toggle_button = QtWidgets.QToolButton(
			text=title, checkable=True, checked=False
		)
		self.toggle_button.setStyleSheet("QToolButton { border: none; }")
		self.toggle_button.setToolButtonStyle(
			QtCore.Qt.ToolButtonTextBesideIcon
		)
		self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
		self.toggle_button.pressed.connect(self.on_pressed)

		self.toggle_animation = QtCore.QParallelAnimationGroup(self)

		self.content_area = QtWidgets.QScrollArea(
			maximumHeight=0, minimumHeight=0
		)
		self.content_area.setSizePolicy(
			QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
		)
		self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

		lay = QtWidgets.QVBoxLayout(self)
		lay.setSpacing(0)
		lay.setContentsMargins(0, 0, 0, 0)
		lay.addWidget(self.toggle_button)
		lay.addWidget(self.content_area)

		self.toggle_animation.addAnimation(
			QtCore.QPropertyAnimation(self, b"minimumHeight")
		)
		self.toggle_animation.addAnimation(
			QtCore.QPropertyAnimation(self, b"maximumHeight")
		)
		self.toggle_animation.addAnimation(
			QtCore.QPropertyAnimation(self.content_area, b"maximumHeight")
		)

	@QtCore.pyqtSlot()
	def on_pressed(self):
		checked = self.toggle_button.isChecked()
		self.toggle_button.setArrowType(
			QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow
		)
		self.toggle_animation.setDirection(
			QtCore.QAbstractAnimation.Forward
			if not checked
			else QtCore.QAbstractAnimation.Backward
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
		self.label = QtWidgets.QLabel(str(attrib.name))

		self.data = QtWidgets.QWidget()
		layout = QtWidgets.QHBoxLayout()
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)
		buttons = [self.create_field(i) for i, v in enumerate(attrib.flags) if v]
		for button in buttons:
			layout.addWidget(button)
		self.data.setLayout(layout)
		# get tooltip
		tooltip = tooltips.get(self.attrib.name, "Undocumented attribute.")
		self.data.setToolTip(tooltip)
		self.label.setToolTip(tooltip)

	def create_field(self, ind):
		default = self.attrib.value[ind]

		def update_ind(v):
			# use a closure to remember index
			# print(self.attrib, ind, v)
			self.attrib.value[ind] = v

		# always float
		field = QtWidgets.QDoubleSpinBox()
		field.setDecimals(3)
		field.setRange(-10000, 10000)
		field.setSingleStep(.05)
		field.valueChanged.connect(update_ind)

		field.setValue(default)
		field.setMinimumWidth(50)
		field.setAlignment(QtCore.Qt.AlignCenter)
		field.setContentsMargins(0, 0, 0, 0)
		return field


class QColorButton(QtWidgets.QPushButton):
	'''
	Custom Qt Widget to show a chosen color.

	Left-clicking the button shows the color-chooser, while
	right-clicking resets the color to None (no-color).
	'''

	colorChanged = QtCore.pyqtSignal(object)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self._color = None
		self.setMaximumWidth(32)
		self.pressed.connect(self.onColorPicker)

	def setColor(self, color):
		if color != self._color:
			self._color = color
			self.colorChanged.emit(color)

		if self._color:
			self.setStyleSheet("background-color: %s;" % self._color.name(QtGui.QColor.NameFormat.HexArgb))
		else:
			self.setStyleSheet("")

	def color(self):
		return self._color

	def onColorPicker(self):
		'''
		Show color-picker dialog to select color.

		Qt will use the native dialog by default.

		'''
		dlg = QtWidgets.QColorDialog(self)
		dlg.setOption(QtWidgets.QColorDialog.ShowAlphaChannel)
		if self._color:
			dlg.setCurrentColor(self._color)
		if dlg.exec_():
			self.setColor(dlg.currentColor())

	def mousePressEvent(self, e):
		if e.button() == QtCore.Qt.RightButton:
			self.setColor(None)

		return super().mousePressEvent(e)

	def setValue(self, c):
		self.setColor(QtGui.QColor(c.r, c.g, c.b, c.a))

	def getValue(self, ):
		if self._color:
			print(self._color.getRgb())


class VectorEntry:
	def __init__(self, attrib, tooltips={}):
		"""attrib must be pyffi attrib object"""
		# QtWidgets.QWidget.__init__(self,)
		self.attrib = attrib
		self.entry = QtWidgets.QLineEdit(attrib.name)
		self.entry.textEdited.connect(self.update_name)
		self.delete = QtWidgets.QPushButton("x")
		self.delete.setMaximumWidth(15)
		self.data = QtWidgets.QWidget()
		layout = QtWidgets.QHBoxLayout()
		buttons = [self.create_field(i) for i in range(len(attrib.value))]
		for button in buttons:
			layout.addWidget(button)
		self.data.setLayout(layout)

		# get tooltip
		tooltip = tooltips.get(self.attrib.name, "Undocumented attribute.")
		self.data.setToolTip(tooltip)
		self.entry.setToolTip(tooltip)

	def update_name(self, name):
		self.attrib.name = name

	def create_field(self, ind):
		default = self.attrib.value[ind]

		def update_ind(v):
			# use a closure to remember index
			# print(self.attrib, ind, v)
			self.attrib.value[ind] = v

		def update_ind_int(v):
			# use a closure to remember index
			# print(self.attrib, ind, v)
			self.attrib.value[ind] = int(v)

		def update_ind_color(c):
			# use a closure to remember index
			# print(self.attrib, ind, v)
			color = self.attrib.value[ind]
			c_new = c.getRgb()
			color.r = c_new[0]
			color.g = c_new[1]
			color.b = c_new[2]
			color.a = c_new[3]

		t = str(type(default))
		# print(t)
		if "float" in t:
			field = QtWidgets.QDoubleSpinBox()
			field.setDecimals(3)
			field.setRange(-10000, 10000)
			field.setSingleStep(.05)
			field.valueChanged.connect(update_ind)
		elif "bool" in t:
			# field = QtWidgets.QSpinBox()
			field = MySwitch()
			field.clicked.connect(update_ind)
		elif "int" in t:
			default = int(default)
			# field = QtWidgets.QSpinBox()
			field = QtWidgets.QDoubleSpinBox()
			field.setDecimals(0)
			field.setRange(-MAX_UINT, MAX_UINT)
			field.valueChanged.connect(update_ind_int)
		elif "Color" in t:
			field = QColorButton()
			field.colorChanged.connect(update_ind_color)
		field.setValue(default)
		field.setMinimumWidth(50)
		return field


class FileWidget(QtWidgets.QWidget):
	"""An entry widget that starts a file selector when clicked and also accepts drag & drop.
	Displays the current file's basename.
	"""

	def __init__(self, parent, cfg, ask_user=True, dtype="OVL", poll=True):
		super().__init__(parent)
		self.entry = QtWidgets.QLineEdit()
		self.icon = QtWidgets.QPushButton()
		self.icon.setIcon(get_icon("dir"))
		self.icon.setFlat(True)
		self.icon.mousePressEvent = self.ignoreEvent
		self.entry.mousePressEvent = self.ignoreEvent
		self.icon.dropEvent = self.dropEvent
		self.entry.dropEvent = self.dropEvent
		self.icon.dragMoveEvent = self.dragMoveEvent
		self.entry.dragMoveEvent = self.dragMoveEvent
		self.icon.dragEnterEvent = self.dragEnterEvent
		self.entry.dragEnterEvent = self.dragEnterEvent
		self.dtype = dtype
		self.dtype_l = dtype.lower()

		self.poll = poll
		self.parent = parent
		self.cfg = cfg
		if not self.cfg:
			self.cfg[f"dir_{self.dtype_l}s_in"] = "C://"
		self.entry.setDragEnabled(True)
		self.entry.setReadOnly(True)
		self.filepath = ""
		self.filename = ""
		self.ask_user = ask_user
		# this checks if the data has been modified by the user, is set from the outside
		self.dirty = False

		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.setContentsMargins(0, 0, 0, 0)
		self.qgrid.addWidget(self.icon, 0, 0)
		self.qgrid.addWidget(self.entry, 0, 1)

		self.setLayout(self.qgrid)

	def abort_open_new_file(self, new_filepath):
		# only return True if we should abort
		if not self.ask_user:
			return False
		if new_filepath == self.filepath:
			return True
		if self.filepath and self.dirty:
			qm = QtWidgets.QMessageBox
			return qm.No == qm.question(self, '', "Do you really want to load " + os.path.basename(
				new_filepath) + "? You will lose unsaved work on " + os.path.basename(self.filepath) + "!",
										qm.Yes | qm.No)

	def set_file_path(self, filepath):
		if not self.abort_open_new_file(filepath):
			self.filepath = filepath
			self.cfg[f"dir_{self.dtype_l}s_in"], self.filename = os.path.split(self.filepath)
			self.setText(self.filename)
			return True

	def accept_file(self, filepath):
		if os.path.isfile(filepath):
			if os.path.splitext(filepath)[1].lower() in (f".{self.dtype_l}",):
				return self.set_file_path(filepath)
			else:
				showdialog("Unsupported File Format")

	def accept_dir(self, dirpath):
		if os.path.isdir(dirpath):
			return self.set_file_path(f"{dirpath}.ovl")

	def setText(self, text):
		self.entry.setText(text)

	def get_files(self, event):
		data = event.mimeData()
		urls = data.urls()
		if urls and urls[0].scheme() == 'file':
			return urls

	def dragEnterEvent(self, event):
		if self.get_files(event):
			event.acceptProposedAction()
			self.setFocus(True)

	def dragMoveEvent(self, event):
		if self.get_files(event):
			event.acceptProposedAction()
			self.setFocus(True)

	def dropEvent(self, event):
		urls = self.get_files(event)
		if urls:
			filepath = str(urls[0].path())[1:]
			self.decide_open(filepath)

	def ask_open(self):
		filepath = QtWidgets.QFileDialog.getOpenFileName(self, f'Load {self.dtype}',
														 self.cfg.get(f"dir_{self.dtype_l}s_in", "C://"),
														 f"{self.dtype} files (*.{self.dtype_l})")[0]
		self.decide_open(filepath)

	def decide_open(self, filepath):
		if self.accept_file(filepath) and self.poll:
			self.parent.poll()

	def ask_open_dir(self):
		file_dir = QtWidgets.QFileDialog.getExistingDirectory()
		if self.accept_dir(file_dir):
			self.parent.create_ovl(file_dir)

	def ignoreEvent(self, event):
		event.ignore()

	def mousePressEvent(self, event):
		self.ask_open()

# Creates a dir widget, same as file but for directories
class DirWidget(QtWidgets.QWidget):
    """An entry widget that starts a file selector when clicked and also accepts drag & drop.
    Displays the current file's basename.
    """

    def __init__(self, parent, cfg, ask_user=True, dtype="OVL", poll=True):
        super(DirWidget, self).__init__(parent)
        self.entry = QtWidgets.QLineEdit()
        self.icon = QtWidgets.QPushButton()
        self.icon.setIcon(self.get_icon("dir"))
        self.icon.setFlat(True)
        self.icon.mousePressEvent = self.ignoreEvent
        self.entry.mousePressEvent = self.ignoreEvent
        self.icon.dropEvent = self.dropEvent
        self.entry.dropEvent = self.dropEvent
        self.icon.dragMoveEvent = self.dragMoveEvent
        self.entry.dragMoveEvent = self.dragMoveEvent
        self.icon.dragEnterEvent = self.dragEnterEvent
        self.entry.dragEnterEvent = self.dragEnterEvent
        self.dtype = dtype
        self.dtype_l = dtype.lower()

        self.poll = poll
        self.parent = parent
        self.cfg = cfg
        if not self.cfg:
            self.cfg[f"dir_{self.dtype_l}s_in"] = "C://"
        self.entry.setDragEnabled(True)
        self.entry.setReadOnly(True)
        self.filepath = ""
        self.filename = ""
        self.ask_user = ask_user
        # this checks if the data has been modified by the user, is set from the outside
        self.dirty = False

        self.qgrid = QtWidgets.QGridLayout()
        self.qgrid.setContentsMargins(0, 0, 0, 0)
        self.qgrid.addWidget(self.icon, 0, 0)
        self.qgrid.addWidget(self.entry, 0, 1)

        self.setLayout(self.qgrid)

    def get_icon(self,name):
        base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        return QtGui.QIcon(os.path.join(base_dir, f'icons/{name}.png'))

    def accept_dir(self, dirpath):
        if os.path.isdir(dirpath):
            self.filepath = dirpath
            self.cfg[f"dir_{self.dtype_l}s_in"], self.filename = os.path.split(dirpath)
            self.setText(dirpath)
            self.parent.settings_changed()
            return True

    def setText(self, text):
        self.entry.setText(text)

    def get_files(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            return urls

    def dragEnterEvent(self, event):
        if self.get_files(event):
            event.acceptProposedAction()
            self.setFocus(True)

    def dragMoveEvent(self, event):
        if self.get_files(event):
            event.acceptProposedAction()
            self.setFocus(True)

    def dropEvent(self, event):
        urls = self.get_files(event)
        if urls:
            filepath = str(urls[0].path())[1:]
            self.decide_open(filepath)

    def decide_open(self, filepath):
        if self.accept_dir(filepath) and self.poll:
            #self.parent.poll()
            pass

    def ask_open_dir(self):
        filepath = QtWidgets.QFileDialog.getExistingDirectory()
        if self.accept_dir(filepath):
           pass

    def ignoreEvent(self, event):
        event.ignore()

    def mousePressEvent(self, event):
        self.ask_open_dir()


def get_icon(name):
	base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	return QtGui.QIcon(os.path.join(base_dir, f'icons/{name}.png'))


class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, name, ):
		QtWidgets.QMainWindow.__init__(self)

		self.central_widget = QtWidgets.QWidget(self)
		self.setCentralWidget(self.central_widget)

		self.name = name
		# self.resize(720, 400)
		self.setWindowTitle(name)
		self.setWindowIcon(get_icon("frontier"))

		self.cfg = config.read_config("config.ini")

	def poll(self):
		if self.file_widget.filepath:
			self.load()

	def report_bug(self):
		webbrowser.open("https://github.com/OpenNaja/cobra-tools/issues/new", new=2)

	def online_support(self):
		webbrowser.open("https://github.com/OpenNaja/cobra-tools/wiki", new=2)

	def update_file(self, filepath):
		self.cfg["dir_in"], file_name = os.path.split(filepath)
		self.setWindowTitle(f"{self.name} {file_name}")

	def add_to_menu(self, button_data):
		for submenu, name, func, shortcut, icon_name in button_data:
			button = QtWidgets.QAction(name, self)
			if icon_name:
				icon = get_icon(icon_name)
				# if not icon:
				# 	icon = self.style().standardIcon(getattr(QtWidgets.QStyle, icon))
				button.setIcon(icon)
			button.triggered.connect(func)
			if shortcut:
				button.setShortcut(shortcut)
			submenu.addAction(button)
