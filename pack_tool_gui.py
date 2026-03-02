import os
import shutil
import pathlib
import logging


if __name__ == "__main__":
	from utils.auto_updater import run_update_check
	run_update_check("pack_tool_gui")

from gui import widgets, startup, GuiOptions
from gui.widgets import window, MenuItem, SeparatorMenuItem
from utils.config import read_str_dict, write_str_dict
from generated.formats.ovl import games, OvlFile
from modules import walker

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
		self.src_widget = widgets.DirWidget(self, self.cfg, cfg_key="pack_tool_src")
		self.src_widget.setPlaceholderText("Source Folder")
		self.src_widget.setToolTip("Source folder to gather loose files from.")
		self.central_layout.addWidget(self.src_widget)
		self.src_widget.dir_opened.connect(self.watch_settings_changed)

		self.dst_widget = widgets.DirWidget(self, self.cfg, cfg_key="pack_tool_dst")
		self.dst_widget.setPlaceholderText("Destination Folder")
		self.dst_widget.setToolTip("Destination folder to pack OVL files into.")
		self.central_layout.addWidget(self.dst_widget)

		# Add a line for controls
		self.boxLayout = QHBoxLayout()
		self.boxLayout.addStretch(1)
		self.central_layout.addLayout(self.boxLayout)

		# Add a button
		self.watch_btn = QCheckBox("Watch changes")
		self.watch_btn.setToolTip("Watch the source folder for changes and rebuild OVLs accordingly")
		self.watch_btn.setChecked(False)
		self.watch_btn.stateChanged.connect(self.watch_btn_clicked)
		self.boxLayout.addWidget(self.watch_btn)
		self.fs_watcher = QtCore.QFileSystemWatcher()

		self.ovl_game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False, changed_fn=self.game_changed)
		self.boxLayout.addWidget(self.ovl_game_choice)

		self.central_layout.addWidget(self.progress)

		self.ovl_data = OvlFile()
		self.reporter = widgets.Reporter()
		self.ovl_data.reporter = self.reporter

		self.reporter.progress_percentage.connect(self.set_progress)
		self.reporter.progress_total.connect(self.set_progress_total)
		self.reporter.success_msg.connect(self.set_progress_message)
		self.reporter.current_action.connect(self.set_progress_message)
		self.run_in_threadpool(self.ovl_data.load_hash_table)

		# collect changes from the fs_watcher
		self.rebuild_timer = QtCore.QTimer()
		self.rebuild_timer.setSingleShot(True)
		self.rebuild_timer.setInterval(500)
		self.rebuild_timer.timeout.connect(self.rebuild_folders)
		self.folders_to_rebuild = set()

		topleft = QtWidgets.QWidget()
		box = QtWidgets.QVBoxLayout()
		box.addLayout(self.central_layout)
		box.addWidget(self.log_splitter)
		topleft.setLayout(box)

		self.layout_logger(topleft, widgets.LOGGER_BOTTOM)

		# from OVL config
		game = self.cfg.get("current_game")
		if game:
			self.ovl_game_choice.entry.setText(game)
		src_recent = self.cfg.get_recent_files("pack_tool_src", game=game)
		if src_recent:
			self.src_widget.accept_dir(src_recent[0])
		dst_recent = self.cfg.get_recent_files("pack_tool_dst", game=game)
		if dst_recent:
			self.dst_widget.accept_dir(dst_recent[0])
		self.watch_btn.setChecked(self.cfg.get("watcher_enabled", False))

	def rebuild_folders(self):
		logging.info(f"Rebuilding {self.folders_to_rebuild}")
		for rel_folder in self.folders_to_rebuild:
			self.pack_folder(rel_folder)
		self.folders_to_rebuild.clear()

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
		# self.apply_from_config(self.config_path)

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
			tconfig = {'src_path': self.src_root, 'dst_path': self.dst_root,
					   'game': self.ovl_game_choice.entry.currentText(), 'watcher_enabled': self.watch_btn.isChecked()}
			write_str_dict(self.config_path, tconfig)
		except IOError:
			logging.info("Config save failed.")

	def game_changed(self, game: Optional[str] = None):
		if game is None:
			game = self.ovl_game_choice.entry.currentText()
		logging.info(f"Setting OVL version to {game}")
		self.ovl_data.game = game

	def directory_dirty(self, watched_folder):
		logging.info(f'Detected changes in {watched_folder}')
		# read the current folder list and proceed to pack that folder
		folders = self.get_non_empty_folders(self.src_root)
		self.watcher_add_folders(folders)

		rel_folder = os.path.relpath(watched_folder, self.src_root)
		# todo - new ovls should also be added / renamed?
		# was the change caused by adding a new folder in root?
		if rel_folder == '.':
			return

		self.folders_to_rebuild.add(rel_folder)
		# stop any running timers
		if self.rebuild_timer.isActive():
			self.rebuild_timer.stop()
		self.rebuild_timer.start()

	def get_non_empty_folders(self, root_folder):
		root = pathlib.Path(root_folder)
		return {os.path.relpath(str(p.parent), root_folder) for p in root.rglob('*') if p.is_file()}

	def watcher_add_folders(self, folders):
		subfolders = ["/".join([self.src_root, x]) for x in folders]
		self.fs_watcher.addPaths(subfolders)

	def watcher_add_files(self, files):
		self.fs_watcher.addPaths(files)

	def watch_btn_clicked(self):
		if not self.src_root:
			logging.info('select source path to enable watch')
			self.watch_btn.setChecked(False)
			return

		if not self.dst_root:
			logging.info('select destination path to enable watch')
			self.watch_btn.setChecked(False)
			return

		self.cfg["watcher_enabled"] = self.watch_btn.isChecked()
		if self.watch_btn.isChecked():
			logging.info("Watch enabled")
			self.fs_watcher.directoryChanged.connect(self.directory_dirty)
			# self.fs_watcher.fileChanged.connect(self.file_changed)
			self.watch_settings_changed(self.src_root)
		else:
			logging.info("Watch disabled")
			self.fs_watcher.directoryChanged.disconnect(self.directory_dirty)
			# self.fs_watcher.fileChanged.disconnect(self.file_changed)


	def watch_settings_changed(self, dirpath):
		folders = self.get_non_empty_folders(dirpath)
		self.watcher_add_folders(folders)
		self.watcher_add_files(walker.walk_type(self.src_root, extension=""))

	def pack_folder(self, rel_folder):
		src_path = os.path.join(self.src_root, rel_folder)
		dst_path = os.path.join(self.dst_root, rel_folder) + ".ovl"
		if not os.path.exists(src_path):
			self.fs_watcher.removePath(src_path)
			return
		logging.info(f"Packing {rel_folder}")

		if not self.src_root:
			logging.warning(f"Source must be set")
			return
		dst_folder = os.path.dirname(dst_path)
		if not os.path.exists(dst_folder):
			os.makedirs(dst_folder)

		# clear the ovl
		self.ovl_data.clear()
		self.game_changed()
		try:
			self.ovl_data.create(src_path)
			self.ovl_data.save(dst_path)
		except:
			self.handle_error("Creating OVL failed, see log!")

	def copy_loose_files(self, src_folder, dst_folder):
		for name in ("Manifest.xml", "Readme.md", "Changelog.md", "License"):
			try:
				src_path = os.path.join(src_folder, name)
				dst_path = os.path.join(dst_folder, name)
				if os.path.exists(src_path):
					shutil.copyfile(src_path, dst_path)
			except:
				logging.info(f"Error copying: {name}")

	def pack_mod(self):
		logging.info("Packing mod")
		for rel_folder in self.get_non_empty_folders(self.src_root):
			# ignore the project root for packing
			if rel_folder == '.':
				continue
			self.pack_folder(rel_folder)

		self.copy_loose_files(self.src_root, self.dst_root)

	def unpack_mod(self):
		if self.src_root and self.dst_root:
			self.run_in_threadpool(self._unpack_mod, (), )

	def _unpack_mod(self):
		logging.info("Unpacking mod")
		for ovl_path in walker.walk_type(self.dst_root, extension=".ovl"):
			self.ovl_data.load(ovl_path, commands={"game": self.ovl_game_choice.entry.currentText(), })
			out_dir = self.ovl_data.get_relative_extract_folder(self.src_root, self.dst_root)
			self.ovl_data.extract(out_dir)
		self.copy_loose_files(self.dst_root, self.src_root)
		
	@property
	def src_root(self):
		return self.src_widget.filepath
	
	@property
	def dst_root(self):
		return self.dst_widget.filepath

if __name__ == '__main__':
	startup(PackToolGUI, GuiOptions(log_name="pack_tool_gui", size=(400, 150), check_update=False  # Check update happens at top now
	))
