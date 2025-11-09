import logging
import os
import re
import fnmatch
from typing import TYPE_CHECKING, Any, AnyStr, Union, Optional, Iterable, Callable, cast, NamedTuple, Literal

from gui.app_utils import *
from gui.tasks import WorkerRunnable
from gui.widgets.input import CleverCombo, IconButton, IconEdit
if TYPE_CHECKING:
	from gui.widgets.window import MainWindow

from modules.walker import valid_packages
from generated.formats.ovl import games

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject, QDir, QFileInfo, QRegularExpression,
						  QTimer, QSortFilterProxyModel, QModelIndex, QDirIterator)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QWidget, QFileDialog, QAbstractItemView, QTreeView, QFileSystemModel, QStyle, 
							 QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)


def cache_directory(root_path: str, name_filters: list[str],
					cancellation_check: Callable[[], bool]) -> tuple[dict, str] | None:
	"""
	Scans a directory and builds a cache map. This function is designed
	to be run in a WorkerRunnable.
	
	Returns a tuple (cache_map, root_path) on success, or None on cancellation.
	"""
	logging.debug(f"[cache_directory] Starting cache map build for: {root_path}")
	if not root_path or not os.path.isdir(root_path):
		return {}, root_path

	cache_map = {}
	iterator = QDirIterator(
		root_path, name_filters,
		QDir.Files | QDir.NoDotAndDotDot,
		QDirIterator.Subdirectories
	)

	while iterator.hasNext():
		# Use the injected cancellation check
		if cancellation_check():
			logging.debug("[cache_directory] Scan cancelled.")
			return None  # Return None to signal cancellation

		file_path = iterator.next()
		dir_path = os.path.dirname(file_path)
		# Normalize paths for case-insensitive matching
		norm_dir = os.path.normcase(os.path.normpath(dir_path))
		norm_file = os.path.normcase(os.path.normpath(file_path))
		# Add the file to its parent directory's set
		if norm_dir not in cache_map:
			cache_map[norm_dir] = set()
		cache_map[norm_dir].add(norm_file)

	total_files = sum(len(file_set) for file_set in cache_map.values())
	logging.debug(f"[cache_directory] Scan complete. Found {total_files} files in {len(cache_map)} directories.")
	
	# Return the results instead of emitting a signal
	return cache_map, root_path


class OvlDataFilterProxy(QSortFilterProxyModel):
	"""A high-performance filter proxy model for `OvlDataFilesystemModel`.

	It optimizes filtering by pre-computing and caching a set of all file and
	directory paths that match the filter regular expression. This avoids slow,
	recursive directory scans during filtering and view updates. It also
	implements custom sorting to handle file names with numbers naturally
	(e.g., 'file10' after 'file2') and emulates `setRootPath` behavior.
	"""

	def __init__(self, parent: Optional[QObject] = None) -> None:
		super().__init__(parent)
		self.setDynamicSortFilter(True)
		self.max_depth: int = 255
		self.root_idx: Optional[QModelIndex] = None
		self.root_depth: int = 0
		# The complete map of {dir -> {files}} from the cacher
		self._full_cache_map: dict[str, set[str]] = {}
		# The set of paths that should be visible for the current filter
		self._filter_results: set[str] = set()
		self._root_path_norm: str = ""
		self._use_filter_cache = False

	def set_directory_cache(self, cache_map: dict, root_path_norm: str) -> None:
		self._full_cache_map = cache_map
		self._root_path_norm = root_path_norm
		self.setFilterRegularExpression(self.filterRegularExpression())

	def clear_cache(self) -> None:
		"""Resets all cache and filter data to a clean state."""
		self._full_cache_map: dict[str, set[str]] = {}
		self._filter_results: set[str] = set()
		self._root_path_norm: str = ""
		self._use_filter_cache = False
		self.invalidateFilter()

	def setFilterRegularExpression(self, regex: QRegularExpression) -> None:
		"""Pre-computes and caches filter results on filter set"""
		super().setFilterRegularExpression(regex)
		self._filter_results.clear()

		if not self._full_cache_map:
			self._use_filter_cache = False
			self.invalidateFilter()
			return

		if not regex or not regex.pattern():
			self._filter_results = set(self._full_cache_map.keys())
			for file_set in self._full_cache_map.values():
				self._filter_results.update(file_set)
			if self._root_path_norm:
				self._filter_results.add(self._root_path_norm)
			self._use_filter_cache = False
			self.invalidateFilter()
			return

		# Find all files that match the filter first
		matching_files = set()
		for files_in_dir in self._full_cache_map.values():
			for file_path in files_in_dir:
				if regex.match(file_path).hasMatch():
					matching_files.add(file_path)

		self._use_filter_cache = True

		# Add the matching files and all their parents to the results
		self._filter_results.update(matching_files)
		for file_path in matching_files:
			parent = os.path.dirname(file_path)
			while len(parent) >= len(self._root_path_norm):
				# Stop if we've already processed this parent chain
				if parent in self._filter_results:
					break
				self._filter_results.add(parent)
				if parent == self._root_path_norm:
					break
				# Move to the next parent up
				new_parent = os.path.dirname(parent)
				if new_parent == parent:
					break
				parent = new_parent
		self.invalidateFilter()

	def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
		"""
		Emulates rootPath/rootIndex and uses cached filter results when possible
		"""
		model = self.sourceModel()
		source_index = model.index(source_row, 0, source_parent)

		# Implement setRootPath/setRootIndex behavior for proxy
		is_dir = model.isDir(source_index)
		if is_dir and (self.root_depth == 0 or self.depth(source_index) <= self.root_depth):
			return True

		if self._use_filter_cache:
			# The cache is ready and a filter has been applied
			path = os.path.normcase(os.path.normpath(model.filePath(source_index)))
			return path in self._filter_results
		else:
			# Fall back to standard behavior for no filter/cache
			# This ensures tree is working and updates when cache is not available
			regex = self.filterRegularExpression()
			item_path = model.filePath(source_index)
			if regex.match(item_path).hasMatch():
				return True
			if is_dir:
				if model.canFetchMore(source_index):
					# Keep filter results accurate in absence of cache
					model.fetchMore(source_index)
				for i in range(model.rowCount(source_index)):
					if self.filterAcceptsRow(i, source_index):
						return True
			return False

	def depth(self, source_index: QModelIndex) -> int:
		"""Depth of the file or directory in the filesystem"""
		level = 0
		while source_index.parent().isValid():
			level += 1
			source_index = source_index.parent()
		return level

	def set_max_depth(self, depth: int) -> None:
		"""Set max subfolder depth. 0 depth = ovldata root folders only."""
		self.max_depth = depth

	def update_root(self, source_index: QModelIndex) -> None:
		"""Update root index and store base depth for ovldata subfolder"""
		self.root_depth = self.depth(source_index)

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


