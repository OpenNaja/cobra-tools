import os
import shutil
import sys
import time
import traceback
import logging
import tempfile

try:
	import numpy as np
	from PyQt5 import QtWidgets, QtGui, QtCore

	from ovl_util.config import logging_setup, get_version_str
	logging_setup("ovl_tool_gui")

	logging.info(f"Running python {sys.version}")
	logging.info(f"Running cobra-tools {get_version_str()}")

	from ovl_util import widgets, interaction, qt_threads
	from modules import walker, remover
	from generated.formats.ovl import OvlFile, games, get_game, set_game, IGNORE_TYPES
	from generated.formats.ovl_base.enum.Compression import Compression
except Exception as err:
	traceback.print_exc()
	time.sleep(15)

SUPPORTED_TYPES = (".dds", ".png", ".ms2", ".txt", ".fgm", ".fdb", ".matcol", ".xmlconfig", ".assetpkg", ".lua", ".wem", ".otf", ".ttf")


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "OVL Archive Editor", )
		self.resize(800, 600)

		self.ovl_data = OvlFile(progress_callback=self.update_progress)
		self.ovl_data.load_hash_table()

		self.filter = "Supported files ({})".format(" ".join("*" + t for t in SUPPORTED_TYPES))

		self.file_widget = widgets.FileWidget(self, self.cfg)
		self.file_widget.setToolTip("The name of the OVL file that is currently open")

		self.p_action = QtWidgets.QProgressBar(self)
		self.p_action.setGeometry(0, 0, 200, 15)
		self.p_action.setTextVisible(True)
		self.p_action.setMaximum(1)
		self.p_action.setValue(0)
		self.t_action_current_message = "No operation in progress"
		self.t_action = QtWidgets.QLabel(self, text=self.t_action_current_message)

		self.game_choice = widgets.LabelCombo("Game:", [g.value for g in games])
		# only listen to user changes
		self.game_choice.entry.textActivated.connect(self.game_changed)
		self.game_choice.entry.setEditable(False)
		
		self.compression_choice = widgets.LabelCombo("Compression:", [c.name for c in Compression])
		# only listen to user changes
		self.compression_choice.entry.textActivated.connect(self.compression_changed)
		self.compression_choice.entry.setEditable(False)

		header_names = ["Name", "File Type", "DJB"]

		self.model = QtWidgets.QFileSystemModel()
		self.dirs_container = QtWidgets.QTreeView()
		self.dirs_container.setModel(self.model)
		self.dirs_container.setColumnHidden(1, True)
		self.dirs_container.setColumnHidden(2, True)
		self.dirs_container.setColumnHidden(3, True)
		self.dirs_container.doubleClicked.connect(self.dirs_clicked)
		self.set_game_dir()

		self.dirs_container.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)
		self.dirs_container.model().sort(self.dirs_container.header().sortIndicatorSection(),
						 self.dirs_container.header().sortIndicatorOrder())

		self.dirs_container.setAnimated(False)
		self.dirs_container.setIndentation(20)
		self.dirs_container.setSortingEnabled(True)

		self.dirs_container.setWindowTitle("Dir View")
		self.dirs_container.resize(640, 480)

		# create the table
		self.files_container = widgets.SortableTable(header_names, IGNORE_TYPES)
		# connect the interaction functions
		self.files_container.table.model.member_renamed.connect(self.rename_handle)
		self.files_container.table.files_dragged.connect(self.drag_files)
		self.files_container.table.files_dropped.connect(self.inject_files)
		# self.files_container.table.file_selected.connect(self.show_dependencies)

		self.included_ovls_view = widgets.EditCombo(self)
		self.included_ovls_view.setToolTip("These OVL files are loaded by the current OVL file, so their files are included")
		self.included_ovls_view.entries_changed.connect(self.ovl_data.set_included_ovl_names)

		self.dat_widget = widgets.FileWidget(self, self.cfg, ask_user=False, dtype="DAT", poll=False)
		self.dat_widget.setToolTip("External .dat file path to overwrite internal OVS data")
		self.dat_widget.hide()

		right_frame = QtWidgets.QWidget()
		hbox = QtWidgets.QVBoxLayout()
		hbox.addWidget(self.file_widget)
		hbox.addWidget(self.files_container)
		hbox.addWidget(self.included_ovls_view)
		hbox.addWidget(self.dat_widget)
		right_frame.setLayout(hbox)

		# toggles
		self.t_show_temp_files = QtWidgets.QCheckBox("Save Temp Files")
		self.t_show_temp_files.setToolTip(
			"By default, temporary files are converted to usable ones and back on the fly")
		self.t_show_temp_files.setChecked(False)

		self.in_folder = QtWidgets.QCheckBox("Process Folder")
		self.in_folder.setToolTip("Runs commands on all OVLs of current folder")
		self.in_folder.setChecked(False)

		self.ext_dat = QtWidgets.QCheckBox("Use External DAT")
		self.ext_dat.setToolTip("Experimental: Save the ovl with an external STATIC DAT instead of one in memory")
		self.ext_dat.setChecked(False)
		self.ext_dat.stateChanged.connect(self.dat_show)

		self.t_animal_ovl = QtWidgets.QCheckBox("Animal OVL Mode")
		self.t_animal_ovl.setToolTip("Renames only MS2, MDL2 and MOTIONGRAPH files.")
		self.t_animal_ovl.setChecked(False)

		self.t_unsafe = QtWidgets.QCheckBox("Unsafe Mode")
		self.t_unsafe.setToolTip("Forces unsafe (brute force) replacement. May break your files.")
		self.t_unsafe.setChecked(False)

		self.e_name_old = QtWidgets.QTextEdit("old")
		self.e_name_new = QtWidgets.QTextEdit("new")
		self.e_name_old.setFixedHeight(100)
		self.e_name_new.setFixedHeight(100)
		self.e_name_old.setTabChangesFocus(True)
		self.e_name_new.setTabChangesFocus(True)

		self.t_write_dat = QtWidgets.QCheckBox("Save DAT")
		self.t_write_dat.setToolTip("Writes decompressed archive streams to DAT files for debugging")
		self.t_write_dat.setChecked(False)
		self.t_write_dat.stateChanged.connect(self.load)

		self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		self.splitter.addWidget(self.dirs_container)
		self.splitter.addWidget(right_frame)
		self.splitter.setSizes([200, 400])
		self.splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.e_name_old, 0, 0, 5, 1)
		self.qgrid.addWidget(self.e_name_new, 0, 1, 5, 1)

		self.qgrid.addWidget(self.t_show_temp_files, 0, 3)
		self.qgrid.addWidget(self.t_write_dat, 1, 3)
		self.qgrid.addWidget(self.ext_dat, 2, 3)
		self.qgrid.addWidget(self.in_folder, 3, 3)
		self.qgrid.addWidget(self.game_choice, 0, 4,)
		self.qgrid.addWidget(self.compression_choice, 1, 4,)
		self.qgrid.addWidget(self.t_animal_ovl, 2, 4)
		self.qgrid.addWidget(self.t_unsafe, 3, 4)

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
			(file_menu, "Save", self.save_ovl, "CTRL+S", "save"),
			(file_menu, "Save As", self.save_as_ovl, "CTRL+SHIFT+S", "save"),
			(file_menu, "Exit", self.close, "", "exit"),
			(edit_menu, "Unpack", self.extract_all, "CTRL+U", "extract"),
			(edit_menu, "Inject", self.inject_ask, "CTRL+I", "inject"),
			(edit_menu, "Rename", self.rename, "CTRL+R", ""),
			(edit_menu, "Rename Contents", self.rename_contents, "CTRL+SHIFT+R", ""),
			(edit_menu, "Remove Selected", self.remover, "DEL", ""),
			(util_menu, "Inspect Models", self.inspect_models, "", ""),
			(util_menu, "Inspect FGMs", self.walker_fgm, "", ""),
			(util_menu, "Generate Hash Table", self.walker_hash, "", ""),
			(util_menu, "Save Frag Log", self.ovl_data.dump_frag_log, "", ""),
			(util_menu, "Open Tools Dir", self.open_tools_dir, "", ""),
			(util_menu, "Export File List", self.save_file_list, "", ""),
			(util_menu, "Set Game Dir", self.ask_game_dir, "", ""),
			(util_menu, "Export included ovl list", self.save_included_ovls, "", ""),
			(help_menu, "Report Bug", self.report_bug, "", "report"),
			(help_menu, "Documentation", self.online_support, "", "manual"))
		self.add_to_menu(button_data)
		self.check_version()

	def ask_game_dir(self):
		dir_game = QtWidgets.QFileDialog.getExistingDirectory(self, "Open game folder")
		self.cfg["dir_game"] = dir_game
		return dir_game

	def set_game_dir(self):
		dir_game = self.cfg.get("dir_game", "")
		if not dir_game:
			dir_game = self.ask_game_dir()
		if dir_game:
			rt_index = self.model.setRootPath(dir_game)
			self.dirs_container.setRootIndex(rt_index)

	def get_selected_dir(self):
		model = self.dirs_container.model()
		ind = self.dirs_container.currentIndex()
		file_path = model.filePath(ind)
		if os.path.isdir(file_path):
			return file_path

	def handle_path(self, save_over=True):
		# get path
		if self.in_folder.isChecked():
			root_dir = self.get_selected_dir()
			if root_dir:
				# walk path
				ovls = walker.walk_type(root_dir, extension=".ovl")
				for ovl_path in ovls:
					# open ovl file
					self.file_widget.decide_open(ovl_path)
					# process each
					yield self.ovl_data
					if save_over:
						self.ovl_data.save(ovl_path, "")
			else:
				interaction.showdialog("Select a root directory!")
		# just the one that's currently open
		else:
			yield self.ovl_data

	def dirs_clicked(self, ind):
		# handle double clicked file paths
		try:
			file_path = ind.model().filePath(ind)
			if os.path.isdir(file_path):
				os.startfile(file_path)
			elif file_path.lower().endswith(".ovl"):
				self.file_widget.decide_open(file_path)
		except BaseException as err:
			print(err)

	@staticmethod
	def open_tools_dir():
		os.startfile(os.getcwd())

	def drag_files(self, file_names):
		logging.info(f"DRAGGING {file_names}")
		drag = QtGui.QDrag(self)
		temp_dir = tempfile.mkdtemp("-cobra")
		try:
			out_paths, errors = self.ovl_data.extract(
				temp_dir, only_names=file_names, show_temp_files=self.show_temp_files)

			data = QtCore.QMimeData()
			data.setUrls([QtCore.QUrl.fromLocalFile(path) for path in out_paths])
			drag.setMimeData(data)
			drag.exec_()
			logging.info(f"Tried to extract {len(file_names)} files, got {len(errors)} errors")
		except BaseException as ex:
			traceback.print_exc()
			interaction.showdialog(str(ex))
			logging.error(ex)
		shutil.rmtree(temp_dir)

	def rename_handle(self, old_name, new_name):
		"""this manages the renaming of a single entry"""
		names = [(old_name, new_name), ]
		self.ovl_data.rename(names)
		self.update_gui_table()

	def game_changed(self):
		game = self.game_choice.entry.currentText()
		# we must set both the context, and the local variable
		set_game(self.ovl_data.context, game)
		set_game(self.ovl_data, game)

	def compression_changed(self):
		compression = self.compression_choice.entry.currentText()
		compression_value = Compression[compression]
		self.ovl_data.context.user_version.compression = compression_value
		self.ovl_data.user_version.compression = compression_value

	@property
	def commands(self):
		# get those commands that are set to True
		return [x for x in ("write_dat", ) if getattr(self, x)]

	@property
	def show_temp_files(self, ):
		return self.t_show_temp_files.isChecked()

	@property
	def use_ext_dat(self, ):
		return self.ext_dat.isChecked()

	@property
	def write_dat(self, ):
		return self.t_write_dat.isChecked()

	def dat_show(self, ):
		if self.use_ext_dat:
			self.dat_widget.show()
		else:
			self.dat_widget.hide()

	def update_commands(self):
		# at some point, just set commands to archive and trigger changes there
		if self.file_widget.filename:
			self.ovl_data.commands = self.commands

	def update_progress(self, message, value=None, vmax=None):
		# avoid gui updates if the value won't actually change the percentage.
		# this saves us from making lots of GUI update calls that don't really
		# matter.
		try:
			if vmax > 100 and (value % (vmax // 100)) and value != 0:
				value = None
		except ZeroDivisionError:
			value = 0
		except TypeError:
			value = None

		# update progress bar values if specified
		if value is not None:
			self.p_action.setValue(value)
		if vmax is not None:
			self.p_action.setMaximum(vmax)

		# don't update the GUI unless the message has changed. label updates
		# are expensive
		if self.t_action_current_message != message:
			self.t_action.setText(message)
			self.t_action_current_message = message

	def show_dependencies(self, file_index):
		# just an example of what can be done when something is selected
		file_entry = self.ovl_data.files[file_index]
		ss_entry = self.ovl_data.get_sized_str_entry(file_entry.name)
		ss_p = ss_entry.pointers[0]
		logging.debug(f"File: {ss_p.pool_index} {ss_p.data_offset} {ss_entry.name}")
		for dep in file_entry.dependencies:
			p = dep.pointers[0]
			logging.debug(f"Dependency: {p.pool_index} {p.data_offset} {dep.name}")
		for f in ss_entry.fragments:
			p0 = f.pointers[0]
			p1 = f.pointers[1]
			logging.debug(f"Fragment: {p0.pool_index} {p0.data_offset} {p1.pool_index} {p1.data_offset}")

	def load(self):
		if self.file_widget.filepath:
			self.file_widget.dirty = False
			try:
				# runTask(self.ovl_data.load, (self.file_widget.filepath,), {"commands": self.commands,})
				# test(2)
				# self.ovl_thread.func = self.ovl_thread.ovl_data.load
				# self.ovl_thread.args = (self.file_widget.filepath,)
				# self.ovl_thread.kwargs = {"commands": self.commands,}
				# self.ovl_thread.start()
				self.ovl_data.load(self.file_widget.filepath, commands=self.commands)
				# print(self.ovl_data.user_version)
				# print(self.ovl_data)
				# for a in self.ovl_data.archives:
				# 	print(a)
				# for a in self.ovl_data.archives[1:]:
				# 	print(a.name)
				# 	for ss in a.content.sized_str_entries:
				# 		print(ss.name)
				# print(self.ovl_data.mimes)
				# print(self.ovl_data.triplets)
				# for a, z in zip(self.ovl_data.archives, self.ovl_data.zlibs):
				# 	print(a, z)
				# 	print(f"zlib sum {z.zlib_thing_1 + z.zlib_thing_2 - 68}")
				# 	print(f"pool size {a.pools_end - a.pools_start}")
				# 	print(f"stream links size {12 * a.num_files}")
				# 	print(f"buffer size {sum([buff.size for buff in a.content.buffer_entries])}")
				# 	print(f"d1 size {sum([data.size_1 for data in a.content.data_entries])}")
				# 	print(f"d2 size {sum([data.size_2 for data in a.content.data_entries])}")
				# 	if a.name != "STATIC":
				# 		streams = self.ovl_data.stream_files[a.stream_files_offset: a.stream_files_offset+a.num_files]
				# 		print(a.name, streams)
				# print(self.ovl_data.stream_files)
				# for i, f in enumerate(self.ovl_data.files):
				# 	if f.ext == ".texturestream":
				# 		print(i, f.name)
				# offsets = list(sorted((f.file_offset, i) for i, f in enumerate(self.ovl_data.stream_files)))
				# # print(self.ovl_data)
				# print(offsets)
				# # for a in self.ovl_data.archives[1:]:
				# # 	print(a.content)
				# for sf in self.ovl_data.stream_files:
				# 	print(sf)
				# 	for a in self.ovl_data.archives:
				# 		if a.pools_start <= sf.stream_offset < a.pools_end:
				# 			print(f"is in {a.name}")
				# 			print(f"pool offset relative {sf.stream_offset - a.pools_start}")
				# 			# print(a.content.sized_str_entries)
				# 	for a in self.ovl_data.archives:
				# 		if a.name == "STATIC":
				# 			for i, pool in enumerate(a.content.pools):
				# 				if pool.offset <= sf.file_offset < pool.offset + pool.size:
				# 					print(f"static pool {i} offset relative {sf.file_offset - pool.offset}")
				# 	logging.debug(a.content)
				# print(self.ovl_data.user_version)
			except Exception as ex:
				traceback.print_exc()
				interaction.showdialog(str(ex))
				print(self.ovl_data)
			self.update_gui_table()
			game = get_game(self.ovl_data)[0]
			self.game_choice.entry.setText(game.value)
			self.compression_choice.entry.setText(self.ovl_data.user_version.compression.name)

	def create_ovl(self, ovl_dir):
		# clear the ovl
		self.ovl_data = OvlFile(progress_callback=self.update_progress)
		self.game_changed()
		try:
			self.ovl_data.create(ovl_dir)
		except Exception as ex:
			traceback.print_exc()
			interaction.showdialog(str(ex))
		self.update_gui_table()

	def is_open_ovl(self):
		if not self.file_widget.filename:
			interaction.showdialog("You must open an OVL file first!")
		else:
			return True

	def update_gui_table(self, ):
		start_time = time.time()
		logging.info(f"Loading {len(self.ovl_data.files)} files into gui")
		self.files_container.set_data([[f.name, f.ext, f.file_hash] for f in self.ovl_data.files])
		self.included_ovls_view.set_data(self.ovl_data.included_ovl_names)
		logging.info(f"Loaded GUI in {time.time() - start_time:.2f} seconds!")
		self.update_progress("Operation completed!", value=1, vmax=1)

	def save_as_ovl(self):
		if self.is_open_ovl():
			filepath = QtWidgets.QFileDialog.getSaveFileName(
				self, 'Save OVL', os.path.join(self.cfg.get("dir_ovls_out", "C://"), self.file_widget.filename),
				"OVL files (*.ovl)", )[0]
			if filepath:
				self.cfg["dir_ovls_out"], ovl_name = os.path.split(filepath)
				self._save_ovl(filepath)

	def save_ovl(self):
		if self.is_open_ovl():
			self._save_ovl(self.file_widget.filepath)

	def _save_ovl(self, filepath):
		try:
			ext_path = self.dat_widget.filepath if self.use_ext_dat else ""
			self.ovl_data.save(filepath, ext_path)
			self.file_widget.dirty = False
			self.update_progress("Operation completed!", value=1, vmax=1)
		except BaseException as ex:
			traceback.print_exc()
			interaction.showdialog(str(ex))

	def extract_all(self):
		out_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg.get("dir_extract", "C://"), )
		if out_dir:
			self.cfg["dir_extract"] = out_dir
			_out_dir = out_dir
			all_error_files = []
			for ovl in self.handle_path(save_over=False):
				if self.is_open_ovl():
					# for bulk extraction, add the ovl basename to the path to avoid overwriting
					if self.in_folder.isChecked():
						root_dir = self.get_selected_dir()
						rel_p = os.path.relpath(ovl.path_no_ext, start=root_dir)
						out_dir = os.path.join(_out_dir, rel_p)
					try:
						out_paths, error_files = ovl.extract(out_dir, show_temp_files=self.show_temp_files)
						all_error_files += error_files
					except Exception as ex:
						traceback.print_exc()
						interaction.showdialog(str(ex))
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
				error_files, foreign_files = self.ovl_data.inject(files, self.show_temp_files)
				self.file_widget.dirty = True
				if foreign_files:
					if interaction.showdialog(f"Do you want to add {len(foreign_files)} files to this ovl?", ask=True):
						self.ovl_data.add_files(foreign_files)
						self.update_gui_table()
			except Exception as ex:
				traceback.print_exc()
				interaction.showdialog(str(ex))

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
		except BaseException as err:
			print(err)

	def rename(self):
		names = self.get_replace_strings()
		if names:
			for ovl in self.handle_path():
				if self.is_open_ovl():
					self.ovl_data.rename(names, animal_mode=self.t_animal_ovl.isChecked())
					self.update_gui_table()

	def rename_contents(self):
		names = self.get_replace_strings()
		if names:
			if self.check_length(names):
				return
			for ovl in self.handle_path():
				if self.is_open_ovl():
					self.ovl_data.rename_contents(names)
					self.update_gui_table()

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

					self.update_progress("Operation completed!", value=1, vmax=1)
				except BaseException as ex:
					traceback.print_exc()
					interaction.showdialog(str(ex))

	# Save the OVL include list to disk
	def save_included_ovls(self):
		if self.is_open_ovl():
			filelist_src = QtWidgets.QFileDialog.getSaveFileName(
				self, 'ovls.include', os.path.join(self.cfg.get("dir_ovls_out", "C://"), "ovls.include" ),
				"Include file (*.include)", )[0]
			if filelist_src:
				try:
					self.ovl_data.save_included_ovls(filelist_src)
					self.update_progress("Operation completed!", value=1, vmax=1)
				except BaseException as ex:
					traceback.print_exc()
					interaction.showdialog(str(ex))

	def remover(self):
		if self.is_open_ovl():
			selected_file_names = self.files_container.table.get_selected_files()
			# todo - might want to check self.files_container.hasFocus(), but does not seem to work!
			if selected_file_names:
				try:
					remover.file_remover(self.ovl_data, selected_file_names)
				except:
					traceback.print_exc()
				self.update_gui_table()

	def walker_hash(self,):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		walker.generate_hash_table(self, start_dir)
		self.update_progress("Operation completed!", value=1, vmax=1)

	def walker_fgm(self,):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		walker.get_fgm_values(self, start_dir)
		self.update_progress("Operation completed!", value=1, vmax=1)

	def inspect_models(self):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		walker.bulk_test_models(self, start_dir, walk_ovls=True)
		self.update_progress("Operation completed!", value=1, vmax=1)

	def closeEvent(self, event):
		if self.file_widget.dirty:
			quit_msg = f"Quit? You will lose unsaved work on {os.path.basename(self.file_widget.filepath)}!"
			if not interaction.showdialog(quit_msg, ask=True):
				event.ignore()
				return
		event.accept()

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
