import os
import shutil
import sys
import time
import logging
import tempfile
import importlib  # used to check if a package exists
import subprocess  # used to launch a pip install process

"""
	Deals with missing packages and tries to install them from the tool itself.
"""


# raw_input returns the empty string for "enter"
def install_prompt(question):
	print(question)
	yes = {'yes', 'y', 'ye'}
	choice = input().lower()
	if choice in yes:
		return True
	else:
		return False


# use pip to install a package
def pip_install(package):
	print(f"Trying to install {package}")
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# use pip to install --update a package
def pip_upgrade(package):
	print(f"Trying to upgrade {package}")
	subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])


missing = []
deps = ['numpy', 'PyQt5', 'imageio', 'vdf']
for package in deps:
	try:
		importlib.import_module(package)
	except ImportError:
		print(f"ERROR | Package {package} not found.")
		missing.append(package)

if len(missing) and install_prompt("Should I install the missing dependencies? (y/N)") == True:
	# upgrade pip then try installing the rest of packages
	pip_upgrade('pip')
	for package in missing:
		pip_install(package)

""" End of installing dependencies """

try:
	import numpy as np
	import imageio
	import winreg
	import vdf
	from PyQt5 import QtWidgets, QtGui, QtCore
	from ovl_util.config import logging_setup, get_version_str, get_commit_str

	stdout_handler = logging_setup("ovl_tool_gui")

	logging.info(f"Running python {sys.version}")
	logging.info(f"Running imageio {imageio.__version__}")
	logging.info(f"Running cobra-tools {get_version_str()}, {get_commit_str()}")

	from ovl_util import widgets, interaction
	from modules import walker
	from root_path import root_dir
	from generated.formats.ovl import games, get_game, set_game
	from generated.formats.ovl_base.enums.Compression import Compression

	games_list = [g.value for g in games]