class OvlDataFilesystemModel(QFileSystemModel):
	"""A QFileSystemModel subclass that is aware of its proxy model.

	It overrides key methods like `fileInfo`, `filePath`, and `fileName` to
	ensure that any QModelIndex passed to it is first mapped from the proxy
	model's space to the source model's space. This guarantees correct file
	information is retrieved, even when the view is filtered or sorted.
	"""

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
	"""The main QTreeView for displaying the ovldata file system.

	It integrates the `OvlDataFilesystemModel` and `OvlDataFilterProxy` to
	provide a filtered and sorted view of files. It initiates a background
	thread to scan and cache the directory structure for performance. A key
	feature is its iterative expansion mechanism, which is necessary to
	overcome the slow lazy-loading of `QFileSystemModel`. It automatically
	expands all directories to reveal items that match the current filter.
	"""
	dir_dbl_clicked = pyqtSignal(str)
	file_dbl_clicked = pyqtSignal(str)
	# Signal to request a new directory scan on the worker thread
	scan_requested = pyqtSignal(str, list)

	def __init__(self, parent: Optional[QWidget] = None, main_window: 'MainWindow' = None, actions={}, filters=()) -> None:
		super().__init__(parent)
		self.current_file_path = None
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
		self.setUniformRowHeights(True)

		self.header().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
		self.model().sort(self.header().sortIndicatorSection(), self.header().sortIndicatorOrder())
		self.setAnimated(False)
		self.setIndentation(12)
		self.setSortingEnabled(True)

		self.clicked.connect(self.item_clicked)
		self.doubleClicked.connect(self.item_dbl_clicked)

		# Store a reference to the main window to access its threadpool
		self.main_window = main_window
		# Store cacher worker to cancel it if necessary
		self.current_cacher_worker: Optional['WorkerRunnable'] = None
		self.cache_ready = False
		self.background_timer = QTimer(self)
		self.background_timer.setSingleShot(True)
		# Connect the timeout signal to a lambda that calls the scan function
		self.background_timer.timeout.connect(lambda: self.start_background_scan(self.file_model.rootPath()))
		# State for the expansion process
		self._is_expanding = False
		self._expand_retry_counter = 0
		# Store filter text to restore on game change
		self.filter_text = ""

		self._expand_start_timer = QTimer(self)
		self._expand_start_timer.setSingleShot(True)
		self._expand_start_timer.timeout.connect(self._start_iterative_expand)
		self._expand_step_timer = QTimer(self)
		self._expand_step_timer.setSingleShot(True)
		self._expand_step_timer.timeout.connect(self._iterative_expand_step)

	def start_background_scan(self, dir_game: str):
		"""Cancels any previous scan and asks the MainWindow to start a new one"""
		if self.current_cacher_worker:
			self.current_cacher_worker.cancel()
		# Unpack result object
		result_adapter = lambda result_tuple: self.on_cache_ready(result_tuple[0], result_tuple[1])
		# Run cacher using MainWindow's facilities
		self.current_cacher_worker = self.main_window.run_background_task(
			func=cache_directory,
			on_result=result_adapter,
			# cache_directory args
			root_path=dir_game,
			name_filters=self.file_model.nameFilters()
		)

	@pyqtSlot(dict, str)
	def on_cache_ready(self, cache_map: dict, scanned_root: str):
		"""Slot to receive the directory cache and apply it to the proxy"""
		current_root = self.file_model.rootPath()
		# Normalize to handle differences in slashes or casing
		if os.path.normpath(os.path.normcase(scanned_root)) == os.path.normpath(os.path.normcase(current_root)):
			logging.debug(
				f"Cache applied for {scanned_root} with {len(cache_map)} directories"
			)
			root_path_norm = os.path.normcase(os.path.normpath(scanned_root))
			self.proxy.set_directory_cache(cache_map, root_path_norm)
			self.cache_ready = True
		else:
			logging.debug(f"Ignoring stale cache for {scanned_root} (Current: {current_root})")

		# Restore existing filter text
		self.set_filter(self.filter_text)

		# qt crashes if the cfg dict is queried here, so just use current_file_path that has been set before
		self.set_selected_path(self.current_file_path)

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
		logging.debug(f"OvlDataTreeView set root: {dir_game}")
		if os.path.normcase(os.path.normpath(self.file_model.rootPath())) == os.path.normcase(os.path.normpath(dir_game)):
			logging.debug("Root Path already set.")
			return
		self.cache_ready = False
		# Clear the old cache immediately. This makes all directories visible
		# while the new cache is being generated, preventing an empty view.
		self.proxy.setFilterRegularExpression(QRegularExpression())
		self.proxy.clear_cache()
		# Sync root path/index
		root_index = self.file_model.setRootPath(dir_game)
		self.proxy.invalidate()
		self.setRootIndex(root_index)
		self.proxy.update_root(root_index)
		# Trigger a new scan in the background after the event loop finishes
		self.background_timer.start(0)

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

	def set_filter(self, filter_str: str) -> None:
		"""Applies the filter and starts the view update process"""
		logging.debug(f"Setting Filter Regex: {filter_str}")
		# Store the most recent filter string
		self.filter_text = filter_str
		if self._is_expanding:
			self._is_expanding = False
		# Apply the filter
		self.proxy.setFilterRegularExpression(
			QRegularExpression(filter_str,
							   options=QRegularExpression.PatternOption.CaseInsensitiveOption)
		)
		if filter_str:
			# Start expanding on a small delay
			self._expand_start_timer.start(50)
		else:
			# Simply collapse all on filter clear
			self.collapseAll()

	def _start_iterative_expand(self) -> None:
		"""Begins the iterative tree expansion"""
		if self._is_expanding:
			return
		# Start the first step of the expansion
		self._is_expanding = True
		self._expand_retry_counter = 0
		self._iterative_expand_step()

	def _iterative_expand_step(self) -> None:
		"""
		Performs one pass of expanding all currently visible, collapsed items.
		Schedules itself to run again if it made any progress.
		"""
		if not self._is_expanding:
			return
		# State of this pass
		items_were_expanded = False
		queue = [self.rootIndex()]
		head = 0
		# Pause GUI updates
		self.setUpdatesEnabled(False)
		try:
			while head < len(queue):
				parent_index = queue[head]
				#parent_data = parent_index.data() if parent_index.isValid() else "ROOT"
				#logging.debug(f"  Processing queue item: head={head}, queue_size={len(queue)}, item='{parent_data}'")
				head += 1
				if not parent_index.isValid():
					continue
				# Check for collapsed directories and expand them
				isDir = self.file_model.isDir(self.proxy.mapToSource(parent_index))
				if isDir:
					#logging.debug(f"    '{parent_data}' is dir")
					if not self.isExpanded(parent_index):
						#logging.debug(f"    >>> Expanding '{parent_data}'")
						self.expand(parent_index)
						items_were_expanded = True
					# Queue the dir's children dirs in this pass if loaded, or next pass
					for row in range(self.model().rowCount(parent_index)):
						child_index = self.model().index(row, 0, parent_index)
						if self.file_model.isDir(self.proxy.mapToSource(child_index)):
							queue.append(child_index)
		finally:
			# Resume GUI updates no matter what
			self.setUpdatesEnabled(True)

		# If we made progress, reset the retry counter and continue the loop
		if items_were_expanded:
			self._expand_retry_counter = 0
			self._expand_step_timer.start(50)
		else:
			# If no progress was made, increment the counter
			self._expand_retry_counter += 1
			# The loop continues if the cache isn't ready OR if we haven't
			# exhausted our attempts. This gives the model time to load.
			if not self.cache_ready or self._expand_retry_counter < 5:
				self._expand_step_timer.start(200)
			else:
				# No progress for several consecutive passes
				self._is_expanding = False

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
	"""A widget for selecting a game from a dropdown list of installed games.

	It includes a combo box populated with detected and user-added games, a
	button to launch the selected game, and a button to manually add a new
	game by selecting its folder. It emits signals when a game is selected
	from the list.
	"""
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
		for game, game_info in sorted_games:
			ovldata = game_info["path"]
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
		for game, path in get_steam_games(self.games_list).items():
			self.cfg.init_game_in_cfg(game, path)
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
			game = os.path.basename(without_suffix)
			# suffix the dir without suffix again and store that if it exists
			added_suffix = os.path.join(without_suffix, "win64", "ovldata")
			if os.path.isdir(added_suffix):
				dir_game = added_suffix
			# store this newly chosen game in cfg
			self.cfg.init_game_in_cfg(game, dir_game)
			# update available games
			self.set_data(self.cfg["games"])
			self.game_chosen(game)


