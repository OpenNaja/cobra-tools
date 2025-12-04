import contextlib
import os
import shutil
import logging
import tempfile
import time
from pathlib import PurePath

if __name__ == "__main__":
	# Guard to hide from pytest or other imports
	from gui.tools.dev_tools import setup_dev_diagnostics
	setup_dev_diagnostics()
	from utils.auto_updater import run_update_check
	run_update_check("ovl_tool_gui")

	# TODO: Temporary location until logs.py code is fixed
	CONFIG_VERSION = "1.0.2"
	# --- MIGRATION ---
	from utils.migrator import Migrator
	migrator = Migrator("config.json", CONFIG_VERSION)
	migrator.run()


from gui import widgets, GuiOptions
from gui.app_utils import DelayedMimeData
from gui.widgets import window, MenuItem, SubMenuItem, SeparatorMenuItem
from modules import walker
import modules.formats.shared
from generated.formats.ovl import games, OvlFile
from generated.formats.ovl_base.enums.Compression import Compression
from PyQt5 import QtWidgets, QtGui, QtCore
from typing import Optional


class SearchWindow(window.MainWindow):

	found_matches = QtCore.pyqtSignal(list)

	def __init__(self, main_window, search_str):
		opt = GuiOptions(
			log_name="ovl_tool_gui",
			size=(800, 600),
			check_update=False  # Check update happens at top now
		)
		super().__init__(f"Results for: {search_str}", opt)
		self.main_window = main_window
		self.search_str = search_str
		self.ovl_game_choice = main_window.ovl_game_choice
		self.results_container = widgets.SortableTable(
			["Name", "File Type", "OVL"], main_window.ovl_data.formats_dict.ignore_types, ignore_drop_type="OVL", opt_hide=True,
			actions={
				QtWidgets.QAction("Open in OVL Tool"): main_window.search_result_open,
				QtWidgets.QAction("Show in Explorer"): main_window.search_result_show,
			}, editable_columns=())
		self.setCentralWidget(self.results_container)
		self.setGeometry(QtCore.QRect(100, 100, 1000, 600))
		self.results_container.set_data([])
		self.reporter = widgets.Reporter()
		reporter = self.reporter
		reporter.progress_percentage.connect(self.set_progress)
		reporter.progress_total.connect(self.set_progress_total)
		reporter.success_msg.connect(self.set_progress_message)
		reporter.current_action.connect(self.set_progress_message)

		self.found_matches.connect(self.show_found_matches)

	def show_found_matches(self, matches):
		self.results_container.table.append_rows(matches)

	def close(self):
		self.main_window.search_views.pop(self.search_str)
		super().close()


