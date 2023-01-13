import os
import shutil
import sys
import time
import logging
import tempfile

try:
	import winreg
	import numpy as np
	import imageio
	from PyQt5 import QtWidgets, QtGui, QtCore
	from ovl_util.config import logging_setup, get_version_str, get_commit_str

	logging_setup("ovl_tool_gui")

	logging.info(f"Running python {sys.version}")
	logging.info(f"Running imageio {imageio.__version__}")
	logging.info(f"Running cobra-tools {get_version_str()}, {get_commit_str()}")

	from ovl_util import widgets, interaction
	from modules import walker
	from modules.formats.formats_dict import build_formats_dict
	from root_path import root_dir
	from generated.formats.ovl import OvlFile, games, get_game, set_game, IGNORE_TYPES
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

		supported_types = [ext for ext in self.ovl_data.formats_dict.keys()]
		self.filter = "Supported files ({})".format(" ".join("*" + t for t in supported_types))

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

		header_names = ["Name", "File Type"]

		self.installed_games_view = widgets.GamesCombo(self)
		self.installed_games_view.setToolTip("Select game for easy access below")
		self.installed_games_view.set_data(self.cfg["games"].keys())
		self.installed_games_view.entry.setEditable(False)
		self.installed_games_view.entry.textActivated.connect(self.installed_game_chosen)
		self.installed_games_view.add_button.clicked.connect(self.add_installed_game)

		self.model = QtWidgets.QFileSystemModel()
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
		self.files_container = widgets.SortableTable(header_names, IGNORE_TYPES, ignore_drop_type="OVL", opt_hide=True)
		# connect the interaction functions
		self.files_container.table.model.member_renamed.connect(self.rename_handle)
		self.files_container.table.files_dragged.connect(self.drag_files)
		self.files_container.table.files_dropped.connect(self.inject_files)
		# self.files_container.table.file_selected.connect(self.show_dependencies)

		self.included_ovls_view = widgets.RelativePathCombo(self, self.file_widget)
		self.included_ovls_view.setToolTip("These OVL files are loaded by the current OVL file, so their files are included")
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

		# toggles
		self.t_show_temp_files = QtWidgets.QCheckBox("Save Temp Files")
		self.t_show_temp_files.setToolTip(
			"By default, temporary files are converted to usable ones and back on the fly")
		self.t_show_temp_files.setChecked(False)

		self.t_in_folder = QtWidgets.QCheckBox("Process Folder")
		self.t_in_folder.setToolTip("Runs commands on all OVLs of current folder")
		self.t_in_folder.setChecked(False)

		self.extract_types_combo = widgets.CheckableComboBox()
		comunes = build_formats_dict()
		self.extract_types_combo.addItems(comunes)

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

		self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		self.splitter.addWidget(left_frame)
		self.splitter.addWidget(right_frame)
		self.splitter.setSizes([200, 400])
		self.splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.e_name_old, 0, 0, 3, 1)
		self.qgrid.addWidget(self.e_name_new, 0, 1, 3, 1)

		self.qgrid.addWidget(self.t_show_temp_files, 0, 3)
		self.qgrid.addWidget(self.t_in_folder, 2, 3)
		self.qgrid.addWidget(self.t_mesh_ovl, 1, 3)
		self.qgrid.addWidget(self.game_choice, 0, 4,)
		self.qgrid.addWidget(self.compression_choice, 1, 4,)
		self.qgrid.addWidget(self.extract_types_combo, 2, 4,)

		self.qgrid.addWidget(self.splitter, 5, 0, 1, 5)
		self.qgrid.addWidget(self.p_action, 6, 0, 1, 5)
		self.qgrid.addWidget(self.t_action, 7, 0, 1, 5)

		self.central_widget.setLayout(self.qgrid)

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
			(util_menu, "Inspect Models", self.inspect_models, "", ""),
			(util_menu, "Inspect FGMs", self.walker_fgm, "", ""),
			(util_menu, "Generate Hash Table", self.walker_hash, "", ""),
			(util_menu, "Dump Debug Data", self.dump_debug_data, "", "dump_debug"),
			(util_menu, "Open Tools Dir", self.open_tools_dir, "", "home"),
			(util_menu, "Export File List", self.save_file_list, "", ""),
			(util_menu, "Export included ovl list", self.save_included_ovls, "", ""),
			(util_menu, "Compare with other OVL", self.compare_ovls, "", ""),
			(help_menu, "Report Bug", self.report_bug, "", "report"),
			(help_menu, "Documentation", self.online_support, "", "manual"))
		self.add_to_menu(button_data)

		# add checkbox to extract from ovls for the diff walkers
		self.t_walk_ovl = QtWidgets.QAction("Walker extracts OVLs")
		self.t_walk_ovl.setToolTip("Extract from OVLS when doing bulk operations: fgm or ms2.")
		self.t_walk_ovl.setCheckable(True)
		self.t_walk_ovl.setChecked(False)
		separator_action = self.actions['generate hash table']
		# we are not adding this to the action list, shall we?
		util_menu.insertAction( separator_action, self.t_walk_ovl )
		util_menu.insertSeparator( separator_action )

		self.check_version()
		# run once here to make sure we catch the default game
		self.populate_game_widget()
		self.game_changed()
		# do these at the end to make sure their requirements have been initialized
		self.ovl_data.files_list.connect(self.update_files_ui)
		self.ovl_data.included_ovls_list.connect(self.included_ovls_view.set_data)
		self.ovl_data.progress_percentage.connect(self.p_action.setValue)
		self.ovl_data.current_action.connect(self.t_action.setText)
		self.run_threaded(self.ovl_data.load_hash_table)

	def enable_gui_options(self, enable=True):
		self.t_in_folder.setEnabled(enable)
		self.t_show_temp_files.setEnabled(enable)
		self.t_mesh_ovl.setEnabled(enable)
		self.t_walk_ovl.setEnabled(enable)
		self.compression_choice.setEnabled(enable)
		self.game_choice.setEnabled(enable)
		# for action_name in ("open", "save", "save as"):
		# just disable all
		for action_name in self.actions.keys():
			self.actions[action_name.lower()].setEnabled(enable)

	def dump_debug_data(self,):
		self.ovl_data.dump_debug_data()

	def get_steam_games(self,):
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
				import vdf
				v = vdf.load(open(vdf_path))
				for folder in v["libraryfolders"].values():
					library_folders.add(folder["path"])
			except:
				logging.warning(f"vdf not installed, can not detect steam games on external drives - run `pip install vdf`")

			# map all installed fdev game names to their path
			fdev_games = {}
			# list all games for each library folder
			for steam_path in library_folders:
				apps_path = os.path.join(steam_path, "steamapps\\common")
				# filter with supported fdev games
				fdev_in_lib = [game for game in os.listdir(apps_path) if game in games_list]
				# generate the whole path for each game, add to dict
				# C:\Program Files (x86)\Steam\steamapps\common\Planet Zoo\win64\ovldata
				fdev_games.update({game: os.path.join(apps_path, game, "win64\\ovldata") for game in fdev_in_lib})
			logging.info(f"Found {len(fdev_games)} Cobra games from Steam")
			return fdev_games
		except:
			logging.exception(f"Getting installed games from steam folder failed")
			return {}

	def compare_ovls(self):
		selected_file_names = self.files_container.table.get_selected_files()
		if not selected_file_names:
			interaction.showdialog("Please select files to compare first")
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
		"""Choose a game from dropdown of installed games"""
		current_game = self.installed_games_view.entry.currentText()
		self.cfg["current_game"] = current_game
		self.populate_game_widget()

	def add_installed_game(self):
		"""Choose a game from dropdown of installed games"""
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
				ovls = walker.walk_type(selected_dir, extension=".ovl")
				for ovl_path in ovls:
					# open ovl file
					self.file_widget.accept_file(ovl_path)
					self.load(threaded=False)
					# process each
					yield self.ovl_data
					if save_over:
						self._save()
			else:
				interaction.showdialog("Select a root directory!")
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
			out_paths, errors = self.ovl_data.extract(
				temp_dir, only_names=file_names, show_temp_files=self.show_temp_files)
			if out_paths:
				data.setUrls([QtCore.QUrl.fromLocalFile(path) for path in out_paths])
			drag.setMimeData(data)
			drag.exec_()
			logging.info(f"Tried to extract {len(file_names)} files, got {len(errors)} errors")
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

	@property
	def show_temp_files(self, ):
		return self.t_show_temp_files.isChecked()

	def show_dependencies(self, file_index):
		# just an example of what can be done when something is selected
		file_entry = self.ovl_data.files[file_index]

	def load(self, threaded=True):
		if self.file_widget.filepath:
			self.file_widget.dirty = False
			logging.info(f"Loading threaded {threaded}")
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
			interaction.showdialog("You must open an OVL file first!")

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
		f_list = [[loader.file_entry.name, loader.file_entry.ext] for loader in self.ovl_data.loaders.values()]
		self.update_files_ui(f_list)
		self.included_ovls_view.set_data(self.ovl_data.included_ovl_names)
		logging.info(f"Loaded GUI in {time.time() - start_time:.2f} seconds")
		self.update_progress("Operation completed!", value=1, vmax=1)

	def _save(self, ):
		"""Saves ovl to file_widget.filepath, clears dirty flag"""
		try:
			self.ovl_data.save(self.file_widget.filepath)
			self.file_widget.dirty = False
			self.update_progress(f"Saved {self.ovl_data.basename}", value=1, vmax=1)
		except:
			self.handle_error("Saving OVL failed, see log!")

	def extract_all(self):
		out_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg.get("dir_extract", "C://"), )
		if out_dir:
			self.cfg["dir_extract"] = out_dir
			_out_dir = out_dir
			all_error_files = []
			only_types = ()

			# check using a filter to extract mimes
			thelist = self.extract_types_combo.currentData()
			if len(thelist) > 0:
				only_types = thelist

			for ovl in self.handle_path(save_over=False):
				if self.is_open_ovl():
					# for bulk extraction, add the ovl basename to the path to avoid overwriting
					if self.t_in_folder.isChecked():
						selected_dir = self.get_selected_dir()
						rel_p = os.path.relpath(ovl.path_no_ext, start=selected_dir)
						out_dir = os.path.join(_out_dir, rel_p)
					try:
						out_paths, error_files = ovl.extract(out_dir, show_temp_files=self.show_temp_files, only_types=only_types)
						all_error_files += error_files
					except:
						self.handle_error("Extraction failed, see log!")
			interaction.extract_error_warning(all_error_files)

	def inject_ask(self):
		if self.is_open_ovl():
			files = QtWidgets.QFileDialog.getOpenFileNames(
				self, 'Inject files', self.cfg.get("dir_inject", "C://"), self.filter)[0]
			self.inject_files(files)

	def inject_files(self, files):
		"""Tries to inject files into self.ovl_data"""
		if files:
			self.cfg["dir_inject"] = os.path.dirname(files[0])
			try:

				error_files = self.ovl_data.inject(files, self.show_temp_files)
				# error_files = []
				# self.run_threaded(self.ovl_data.inject, files, self.show_temp_files)
				self.file_widget.dirty = True
				# if error_files:
				# 	interaction.showdialog(f"Injection caused errors on {len(error_files)} files, see console for details!")
				# self.update_gui_table()
				self.update_progress("Injection completed", value=1, vmax=1)
			except:
				self.handle_error("Injection failed, see log!")

	def get_replace_strings(self):
		try:
			newline = "\n"
			old = self.e_name_old.toPlainText()
			new = self.e_name_new.toPlainText()
			old = old.split(newline)
			new = new.split(newline)
			if len(old) != len(new):
				interaction.showdialog(f"Old {len(old)} and new {len(new)} must have the same amount of lines!")
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
					self.update_gui_table()
                    
	def rename_both(self):
		self.rename_contents()
		self.rename()

	# Save the OVL file list to disk
	def save_file_list(self):
		if self.is_open_ovl():
			filelist_src = QtWidgets.QFileDialog.getSaveFileName(
				self, 'Save File List', os.path.join(self.cfg.get("dir_ovls_out", "C://"), self.file_widget.filename + ".files.txt" ),
				"Txt file (*.txt)", )[0]
			if filelist_src:
				try:
					file_names = self.files_container.table.get_files()
					with open(filelist_src, 'w') as f:
						f.write("\n".join(file_names))

					self.update_progress("Saved file list", value=1, vmax=1)
				except:
					self.handle_error("Writing file list failed, see log!")

	# Save the OVL include list to disk
	def save_included_ovls(self):
		if self.is_open_ovl():
			filelist_src = QtWidgets.QFileDialog.getSaveFileName(
				self, 'ovls.include', os.path.join(self.cfg.get("dir_ovls_out", "C://"), "ovls.include" ),
				"Include file (*.include)", )[0]
			if filelist_src:
				try:
					self.ovl_data.save_included_ovls(filelist_src)
					self.update_progress("Saved included OVLs", value=1, vmax=1)
				except:
					self.handle_error("Writing included OVLs failed, see log!")

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

	def walker_hash(self,):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		walker.generate_hash_table(self, start_dir)
		self.update_progress("Hashed", value=1, vmax=1)

	def walker_fgm(self,):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		walker.get_fgm_values(self, start_dir, walk_ovls=self.t_walk_ovl.isChecked())
		self.update_progress("Walked FGMs", value=1, vmax=1)

	def inspect_models(self):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		walker.bulk_test_models(self, start_dir, walk_ovls=self.t_walk_ovl.isChecked())
		self.update_progress("Inspected models", value=1, vmax=1)

	@staticmethod
	def check_length(name_tups):
		# Ask and return true if error is found and process should be stopped
		for old, new in name_tups:
			if len(old) != len(new):
				if interaction.showdialog(
						f"WARNING: length of '{old}' [{len(old)}] and '{new}' [{len(new)}] don't match!\n"
						f"Stop renaming?", ask=True):
					return True

	@staticmethod
	def check_version():
		is_64bits = sys.maxsize > 2 ** 32
		if not is_64bits:
			interaction.showdialog(
				"Either your operating system or your python installation is not 64 bits.\n"
				"Large OVLs will crash unexpectedly!")
		if sys.version_info[0] != 3 or sys.version_info[1] < 7 or (
				sys.version_info[1] == 7 and sys.version_info[2] < 6):
			interaction.showdialog("Python 3.7.6+ x64 bit is expected!")


if __name__ == '__main__':
	widgets.startup(MainWindow)
