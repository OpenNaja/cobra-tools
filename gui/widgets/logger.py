import threading
from collections import deque
from dataclasses import dataclass
from textwrap import dedent
from typing import TYPE_CHECKING, Any, AnyStr, Union, Optional, Iterable, Callable, cast, NamedTuple, Literal

from ovl_util import logs

from gui import qt_theme
from gui.widgets.input import LabelCombo
from gui.widgets.layout import OrientationToolBar, SnapCollapseWidget, ToolbarSpacingProxyStyle
from gui.app_utils import *
if TYPE_CHECKING:
	from gui.widgets.window import MainWindow

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject, QRect, QRectF, QSize, QTimer, QUrl, QMimeData,
						  QModelIndex, QAbstractListModel, QPersistentModelIndex, QItemSelectionModel, QVariant)
from PyQt5.QtGui import (QColor, QFont, QFontMetrics, QIcon, QPainter, QPen, QPainterPath, QLinearGradient,
						 QTextOption, QCloseEvent, QShowEvent, QHideEvent, QKeyEvent)
from PyQt5.QtWidgets import (QWidget, QApplication, QAbstractItemView, QListView, QLabel, QTextEdit, QPushButton,
							 QFrame, QHBoxLayout, QSizePolicy, QSplitter, QTextBrowser,
							 QStyleFactory, QStyleOptionViewItem, QStyledItemDelegate)


LOGGER_RIGHT = Qt.Orientation.Horizontal
LOGGER_BOTTOM = Qt.Orientation.Vertical


class LogStatus(QWidget):
	"""A compact status widget that displays an icon and a running count for a
	specific log level (e.g., WARNING, ERROR).

	It can optionally show the text of the most recent log message. Clicking the
	widget cycles through the messages in its queue and emits a `select_row`
	signal, allowing a parent view to highlight the corresponding log entry.
	"""
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

	def setOrientation(self, orientation: Qt.Orientation) -> None:
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
	"""A custom QStyledItemDelegate responsible for the advanced rendering of
	individual rows in the LogView.

	It handles drawing the log level icon, the colored background gradient,
	and the main log text. The key feature is the dynamic 'Details' indicator
	that appears on hover for log entries containing extended information,
	prompting user interaction.
	"""
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

		content_rect: QRect = option.rect.adjusted(
			self.TEXT_PADDING,       # Left padding from item edge
			self.TEXT_PADDING // 2,  # Top padding from item edge
			-self.TEXT_PADDING,      # Right padding from item edge
			-self.TEXT_PADDING // 2  # Bottom padding from item edge
		)
		# Effective vertical drawing area for text/indicator:
		drawing_y: int = content_rect.top()
		drawing_height: int = content_rect.height()
		# Define where text will start horizontally
		text_summary_start_x: int = option.rect.left() + self.ICON_AREA_WIDTH

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
			dpr = icon_pixmap.devicePixelRatioF()
			logical_icon_height = int(icon_pixmap.height() / dpr)
			icon_y = drawing_y + (drawing_height - logical_icon_height) // 2
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
				dpr = indicator_pixmap.devicePixelRatioF()
				logical_icon_height = int(indicator_pixmap.height() / dpr)
				arrow_y = drawing_y + (drawing_height - logical_icon_height) // 2
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
				dpr = indicator_pixmap.devicePixelRatioF()
				logical_icon_height = int(indicator_pixmap.height() / dpr)
				info_y = drawing_y + (drawing_height - logical_icon_height) // 2
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
	"""The data model for the LogView, designed to efficiently handle very large
	numbers of log entries.

	It implements lazy loading via the `fetchMore` mechanism, incrementally
	adding logs to the view to keep the UI responsive. The model stores log
	records as `LogListData` objects and serves the data for various display
	roles, such as the content, icon, and detailed information for each
	entry.
	"""
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
	"""The primary QListView widget for displaying formatted log messages.

	It integrates the `LogModel` for data management and the `LogViewDelegate`
	for custom row rendering. It orchestrates the lazy-loading of log records
	by periodically calling the model's `fetchMore` method, ensuring the
	application remains responsive even with a high volume of logs. It also
	features automatic scrolling, custom styling, and emits signals to update
	error/warning counts.
	"""
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
		self.setPalette(parent.parent().get_palette_from_cfg())
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
	def set_fetch_interval(self, interval_ms: int) -> None:
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

	def _pull_logs(self) -> None:
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
	def on_model_number_fetched(self, newly_fetched_count: int) -> None:
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


class LoggerWidget(SnapCollapseWidget):
	"""A comprehensive logging console widget that integrates a live log view
	with detailed inspection capabilities.

	It contains the `LogView` for displaying a list of logs, a `QTextBrowser`
	for showing detailed tracebacks or extra information, and a toolbar with
	error/warning counters and a log level filter. This widget captures
	application logs via its internal `Handler` class and manages the overall
	layout and user interaction for the logging system.
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
		"""A custom logging.Handler that captures log records from the
		application's logging system.

		It formats the records and stores them in a thread-safe buffer. The
		main LoggerWidget periodically polls this handler to retrieve and
		display new log messages.
		"""

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

		self.setPalette(parent.get_palette_from_cfg())

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
			parent.file_widget.file_clear_logger.connect(self.clear)
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

	def create_detail_view(self) -> QTextBrowser:
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

	def close_detail_pane(self, init_mode: bool = False) -> None:
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
	def on_detail_link_clicked(self, url: QUrl) -> None:
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

	def toggle_clear_logs(self, enabled: bool) -> None:
		self._clear_logs = enabled

	def reset_warnings(self) -> None:
		self.warnings.clear()

	def reset_errors(self) -> None:
		self.errors.clear()

