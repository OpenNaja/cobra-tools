import logging
import os
from pathlib import Path
from typing import Any, AnyStr, Union, Optional, Iterable, Callable, cast, NamedTuple, Literal

from utils.config import Config

from gui.widgets.event_filters import ClickGuard, DragDropPassthrough
from gui.app_utils import *

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject, QUrl)
from PyQt5.QtGui import (QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent, QMouseEvent)
from PyQt5.QtWidgets import (QWidget, QFileDialog, QLineEdit, QMessageBox, QPushButton, QGridLayout)


class FileDirWidget(QWidget):
	"""A base widget for file or directory selection that combines an icon
	button with a line edit.

	It provides the core functionality for handling file paths, managing
	configuration for recent and last-used directories, and accepting
	drag-and-drop events. This class is intended to be subclassed by more
	specific widgets like `FileWidget` and `DirWidget`.
	"""
	dir_opened = pyqtSignal(str)
	filepath_changed = pyqtSignal(str, bool)

	def __init__(self, parent: QWidget, cfg: 'Config', cfg_key: str, ask_user: bool = True, editable: bool = False,
				 check_exists: bool = False, root: Optional[str] = None) -> None:
		super().__init__(parent)
		self.mainWidget = parent
		self.ftype = cfg_key
		self.cfg_key = cfg_key.lower()
		self.root = root
		self.cfg: 'Config' = cfg
		self.cfg.setdefault(self.cfg_last_dir_save, "C:/")

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
		# todo - only pass game when it makes sense to store per-game
		game = self.cfg["current_game"]
		last_file = self.cfg.get_last_file(self.ftype_lower, game=game)
		if last_file:
			return os.path.dirname(last_file)
		else:
			return "C://"

	@property
	def cfg_last_dir_save(self) -> str:
		return f"dir_{self.cfg_key}s_out"

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
	"""A specialized widget for selecting a single file.

	It inherits from `FileDirWidget` and adds functionality for opening,
	saving, and managing a specific file path. Clicking the widget opens a
	`QFileDialog`. It includes logic to prompt the user about unsaved
	changes before opening a new file and emits signals like `file_opened`
	and `file_saved` to integrate with application logic.
	"""
	file_clear_logger = pyqtSignal(str)
	file_opened = pyqtSignal(str)
	file_saved = pyqtSignal(str)

	def __init__(self, parent: QWidget, cfg: 'Config', ftype: str = "OVL", ask_user: bool = True, editable: bool = False,
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
			self.file_clear_logger.emit(filepath)
			self.set_file_path(filepath)
			# todo - only pass game when it makes sense to store per-game
			game = self.cfg["current_game"]
			self.cfg.add_recent_file(filepath, self.ftype_lower, game=game)
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

	def get_open_file_name(self, title: Optional[str] = None):
		title = title if title else f'Load {self.ftype}'
		filepath = QFileDialog.getOpenFileName(
			self, title, self.cfg_last_dir_open, self.files_filter_str)[0]
		return filepath

	def ask_open_dir(self) -> None:
		# TODO: This is generally confusing for something named FileWidget
		#       although it is no longer hardcoded for OVL Tool
		dirpath = QFileDialog.getExistingDirectory(directory=self.cfg_last_dir_open)
		if self.accept_dir(dirpath):
			self.file_clear_logger.emit(dirpath)
			self.dir_opened.emit(dirpath)
			# Store the parent directory so that the next File > New
			# opens in root to allow selection of sibling folders.
			# self.cfg[self.cfg_last_dir_open], _ = os.path.split(dirpath)
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


class DirWidget(FileDirWidget):
	"""A specialized widget for selecting a single directory.

	It inherits from `FileDirWidget` and configures the click and drop
	behavior to work with directories instead of files. Clicking the widget
	opens a `QFileDialog` in directory selection mode and emits the

	`dir_opened` signal upon a successful selection.
	"""

	def __init__(self, parent: QWidget, cfg: 'Config', cfg_key: str = "DIR", ask_user: bool = True) -> None:
		super().__init__(parent=parent, cfg=cfg, cfg_key=cfg_key, ask_user=ask_user)

	def open_dir(self, filepath: str) -> None:
		if not self.accept_dir(filepath):
			logging.warning(f"{filepath} could not be opened as a directory.")

	def ask_open_dir(self) -> None:
		filepath = QFileDialog.getExistingDirectory(directory=self.cfg_last_dir_open)
		if self.accept_dir(filepath):
			pass

	def accept_dir(self, dirpath: str) -> bool:
		if os.path.isdir(dirpath):
			self.filepath = dirpath
			# self.cfg[self.cfg_last_dir_open], self.basename = os.path.split(dirpath)
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