class OvlSearchWidget(QWidget):
	"""A simple search input widget, consisting of a line edit and a search
	button.

	It is designed to trigger a content search within OVL archives. It emits
	the `search_content_clicked` signal with the search term when the button is
	clicked or enter is pressed. All input is automatically converted to
	lowercase.
	"""
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
	"""A widget containing a set of controls for filtering the file list in
	OvlDataTreeView.

	It provides a text input for name-based filtering (with wildcard support)
	and toggle buttons for quickly showing only 'official' or 'modded' OVL
	files. It emits the `filter_changed` signal with a regular expression
	pattern corresponding to the user's selection.
	"""
	filter_changed = pyqtSignal(str)
	
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
			self.filter_changed.emit(rf"^(?:(?!(?:{'|'.join(valid_packages)})).)*\Z")
		else:
			self.filter_changed.emit("")

	def show_official_toggle(self, checked: bool) -> None:
		if checked:
			self.filter_entry.entry.setText("")
			self.show_modded_button.setChecked(False)
			self.filter_changed.emit(rf"^.*(?:{'|'.join(valid_packages)}).*\Z")
		else:
			self.filter_changed.emit("")

	def set_filter(self):
		filter_str = self.filter_entry.entry.text()
		if not filter_str:
			self.filter_changed.emit("")
			return
		# Turn off the other filters if a search string was entered
		self.show_modded_button.setChecked(False)
		self.show_official_button.setChecked(False)
		# Wildcard (*, ?) substring search
		final_pattern = fnmatch.translate(f"ovldata*{filter_str}*")  # translate() adds \Z, so wrap with *
		self.filter_changed.emit(final_pattern)


class OvlManagerWidget(QWidget):
	"""A high-level composite widget that assembles the entire OVL file
	management panel.

	It integrates the `GameSelectorWidget`, `OvlSearchWidget`,
	`OvlFilterWidget`, and `OvlDataTreeView` into a single functional unit.
	This class is responsible for connecting the signals and slots between the
	various sub-widgets, orchestrating the overall user workflow for game
	selection, searching, filtering, and file navigation.
	"""

	def __init__(self, parent: 'MainWindow',
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
		self.dirs = OvlDataTreeView(self, parent, actions=actions, filters=filters)

		self.filters = OvlFilterWidget(self)
		self.filters.filter_changed.connect(self.dirs.set_filter)

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
		dict_game = self.cfg["games"].get(game, None)
		# if current_game has been set, assume it exists in the games dict too (from steam)
		if dict_game:
			self.dirs.set_root(dict_game["path"])
			self.dirs.current_file_path = self.cfg.get_last_file("ovl", game)
			self.game_choice.entry.blockSignals(True)
			self.game_choice.entry.setText(game)
			self.game_choice.entry.blockSignals(False)

