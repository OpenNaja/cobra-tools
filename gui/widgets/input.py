

from typing import TYPE_CHECKING, Any, AnyStr, List, Union, Optional, Iterable, Callable, cast, NamedTuple, Literal

from gui.app_utils import *
from gui.widgets.file_input import FileWidget
from gui.widgets.utils import get_main_window
from gui.widgets.event_filters import MouseWheelGuard

if TYPE_CHECKING:
	from gui.widgets.file_input import FileWidget
	from generated.formats.ovl_base.compounds import ByteColor
	from generated.formats.matcol.compounds import FloatAttrib

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject, QDir, QMimeData, QUrl,
						  QRect, QSize, QEvent, QTimer, QTimerEvent, QModelIndex, QItemSelection)
from PyQt5.QtGui import (QBrush, QColor, QFontMetrics, QIcon, QPainter, QPen, QStandardItemModel, QStandardItem,
						 QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent,
						 QMouseEvent, QPaintEvent, QResizeEvent)
from PyQt5.QtWidgets import (QWidget, QColorDialog, QFileDialog, QComboBox, QDoubleSpinBox, QLabel, QLineEdit,
							 QPushButton, QHBoxLayout, QSizePolicy, QStyleOptionViewItem, QStyledItemDelegate)


# -------------------------------------------------------------------------- #
#                               QPushButton                                  #
# region ------------------------------------------------------------------- #

class SelectedItemsButton(QPushButton):
	"""A QPushButton that is enabled only when items in a view are selected.

	Connect a view's selectionChanged signal to this widget's
	`setEnabledFromSelection` slot.
	"""
	def __init__(self, parent: Optional[QWidget] = None, text: str = "", icon: Optional[QIcon] = None) -> None:
		if icon:
			super().__init__(icon, text, parent)
		else:
			super().__init__(text, parent)
		self.setStyleSheet("SelectedItemsButton:disabled { background-color: #252525; } ")

	def setEnabledFromSelection(self, selection: QItemSelection) -> None:
		self.setEnabled(selection.count() > 0)


class IconButton(QPushButton):
	"""A compact, stylized QPushButton designed to display only an icon.

	It features a flat appearance with custom hover, pressed, and checked
	visual states to provide clear user feedback.
	"""
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


class OnOffSwitch(QPushButton):
	"""A custom QPushButton that visually represents an 'ON'/'OFF' toggle switch.

	This widget is checkable and uses a custom `paintEvent` to draw its state,
	providing a clear visual indicator for boolean settings.
	"""
	PRIMARY = QColor(53, 53, 53)
	SECONDARY = QColor(35, 35, 35)
	OUTLINE = QColor(122, 122, 122)
	TERTIARY = QColor(42, 130, 218)
	BLACK = QColor(0, 0, 0)
	WHITE = QColor(255, 255, 255)

	def __init__(self, parent: Optional[QWidget] = None) -> None:
		super().__init__(parent)
		self.setCheckable(True)
		self.setMinimumWidth(66)
		self.setMinimumHeight(22)

	def setValue(self, v: bool) -> None:
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


class QColorButton(QPushButton):
	"""A specialized QPushButton that displays a color swatch.

	A left-click opens a `QColorDialog` to select a new color, while a
	right-click clears the selection. Emits a `colorChanged` signal whenever
	the color is modified.
	"""

	colorChanged = pyqtSignal(object)

	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

		self._color: QColor = QColor()
		self.setMaximumWidth(32)
		self.pressed.connect(self.onColorPicker)
		QDir.addSearchPath("icon", self.get_icon_dir())

	def get_icon_dir(self) -> str:
		return os.path.join(ROOT_DIR, "icons")

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

	def setValue(self, c: 'ByteColor') -> None:
		self.setColor(QColor(c.r, c.g, c.b, c.a))

	def getValue(self, ) -> None:
		if self._color:
			print(self._color.getRgb())

# endregion


# -------------------------------------------------------------------------- #
#                           QLineEdit Composites                             #
# region ------------------------------------------------------------------- #

class LabelEdit(QWidget):
	"""A simple composite widget that pairs a `QLabel` with a `QLineEdit`.

	It provides a convenient way to create labeled text input fields with a
	horizontal layout.
	"""
	def __init__(self, name: str) -> None:
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
	"""A composite widget that combines an icon `QPushButton` with a `QLineEdit`.

	It's ideal for creating search or filter input fields. It includes a
	debouncing mechanism that emits the `search_text` signal only after the user
	has stopped typing for a brief period.
	"""
	search_text = pyqtSignal(str)

	def __init__(self, icon_name: str, default_str: str = "", callback: Optional[Callable] = None) -> None:
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

	def search_text_changed(self) -> None:
		# wait for 250 ms before
		if self.typing_timer.isActive():
			self.typing_timer.stop()
		self.typing_timer.start(350)

	def timer_up(self) -> None:
		# emit the text on the signal
		self.search_text.emit(self.entry.text())

# endregion


# -------------------------------------------------------------------------- #
#                                QComboBox                                   #
# region ------------------------------------------------------------------- #

class CleverCombo(QComboBox):
	"""An enhanced `QComboBox` that allows setting its current text
	programmatically.

	If the specified text is not already in the list of items, it will be added
	automatically. Includes an optional `MouseWheelGuard` to prevent accidental
	value changes from scrolling.
	"""

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


