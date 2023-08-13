import os
import shutil
import sys
import logging
import tempfile
from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from ovl_util.logs import HtmlFormatter, AnsiFormatter, get_stdout_handler
from gui.widgets import Reporter
from modules import walker
from root_path import root_dir
from generated.formats.ovl import games, get_game, set_game, OvlFile
from generated.formats.ovl_base.enums.Compression import Compression
from PyQt5 import QtWidgets, QtGui, QtCore
from typing import Any, Optional

class MainWindow(widgets.MainWindow):

	def __init__(self, opts: GuiOptions):
		widgets.MainWindow.__init__(self, "OVL Tool", opts=opts)
		self.resize(800, 600)
		self.setAcceptDrops(True)

		self.reporter = Reporter()
		self.ovl_data = OvlFile()
		self.ovl_data.reporter = self.reporter

		exts = " ".join([f"*{ext}" for ext in self.ovl_data.formats_dict.extractables])
		self.filter = f"Supported files ({exts})"

		self.file_widget = self.make_file_widget()

		self.game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False, changed_fn=self.game_changed)

		self.compression_choice = widgets.LabelCombo("Compression", [c.name for c in Compression], editable=False, changed_fn=self.compression_changed)

		self.log_level_choice = widgets.LabelCombo("Log Level", ("DEBUG", "INFO", "WARNING", "ERROR"), editable=False, changed_fn=self.log_level_changed)
		self.log_level_choice.setToolTip("Defines how much information is shown in the console window")

		if "games" not in self.cfg:
			self.cfg["games"] = {}
		self.installed_games = widgets.GamesWidget(self, game_chosen_fn=self.populate_game, file_dbl_click_fn=self.open_clicked_file)

		# create the table
		self.files_container = widgets.SortableTable(("Name", "File Type"), self.ovl_data.formats_dict.ignore_types,
													 ignore_drop_type="OVL", opt_hide=True)
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

		left_frame = QtWidgets.QWidget()
		hbox = QtWidgets.QVBoxLayout()
		hbox.addWidget(self.installed_games)
		hbox.addWidget(self.installed_games.dirs)
		left_frame.setLayout(hbox)

		right_frame = QtWidgets.QWidget()
		hbox = QtWidgets.QVBoxLayout()
		hbox.addWidget(self.file_widget)
		hbox.addWidget(self.files_container)
		hbox.addWidget(self.included_ovls_view)
		right_frame.setLayout(hbox)

		self.splitter_lr = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
		self.splitter_lr.addWidget(left_frame)
		self.splitter_lr.addWidget(right_frame)
		self.splitter_lr.setSizes([200, 400])
		self.splitter_lr.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.splitter_lr.setContentsMargins(0, 0, 0, 0)

		# toggles
		self.t_do_debug = QtWidgets.QCheckBox("Debug Mode")
		self.t_do_debug.setToolTip(
			"Enables debugging when checked:\n"
			" - OVLs open slower to verify structs don't miss pointers\n"
			" - temporary files are kept in extract folder\n"
			" - debug info is added to XML-like extracts")
		self.t_do_debug.setChecked(False)
		self.t_do_debug.setVisible(self.dev_mode)
		self.t_do_debug.clicked.connect(self.do_debug_changed)

		self.t_in_folder = QtWidgets.QCheckBox("Process Folder")
		self.t_in_folder.setToolTip("Runs commands on all OVLs of current folder")
		self.t_in_folder.setChecked(False)

		self.extract_types_combo = widgets.CheckableComboBox()
		self.extract_types_combo.addItems(self.ovl_data.formats_dict.extractables)
		self.extract_types_combo.setToolTip("Select file formats processed by batch tasks")

		self.t_mesh_ovl = QtWidgets.QCheckBox("Mesh OVL Mode")
		self.t_mesh_ovl.setToolTip("Renames only MS2, MDL2 and MOTIONGRAPH files.")
		self.t_mesh_ovl.setChecked(False)

		self.e_name_old = QtWidgets.QTextEdit("")
		self.e_name_old.setPlaceholderText("Find")
		self.e_name_old.setToolTip("Old strings - one item per line")
		self.e_name_new = QtWidgets.QTextEdit("")
		self.e_name_new.setPlaceholderText("Replace")
		self.e_name_new.setToolTip("New strings - one item per line")
		self.e_name_old.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
		self.e_name_old.setTabChangesFocus(True)
		self.e_name_new.setTabChangesFocus(True)

		grid = QtWidgets.QGridLayout()
		grid.addWidget(self.e_name_old, 0, 0, 4, 1)
		grid.addWidget(self.e_name_new, 0, 1, 4, 1)

		grid.addWidget(self.t_mesh_ovl, 0, 3)
		grid.addWidget(self.t_in_folder, 1, 3)
		grid.addWidget(self.t_do_debug, 2, 3)

		grid.addWidget(self.game_choice, 0, 4)
		grid.addWidget(self.compression_choice, 1, 4)
		grid.addWidget(self.log_level_choice, 2, 4)
		grid.addWidget(self.extract_types_combo, 3, 3, 1, 2)

		self.stdout_handler = get_stdout_handler("ovl_tool_gui") # self.log_name not set until after init
		# log to text box
		self.gui_log_handler = widgets.TextEditLogger(self)
		self.gui_log_handler.setFormatter(HtmlFormatter('%(levelname)s | %(message)s'))
		self.gui_log_handler.setLevel(logging.INFO)
		logging.getLogger().addHandler(self.gui_log_handler)

		self.splitter_tb = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
		self.splitter_tb.addWidget(self.splitter_lr)
		self.splitter_tb.addWidget(self.gui_log_handler.widget)
		self.splitter_tb.setSizes([600, 200])
		self.splitter_tb.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.splitter_tb.setStyleSheet(R"""
			QSplitter::handle:vertical {
				padding: 0px 0px 4px 0px;
			}
		""")

		box = QtWidgets.QVBoxLayout()
		box.addLayout(grid)
		box.addWidget(self.splitter_tb, 3)

		self.central_widget.setLayout(box)

		main_menu = self.menu_bar
		file_menu = main_menu.addMenu('File')
		edit_menu = main_menu.addMenu('Edit')
		util_menu = main_menu.addMenu('Util')
		help_menu = main_menu.addMenu('Help')
		button_data = (
			(file_menu, "New", self.file_widget.ask_open_dir, "CTRL+N", "new"),
			(file_menu, "Open", self.file_widget.ask_open, "CTRL+O", "dir"),
			(file_menu, "Save", self.file_widget.ask_save, "CTRL+S", "save"),
			(file_menu, "Save As", self.file_widget.ask_save_as, "CTRL+SHIFT+S", "save"),
			(file_menu, "Exit", self.close, "", "exit"),
			(edit_menu, "Unpack All", self.extract_all, "CTRL+U", "extract"),
			(edit_menu, "Inject", self.inject_ask, "CTRL+I", "inject"),
			(edit_menu, "Rename", self.rename, "CTRL+R", ""),
			(edit_menu, "Rename Contents", self.rename_contents, "CTRL+SHIFT+R", ""),
			(edit_menu, "Rename Both", self.rename_both, "CTRL+ALT+R", ""),
			(edit_menu, "Remove Selected", self.remove, "DEL", ""),
			(edit_menu, "Load included ovl list", self.load_included_ovls, "", ""),
			(edit_menu, "Export included ovl list", self.save_included_ovls, "", ""),
			(util_menu, "Inspect Models", self.inspect_models, "", "", True),
			(util_menu, "Inspect FGMs", self.walker_fgm, "", "", True),
			(util_menu, "Inspect Manis", self.walker_manis, "", "", True),
			(util_menu, "Generate Hash Table", self.walker_hash, "", ""),
			(util_menu, "Dump Debug Data", self.dump_debug_data, "", "dump_debug", True),
			(util_menu, "Open Tools Dir", self.open_tools_dir, "", "home"),
			(util_menu, "Export File List", self.save_file_list, "", ""),
			(util_menu, "Compare with other OVL", self.compare_ovls, "", ""),
			(help_menu, "Report Bug", self.report_bug, "", "report"),
			(help_menu, "Documentation", self.online_support, "", "manual"))
		self.add_to_menu(button_data)

		# add checkbox to extract from ovls for the diff walkers
		self.t_walk_ovl = QtWidgets.QAction("Walker extracts OVLs")
		self.t_walk_ovl.setToolTip("Extract from OVLS when doing bulk operations: fgm or ms2.")
		self.t_walk_ovl.setCheckable(True)
		self.t_walk_ovl.setChecked(False)
		self.t_walk_ovl.setVisible(self.dev_mode)

		# add checkbox to extract from ovls for the diff walkers
		self.t_logger = QtWidgets.QAction("Show log console")
		self.t_logger.setToolTip("Show/hide the dev log console.")
		self.t_logger.setCheckable(True)
		logger_show = self.cfg.get("show_logger", True)
		self.t_logger.setChecked(logger_show)
		self.t_logger.triggered.connect(self.logger_show_triggered)
		self.logger_show_triggered()

		separator_action = self.actions['generate hash table']
		# we are not adding this to the action list, shall we?
		util_menu.insertAction(separator_action, self.t_walk_ovl)
		# TODO: This is left for now, but the trigger logic has been
		# update for the splitter
		util_menu.insertAction(separator_action, self.t_logger)
		util_menu.insertSeparator(separator_action)

		self.file_info = QtWidgets.QLabel(self)
		
		vline = QtWidgets.QFrame(self)
		vline.setFrameStyle(QtWidgets.QFrame.Shape.VLine)
		vline.setStyleSheet("color: #777;")
		vline.setMaximumHeight(15)

		self.status_bar.addPermanentWidget(vline)
		self.status_bar.addPermanentWidget(self.file_info)

		self.check_version()
		# run once here to make sure we catch the default game
		self.populate_game()
		self.game_changed()

		log_level = self.cfg.get("logger_level", "INFO")
		self.log_level_choice.entry.setText(log_level)
		self.log_level_changed(log_level)

		# do these at the end to make sure their requirements have been initialized
		reporter = self.ovl_data.reporter
		reporter.files_list.connect(self.update_files_ui)
		reporter.included_ovls_list.connect(self.included_ovls_view.set_data)
		reporter.warning_msg.connect(self.notify_user)
		reporter.progress_percentage.connect(self.set_progress)
		reporter.current_action.connect(self.set_msg_temporarily)
		self.run_threaded(self.ovl_data.load_hash_table)

	def get_file_count_text(self):
		return f"{self.files_container.table.table_model.rowCount()} items"
	
	def update_file_counts(self, selected_count=0):
		if selected_count == 0:
			self.file_info.setText(self.get_file_count_text())
		else:
			self.file_info.setText(f"{selected_count} / {self.get_file_count_text()} selected")

	def do_debug_changed(self, do_debug):
		self.ovl_data.do_debug = do_debug

	def notify_user(self, msg_list):
		msg = msg_list[0]
		details = msg_list[1] if len(msg_list) > 1 else None
		self.showwarning(msg, details=details)

	def logger_show_triggered(self):
		show = self.t_logger.isChecked()
		self.cfg["show_logger"] = show
		if show:
			self.splitter_tb.setSizes([self.splitter_lr.height(), 120])
		else:
			self.splitter_tb.setSizes([800, 0])

	def enable_gui_options(self, enable=True):
		self.t_in_folder.setEnabled(enable)
		self.t_do_debug.setEnabled(enable)
		self.t_mesh_ovl.setEnabled(enable)
		self.t_walk_ovl.setEnabled(enable)
		self.compression_choice.setEnabled(enable)
		self.game_choice.setEnabled(enable)
		# just disable all actions
		for action_name in self.actions.keys():
			self.actions[action_name.lower()].setEnabled(enable)

	def dump_debug_data(self, ):
		self.ovl_data.dump_debug_data()

	def compare_ovls(self):
		selected_file_names = self.files_container.table.get_selected_files()
		if not selected_file_names:
			self.showwarning("Please select files to compare first")
			return
		if self.is_open_ovl():
			filepath = QtWidgets.QFileDialog.getOpenFileName(
				self, "Open OVL to compare with", self.cfg.get(f"dir_ovls_in", "C://"), f"OVL files (*.ovl)")[0]
			if filepath:
				other_ovl_data = OvlFile()
				other_ovl_data.load_hash_table()
				other_ovl_data.load(filepath)
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

	def populate_game(self, current_game=None):
		if current_game is None:
			current_game = self.cfg.get("current_game")
		logging.debug(f"Setting Current Game to {current_game}")
		if self.installed_games.set_selected_game(current_game):
			self.game_choice.entry.setText(current_game)

	def handle_path(self, save_over=True):
		# get path
		if self.t_in_folder.isChecked():
			selected_dir = self.installed_games.get_selected_dir()
			if selected_dir:
				# walk path
				for ovl_path in walker.walk_type(selected_dir, extension=".ovl"):
					# open ovl file
					self.file_widget.set_file_path(ovl_path)
					self.open(ovl_path, threaded=False)
					# process each
					yield self.ovl_data
					if save_over:
						self.save(ovl_path)
			else:
				self.showwarning("Select a root directory!")
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
		os.startfile(root_dir)

	def drag_files(self, file_names):
		logging.info(f"Dragging {file_names}")
		drag = QtGui.QDrag(self)
		data = QtCore.QMimeData()
		temp_dir = tempfile.mkdtemp("-cobra")
		try:
			out_paths = self.ovl_data.extract(temp_dir, only_names=file_names)
			if out_paths:
				data.setUrls([QtCore.QUrl.fromLocalFile(path) for path in out_paths])
				drag.setMimeData(data)
				drag.exec_()
		except:
			self.handle_error("Dragging failed, see log!")
		shutil.rmtree(temp_dir)

	def rename_handle(self, old_name, new_name):
		"""this manages the renaming of a single entry"""
		# force new name to be lowercase
		names = [(old_name, new_name.lower()), ]
		self.ovl_data.rename(names)
		self.set_file_modified(True)

	def game_changed(self, game: Optional[str] = None):
		if game is None:
			game = self.game_choice.entry.currentText()
		logging.info(f"Setting OVL context to {game}")
		set_game(self.ovl_data, game)

	def compression_changed(self, compression: str):
		compression_value = Compression[compression]
		self.ovl_data.user_version.compression = compression_value

	def log_level_changed(self, level: str):
		self.gui_log_handler.setLevel(level)
		if self.stdout_handler:
			self.stdout_handler.setLevel(level)
		self.cfg["logger_level"] = level

	def show_dependencies(self, file_index):
		# just an example of what can be done when something is selected
		file_entry = self.ovl_data.files[file_index]

	def open(self, filepath, threaded=True):
		if filepath:
			self.set_file_modified(False)
			logging.debug(f"Loading threaded {threaded}")
			if threaded:
				self.run_threaded(self.ovl_data.load, filepath)
			else:
				try:
					self.ovl_data.load(filepath)
				except:
					logging.debug(self.ovl_data)
					self.handle_error("OVL loading failed, see log!")

	def open_dir(self, dirpath: str) -> None:
		self.create_ovl(dirpath)
		self.set_file_modified(True)

	def choices_update(self):
		game = get_game(self.ovl_data)[0]
		self.game_choice.entry.setText(game.value)
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
		with self.reporter.log_duration(f"Loading {len(f_list)} files into gui"):
			self.files_container.set_data(f_list)
			self.update_file_counts()

	def update_includes(self, includes):
		self.ovl_data.included_ovl_names = includes

	def save(self, filepath):
		"""Saves ovl to file_widget.filepath, clears dirty flag"""
		try:
			self.ovl_data.save(filepath)
			self.set_file_modified(False)
			self.set_msg_temporarily(f"Saved {self.ovl_data.basename}")
		except:
			self.handle_error("Saving OVL failed, see log!")

	def extract_all(self):
		out_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder',
															 self.cfg.get("dir_extract", "C://"), )
		if out_dir:
			self.cfg["dir_extract"] = out_dir
			_out_dir = out_dir
			# check using a filter to extract mimes
			only_types = self.extract_types_combo.currentData()
			for ovl in self.handle_path(save_over=False):
				# for bulk extraction, add the ovl basename to the path to avoid overwriting
				if self.t_in_folder.isChecked():
					selected_dir = self.installed_games.get_selected_dir()
					rel_p = os.path.relpath(ovl.path_no_ext, start=selected_dir)
					out_dir = os.path.join(_out_dir, rel_p)
				ovl.extract(out_dir, only_types=only_types)

	def inject_ask(self):
		files = QtWidgets.QFileDialog.getOpenFileNames(
			self, 'Inject files', self.cfg.get("dir_inject", "C://"), self.filter)[0]
		self.inject_files(files)

	def inject_files(self, files):
		"""Tries to inject files into self.ovl_data"""
		if files:
			self.cfg["dir_inject"] = os.path.dirname(files[0])
			self.set_file_modified(True)
			# threaded injection seems to be fine now
			# self.ovl_data.add_files(files)
			self.run_threaded(self.ovl_data.add_files, files)
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
			return list(zip(old, new))
		except:
			self.handle_error("Getting replace strings failed, see log!")

	def rename(self):
		names = self.get_replace_strings()
		try:
			if names:
				for ovl in self.handle_path():
					ovl.rename(names, mesh_mode=self.t_mesh_ovl.isChecked())
					if not self.t_in_folder.isChecked():
						self.set_file_modified(True)
		except:
			self.handle_error("Renaming failed, see log!")

	def rename_contents(self):
		names = self.get_replace_strings()
		if names:
			if self.check_length(names):
				return
			# if we are operating only on the current ovl, check selection state
			if not self.t_in_folder.isChecked():
				only_files = self.files_container.table.get_selected_files()
			else:
				only_files = ()
			for ovl in self.handle_path():
				ovl.rename_contents(names, only_files)
				if not self.t_in_folder.isChecked():
					self.set_file_modified(True)
				# file names don't change, so no need to update gui

	def rename_both(self):
		self.rename_contents()
		self.rename()

	def save_file_list(self):
		"""Save the OVL file list to disk"""
		if self.is_open_ovl():
			filelist_src = QtWidgets.QFileDialog.getSaveFileName(
				self, 'Save File List',
				os.path.join(self.cfg.get("dir_ovls_out", "C://"), self.file_widget.filename + ".files.txt"),
				"Txt file (*.txt)", )[0]
			if filelist_src:
				try:
					file_names = self.files_container.table.get_files()
					with open(filelist_src, 'w') as f:
						f.write("\n".join(file_names))

					self.set_msg_temporarily("Saved file list")
				except:
					self.handle_error("Writing file list failed, see log!")

	def save_included_ovls(self):
		"""Save the OVL include list to disk"""
		if self.is_open_ovl():
			filepath = QtWidgets.QFileDialog.getSaveFileName(
				self, 'Save ovls.include', os.path.join(self.cfg.get("dir_ovls_out", "C://"), "ovls.include"),
				"Include file (*.include)", )[0]
			if filepath:
				try:
					self.ovl_data.save_included_ovls(filepath)
					self.set_msg_temporarily("Saved included OVLs")
				except:
					self.handle_error("Writing included OVLs failed, see log!")

	def load_included_ovls(self):
		filepath = QtWidgets.QFileDialog.getOpenFileName(
			self, "Open ovls.include", os.path.join(self.cfg.get("dir_ovls_out", "C://"), "ovls.include"),
				"Include file (*.include)", )[0]
		if filepath:
			try:
				self.ovl_data.load_included_ovls(filepath)
				self.set_file_modified(True)
				self.set_msg_temporarily("Loaded included OVLs")
			except:
				self.handle_error("Opening included OVLs failed, see log!")

	def remove(self):
		if self.is_open_ovl():
			selected_file_names = self.files_container.table.get_selected_files()
			# todo - might want to check self.files_container.hasFocus(), but does not seem to work!
			if selected_file_names:
				try:
					self.ovl_data.remove(selected_file_names)
					self.set_file_modified(True)
				except:
					self.handle_error("Removing file from OVL failed, see log!")

	def walker_hash(self, ):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(
			self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		self.run_threaded(walker.generate_hash_table, self, start_dir)
		self.set_msg_temporarily("Hashed")

	def walker_fgm(self, ):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(
			self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		self.run_threaded(walker.get_fgm_values, self, start_dir, walk_ovls=self.t_walk_ovl.isChecked())
		self.set_msg_temporarily("Walked FGMs")

	def walker_manis(self, ):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(
			self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		self.run_threaded(walker.get_manis_values, self, start_dir, walk_ovls=self.t_walk_ovl.isChecked())
		self.set_msg_temporarily("Walked Manis")

	def inspect_models(self):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(
			self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		self.run_threaded(walker.bulk_test_models, self, start_dir, walk_ovls=self.t_walk_ovl.isChecked())
		self.set_msg_temporarily("Inspected models")

	def check_length(self, name_tups):
		# Ask and return true if error is found and process should be stopped
		for old, new in name_tups:
			if len(old) != len(new):
				if not self.showconfirmation(
						f"Length of '{old}' [{len(old)}] and '{new}' [{len(new)}] don't match!\n"
						f"Continue renaming anyway?", title="Length Warning"):
					return True

	def check_version(self):
		is_64bits = sys.maxsize > 2 ** 32
		if not is_64bits:
			self.showerror(
				"Either your operating system or your python installation is not 64 bits.\n"
				"Large OVLs will crash unexpectedly!")
		if sys.version_info[0] != 3 or sys.version_info[1] < 7 or (
				sys.version_info[1] == 7 and sys.version_info[2] < 6):
			self.showerror("Python 3.7.6+ x64 bit is expected!")


if __name__ == '__main__':
	startup(MainWindow, GuiOptions(log_name="ovl_tool_gui"))