except:
	logging.exception("Some modules could not be imported; make sure you install the required dependencies with pip!")
	time.sleep(15)


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "OVL Archive Editor", )
		self.resize(800, 600)
		self.setAcceptDrops(True)

		self.ovl_data = widgets.OvlReporter()

		exts = " ".join([f"*{ext}" for ext in self.ovl_data.formats_dict.extractables])
		self.filter = f"Supported files ({exts})"

		# add games from steam to the dict
		if "games" not in self.cfg:
			self.cfg["games"] = {}
		self.cfg["games"].update(self.get_steam_games())

		self.file_widget = widgets.FileWidget(self, self.cfg)

		self.game_choice = widgets.LabelCombo("Game:", [g.value for g in games])
		# only listen to user changes
		self.game_choice.entry.textActivated.connect(self.game_changed)
		self.game_choice.entry.setEditable(False)

		self.compression_choice = widgets.LabelCombo("Compression:", [c.name for c in Compression])
		# only listen to user changes
		self.compression_choice.entry.textActivated.connect(self.compression_changed)
		self.compression_choice.entry.setEditable(False)

		self.log_level_choice = widgets.LabelCombo("Log Level:", ("DEBUG", "INFO", "WARNING", "ERROR"))
		self.log_level_choice.entry.textActivated.connect(self.log_level_changed)
		self.log_level_choice.entry.setEditable(False)
		self.log_level_choice.setToolTip("Defines how much information is shown in the console window")

		self.installed_games_view = widgets.GamesCombo(self)
		self.installed_games_view.setToolTip("Select game for easy access below")
		self.installed_games_view.set_data(self.cfg["games"].keys())
		self.installed_games_view.entry.setEditable(False)
		self.installed_games_view.entry.textActivated.connect(self.installed_game_chosen)
		self.installed_games_view.add_button.clicked.connect(self.add_installed_game)

		self.model = QtWidgets.QFileSystemModel()
		self.model.setNameFilters(["*.ovl", ])
		self.dirs_container = QtWidgets.QTreeView()
		self.dirs_container.setModel(self.model)
		self.dirs_container.setColumnHidden(1, True)
		self.dirs_container.setColumnHidden(2, True)
		self.dirs_container.setColumnHidden(3, True)
		self.dirs_container.doubleClicked.connect(self.dirs_clicked)

		self.dirs_container.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)
		self.dirs_container.model().sort(self.dirs_container.header().sortIndicatorSection(),
										 self.dirs_container.header().sortIndicatorOrder())

		self.dirs_container.setAnimated(False)
		self.dirs_container.setIndentation(20)
		self.dirs_container.setSortingEnabled(True)

		self.dirs_container.setWindowTitle("Dir View")
		self.dirs_container.resize(640, 480)

		# create the table
		self.files_container = widgets.SortableTable(("Name", "File Type"), self.ovl_data.formats_dict.ignore_types,
													 ignore_drop_type="OVL", opt_hide=True)
		# connect the interaction functions
		self.files_container.table.model.member_renamed.connect(self.rename_handle)
		self.files_container.table.files_dragged.connect(self.drag_files)
		self.files_container.table.files_dropped.connect(self.inject_files)
		# self.files_container.table.file_selected.connect(self.show_dependencies)

		self.included_ovls_view = widgets.RelativePathCombo(self, self.file_widget)
		self.included_ovls_view.setToolTip(
			"These OVL files are loaded by the current OVL file, so their files are included")
		self.included_ovls_view.entries_changed.connect(self.update_includes)

		left_frame = QtWidgets.QWidget()
		hbox = QtWidgets.QVBoxLayout()
		hbox.addWidget(self.installed_games_view)
		hbox.addWidget(self.dirs_container)
		left_frame.setLayout(hbox)

		right_frame = QtWidgets.QWidget()
		hbox = QtWidgets.QVBoxLayout()
		hbox.addWidget(self.file_widget)
		hbox.addWidget(self.files_container)
		hbox.addWidget(self.included_ovls_view)
		right_frame.setLayout(hbox)

		splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		splitter.addWidget(left_frame)
		splitter.addWidget(right_frame)
		splitter.setSizes([200, 400])
		splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

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

		# log to text box
		self.gui_log_handler = widgets.QTextEditLogger(self)
		self.gui_log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'))
		logging.getLogger().addHandler(self.gui_log_handler)

		box = QtWidgets.QVBoxLayout(self)
		box.addLayout(grid)
		box.addWidget(splitter, 3)
		box.addWidget(self.gui_log_handler.widget, 1)
		# box.addWidget(self.p_action)
		self.central_widget.setLayout(box)

		main_menu = self.menuBar()
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
		logger_show = self.cfg.get("logger_show", False)
		self.t_logger.setChecked(logger_show)
		self.t_logger.triggered.connect(self.logger_show_triggered)
		self.logger_show_triggered()

		separator_action = self.actions['generate hash table']
		# we are not adding this to the action list, shall we?
		util_menu.insertAction(separator_action, self.t_walk_ovl)
		util_menu.insertAction(separator_action, self.t_logger)
		util_menu.insertSeparator(separator_action)

		self.check_version()
		# run once here to make sure we catch the default game
		self.populate_game_widget()
		self.game_changed()

		log_level = self.cfg.get("logger_level", None)
		if log_level:
			self.log_level_choice.entry.setText(log_level)
			self.log_level_changed(log_level)
		# do these at the end to make sure their requirements have been initialized
		self.ovl_data.files_list.connect(self.update_files_ui)
		self.ovl_data.warning_msg.connect(self.notify_user)
		self.ovl_data.included_ovls_list.connect(self.included_ovls_view.set_data)
		self.ovl_data.progress_percentage.connect(self.p_action.setValue)
		self.ovl_data.current_action.connect(self.set_msg_temporarily)
		self.run_threaded(self.ovl_data.load_hash_table)

	def do_debug_changed(self, do_debug):
		self.ovl_data.do_debug = do_debug

	def notify_user(self, msg_list):
		msg = msg_list[0]
		details = msg_list[1] if len(msg_list) > 1 else None
		interaction.showwarning(msg, details=details)

	def logger_show_triggered(self):
		show = self.t_logger.isChecked()
		self.cfg["logger_show"] = show
		if show:
			self.gui_log_handler.widget.show()
		else:
			self.gui_log_handler.widget.hide()

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

	def get_steam_games(self, ):
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

	def compare_ovls(self):
		selected_file_names = self.files_container.table.get_selected_files()
		if not selected_file_names:
			interaction.showwarning("Please select files to compare first")
			return
		if self.is_open_ovl():
			filepath = QtWidgets.QFileDialog.getOpenFileName(
				self, "Open OVL to compare with", self.cfg.get(f"dir_ovls_in", "C://"), f"OVL files (*.ovl)")[0]
			if filepath:
				other_ovl_data = widgets.OvlReporter()
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

	def installed_game_chosen(self):
		"""Run after choosing a game from dropdown of installed games"""
		current_game = self.installed_games_view.entry.currentText()
		self.cfg["current_game"] = current_game
		self.populate_game_widget()

	def add_installed_game(self):
		"""Add a new game to the list of available games"""
		dir_game = self.ask_game_dir()
		if dir_game:
			# todo - try to find the name of the game by stripping usual suffixes, eg. "win64\\ovldata"
			current_game = os.path.basename(dir_game)
			# store this newly chosen game in cfg
			self.cfg["games"][current_game] = dir_game
			self.cfg["current_game"] = current_game
			# update available games
			self.installed_games_view.set_data(self.cfg["games"].keys())

	def ask_game_dir(self):
		"""Ask the user to specify a game root folder"""
		dir_game = QtWidgets.QFileDialog.getExistingDirectory(self, "Open game folder")
		if dir_game:
			self.populate_game_widget()
			return dir_game

	def populate_game_widget(self):
		current_game = self.cfg.get("current_game")
		logging.info(f"Setting current_game {current_game}")
		# if current_game hasn't been set (no config.json), fall back on currently selected game
		dir_game = self.cfg["games"].get(current_game, self.installed_games_view.entry.currentText())
		# if current_game has been set, assume it exists in the games dict too (from steam)
		if dir_game:
			rt_index = self.model.setRootPath(dir_game)
			self.dirs_container.setRootIndex(rt_index)
			self.set_selected_dir(self.cfg.get("last_ovl_in", None))
			self.installed_games_view.entry.setText(current_game)
			# Set Game Choice default based on current game
			if current_game in games_list:
				self.game_choice.entry.setText(current_game)

	def get_selected_dir(self):
		model = self.dirs_container.model()
		ind = self.dirs_container.currentIndex()
		file_path = model.filePath(ind)
		if os.path.isdir(file_path):
			return file_path

	def set_selected_dir(self, dir_path):
		"""Show dir_path in dirs_container"""
		try:
			ind = self.dirs_container.model().index(dir_path)
			self.dirs_container.setCurrentIndex(ind)
		except:
			self.handle_error("Setting dir failed, see log!")

	def handle_path(self, save_over=True):
		# get path
		if self.t_in_folder.isChecked():
			selected_dir = self.get_selected_dir()
			if selected_dir:
				# walk path
				for ovl_path in walker.walk_type(selected_dir, extension=".ovl"):
					# open ovl file
					self.file_widget.accept_file(ovl_path)
					self.load(threaded=False)
					# process each
					yield self.ovl_data
					if save_over:
						self._save()
			else:
				interaction.showwarning("Select a root directory!")
		# just the one that's currently open
		else:
			yield self.ovl_data

	def dirs_clicked(self, ind):
		# handle double clicked file paths
		try:
			file_path = ind.model().filePath(ind)
			# open folder in explorer
			if os.path.isdir(file_path):
				os.startfile(file_path)
			# open ovl in tool
			elif file_path.lower().endswith(".ovl"):
				self.file_widget.decide_open(file_path)
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
		self.file_widget.dirty = True
		self.update_gui_table()

	def game_changed(self):
		game = self.game_choice.entry.currentText()
		set_game(self.ovl_data, game)

	def compression_changed(self):
		compression = self.compression_choice.entry.currentText()
		compression_value = Compression[compression]
		self.ovl_data.user_version.compression = compression_value

	def log_level_changed(self, level):
		self.gui_log_handler.setLevel(level)
		stdout_handler.setLevel(level)
		self.cfg["logger_level"] = level

	def show_dependencies(self, file_index):
		# just an example of what can be done when something is selected
		file_entry = self.ovl_data.files[file_index]

	def load(self, threaded=True):
		if self.file_widget.filepath:
			self.file_widget.dirty = False
			logging.debug(f"Loading threaded {threaded}")
			if threaded:
				self.run_threaded(self.ovl_data.load, self.file_widget.filepath)
			else:
				try:
					self.ovl_data.load(self.file_widget.filepath)
				except:
					logging.debug(self.ovl_data)
					self.handle_error("OVL loading failed, see log!")

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
		self.update_gui_table()

	def is_open_ovl(self):
		if self.file_widget.filename or self.file_widget.dirty:
			return True
		else:
			interaction.showwarning("You must open an OVL file first!")

	def update_files_ui(self, f_list):
		start_time = time.time()
		logging.info(f"Loading {len(f_list)} files into gui")
		f_list.sort(key=lambda t: (t[1], t[0]))
		self.files_container.set_data(f_list)
		logging.info(f"Loaded files into GUI in {time.time() - start_time:.2f} seconds")

	def update_includes(self, includes):
		self.ovl_data.included_ovl_names = includes

	def update_gui_table(self, ):
		start_time = time.time()
		f_list = [[loader.name, loader.ext] for loader in self.ovl_data.loaders.values()]
		self.update_files_ui(f_list)
		self.included_ovls_view.set_data(self.ovl_data.included_ovl_names)
		logging.info(f"Loaded GUI in {time.time() - start_time:.2f} seconds")
		self.update_progress("Operation completed!", value=100, vmax=100)

	def _save(self, ):
		"""Saves ovl to file_widget.filepath, clears dirty flag"""
		try:
			self.ovl_data.save(self.file_widget.filepath)
			self.file_widget.dirty = False
			self.update_progress(f"Saved {self.ovl_data.basename}", value=100, vmax=100)
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
				if self.is_open_ovl():
					# for bulk extraction, add the ovl basename to the path to avoid overwriting
					if self.t_in_folder.isChecked():
						selected_dir = self.get_selected_dir()
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
			self.file_widget.dirty = True
			# threaded injection seems to be fine now
			# self.ovl_data.add_files(files)
			self.run_threaded(self.ovl_data.add_files, files)
		# the gui is updated from the signal ovl.files_list emitted from add_files

	def get_replace_strings(self):
		try:
			newline = "\n"
			old = self.e_name_old.toPlainText()
			new = self.e_name_new.toPlainText()
			old = old.split(newline)
			new = new.split(newline)
			if len(old) != len(new):
				interaction.showwarning(f"Old {len(old)} and new {len(new)} must have the same amount of lines!")
			return list(zip(old, new))
		except:
			self.handle_error("Getting replace strings failed, see log!")

	def rename(self):
		names = self.get_replace_strings()
		try:
			if names:
				for ovl in self.handle_path():
					if self.is_open_ovl():
						self.ovl_data.rename(names, mesh_mode=self.t_mesh_ovl.isChecked())
						self.file_widget.dirty = True
						self.update_gui_table()
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
				if self.is_open_ovl():
					self.ovl_data.rename_contents(names, only_files)
					self.file_widget.dirty = True
					# file names don't change, so no need to update gui
					# self.update_gui_table()

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

					self.update_progress("Saved file list", value=100, vmax=100)
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
					self.update_progress("Saved included OVLs", value=100, vmax=100)
				except:
					self.handle_error("Writing included OVLs failed, see log!")

	def load_included_ovls(self):
		filepath = QtWidgets.QFileDialog.getOpenFileName(
			self, "Open ovls.include", os.path.join(self.cfg.get("dir_ovls_out", "C://"), "ovls.include"),
				"Include file (*.include)", )[0]
		if filepath:
			try:
				self.ovl_data.load_included_ovls(filepath)
				self.file_widget.dirty = True
				self.update_progress("Loaded included OVLs", value=100, vmax=100)
			except:
				self.handle_error("Opening included OVLs failed, see log!")

	def remove(self):
		if self.is_open_ovl():
			selected_file_names = self.files_container.table.get_selected_files()
			# todo - might want to check self.files_container.hasFocus(), but does not seem to work!
			if selected_file_names:
				try:
					self.ovl_data.remove(selected_file_names)
					self.file_widget.dirty = True
				except:
					self.handle_error("Removing file from OVL failed, see log!")
				self.update_gui_table()

	def walker_hash(self, ):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder',
															   self.cfg.get("dir_ovls_in", "C://"))
		walker.generate_hash_table(self, start_dir)
		self.update_progress("Hashed", value=100, vmax=100)

	def walker_fgm(self, ):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder',
															   self.cfg.get("dir_ovls_in", "C://"))
		walker.get_fgm_values(self, start_dir, walk_ovls=self.t_walk_ovl.isChecked())
		self.update_progress("Walked FGMs", value=100, vmax=100)

	def walker_manis(self, ):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder',
															   self.cfg.get("dir_ovls_in", "C://"))
		walker.get_manis_values(self, start_dir, walk_ovls=self.t_walk_ovl.isChecked())
		self.update_progress("Walked Manis", value=100, vmax=100)

	def inspect_models(self):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder',
															   self.cfg.get("dir_ovls_in", "C://"))
		walker.bulk_test_models(self, start_dir, walk_ovls=self.t_walk_ovl.isChecked())
		self.update_progress("Inspected models", value=100, vmax=100)

	@staticmethod
	def check_length(name_tups):
		# Ask and return true if error is found and process should be stopped
		for old, new in name_tups:
			if len(old) != len(new):
				if not interaction.showconfirmation(
						f"WARNING: length of '{old}' [{len(old)}] and '{new}' [{len(new)}] don't match!\n"
						f"Continue renaming anyway?"):
					return True

	@staticmethod
	def check_version():
		is_64bits = sys.maxsize > 2 ** 32
		if not is_64bits:
			interaction.showerror(
				"Either your operating system or your python installation is not 64 bits.\n"
				"Large OVLs will crash unexpectedly!")
		if sys.version_info[0] != 3 or sys.version_info[1] < 7 or (
				sys.version_info[1] == 7 and sys.version_info[2] < 6):
			interaction.showerror("Python 3.7.6+ x64 bit is expected!")


if __name__ == '__main__':
	widgets.startup(MainWindow)