class CheckableComboBox(QComboBox):
	"""A `QComboBox` that presents a list of checkable items.

	The main display text shows a comma-separated summary of the currently
	checked items. The popup view remains open on item clicks to allow for
	multiple selections at once.
	"""

	class Delegate(QStyledItemDelegate):
		"""A custom item delegate used by `CheckableComboBox` to increase the
		height of each row in the dropdown list, improving readability and
		clickability.
		"""
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

# endregion


# -------------------------------------------------------------------------- #
#                           QComboBox Composites                             #
# region ------------------------------------------------------------------- #

class EditCombo(QWidget):
	"""A composite widget that provides a user-editable `QComboBox`.

	It includes '+' and '-' buttons to allow users to dynamically add the
	current text as a new item or delete the currently selected item from the
	list. Emits the `entries_changed` signal when the item list is modified.
	"""
	entries_changed = pyqtSignal(list)

	def __init__(self, parent: Optional[QWidget]) -> None:
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
	def items(self) -> list[str]:
		return [self.entry.itemText(i) for i in range(self.entry.count())]

	def add(self, _checked: bool = False, text: str = None) -> None:
		name = self.entry.currentText() if text is None else text
		if name and name not in self.items:
			self.entry.addItem(name)
			self.entries_changed.emit(self.items)

	def delete(self) -> None:
		name = self.entry.currentText()
		if name:
			ind = self.entry.findText(name)
			self.entry.removeItem(ind)
			self.entries_changed.emit(self.items)

	def set_data(self, items: Iterable[str]) -> None:
		items = sorted(set(items))
		self.entry.clear()
		self.entry.addItems(items)


class RelativePathCombo(EditCombo):
	"""A specialized `EditCombo` for managing a list of file paths.

	It automatically converts absolute paths to paths relative to a specified
	root file. It supports adding files via a file dialog, as well as by
	dragging and dropping them onto the widget.
	"""

	def __init__(self, parent: QWidget, file_widget: 'FileWidget', dtype="OVL") -> None:
		super().__init__(parent)
		self.file: 'FileWidget' = file_widget
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
	def root(self) -> str:
		return os.path.dirname(self.file.filepath)

	def relative_path(self, path) -> str:
		return os.path.normpath(os.path.relpath(path, self.root))

	def accept_file(self, filepath) -> bool:
		if os.path.isfile(filepath):
			if os.path.splitext(filepath)[1].lower() in (f".{self.dtype}",):
				return True
		return False

	def decide_add(self, filepath) -> None:
		if self.accept_file(filepath):
			path: str = self.relative_path(filepath)
			self.add(text=path)
			self.entry.setCurrentIndex(self.items.index(path))

	def ask_open(self) -> None:
		if self.file.filepath:
			filepath, _ = QFileDialog.getOpenFileName(self, f'Choose {self.dtype}', self.root, f"{self.dtype} files (*.{self.dtype})")
			self.decide_add(filepath)

	def get_files(self, event: QDropEvent ) -> List[QUrl] | None:
		data: QMimeData | None = event.mimeData()
		urls: List[QUrl] | None = data.urls() if data else None
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
		urls: List[QUrl] | None = self.get_files(event)
		if urls:
			self.decide_add(str(urls[0].path())[1:])


class LabelCombo(QWidget):
	"""A simple composite widget that pairs a `QLabel` with a `CleverCombo`.

	It provides a convenient way to create labeled dropdown selection fields
	with a horizontal layout.
	"""
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

# endregion


# -------------------------------------------------------------------------- #
#                                Q*SpinBox                                   #
# region ------------------------------------------------------------------- #

class NoScrollDoubleSpinBox(QDoubleSpinBox):
	"""A `QDoubleSpinBox` subclass that prevents its value from being changed
	by the mouse wheel unless the widget has focus.

	This is useful for preventing accidental edits when scrolling through a
	form or window.
	"""

	def __init__(self, parent: Optional[QWidget] = None, allow_scroll: bool = False) -> None:
		super().__init__(parent)
		# Allow scroll events before clicking
		self.allow_scroll = allow_scroll
		if not allow_scroll:
			self.installEventFilter(MouseWheelGuard(self))
			self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

# endregion


# -------------------------------------------------------------------------- #
#                              Constructors                                  #
# region ------------------------------------------------------------------- #

class MatcolFloatAttrib:
	"""A specialized widget for editing multi-value float attributes from a
	`FloatAttrib` object.

	It dynamically generates a horizontal row of `QDoubleSpinBox` widgets
	corresponding to the flags of the attribute, and includes
	integrated tooltips.
	"""

	def __init__(self, attrib: 'FloatAttrib', tooltips: dict = {}) -> None:
		self.attrib: 'FloatAttrib' = attrib
		name = attrib.attrib_name.data
		self.label = QLabel(name)

		self.data = QWidget()
		layout = QHBoxLayout()
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)
		buttons: list[QDoubleSpinBox] = [self.create_field(i) for i, v in enumerate(attrib.flags) if v]
		for button in buttons:
			layout.addWidget(button)
		self.data.setLayout(layout)
		# get tooltip
		tooltip = tooltips.get(name, "Undocumented attribute.")
		self.data.setToolTip(tooltip)
		self.label.setToolTip(tooltip)

	def create_field(self, ind: int) -> QDoubleSpinBox:
		default = self.attrib.value[ind]

		def update_ind(v: float) -> None:
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

# endregion
