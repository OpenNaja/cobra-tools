import os
import sys
import time
import traceback
import logging
import tempfile

from ovl_util.interaction import showdialog

try:
	import numpy as np
	from PyQt5 import QtWidgets, QtGui, QtCore
	from importlib import reload

	from ovl_util import widgets, interaction, qt_threads
	from modules import extract, inject, hasher, walker, remover
	from generated.formats.ovl import OvlFile, games, get_game, set_game
except Exception as err:
	traceback.print_exc()
	time.sleep(15)


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "OVL Archive Editor", )
		self.resize(800, 600)

		self.ovl_data = OvlFile(progress_callback=self.update_progress)

		self.filter = "Supported files ({})".format(" ".join("*" + t for t in extract.SUPPORTED_TYPES))

		self.file_widget = widgets.FileWidget(self, self.cfg)
		self.file_widget.setToolTip("The name of the OVL file that is currently open.")

		self.p_action = QtWidgets.QProgressBar(self)
		self.p_action.setGeometry(0, 0, 200, 15)
		self.p_action.setTextVisible(True)
		self.p_action.setMaximum(1)
		self.p_action.setValue(0)
		self.t_action_current_message = "No operation in progress"
		self.t_action = QtWidgets.QLabel(self, text=self.t_action_current_message)

		self.game_container = widgets.LabelCombo("Game:", games)
		# only listen to user changes
		self.game_container.entry.textActivated.connect(self.game_changed)
		self.game_container.entry.setEditable(False)

		header_names = ["Name", "File Type", "DJB", "Unk0", "Unk1"]

		# create the table
		self.files_container = widgets.SortableTable(header_names)
		# connect the interaction functions
		self.files_container.table.model.member_renamed.connect(self.rename_handle)
		self.files_container.table.files_dragged.connect(self.drag_files)
		self.files_container.table.files_dropped.connect(self.inject_files)
		self.files_container.table.file_selected.connect(self.show_dependencies)

		self.dir_container = widgets.EditCombo(self)
		# toggles
		self.t_show_temp_files = QtWidgets.QCheckBox("Save Temp Files")
		self.t_show_temp_files.setToolTip(
			"By default, temporary files are converted to usable ones and back on the fly.")
		self.t_show_temp_files.setChecked(False)

		self.t_2K = QtWidgets.QCheckBox("Inject 2K")
		self.t_2K.setToolTip("Experimental: Increase a JWE Diffuse or Normal map to 2048x2048 resolution.")
		self.t_2K.setChecked(False)

		self.sp_hash = QtWidgets.QCheckBox("New Species Hash")
		self.sp_hash.setToolTip("Experimental")
		self.sp_hash.setChecked(False)

		self.ext_dat = QtWidgets.QCheckBox("Use External DAT")
		self.ext_dat.setToolTip("Experimental: Save the ovl with an external STATIC DAT instead of one in memory")
		self.ext_dat.setChecked(False)
		self.ext_dat.stateChanged.connect(self.dat_show)

		self.dat_widget = widgets.FileWidget(self, self.cfg, ask_user=False, dtype="DAT", poll=False)
		self.dat_widget.setToolTip("External .dat file path")
		self.dat_widget.hide()

		self.e_name_old = QtWidgets.QLineEdit("old")
		self.e_name_new = QtWidgets.QLineEdit("new")

		self.t_write_dat = QtWidgets.QCheckBox("Save DAT")
		self.t_write_dat.setToolTip("Writes decompressed archive streams to DAT files for debugging.")
		self.t_write_dat.setChecked(False)
		self.t_write_dat.stateChanged.connect(self.load)

		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.file_widget, 0, 0, 1, 5)
		self.qgrid.addWidget(self.t_show_temp_files, 1, 0)
		self.qgrid.addWidget(self.t_write_dat, 1, 1)
		self.qgrid.addWidget(self.ext_dat, 1, 2)
		self.qgrid.addWidget(self.sp_hash, 1, 3)
		self.qgrid.addWidget(self.e_name_old, 2, 0, 1, 2)
		self.qgrid.addWidget(self.e_name_new, 2, 2, 1, 2)
		self.qgrid.addWidget(self.game_container, 2, 4,)
		self.qgrid.addWidget(self.files_container, 3, 0, 1, 5)
		self.qgrid.addWidget(self.dir_container, 4, 0, 1, 5)
		self.qgrid.addWidget(self.p_action, 5, 0, 1, 5)
		self.qgrid.addWidget(self.t_action, 6, 0, 1, 5)
		self.qgrid.addWidget(self.dat_widget, 7, 0, 1, 5)
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
			(file_menu, "Exit", self.close, "", "exit"),
			(edit_menu, "Unpack", self.extract_all, "CTRL+U", "extract"),
			(edit_menu, "Inject", self.inject_ask, "CTRL+I", "inject"),
			(edit_menu, "Rename", self.hasher, "CTRL+R", ""),
			(edit_menu, "Dat Edit", self.dat_replacement, "CTRL+J", ""),
			(edit_menu, "Remove Selected", self.remover, "DEL", ""),
			(util_menu, "Inspect Models", self.walker, "", ""),
			(util_menu, "Generate Hash Table", self.walker_hash, "", ""),
			(util_menu, "Save Frag Log", self.ovl_data.write_frag_log, "", ""),
			(util_menu, "Open Tools Dir", self.open_tools_dir, "", ""),
			# (edit_menu, "Reload", self.reload, "", ""),
			(help_menu, "Report Bug", self.report_bug, "", "report"),
			(help_menu, "Documentation", self.online_support, "", "manual"))
		self.add_to_menu(button_data)
		self.check_version()
		self.load_hash_table()

	def open_tools_dir(self):
		os.startfile(os.getcwd())

	def drag_files(self, file_names):
		print("DRAGGING", file_names)
		drag = QtGui.QDrag(self)
		try:
			temp_dir = tempfile.gettempdir()
			out_paths, errors, skips = self.ovl_data.extract(
				temp_dir, only_names=file_names, show_temp_files=self.show_temp_files)

			data = QtCore.QMimeData()
			data.setUrls([QtCore.QUrl.fromLocalFile(path) for path in out_paths])
			drag.setMimeData(data)
			drag.exec_()
		except BaseException as ex:
			traceback.print_exc()
			showdialog(str(ex))
			print(ex)

	# todo - clear temp sub dir
	# mime = DelayedMimeData()
	# path_list = []
	# for name in names:
	# 	path = os.path.join(tempfile.gettempdir(), 'DragTest', name)
	# 	os.makedirs(os.path.dirname(path), exist_ok=True)
	#
	# 	def write_to_file(path=path, contents=name, widget=self):
	# 		if widget.underMouse():
	# 			return False
	# 		else:
	# 			with open(path, 'w') as f:
	# 				import time
	# 				# time.sleep(1)  # simulate large file
	# 				f.write(contents)
	#
	# 			return True
	#
	# 	mime.add_callback(write_to_file)
	#
	# 	path_list.append(QtCore.QUrl.fromLocalFile(path))
	# mime.setUrls(path_list)
	# drag.setMimeData(mime)
	# drag.exec_(QtCore.Qt.CopyAction)

	def rename_handle(self, old_name, new_name):
		names = [(old_name, new_name), ]
		hasher.rename(self.ovl_data, names, species_mode=self.species_hash)
		self.update_gui_table()

	def game_changed(self,):
		game = self.game_container.entry.currentText()
		set_game(self.ovl_data, game)

	@property
	def commands(self, ):
		# get those commands that are set to True
		return [x for x in ("write_dat", ) if getattr(self, x)]

	@property
	def show_temp_files(self, ):
		return self.t_show_temp_files.isChecked()

	@property
	def write_2K(self, ):
		return self.t_2K.isChecked()

	@property
	def species_hash(self, ):
		return self.sp_hash.isChecked()

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

	def load_hash_table(self):
		print("Loading hash table...")
		start_time = time.time()
		self.hash_table = {}
		hashes_dir = os.path.join(os.getcwd(), "hashes")
		try:
			for file in os.listdir(hashes_dir):
				self.read_table(os.path.join(hashes_dir, file), self.hash_table, int_key=True)
		except:
			pass
		# print(self.hash_table)
		print(f"Loaded {len(self.hash_table)} hash - name pairs in {time.time() - start_time:.2f} seconds.")

	def show_dependencies(self, file_index):
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

	@staticmethod
	def read_table(fp, dic, int_key=False):
		if fp.endswith(".txt"):
			with open(fp, "r") as f:
				for line in f:
					line = line.strip()
					if line:
						k, v = line.split(" = ")
						if int_key:
							dic[int(k)] = v
						else:
							dic[k] = v

	def load(self):
		if self.file_widget.filepath:
			self.file_widget.dirty = False
			try:
				# runTask(self.ovl_data.load, (self.file_widget.filepath,), {"commands": self.commands, "hash_table": self.hash_table})
				# test(2)
				# self.ovl_thread.func = self.ovl_thread.ovl_data.load
				# self.ovl_thread.args = (self.file_widget.filepath,)
				# self.ovl_thread.kwargs = {"commands": self.commands, "hash_table": self.hash_table}
				# self.ovl_thread.start()
				self.ovl_data.load(self.file_widget.filepath, commands=self.commands, hash_table=self.hash_table)
				# print(self.ovl_data)
			except Exception as ex:
				traceback.print_exc()
				interaction.showdialog(str(ex))
			self.update_gui_table()
			game = get_game(self.ovl_data)
			self.game_container.entry.setText(game)

	def create_ovl(self, ovl_dir):
		# clear the ovl
		self.ovl_data = OvlFile(progress_callback=self.update_progress)
		self.game_changed()

		# read tables for constants
		mimes_table = {}
		tables_dir = os.path.join(os.getcwd(), "dicts")
		self.read_table(os.path.join(tables_dir, "mimes.txt"), mimes_table)
		try:
			self.ovl_data.create(ovl_dir, mime_names_dict=mimes_table)
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
		print(f"Loading {len(self.ovl_data.files)} files into gui...")
		self.files_container.set_data([[f.name, f.ext, f.file_hash, f.unkn_0, f.unkn_1] for f in self.ovl_data.files])
		self.dir_container.set_data(self.ovl_data.dir_names)
		print(f"Loaded GUI in {time.time() - start_time:.2f} seconds!")
		self.update_progress("Operation completed!", value=1, vmax=1)

	def save_ovl(self):
		if self.is_open_ovl():
			file_src = QtWidgets.QFileDialog.getSaveFileName(
				self, 'Save OVL', os.path.join(self.cfg.get("dir_ovls_out", "C://"), self.file_widget.filename),
				"OVL files (*.ovl)", )[0]
			if file_src:
				self.cfg["dir_ovls_out"], ovl_name = os.path.split(file_src)
				try:
					ext_path = self.dat_widget.filepath if self.use_ext_dat else ""
					self.ovl_data.save(file_src, ext_path)
					self.file_widget.dirty = False
					self.update_progress("Operation completed!", value=1, vmax=1)
				except BaseException as ex:
					traceback.print_exc()
					interaction.showdialog(str(ex))

	def extract_all(self):
		if self.is_open_ovl():
			out_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder',
																 self.cfg.get("dir_extract", "C://"), )
			if out_dir:
				self.cfg["dir_extract"] = out_dir
				try:
					out_paths, error_files, skip_files = self.ovl_data.extract(out_dir, show_temp_files=self.show_temp_files)
					interaction.skip_messages(error_files, skip_files)
				except Exception as ex:
					traceback.print_exc()
					interaction.showdialog(str(ex))

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
				inject.inject(self.ovl_data, files, self.show_temp_files, self.write_2K, self.update_progress)
				self.file_widget.dirty = True
			except Exception as ex:
				traceback.print_exc()
				interaction.showdialog(str(ex))

	def hasher(self):
		if self.is_open_ovl():
			names = [(self.e_name_old.text(), self.e_name_new.text())]
			hasher.rename(self.ovl_data, names, species_mode=self.species_hash)
			self.update_gui_table()

	def dat_replacement(self):
		if self.is_open_ovl():
			names = [(self.e_name_old.text(), self.e_name_new.text())]
			if self.species_hash:
				hasher.species_dat_replacer(self.ovl_data, names)
			else:
				hasher.dat_replacer(self.ovl_data, names)
			self.update_gui_table()

	# reload modules, debug feature, allows reloading extraction modules without restarting the gui
	# modules need to be imported completely, import xxxx, from xxx import yyy will not work.
	# def reload(self):
	# 	reload(modules.formats.SPECDEF)
	# 	reload(modules.extract)

	def remover(self):
		if self.is_open_ovl():
			selected_file_names = self.files_container.table.get_selected_files()
			if selected_file_names:
				try:
					remover.file_remover(self.ovl_data, selected_file_names)
				except:
					traceback.print_exc()
				self.update_gui_table()

	def walker_hash(self,):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"))
		walker.generate_hash_table(self, start_dir)

	def walker(self):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"), )
		walker.bulk_test_models(self, start_dir)

	def closeEvent(self, event):
		if self.file_widget.dirty:
			quit_msg = f"Quit? You will lose unsaved work on {os.path.basename(self.file_widget.filepath)}!"
			if not interaction.showdialog(quit_msg, ask=True):
				event.ignore()
				return
		event.accept()

	@staticmethod
	def check_version():
		is_64bits = sys.maxsize > 2 ** 32
		if not is_64bits:
			interaction.showdialog("Either your operating system or your python installation is not 64 bits.\n"
										"Large OVLs will crash unexpectedly!")
		if sys.version_info[0] != 3 or sys.version_info[1] < 7 or (
				sys.version_info[1] == 7 and sys.version_info[2] < 6):
			interaction.showdialog("Python 3.7.6+ x64 bit is expected!")


if __name__ == '__main__':
	print("running python", sys.version)
	widgets.startup(MainWindow)
