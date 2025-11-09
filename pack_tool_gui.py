import os
import sys
import time
import shutil
import pathlib
import logging
from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from gui.widgets import window, MenuItem, SeparatorMenuItem
from utils.config import read_str_dict, write_str_dict
from utils.logs import HtmlFormatter, AnsiFormatter
from generated.formats.ovl import games, OvlFile

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, QMenuBar, QCheckBox
from PyQt5 import QtWidgets
from typing import Any, Optional

__version__ = '0.1'
__author__ = 'Open-Naja'


class PackToolGUI(window.MainWindow):
	"""Main's View (GUI)."""

	def __init__(self, opts: GuiOptions):

		"""View initializer."""
		super().__init__("PackToolGUI", opts=opts)

		# save config file name from args
		self.config_path = ''

		# Set some main window's properties
		self.setWindowTitle('Pack Tool ' + __version__)

		# Setup Menus
		self.build_menus({
			widgets.FILE_MENU: [
				MenuItem("Open", self.load_config, shortcut="CTRL+O", icon="dir"),
				MenuItem("Save", self.save_config, shortcut="CTRL+S", icon="save"),
				SeparatorMenuItem(),
				MenuItem("Pack", self.pack_mod, shortcut="CTRL+P", icon="inject"),
				MenuItem("Unpack", self.unpack_mod, shortcut="CTRL+U", icon="extract"),
				SeparatorMenuItem(),
				MenuItem("Exit", self.close, icon="exit"),
			],
			widgets.VIEW_MENU: self.view_menu_items,
			widgets.HELP_MENU: self.help_menu_items,
		})

		# Add app widgets
		self.src_widget = widgets.DirWidget(self, self.cfg, cfg_key="pack_tool")
		self.src_widget.setPlaceholderText("Source Folder")
		self.src_widget.setToolTip("Source folder to pack files from.")
		self.central_layout.addWidget(self.src_widget)
		self.src_widget.dir_opened.connect(self.settings_changed)

		self.dst_widget = widgets.DirWidget(self, self.cfg, cfg_key="pack_tool")
		self.dst_widget.setPlaceholderText("Destination Folder")
		self.dst_widget.setToolTip("Destination folder to pack files to.")
		self.central_layout.addWidget(self.dst_widget)

		# Add a line for controls
		self.boxLayout = QHBoxLayout()
		self.boxLayout.addStretch(1)
		self.central_layout.addLayout(self.boxLayout)

		# Add a button
		self.watch = QCheckBox("Watch changes")
		self.watch.setToolTip("Experimental")
		self.watch.setChecked(False)
		self.watch.stateChanged.connect(self.watchChanged)
		self.boxLayout.addWidget(self.watch)
		self.fs_watcher = ''

		self.game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False, changed_fn=self.game_changed)
		self.boxLayout.addWidget(self.game_choice)

		self.central_layout.addWidget(self.progress)

		self.ovl_data = OvlFile()
		self.run_in_threadpool(self.ovl_data.load_hash_table)

		topleft = QtWidgets.QWidget()
		box = QtWidgets.QVBoxLayout()
		box.addLayout(self.central_layout)
		box.addWidget(self.log_splitter)
		topleft.setLayout(box)

		self.layout_logger(topleft, widgets.LOGGER_BOTTOM)

		if len(sys.argv) > 1:
			self.apply_from_config(sys.argv[1])



	def apply_from_config(self, path):
		try:
			tconfig = read_str_dict(path)
			self.src_widget.filepath = tconfig['src_path'] or ''
			self.src_widget.setText(tconfig['src_path'] or '')
			self.dst_widget.filepath = tconfig['dst_path'] or ''
			self.dst_widget.setText(tconfig['dst_path'] or '')
			self.game_choice.entry.setText(tconfig['game'] or '')
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
					   'game': self.game_choice.entry.currentText(), 'watcher_enabled': self.watch.isChecked()}
			write_str_dict(self.config_path, tconfig)
		except IOError:
			logging.info("Config save failed.")

	def set_src_path(self, sPath):
		self.src_widget.setText(sPath)
		pass

	def set_dst_path(self, sPath):
		self.dst_widget.setText(sPath)
		pass

	def game_changed(self, game: Optional[str] = None):
		if game is None:
			game = self.game_choice.entry.currentText()
		logging.info(f"Setting OVL version to {game}")
		self.ovl_data.game = game

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

	def settings_changed(self, dirpath):
		folders = self.get_src_folder_list(dirpath)
		self.watcher_add_folders(folders)
		files = self.get_src_file_list()
		self.watcher_add_files(files)

	def create_ovl(self, ovl_dir, dst_file):
		# clear the ovl
		self.ovl_data.clear()
		self.game_changed()
		try:
			self.ovl_data.create(ovl_dir)
			self.ovl_data.save(dst_file)
		except:
			self.handle_error("Creating OVL failed, see log!")

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
	startup(PackToolGUI, GuiOptions(log_name="pack_tool_gui", size=(400, 150)))