class MainWindow(window.MainWindow):

	def __init__(self, opts: GuiOptions):
		window.MainWindow.__init__(self, "OVL Tool", opts=opts)
		self.setAcceptDrops(True)
		self.suppress_popups = False

		self.reporter = widgets.Reporter()
		self.ovl_data = OvlFile()
		self.ovl_data.reporter = self.reporter
		self.ovl_data.cfg = self.cfg
		self.temp_dir = tempfile.mkdtemp("-cobra")

		exts = " ".join([f"*{ext}" for ext in self.ovl_data.formats_dict.extractables])
		self.filter = f"Supported files ({exts})"

		self.file_widget = self.make_file_widget()

		self.ovl_game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False, changed_fn=self.game_changed)
		self.ovl_game_choice.setToolTip("Game version of current OVL")
		self.ovl_game_choice.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

		self.compression_choice = widgets.LabelCombo(
			"Compression", [c.name for c in Compression], editable=False, changed_fn=self.compression_changed,
			activated_fn=self.compression_touched_by_user)
		self.compression_choice.setToolTip("Compression of current OVL")
		self.compression_choice.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

		self.extract_types_choice = widgets.CheckableComboBox()
		self.extract_types_choice.addItems(self.ovl_data.formats_dict.extractables)
		self.extract_types_choice.setToolTip("Select file formats processed by batch tasks")

		self.ovl_manager = widgets.OvlManagerWidget(
			self,
			game_chosen_fn=self.set_ovl_game_choice_game,
			file_dbl_click_fn=self.open_clicked_file,
			search_content_fn=self.search_ovl_contents,
			actions={
				QtWidgets.QAction(widgets.get_icon("extract"), "Unpack All"): self.extract_all_batch,
				QtWidgets.QAction(widgets.get_icon("rename"), "Rename Files"): self.rename_batch,
				QtWidgets.QAction(widgets.get_icon("rename_contents"), "Rename Contents"): self.rename_contents_batch,
				})
		self.ovl_manager.set_selected_game()
		self.ovl_manager.game_choice.game_chosen(self.ovl_manager.game_choice.entry.currentText())

		# create the table
		self.files_container = widgets.SortableTable(
			["Name", "File Type"], self.ovl_data.formats_dict.ignore_types, ignore_drop_type="OVL", opt_hide=True,
			actions={
				QtWidgets.QAction(widgets.get_icon("extract"), "Extract Selected"): self.extract_selected,
			})
		# connect the interaction functions
		self.files_container.table.table_model.member_renamed.connect(self.rename_handle)
		self.files_container.table.files_dragged.connect(self.drag_files)
		self.files_container.table.files_dropped.connect(self.inject_files)
		self.files_container.table.file_selected_count.connect(self.update_file_counts)
		# self.files_container.table.file_selected.connect(self.show_dependencies)

		self.included_ovls_view = widgets.RelativePathCombo(self, self.file_widget)
		self.included_ovls_view.setToolTip(
			"These OVL files are loaded by the current OVL file, so their files are included")
		self.included_ovls_view.entries_changed.connect(self.update_includes)

		# toggles
		self.e_name_old = QtWidgets.QTextEdit("")
		self.e_name_old.setPlaceholderText("Find")
		self.e_name_old.setToolTip("Old strings - one item per line, case-sensitive")
		self.e_name_new = QtWidgets.QTextEdit("")
		self.e_name_new.setPlaceholderText("Replace")
		self.e_name_new.setToolTip("New strings - one item per line, case-sensitive")
		self.e_name_new.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
		self.e_name_old.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
		self.e_name_old.setTabChangesFocus(True)
		self.e_name_new.setTabChangesFocus(True)

		grid = QtWidgets.QGridLayout()
		grid.addWidget(self.e_name_old, 0, 0, 3, 1)
		grid.addWidget(self.e_name_new, 0, 1, 3, 1)
		grid.addWidget(self.ovl_game_choice, 0, 2)
		grid.addWidget(self.compression_choice, 1, 2)
		grid.addWidget(self.extract_types_choice, 2, 2)

		right_frame = widgets.pack_in_box(
			self.file_widget,
			self.files_container,
			self.included_ovls_view,
			margins=(3, 0, 0, 0)
		)
		self.create_main_splitter(grid, self.ovl_manager, right_frame)

		# Setup Menus
		self.build_menus({
			widgets.FILE_MENU: [
				MenuItem("New", self.file_widget.ask_open_dir, shortcut="CTRL+N", icon="new"),
				*self.file_menu_items,
			],
			widgets.EDIT_MENU: [
				MenuItem("Unpack All", self.extract_all, shortcut="CTRL+U", icon="extract"),
				MenuItem("Inject", self.inject_ask, shortcut="CTRL+I", icon="inject"),
				MenuItem("Remove Selected", self.remove, shortcut="DEL", icon="remove"),
				SeparatorMenuItem(),
				MenuItem("Rename Files", self.rename, shortcut="CTRL+R", icon="rename"),
				MenuItem("Rename Contents", self.rename_contents, shortcut="CTRL+SHIFT+R", icon="rename_contents"),
				MenuItem("Rename Both", self.rename_both, shortcut="CTRL+ALT+R"),
				SeparatorMenuItem(),
				MenuItem("Load Included OVL List", self.load_included_ovls),
				MenuItem("Export Included OVL List", self.save_included_ovls),
				SeparatorMenuItem(),
				MenuItem("Preferences", self.open_cfg_editor, shortcut="CTRL+,", icon="preferences"),
			],
			widgets.VIEW_MENU: self.view_menu_items,
			widgets.UTIL_MENU: [
				MenuItem("Open Tools Dir", self.open_tools_dir, icon="home"),
				MenuItem("Export File List", self.save_file_list),
				MenuItem("Compare with other OVL", self.compare_ovls, icon="compare"),
				# --- Dev Tools Submenu ---
				SubMenuItem("Dev Tools",
					items=[
						MenuItem("Inspect MS2", self.inspect_models, icon="ms2"),
						MenuItem("Inspect FGM", self.walker_fgm, icon="fgm"),
						MenuItem("Inspect MANIS", self.walker_manis, icon="manis"),
						MenuItem("Inspect TEX", self.walker_tex, icon="tex"),
						MenuItem("Generate Audio Events", self.walker_audio, icon="bnk"),
						MenuItem("Generate Hash Table", self.walker_hash),
						MenuItem("Dump Debug Data", self.dump_debug_data, icon="dump_debug"),
					]
				),
			],
			widgets.HELP_MENU: self.help_menu_items,
		})

		self.file_info = QtWidgets.QLabel(self)
		
		self.finfo_sep = QtWidgets.QFrame(self)
		self.finfo_sep.setFrameStyle(QtWidgets.QFrame.Shape.VLine)
		self.finfo_sep.setStyleSheet("color: #777;")
		self.finfo_sep.setMaximumHeight(15)
		self.finfo_sep.hide()

		self.status_bar.insertPermanentWidget(2, self.finfo_sep)
		self.status_bar.insertPermanentWidget(3, self.file_info)

		self.search_views = {}
		# do these at the end to make sure their requirements have been initialized
		reporter = self.ovl_data.reporter
		reporter.files_list.connect(self.update_files_ui)
		reporter.included_ovls_list.connect(self.included_ovls_view.set_data)
		reporter.warning_msg.connect(self.notify_user)
		reporter.progress_percentage.connect(self.set_progress)
		reporter.progress_total.connect(self.set_progress_total)
		reporter.success_msg.connect(self.set_progress_message)
		reporter.current_action.connect(self.set_progress_message)
		self.run_in_threadpool(self.ovl_data.load_hash_table)
		self.preferences_widget = None

	def open_cfg_editor(self):
		self.preferences_widget = window.ConfigWindow(self)
		self.preferences_widget.setWindowTitle(f"Preferences")
		self.preferences_widget.show()

	def abs_path_from_row(self, row_data):
		start_dir = self.ovl_manager.dirs.get_root()
		full_path = os.path.join(start_dir, row_data[2])
		return PurePath(full_path).as_posix()

	def search_result_open(self, row_data):
		ovl_path = self.abs_path_from_row(row_data)
		if self.files_container.table.isEnabled():
			self.file_widget.open_file(ovl_path)
		else:
			logging.warning(f"Wait with opening {ovl_path} until the previous ovl has loaded")

	def search_result_show(self, row_data):
		ovl_path = self.abs_path_from_row(row_data)
		logging.info(f"Showing {ovl_path} in Explorer")
		os.startfile(os.path.dirname(ovl_path))

	@staticmethod
	def run_action(*args):
		print("action", args)

	def close(self) -> bool:
		try:
			shutil.rmtree(self.temp_dir)
		except FileNotFoundError:
			pass
		for results_container in list(self.search_views.values()):
			results_container.close()
		return super().close()

	def get_file_count_text(self):
		return f"{self.files_container.table.table_model.rowCount()} items"
	
	def update_file_counts(self, selected_count=0):
		text = self.get_file_count_text()
		if selected_count > 0:
			text = f"{selected_count} / {text} selected"
		self.file_info.setText(text)
		self.finfo_sep.show()

	def search_ovl_contents(self, search_str):
		search_str = search_str.lower()
		if search_str not in self.search_views:
			results_window = SearchWindow(self, search_str)
			results_window.results_container.table.file_double_clicked.connect(self.search_result_open)
			results_window.show()

			self.search_views[search_str] = results_window

			start_dir = self.ovl_manager.dirs.get_root()
			# thread this to immediately show the window
			self.run_in_threadpool(walker.search_for_files_in_ovls, (), results_window, start_dir, search_str)
		else:
			logging.warning(f"Search results for '{search_str}' are still open")


	def notify_user(self, msg_list):
		msg = msg_list[0]
		details = msg_list[1] if len(msg_list) > 1 else None
		if self.suppress_popups:
			logging.warning(f"Dragging encountered an error: {details}")
		else:
			self.showwarning(msg, details=details)

	def enable_gui_options(self, enable=True):
		self.compression_choice.setEnabled(enable)
		self.ovl_manager.game_choice.setEnabled(enable)
		self.ovl_manager.dirs.setEnabled(enable)
		self.ovl_manager.search.setEnabled(enable)
		self.file_widget.setEnabled(enable)
		self.file_widget.icon.setEnabled(enable)
		self.file_widget.entry.setEnabled(enable)
		self.files_container.table.setEnabled(enable)
		self.ovl_game_choice.setEnabled(enable)
		# just disable all actions
		for action_name in self.actions.keys():
			self.actions[action_name.lower()].setEnabled(enable)

	def dump_debug_data(self, ):
		self.run_in_threadpool(self.ovl_data.dump_debug_data, (), self.files_container.table.get_selected_files())

	def compare_ovls(self):
		selected_file_names = self.files_container.table.get_selected_files()
		if not selected_file_names:
			self.showwarning("Please select files to compare first")
			return
		if self.is_open_ovl():
			filepath = self.file_widget.get_open_file_name(f'Open OVL to compare with')
			if filepath:
				commands = {"game": self.ovl_game_choice.entry.currentText()}
				other_ovl_data = OvlFile()
				try:
					other_ovl_data.load_hash_table()
					other_ovl_data.load(filepath, commands)
					for file_name in selected_file_names:
						try:
							loader_a = self.ovl_data.loaders[file_name]
							loader_b = other_ovl_data.loaders[file_name]
							if loader_a == loader_b:
								logging.info(f"'{file_name}' is the same")
							else:
								logging.warning(f"'{file_name}' differs")
						except:
							logging.exception(f"Could not compare '{file_name}'")
				except:
					logging.exception(f"Could not compare '{filepath}'")

	def set_ovl_game_choice_game(self, game=None):
		# logging.debug(f"Setting OVL game to {game}")
		self.ovl_game_choice.entry.setText(game)

	def handle_path(self, save_over=True, batch=False):
		if batch:
			with self.no_popups():
				with self.log_level_override("WARNING"):
					for ovl_path in modules.formats.shared.walk_type(self.walk_root(), extension=".ovl"):
						# open ovl file
						self.open(ovl_path)
						# todo clear logger after each file, using self.file_widget.open_file would do that
						#      however the open_file signal and thus ovl loading is processed later than the yield
						# self.file_widget.open_file(ovl_path)
						# process each
						yield self.ovl_data
						if save_over:
							self.save(ovl_path)
		# just the one that's currently open, do not save over
		elif self.is_open_ovl():
			yield self.ovl_data

	def open_clicked_file(self, filepath: str):
		# handle double clicked file paths
		try:
			if filepath.lower().endswith(".ovl"):
				self.file_widget.open_file(filepath)
		except:
			self.handle_error("Clicked dir failed, see log!")

	@staticmethod
	def open_tools_dir():
		os.startfile(os.path.abspath(os.path.dirname(__file__)))

	@contextlib.contextmanager
	def no_popups(self):
		self.suppress_popups = True
		yield
		self.suppress_popups = False

	def drag_files(self, file_names):
		# logging.debug(f"Dragging {file_names}")
		with self.no_popups():
			out_paths = self.ovl_data.get_extract_paths(self.temp_dir, only_names=file_names)
			out_paths = self.handle_flattened_folders(out_paths, self.temp_dir)
			def extract_callback():
				try:
					self.ovl_data.extract(self.temp_dir, only_names=file_names)
				except:
					self.handle_error("Dragging failed, see log!")
			if out_paths:
				# set paths to mime
				mime = DelayedMimeData()
				mime.setUrls([QtCore.QUrl.fromLocalFile(path) for path in out_paths])
				mime.add_callback(extract_callback)
				drag = QtGui.QDrag(self)
				drag.setMimeData(mime)
				drag.exec_()

	def handle_flattened_folders(self, out_paths, temp_dir):
		"""Takes list of file paths and replaces any folders containing sub-paths in temp_dir with their relative base folder so that the subfolder is returned instead of the loose files"""
		rel_out_paths = set()
		for out_path in out_paths:
			# make out_paths relative to output folder
			rel_path = PurePath(os.path.relpath(out_path, temp_dir))
			# get the first dir in the path, files are nested inside
			if len(rel_path.parents) > 1:
				# parents are reversed, so this gets the first subfolder ['components/render', 'components', '.']
				rel_out_paths.add(str(rel_path.parents[-2]))
			# no dir, just a file itself
			else:
				rel_out_paths.add(str(rel_path))
		# join the relative paths back to temp_dir
		return set(os.path.join(temp_dir, p) for p in rel_out_paths)

	def rename_handle(self, old_name, new_name):
		"""this manages the renaming of a single entry"""
		# force new name to be lowercase
		names = {(old_name, new_name.lower()), }
		try:
			self.ovl_data.rename(names)
			self.set_dirty()
		except:
			self.handle_error("Renaming failed, see log!")

	def game_changed(self, game: Optional[str] = None):
		"""Updates game for self.ovl_data from current GUI selection"""
		if game is None:
			game = self.ovl_game_choice.entry.currentText()
		logging.info(f"Setting OVL version to {game}")
		self.ovl_data.game = game

	def compression_changed(self, compression: str):
		compression_value = Compression[compression]
		self.ovl_data.user_version.compression = compression_value
		# self.set_dirty()
		
	def compression_touched_by_user(self, compression: str):
		# emitted regardless of change - no way to compare to the old value
		self.set_dirty()

	def show_dependencies(self, file_index):
		# just an example of what can be done when something is selected
		file_entry = self.ovl_data.files[file_index]

	def print_debug_ovl(self):
		if self.cfg.get("debug_mode", False):
			logging.debug(f"Header '{self.ovl_data.name}'", extra={'details': self.ovl_data})
			for archive in self.ovl_data.archives:
				if hasattr(archive, "content"):
					logging.debug(f"Archive '{archive.name if archive.name else ''}'", extra={'details': archive.content})

	def open(self, filepath):
		if filepath:
			commands = {"game": self.ovl_game_choice.entry.currentText(), "update_aux": self.cfg.get("update_aux")}
			self.set_clean()
			# logging.debug(f"Loading threaded {threaded}")
			logging.debug(f"Loading self.suppress_popups {self.suppress_popups}")
			if not self.suppress_popups:
				self.ovl_manager.dirs.set_selected_path(filepath)
				self.run_in_threadpool(self.ovl_data.load, (self.set_clean, self.print_debug_ovl), filepath, commands)
			else:
				try:
					self.ovl_data.load(filepath, commands)
					self.print_debug_ovl()
				except:
					self.handle_error("OVL loading failed, see log!")

	def open_dir(self, dirpath: str) -> None:
		self.create_ovl(dirpath)
		self.set_dirty()

	def choices_update(self):
		self.set_ovl_game_choice_game(self.ovl_data.game)
		self.compression_choice.entry.setText(self.ovl_data.user_version.compression.name)

	def create_ovl(self, ovl_dir):
		# clear the ovl
		self.ovl_data.clear()
		self.game_changed()
		try:
			self.ovl_data.create(ovl_dir)
		except:
			self.handle_error("Creating OVL failed, see log!")

	def is_open_ovl(self):
		if self.file_widget.filename or self.file_widget.dirty:
			return True
		else:
			self.showwarning("You must open an OVL file first!")

	def update_files_ui(self, f_list):
		"""Give table widget new files"""
		with self.reporter.log_duration(f"Loading {len(f_list)} files into GUI"):
			self.files_container.set_data(f_list)
			self.update_file_counts()

	def update_includes(self, includes):
		self.ovl_data.included_ovl_names = includes
		self.set_dirty()

	def run_current_game(self):
		if self.cfg.get("play_on_saving", False):
			self.ovl_manager.run_selected_game()

	def save(self, filepath):
		"""Saves ovl to file_widget.filepath, clears dirty flag"""
		commands = {"update_aux" : self.cfg.get("update_aux")}
		if not self.suppress_popups:
			self.run_in_threadpool(self.ovl_data.save, (self.set_clean, self.run_current_game), filepath, commands=commands)
		else:
			try:
				self.ovl_data.save(filepath, commands=commands)
				self.set_clean()
			except:
				self.handle_error("Saving OVL failed, see log!")

	def extract_all(self):
		if self.is_open_ovl():
			self.extract_all_ask(batch=False)

	def extract_selected(self, cb=None):
		if self.is_open_ovl():
			only_names = self.files_container.table.get_selected_files()
			self.extract_all_ask(batch=False, only_names=only_names)

	def extract_all_ask(self, batch=False, only_names=()):
		out_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg.get("dir_extract", "C://"), )
		if out_dir:
			self.cfg["dir_extract"] = out_dir
			self.run_in_threadpool(self._extract, (), out_dir, batch, only_names)

	def extract_all_batch(self):
		self.extract_all_ask(batch=True)

	def _extract(self, out_dir, batch=False, only_names=()):
		_out_dir = out_dir
		# check using a filter to extract mimes
		only_types = self.extract_types_choice.currentData()
		selected_dir = self.walk_root()
		for ovl in self.handle_path(save_over=False, batch=batch):
			# for bulk extraction, add the ovl basename to the path to avoid overwriting
			if batch:
				rel_p = os.path.relpath(ovl.path_no_ext, start=selected_dir)
				out_dir = os.path.join(_out_dir, rel_p)
			ovl.extract(out_dir, only_names=only_names, only_types=only_types)

	def inject_ask(self):
		files = QtWidgets.QFileDialog.getOpenFileNames(
			self, 'Inject files', self.cfg.get("dir_inject", "C://"), self.filter)[0]
		self.inject_files(files)

	def inject_files(self, files):
		"""Tries to inject files into self.ovl_data"""
		if files:
			# any path added from the gui is necessarily at the same folder level, dirs need to be expanded
			common_root_dir = os.path.dirname(files[0])
			self.cfg["dir_inject"] = common_root_dir
			self.set_dirty()
			self.run_in_threadpool(self.ovl_data.add_files, (), files, common_root_dir)
		# the gui is updated from the signal ovl.files_list emitted from add_files

	def get_replace_strings(self):
		try:
			newline = "\n"
			old = self.e_name_old.toPlainText()
			new = self.e_name_new.toPlainText()
			# make sure at least one is non-empty
			if not (old or new):
				return
			old = old.split(newline)
			new = new.split(newline)
			if len(old) != len(new):
				self.showwarning(f"Old {len(old)} and new {len(new)} must have the same amount of lines!")
			return set(zip(old, new))
		except:
			self.handle_error("Getting replace strings failed, see log!")

	def rename(self, batch=False):
		names = self.get_replace_strings()
		try:
			if names:
				for ovl in self.handle_path():
					ovl.rename(names)
					if not batch:
						self.set_dirty()
		except:
			self.handle_error("Renaming failed, see log!")

	def rename_batch(self):
		names = self.get_replace_strings()
		if names:
			try:
				for ovl in self.handle_path(batch=True):
					ovl.rename(names)
			except:
				self.handle_error("Renaming failed, see log!")

	def rename_contents(self):
		names = self.get_replace_strings()
		if names:
			# we are operating only on the current ovl, so check selection state
			only_files = self.files_container.table.get_selected_files()
			for ovl in self.handle_path():
				ovl.rename_contents(names, only_files)
				self.set_dirty()
				# file names don't change, so no need to update gui

	def rename_contents_batch(self):
		names = self.get_replace_strings()
		if names:
			only_files = ()
			for ovl in self.handle_path(batch=True):
				ovl.rename_contents(names, only_files)

	def rename_both(self):
		self.rename_contents()
		self.rename()

	def save_file_list(self):
		"""Save the OVL file list to disk"""
		if self.is_open_ovl():
			filelist_src = QtWidgets.QFileDialog.getSaveFileName(
				self, 'Save File List',
				os.path.join(self.cfg.get("dir_extract", "C://"), self.file_widget.filename + ".files.txt"),
				"Txt file (*.txt)", )[0]
			if filelist_src:
				try:
					file_names = self.files_container.table.get_files()
					with open(filelist_src, 'w') as f:
						f.write("\n".join(file_names))

					self.set_progress_message("Saved file list")
				except:
					self.handle_error("Writing file list failed, see log!")

	def save_included_ovls(self):
		"""Save the OVL include list to disk"""
		if self.is_open_ovl():
			filepath = QtWidgets.QFileDialog.getSaveFileName(
				self, 'Save ovls.include', os.path.join(self.cfg.get("dir_extract", "C://"), "ovls.include"),
				"Include file (*.include)", )[0]
			if filepath:
				try:
					self.ovl_data.save_included_ovls(filepath)
					self.set_progress_message("Saved included OVLs")
				except:
					self.handle_error("Writing included OVLs failed, see log!")

	def load_included_ovls(self):
		filepath = QtWidgets.QFileDialog.getOpenFileName(
			self, "Open ovls.include", os.path.join(self.cfg.get("dir_inject", "C://"), "ovls.include"),
			"Include file (*.include)", )[0]
		if filepath:
			try:
				self.ovl_data.load_included_ovls(filepath)
				self.set_dirty()
				self.set_progress_message("Loaded included OVLs")
			except:
				self.handle_error("Opening included OVLs failed, see log!")

	def remove(self):
		if self.is_open_ovl() and self.files_container.table.hasFocus():
			selected_file_names = self.files_container.table.get_selected_files()
			if selected_file_names:
				try:
					self.ovl_data.remove(selected_file_names)
					self.set_dirty()
				except:
					self.handle_error("Removing file from OVL failed, see log!")

	def ask_game_root(self):
		return QtWidgets.QFileDialog.getExistingDirectory(
			self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))

	def game_root(self):
		root_path = self.ovl_manager.dirs.get_root()
		if root_path.endswith("ovldata"):
			return root_path
		return ""
	
	def walk_root(self):
		"""Choose a reasonable root path for walking the ovldata folder structure"""
		selected_path = self.ovl_manager.dirs.get_selected_path()
		# take sub-folders to allow for partial walking
		if os.path.isdir(selected_path):
			if PurePath(self.game_root()) in PurePath(selected_path).parents:
				return selected_path
		# fall back on game root dir
		return self.game_root()

	def walker_audio(self, ):
		self.run_in_threadpool(walker.get_audio_names, (), self, self.game_root())

	def walker_hash(self, ):
		self.run_in_threadpool(walker.generate_hash_table, (), self, self.game_root())

	def walker_fgm(self, ):
		self.change_log_speed.emit("slow")
		dialog = window.WalkerDialog(self, "Inspect FGMs", self.walk_root())
		chk_full_report = widgets.QCheckBox("Full Report")
		chk_full_report.setChecked(self.walk_root() == self.game_root())
		dialog.options.addWidget(chk_full_report)
		if dialog.exec():
			self.run_in_threadpool(
				walker.get_fgm_values, (), self, self.game_root(),
				dir_walk=dialog.dir_walk, walk_ovls=dialog.walk_ovls,
				official_only=dialog.official_only, full_report=chk_full_report.isChecked()
			)

	def walker_manis(self, ):
		self.change_log_speed.emit("slow")
		dialog = window.WalkerDialog(self, "Inspect Manis", self.walk_root())
		if dialog.exec():
			self.run_in_threadpool(
				walker.get_manis_values, (), self, dir_walk=dialog.dir_walk,
				walk_ovls=dialog.walk_ovls, official_only=dialog.official_only
			)

	def walker_tex(self, ):
		self.change_log_speed.emit("slow")
		dialog = window.WalkerDialog(self, "Inspect Tex", self.walk_root())
		if dialog.exec():
			self.run_in_threadpool(
				walker.get_tex_values, (), self, dir_walk=dialog.dir_walk,
				walk_ovls=dialog.walk_ovls, official_only=dialog.official_only
			)

	def inspect_models(self):
		self.change_log_speed.emit("slow")
		dialog = window.WalkerDialog(self, "Inspect Models", self.walk_root())
		if dialog.exec():
			self.run_in_threadpool(
				walker.bulk_test_models, (), self, self.game_root(), dir_walk=dialog.dir_walk,
				walk_ovls=dialog.walk_ovls, official_only=dialog.official_only
			)


if __name__ == '__main__':
	from gui import startup
	#from gui.tools.qt_debug import install_signal_tracer, install_qtimer_tracer
	#install_signal_tracer(ignore=["LogModel.number_fetched", "QTimer.timeout"])
	#install_qtimer_tracer(ignore=["LogView.startFetches", "_handler_poll_timer"])

	startup(MainWindow,
		GuiOptions(
			log_name="ovl_tool_gui",
			size=(800, 600),
			check_update=False  # Check update happens at top now
		)
	)
