#!/usr/bin/env python3

# Filename: mod_tool_gui.py

"""Mod Packing tool"""

# TODO: split getting src folder list, watcher folder should contain all 
# directiories, or it wont detect changes in empty folders.

import sys
import os
import shutil
import pathlib
import logging

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QCheckBox

from ovl_util import widgets
from ovl_util.config import logging_setup, get_version_str, get_commit_str, read_str_dict, write_str_dict

logging_setup("mod_tool_gui")
logging.info(f"Running python {sys.version}")
logging.info(f"Running cobra-tools {get_version_str()}, {get_commit_str()}")

from ovl_util.widgets import startup, MainWindow, OvlReporter
from generated.formats.ovl import games, set_game

__version__ = '0.1'
__author__ = 'Open-Naja'


class ModToolGUI(MainWindow):
	"""Main's View (GUI)."""

	def __init__(self):

		"""View initializer."""
		super().__init__("ModToolGUI")

		# save config file name from args
		self.config_path = ''

		# Set some main window's properties
		self.setWindowTitle('Mod Pack Tool ' + __version__)
		# self.setFixedSize(435, 250)

		# Add a menu
		main_menu = QMenuBar(self)
		file_menu = main_menu.addMenu('File')
		help_menu = main_menu.addMenu('Help')
		button_data = (
			(file_menu, "Open", self.load_config, "CTRL+O", "dir"),
			(file_menu, "Save", self.save_config, "CTRL+S", "save"),
			(file_menu, "Pack", self.pack_mod, "CTRL+P", "inject"),
			(file_menu, "Unpack", self.unpack_mod, "CTRL+U", "extract"),
			(file_menu, "Exit", self.close, "", "exit"),
			(help_menu, "Report Bug", self.report_bug, "", "report"),
			(help_menu, "Documentation", self.online_support, "", "manual"))
		self.add_to_menu(button_data)
		self.setMenuBar(main_menu)

		# Set the central widget
		self.generalLayout = QVBoxLayout()
		self._centralWidget = QWidget()
		self._centralWidget.setLayout(self.generalLayout)
		self.setCentralWidget(self._centralWidget)

		# Add app widgets
		self.src_widget = widgets.DirWidget(self, {})
		self.src_widget.setToolTip("Source folder to pack files from.")
		self.generalLayout.addWidget(self.src_widget)

		self.dst_widget = widgets.DirWidget(self, {})
		self.dst_widget.setToolTip("Destination folder to pack files to.")
		self.generalLayout.addWidget(self.dst_widget)

		# Add a line for controls
		self.boxLayout = QHBoxLayout()
		self.boxLayout.addStretch(1)
		self.generalLayout.addLayout(self.boxLayout)

		# Add a button
		self.watch = QCheckBox("Watch changes")
		self.watch.setToolTip("Experimental")
		self.watch.setChecked(False)
		self.watch.stateChanged.connect(self.watchChanged)
		self.boxLayout.addWidget(self.watch)
		self.fs_watcher = ''

		self.game_container = widgets.LabelCombo("Game:", [g.value for g in games])
		self.boxLayout.addWidget(self.game_container)

		self.generalLayout.addWidget(self.p_action)
		self.generalLayout.addWidget(self.t_action)

		if len(sys.argv) > 1:
			self.apply_from_config(sys.argv[1])

		self.ovl_data = OvlReporter()
		# self.ovl_data.load_hash_table()
		self.run_threaded(self.ovl_data.load_hash_table)

	def apply_from_config(self, path):
		try:
			tconfig = read_str_dict(path)
			self.src_widget.filepath = tconfig['src_path'] or ''
			self.src_widget.setText(tconfig['src_path'] or '')
			self.dst_widget.filepath = tconfig['dst_path'] or ''
			self.dst_widget.setText(tconfig['dst_path'] or '')
			self.game_container.entry.setText(tconfig['game'] or '')
			self.watch.setChecked(bool(tconfig['watcher_enabled']) or False)
		except IOError:
			logging.info("Config load failed.")
		pass

	def load_config(self):
		filedialog = QFileDialog(self)
		filedialog.setDefaultSuffix("mptconfig")
		filedialog.setNameFilter("Mod Packing Tool Files (*.mptconfig);;All files (*.*)")
		filedialog.setFileMode(QFileDialog.ExistingFile)
		selected = filedialog.exec()
		if selected:
			self.config_path = filedialog.selectedFiles()[0]
		else:
			return
		if self.config_path == "":
			logging.info("No file name selected.")
			return
		self.apply_from_config(self.config_path)

	def save_config(self):
		filedialog = QFileDialog(self)
		filedialog.setDefaultSuffix("mptconfig")
		filedialog.setNameFilter("Mod Packing Tool Files (*.mptconfig);;All files (*.*)")
		filedialog.setAcceptMode(QFileDialog.AcceptSave)
		selected = filedialog.exec()
		if selected:
			self.config_path = filedialog.selectedFiles()[0]
		else:
			return
		if self.config_path == "":
			logging.info("No file name selected.")
			return
		try:
			tconfig = {'src_path': self.src_widget.filepath, 'dst_path': self.dst_widget.filepath,
					   'game': self.game_container.entry.currentText(), 'watcher_enabled': self.watch.isChecked()}
			write_str_dict(self.config_path, tconfig)
		except IOError:
			logging.info("Config save failed.")

	def set_src_path(self, sPath):
		self.src_widget.setText(sPath)
		pass

	def set_dst_path(self, sPath):
		self.dst_widget.setText(sPath)
		pass

	def game_changed(self, ):
		game = self.game_container.entry.currentText()
		# we must set both the context, and the local variable
		set_game(self.ovl_data.context, game)
		set_game(self.ovl_data, game)

	def directory_changed(self, path):
		logging.info(f'Detected changes in {path}')
		# read the current folder list and proceed to pack that folder
		folders = self.get_src_folder_list()
		self.watcher_add_folders(folders)

		basepath = self.src_widget.filepath
		relpath = os.path.relpath(path, basepath)
		if relpath == '.':
			return

		logging.info(f're-packing ovl: {relpath}')
		self.pack_folder(relpath)

	def file_changed(self, path):
		logging.info(f'Detected file changes in {path}')

	def get_src_folder_list(self, basepath=''):

		if basepath == '':
			basepath = self.src_widget.filepath

		root = pathlib.Path(basepath)
		non_empty_dirs = {os.path.relpath(str(p.parent), basepath) for p in root.rglob('*') if p.is_file()}

		return non_empty_dirs

	def get_dst_folder_list(self, basepath=''):

		if basepath == '':
			basepath = self.dst_widget.filepath

		root = pathlib.Path(basepath)
		non_empty_dirs = {os.path.relpath(str(p.parent), basepath) for p in root.rglob('*') if p.is_file()}

		return non_empty_dirs

	def get_src_file_list(self):
		file_list = []
		if self.src_widget.filepath:
			for (dirpath, dirnames, filenames) in os.walk(self.src_widget.filepath):
				file_list += [os.path.join(dirpath, file) for file in filenames]

		return file_list

	def get_dst_file_list(self, basepath=''):

		if basepath == '':
			basepath = self.dst_widget.filepath

		file_list = list()
		for (dirpath, dirnames, filenames) in os.walk(basepath):
			file_list += [os.path.join(dirpath, file) for file in filenames]

		return file_list

	def watcher_add_folders(self, folders):
		if self.fs_watcher:
			srcpath = self.src_widget.filepath
			subfolders = ["/".join([srcpath, x]) for x in folders]
			self.fs_watcher.addPaths(subfolders)

	def watcher_add_files(self, files):
		if self.fs_watcher:
			srcpath = self.src_widget.filepath
			self.fs_watcher.addPaths(files)

	def watchChanged(self):
		if self.src_widget.filepath == '':
			logging.info('select source path to enable watch')
			self.watch.setChecked(False)
			return

		if self.dst_widget.filepath == '':
			logging.info('select destination path to enable watch')
			self.watch.setChecked(False)
			return

		if self.watch.isChecked():
			self.fs_watcher = QtCore.QFileSystemWatcher()
			self.fs_watcher.directoryChanged.connect(self.directory_changed)
			self.fs_watcher.fileChanged.connect(self.file_changed)
			folders = self.get_src_folder_list()
			self.watcher_add_folders(folders)
			files = self.get_src_file_list()
			self.watcher_add_files(files)
			logging.info("Watch enabled")
		else:
			self.watch.setChecked(False)
			logging.info("Watch disabled")
			self.fs_watcher.directoryChanged.disconnect(self.directory_changed)
			self.fs_watcher.fileChanged.disconnect(self.file_changed)

	def settings_changed(self):
		basepath = self.src_widget.filepath
		folders = self.get_src_folder_list()
		self.watcher_add_folders(folders)
		files = self.get_src_file_list()
		self.watcher_add_files(files)

	def create_ovl(self, ovl_dir, dst_file):
		# clear the ovl
		self.ovl_data = OvlReporter()
		self.game_changed()
		try:
			self.ovl_data.create(ovl_dir)
			self.ovl_data.save(dst_file)
			return True
		except:
			logging.exception(f"Could not create OVL from {ovl_dir}")
			return False

	# relative path
	def pack_folder(self, folder):
		logging.info(f"Packing {folder}")
		srcbasepath = self.src_widget.filepath
		dstbasepath = self.dst_widget.filepath

		if not srcbasepath:
			logging.warning(f"Source must be set")
			return
		src_path = os.path.join(srcbasepath, folder)
		dst_file = os.path.join(dstbasepath, folder) + ".ovl"
		dst_path = os.path.dirname(dst_file)
		if not os.path.exists(dst_path):
			os.makedirs(dst_path)

		self.create_ovl(src_path, dst_file)

	# file has full path.
	def unpack_ovl(self, file):
		srcbasepath = self.src_widget.filepath
		dstbasepath = self.dst_widget.filepath
		dstfolder = os.path.relpath(file, dstbasepath)
		logging.info(f"Unpacking {dstfolder}")
		filename = os.path.splitext(os.path.basename(dstfolder))[0]
		srcfolder = os.path.join(srcbasepath, os.path.dirname(dstfolder), filename)

		if not os.path.exists(srcfolder):
			logging.info(srcfolder)
			os.makedirs(srcfolder)

		self.ovl_data.load(file)
		out_paths, error_files = self.ovl_data.extract(srcfolder, show_temp_files=False)

	def copy_file(self, srcpath, dstpath, fname):
		try:
			shutil.copyfile(os.path.join(srcpath, fname), os.path.join(dstpath, fname))
		except:
			logging.info(f"error copying: {fname}")

	def pack_mod(self):
		logging.info("Packing mod")
		subfolders = self.get_src_folder_list()
		for folder in subfolders:
			# ignore the project root for packing
			if folder == '.':
				# logging.info(f"Skipping {folder}: root")
				continue
			self.pack_folder(folder)

		# Also copy Manifest.xml and Readme.md files if any
		srcbasepath = self.src_widget.filepath
		dstbasepath = self.dst_widget.filepath
		self.copy_file(srcbasepath, dstbasepath, "Manifest.xml")
		self.copy_file(srcbasepath, dstbasepath, "Readme.md")
		self.copy_file(srcbasepath, dstbasepath, "License")

	def unpack_mod(self):
		srcbasepath = self.src_widget.filepath
		dstbasepath = self.dst_widget.filepath
		if not srcbasepath or not dstbasepath:
			return

		logging.info("Unpacking mod")
		dstfiles = self.get_dst_file_list()

		for file in dstfiles:
			# ignore all other files, unpack ovl files only.
			if file.lower().endswith(".ovl"):
				self.unpack_ovl(file)
				continue

		# The previous loop will not copy Manifest.xml and Readme.md files if any
		self.copy_file(dstbasepath, srcbasepath, "Manifest.xml")
		self.copy_file(dstbasepath, srcbasepath, "Readme.md")
		self.copy_file(dstbasepath, srcbasepath, "License")


if __name__ == '__main__':
	startup(ModToolGUI)
