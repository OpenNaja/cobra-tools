import contextlib
import logging
import os
import time
import webbrowser
from abc import abstractmethod
from pathlib import Path
from typing import Any, AnyStr, Union, Optional, Iterable, Callable, cast, NamedTuple, Literal

from utils import logs
from utils.config import Config, ImmediateSetting, RestartSetting

from gui import GuiOptions, qt_theme
from gui.widgets.file_input import DirWidget, FileWidget
from gui.widgets.input import LabelCombo
from gui.widgets.layout import SnapCollapseSplitter
from gui.widgets.logger import LOGGER_BOTTOM, LOGGER_RIGHT, LoggerWidget
from gui.widgets.menu import BaseMenuItem, CheckableMenuItem, MenuItem, SeparatorMenuItem, SubMenuItem, add_label_separator
from gui.app_utils import *
from gui.tasks import WorkerRunnable

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QCoreApplication, QObject, QSize, QTimer, QThreadPool)
from PyQt5.QtGui import (QFont, QIcon, QCloseEvent, QDragEnterEvent, QDropEvent, QShowEvent)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QAction, QCheckBox, QLabel, QMenu,
							 QMessageBox, QMenuBar, QProgressBar, QStatusBar, QSpacerItem,
							 QFrame, QLayout, QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy,
							 QSplitter, QDialog, QDialogButtonBox)

try:
	from PyQt5.QtWinExtras import QWinTaskbarButton
	win_available = True
except ImportError:
	win_available = False

FRAMELESS = True
try:
	from qframelesswindow import FramelessMainWindow, StandardTitleBar
except ImportError:
	FRAMELESS = False
	from PyQt5.QtWidgets import QMainWindow as FramelessMainWindow
	StandardTitleBar = object

from __version__ import VERSION, COMMIT_HASH


class StatusSpacer(QWidget):
	"""Right aligns permanent status widgets by providing a dynamic space."""
	def __init__(self, parent: Optional[QWidget] = None) -> None:
		super().__init__(parent)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.splitter: QSplitter | None = None
		self._preferred_width = 0
		# Add a timer to defer the geometry update
		self._update_timer = QTimer(self)
		self._update_timer.setSingleShot(True)
		self._update_timer.timeout.connect(self._do_update_width)
		self._update_timer.setInterval(0)

	def set_splitter(self, splitter: QSplitter) -> None:
		"""Stores a reference to the log splitter."""
		self.splitter = splitter

	def sizeHint(self) -> QSize:
		"""Reports the dynamic preferred width."""
		return QSize(self._preferred_width, super().sizeHint().height())

	def initial_update(self) -> None:
		"""A safe, public method to perform the initial size calculation."""
		if self.splitter:
			# Just trigger the timer
			self._update_timer.start()

	@pyqtSlot(int, int)
	def update_width(self, pos: int, index: int) -> None:
		"""
		Public slot to be connected to the a splitterMoved signal.
		This just schedules the update to happen on the next event loop tick.
		"""
		# Just trigger the timer
		self._update_timer.start()

	@pyqtSlot()
	def _do_update_width(self) -> None:
		"""
		This slot is connected to the timer and does the actual work
		when the event loop is stable.
		"""
		parent = self.parent()
		if not self.splitter:
			return

		target_widget = self.splitter.widget(1)
		if isinstance(parent, QStatusBar) and target_widget:
			# If the widget isn't ready (width 0), try again
			if not target_widget.isVisible() or target_widget.width() == 0:
				self._update_timer.start(10)
				return

			new_width = max(1, target_widget.width() - 20)
			
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
	def __init__(self, parent: Optional[QWidget] = None, title: str = "", dir_walk: str = "") -> None:
		super().__init__(parent)
		self.setWindowTitle(title)
		self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, False)
		self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
		self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

		# Directory selector
		self.dir_widget = DirWidget(self, {})
		self.dir_widget.entry.setMinimumWidth(480)
		if dir_walk:
			self.dir_widget.open_dir(dir_walk)
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
	def dir_walk(self):
		return self.dir_widget.filepath

	@property
	def official_only(self):
		return self.chk_official.isChecked()

	@property
	def walk_ovls(self):
		return self.chk_ovls.isChecked()

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
		self.iconLabel = QtSvg.QSvgWidget(os.path.join(ROOT_DIR, f'icons/Cobra_Tools_Logo_24px.svg'), parent)
		self.iconLabel.setGeometry(6, 6, 24, 24)

	def setIcon(self, icon):
		"""Overriding StandardTitleBar.setIcon since self.iconLabel widget was changed due to DPI issues."""
		pass


class MainWindow(FramelessMainWindow):
	aboutToQuit = pyqtSignal()
	modified = pyqtSignal(bool)
	set_log_level = pyqtSignal(str)
	change_log_speed = pyqtSignal(str)  # Emits "fast", "normal", "slow"

	CANCEL_WAIT_MS = 2000

	def __init__(self, name: str, opts: GuiOptions, central_widget: Optional[QWidget] = None) -> None:
		self.opts = opts
		self.opts.frameless = self.opts.frameless and FRAMELESS
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
		self.setWindowIcon(QIcon(os.path.join(ROOT_DIR, f'icons/Cobra_Tools_Logo_24px.svg')))  # Do not cache with get_icon
		self._stdout_handler: logging.StreamHandler = logs.get_stdout_handler(opts.log_name)

		# Threadpool workers
		self.active_workers = set()
		self._current_batch_start_time: Optional[float] = None
		self._is_processing_worker_batch: bool = False

		self.file_widget: Optional['FileWidget'] = None
		self.logger: Optional['LoggerWidget'] = None
		self.log_splitter: Optional[QSplitter] = None

		if win_available:
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

		self.cfg: Config[str, Any] = Config(ROOT_DIR)
		self.cfg.load()
		# Flags for managing application lifecycle, controlled externally
		self.RESTART_ON_EXIT: bool = False
		self.SHUTDOWN_RUN: bool = False

		if self.opts.frameless:
			# Frameless titlebar
			self.titleBar.raise_()

		self.threadpool = QThreadPool.globalInstance()
		self.setCentralWidget(self.central_widget)
		self.resize(*opts.size)

		QApplication.instance().aboutToQuit.connect(self.aboutToQuit)

	@contextlib.contextmanager
	def log_level_override(self, level):
		# temporarily disable spamming the log widget
		log_level = self.cfg.get("logger_level", "INFO")
		self.set_log_level.emit(level)
		yield
		# go back to original log level
		self.set_log_level.emit(log_level)

	def showEvent(self, a0: QShowEvent) -> None:
		"""Post-init setup on show"""
		log_level = self.cfg.get("logger_level", "INFO")
		self.set_log_level.emit(log_level)
		super().showEvent(a0)
		# Defer layout until after the event loop finishes
		QTimer.singleShot(0, self.perform_initial_layout)

	def perform_initial_layout(self) -> None:
		"""
		This function should be called deferred (e.g., from showEvent)
		to finalize layout when geometry is stable.
		"""
		if self.logger and self.log_splitter:
			if not hasattr(self, "status_spacer"):
				self.status_spacer = StatusSpacer(self)
				self.status_spacer.set_splitter(self.log_splitter)
				self.status_bar.addPermanentWidget(self.status_spacer)
				self.log_splitter.splitterMoved.connect(self.status_spacer.update_width)

			# This is the deferred call to setSizes
			self._set_initial_logger_sizes()

			style = ""
			if self.logger.orientation == LOGGER_BOTTOM:
				style = R"""
					SnapCollapseSplitter::handle:vertical {
						padding: 0px 0px 4px 0px;
					}
				"""
			elif self.logger.orientation == LOGGER_RIGHT:
				style = R"""
					SnapCollapseSplitter::handle:horizontal {
						width: 5px; /* Make handle visible */
					}
				"""
			self.log_splitter.setStyleSheet(style)

			if hasattr(self, "status_spacer"):
				self.status_spacer.initial_update()
	
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
		if enable_logger and self.opts.logger_enabled:
			# This creates the logger, splitter, applies styles,
			# and performs the one-time window resize.
			self.layout_logger(self.main_content_widget)
		else:
			# No logger, just add the main content widget directly.
			self.central_layout.addWidget(self.main_content_widget)

	def layout_logger(self, main_content: QWidget, orientation = None) -> None:
		"""
		Creates, configures, and lays out the logger and its splitter.
		This is called once from create_main_splitter during initialization.
		"""
		logger_orientation = orientation
		if orientation is None:
			logger_orientation = LOGGER_BOTTOM if self.cfg.get("logger_orientation", "V") == "V" else LOGGER_RIGHT

		# Create LoggerWidget
		self.logger = LoggerWidget(self, logger_orientation)
		self.logger.handler.setFormatter(logs.DelegatingFormatter(logs.LoggerFormatter()))
		self.logger.handler.setLevel(logging.INFO)
		
		listener = logs.get_global_listener()
		if listener:
			handlers = list(listener.handlers)
			handlers.append(self.logger.handler)
			listener.handlers = tuple(handlers)

		# Connect signals
		self.change_log_speed.connect(self.logger.set_logging_speed)
		self.logger.log_level_changed.connect(self.on_log_level_changed)
		self.logger.resize_requested.connect(self.resize_logger)

		#  Create Splitter
		self.log_splitter = SnapCollapseSplitter(logger_orientation)
		self.log_splitter.addWidget(main_content)
		self.log_splitter.addWidget(self.logger)

		# Apply Styles
		self.log_splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.log_splitter.setContentsMargins(0, 0, 0, 0)
		self.log_splitter.setCollapsible(0, True)
		self.log_splitter.setCollapsible(1, False)
		self.log_splitter.setHandleWidth(8)
		self.log_splitter.setStretchFactor(0, 1)  # Main content
		self.log_splitter.setStretchFactor(1, 0)  # Logger

		style = ""
		if logger_orientation == LOGGER_BOTTOM:
			# Set margins on the content widget
			main_content.setContentsMargins(5, 0, 5, 5)
			
			# Initial size
			self.resize(self.opts.size.width, self.opts.size.height + self.opts.logger_height)

		elif logger_orientation == LOGGER_RIGHT:
			# Set margins on the content widget
			main_content.setContentsMargins(5, 0, 0, 0)
			
			# Initial size
			self.resize(self.opts.size.width + self.opts.logger_width, self.opts.size.height)

		# Add Splitter to Central Layout
		self.central_layout.addWidget(self.log_splitter)

		# Handle Initial Visibility
		self.show_logger = self.cfg.get("show_logger_widget", True)
		if not self.show_logger:
			self.logger.close()
			# Reset to non-logger size if starting hidden
			self.resize(*self.opts.size)

	def _set_initial_logger_sizes(self) -> None:
		"""
		Sets the initial sizes of the log_splitter's panes.
		This is separate from setup and should be called deferred
		(e.g., from perform_initial_layout) when geometry is stable.
		"""
		if not self.logger or not self.log_splitter:
			return  # No logger to size

		splitter_size = self.log_splitter.size()
		if splitter_size.width() == 0 or splitter_size.height() == 0:
			return  # Splitter not ready, abort.

		if self.logger.orientation == LOGGER_BOTTOM:
			logger_height = self.opts.logger_height
			main_content_height = splitter_size.height() - logger_height
			if main_content_height < 0: main_content_height = 0
			
			self.log_splitter.setSizes([main_content_height, logger_height])

		elif self.logger.orientation == LOGGER_RIGHT:
			logger_width = self.opts.logger_width
			main_content_width = splitter_size.width() - logger_width
			if main_content_width < 0: main_content_width = 0
			
			self.log_splitter.setSizes([main_content_width, logger_width])

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
		game = self.cfg["current_game"]
		recent_files_from_cfg = self.cfg["games"][game]["recent"]
		valid_files = [fp for fp in recent_files_from_cfg if os.path.isfile(fp)]
		# If stale paths were removed, update the configuration
		if len(valid_files) != len(recent_files_from_cfg):
			self.cfg["games"][game]["recent"] = valid_files
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
			self.cfg["games"][game]["recent"] = []

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
		if win_available:
			self.taskbar_progress.setValue(value)
		# stop any running timers that would hide the progress bar
		if self.status_timer.isActive():
			self.status_timer.stop()
		# start the countdown for hiding the progress bar if progress is finished
		if self.progress.value() >= self.progress.maximum():
			self.status_timer.start()

	def set_progress_total(self, value: int) -> None:
		if self.progress.isHidden():
			self.show_progress()
		self.progress.setMaximum(value)
		if win_available:
			self.taskbar_progress.setMaximum(value)

	def reset_progress(self) -> None:
		if win_available:
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
			worker.signals.finished.disconnect(worker_cleanup_slot)

		# Connect the cleanup slot to run when the worker is done
		worker.signals.finished.connect(worker_cleanup_slot)

		self.active_workers.add(worker)
		logging.debug(f"Starting worker for '{func.__name__}'. Total active: {len(self.active_workers)}")
		self.threadpool.start(worker)
		self.enable_gui_options(False)

	def run_background_task(self, func: Callable, on_result: Callable, *args, **kwargs) -> WorkerRunnable:
		"""
		Runs a function in the threadpool for non-blocking UI tasks.
		Does not disable the GUI or manage batch timing.

		Args:
			func: The function to execute in the worker.
			on_result: The callback slot to connect to the worker's `result` signal.
			*args, **kwargs: Arguments to pass to the function.

		Returns:
			The WorkerRunnable instance, allowing the caller to manage it (e.g., for cancellation).
		"""
		logging.debug(f"Starting background task for '{func.__name__}'")
		worker = WorkerRunnable(func, *args, **kwargs)

		# Connect the essential signals
		worker.signals.error_msg.connect(self.showerror)
		worker.signals.result.connect(on_result) # Connect the specific result callback

		# Add a simplified cleanup slot to remove the worker from the active set
		# This ensures it's still tracked for a clean shutdown via cancel_workers()
		def worker_cleanup_slot():
			if worker in self.active_workers:
				self.active_workers.remove(worker)
			logging.debug(f"Background task '{func.__name__}' finished. Active workers: {len(self.active_workers)}")
			worker.signals.finished.disconnect(worker_cleanup_slot)

		worker.signals.finished.connect(worker_cleanup_slot)
		
		# Add the worker to the set and start it
		self.active_workers.add(worker)
		self.threadpool.start(worker)
		
		# Return the worker instance so the caller can manage it
		return worker

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

		# Shut down log splitter
		if self.log_splitter and isinstance(self.log_splitter, SnapCollapseSplitter):
			self.log_splitter.shutdown()
		# Stop the status timer
		if self.status_timer.isActive():
			self.status_timer.stop()
		# Close logger widget
		if self.logger:
			self.logger.close()
		# Custom splitter style has strange error with QSS on pytest teardown
		if hasattr(self, 'log_splitter') and self.log_splitter:
			try:
				self.log_splitter.setStyleSheet("")
			except RuntimeError:
				pass

		event.accept()
		# Last resort workaround for console hanging
		# NOTE: Left as documentation in case it happens again.
		#       Instead, ensure any unparented widgets are closed or made parented
		#QCoreApplication.instance().quit()

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
		"""
		It receives the user's choice and applies the correct levels to all handlers
		"""
		# Determine the actual numeric level to set on the handlers
		actual_level = level
		if level == "WARNING":
			actual_level = "SUCCESS"

		if self.stdout_handler:
			# Set the level on the console handler
			self.stdout_handler.setLevel(actual_level)
		if self.logger:
			# Set the level on the GUI's handler
			self.logger.handler.setLevel(actual_level)
			# Update the logger's combo box to reflect the choice
			self.logger.log_level_choice.entry.setText(level)

		# Persist the user's choice to the config
		self.cfg["logger_level"] = level

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
		msg = QMessageBox(self)
		msg.setIcon(QMessageBox.Icon.Information)
		msg.setText(info)
		msg.setWindowTitle(title)
		msg.setStandardButtons(msg.Ok if not buttons else buttons)
		if details:
			msg.setDetailedText(details)
		return msg.exec_() not in [msg.No, msg.Cancel]

	def showquestion(self, info, title=None, details=None):
		logging.debug(f"User Prompt: {info}")
		return self.showdialog(info, title="Question" if not title else title,
						buttons=(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No), details=details)

	def showconfirmation(self, info, title=None, details=None):
		logging.debug(f"User Prompt: {info}")
		return self.showdialog(info, title="Confirm" if not title else title,
						buttons=(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel), details=details)

	def showwarning(self, info, details=None):
		logging.debug(f"User Prompt: {info}")
		return self.showdialog(info, title="Warning", details=details)

	def showerror(self, info, details=None):
		logging.debug(f"User Prompt: {info}")
		return self.showdialog(info, title="Error", details=details)


class ConfigWindow(QWidget):

	def __init__(self, main_window: 'MainWindow') -> None:
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
					cfg_manager2.update(self.cfg, cfg_key2, v)
					if isinstance(cfg_manager2, RestartSetting):
						self.needs_restart()

				return set_key

			set_key = make_setter()
			c = LabelCombo(cfg_manager.name, [str(x) for x in cfg_manager.options],
						   editable=not bool(cfg_manager.options), activated_fn=set_key)
			c.setToolTip(cfg_manager.tooltip)
			c.entry.setText(str(self.cfg.get(cfg_key, cfg_manager.default)))
			# if isinstance(cfg_manager, ImmediateSetting):
			# 	logging.debug(f"Saved '{self.name}' after storing '{k}'")
			# 	self.cfg.save()
			self.vlayout.addWidget(c)
		self.setLayout(self.vlayout)

	def needs_restart(self):
		from gui import root_dir
		from utils.config import save_config
		if self.main_window.showconfirmation(
			"The application must restart for changes to take effect. If you have "
			"any unsaved changes, cancel and restart manually.",
			title="Restart Required"
		):
			save_config(root_dir / "config.json", self.cfg)
			self.main_window.RESTART_ON_EXIT = True
			self.close()
			self.main_window.close()
