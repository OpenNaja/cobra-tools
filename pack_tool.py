import os
import shutil
import pathlib
import logging
import sys

if __name__ == "__main__":
	from utils.auto_updater import run_update_check

	run_update_check("pack_tool")

from gui import widgets, startup, GuiOptions
from gui.widgets import window, MenuItem, SeparatorMenuItem
from utils.config import Config, save_config, read_str_dict
from utils.logs import logging_setup
from generated.formats.ovl import games, OvlFile
from modules import walker

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, QMenuBar, QCheckBox
from PyQt5 import QtWidgets
from typing import Any, Optional, Callable, Iterable


class PackTool:

	def __init__(self, **kwargs):
		self.folders_to_rebuild = set()
		self.ovl_data = OvlFile()
		self.fs_watcher = None
		# need to use custom getters and setters to inherit, can't overwrite game directly with get/set
		self._game = [g for g in games][0]
		self._watching = False
		self._src_root = ""
		self._dst_root = ""

	@staticmethod
	def run_in_threadpool(func: Callable, callbacks: Iterable = (), *args, **kwargs) -> None:
		print("Skipping threadpool")
		func(*args, **kwargs)
		for callback in callbacks:
			callback()

	def get_non_empty_folders(self, root_folder):
		root = pathlib.Path(root_folder)
		return {os.path.relpath(str(p.parent), root_folder) for p in root.rglob('*') if p.is_file()}

	def load_config_file(self, config_path):
		config_dir, config_name = os.path.split(config_path)
		cfg: Config[str, Any] = Config(config_dir, name=config_name)
		cfg.load()
		self.cfg.update(cfg)
		self.apply_from_config(cfg)

	def rebuild_folders(self):
		logging.info(f"Rebuilding {len(self.folders_to_rebuild)} OVLs")
		for rel_folder in self.folders_to_rebuild:
			self.pack_folder(rel_folder)
		self.folders_to_rebuild.clear()

	def game_changed(self, game: Optional[str] = None):
		if game is None:
			game = self.game
		logging.info(f"Setting OVL version to {game}")
		self.ovl_data.game = game

	def pack_folder(self, rel_folder):
		src_folder = os.path.join(self.src_root, rel_folder)
		dst_path = os.path.join(self.dst_root, rel_folder) + ".ovl"
		if not os.path.exists(src_folder):
			if self.fs_watcher:
				self.fs_watcher.removePath(src_folder)
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
		commands = {"game": self.game, }
		try:
			self.ovl_data.create(src_folder, commands=commands)
			self.ovl_data.save(dst_path)
		except:
			logging.warning("Creating OVL failed, see log!")

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
			self.ovl_data.load(ovl_path, commands={"game": self.game, })
			out_dir = self.ovl_data.get_relative_extract_folder(self.src_root, self.dst_root)
			self.ovl_data.extract(out_dir)
		self.copy_loose_files(self.dst_root, self.src_root)

	@staticmethod
	def copy_loose_files(src_folder, dst_folder):
		for name in ("Manifest.xml", "Readme.md", "Changelog.md", "License"):
			try:
				src_path = os.path.join(src_folder, name)
				dst_path = os.path.join(dst_folder, name)
				if os.path.exists(src_path):
					shutil.copyfile(src_path, dst_path)
			except:
				logging.info(f"Error copying: {name}")

	def apply_from_config(self, cfg: Config[str, Any]):
		# from OVL config
		game = cfg.get("current_game")
		if game:
			self.game = game
		src_recent = cfg.get_recent_files("pack_tool_src", game=game)
		if src_recent:
			self.src_root = src_recent[0]
		dst_recent = cfg.get_recent_files("pack_tool_dst", game=game)
		if dst_recent:
			self.dst_root = dst_recent[0]
		self.watching = cfg.get("watcher_enabled", False)


class PackToolCMD(PackTool):

	def __init__(self):
		super().__init__()
		self.run_in_threadpool(self.ovl_data.load_hash_table)
		print(f"Arguments: {sys.argv[1:]}")
		if len(sys.argv) < 3:
			self.usage("Wrong number of arguments.")

		mptfile = sys.argv[1]
		if os.path.isfile(mptfile):
			tconfig = read_str_dict(mptfile)
			self.game = tconfig['game'] or ''
			self.src_root = tconfig['src_path']
			self.dst_root = tconfig['dst_path']
		else:
			self.game = sys.argv[1]
			self.src_root = sys.argv[3]
			self.dst_root = sys.argv[4]

		action = sys.argv[2]

		if action.lower() == 'pack':
			self.pack_mod()
		elif action.lower() == 'unpack':
			self.unpack_mod()
		else:
			self.usage("Wrong action")
		print("done.\n\n")

	@staticmethod
	def usage(msg):
		print(f"{msg}\n")
		print("Usage: pack_tool.py GAMESTR ACTION folder/src_files folder/ovl_files\n")
		print("* GAMESTR is one of the following:")
		for game in games:
			print(f"  - {game.name}")
		print("* ACTION is one of the following:")
		print("  - PACK (pack loose files from folder/src_files into folder/ovl_files)")
		print("  - UNPACK (extract from folder/ovl_files into folder/src_files)")
		print("")
		print("Alternatively, you can use a .mptconfig file:")
		print("Usage: pack_tool.py path/to/.mptconfig ACTION\n")
		exit()

	@property
	def game(self):
		return self._game

	@game.setter
	def game(self, v):
		if v not in games._member_map_:
			self.usage(f"Wrong game string: {v}")
		self._game = games[v].value

	@property
	def watching(self):
		return self._watching

	@watching.setter
	def watching(self, v):
		self._watching = v

	@property
	def src_root(self):
		return self._src_root

	@src_root.setter
	def src_root(self, v):
		if not os.path.isdir(v):
			self.usage(f"Wrong source path: {v}")
		self._src_root = v

	@property
	def dst_root(self):
		return self._dst_root

	@dst_root.setter
	def dst_root(self, v):
		if not os.path.isdir(v):
			self.usage(f"Wrong destination path: {v}")
		self._dst_root = v


class PackToolGUI(window.MainWindow, PackTool):

	def __init__(self, opts: GuiOptions):

		"""View initializer."""
		super().__init__("PackToolGUI", opts=opts)

		# Set some main window's properties
		self.setWindowTitle('Pack Tool')

		# Setup Menus
		self.build_menus({
			widgets.FILE_MENU: [
				MenuItem("Open Project", self.load_config, shortcut="CTRL+O", icon="dir"),
				MenuItem("Save Project", self.save_config, shortcut="CTRL+S", icon="save"),
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

		self.ovl_game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False,
												  changed_fn=self.game_changed)
		self.boxLayout.addWidget(self.ovl_game_choice)

		self.central_layout.addWidget(self.progress)

		self.reporter = widgets.Reporter()
		self.reporter.progress_percentage.connect(self.set_progress)
		self.reporter.progress_total.connect(self.set_progress_total)
		self.reporter.success_msg.connect(self.set_progress_message)
		self.reporter.current_action.connect(self.set_progress_message)

		self.ovl_data.reporter = self.reporter

		# collect changes from the fs_watcher
		self.rebuild_timer = QtCore.QTimer()
		self.rebuild_timer.setSingleShot(True)
		self.rebuild_timer.setInterval(500)
		self.rebuild_timer.timeout.connect(self.rebuild_folders)

		topleft = QtWidgets.QWidget()
		box = QtWidgets.QVBoxLayout()
		box.addLayout(self.central_layout)
		box.addWidget(self.log_splitter)
		topleft.setLayout(box)

		self.layout_logger(topleft, widgets.LOGGER_BOTTOM)

		self.apply_from_config(self.cfg)

	@property
	def game(self):
		return self.ovl_game_choice.entry.currentText()

	@game.setter
	def game(self, v):
		self.ovl_game_choice.entry.setText(v)

	@property
	def watching(self):
		return self.watch_btn.isChecked()

	@watching.setter
	def watching(self, v):
		self.watch_btn.setChecked(v)

	@property
	def src_root(self):
		return self.src_widget.filepath

	@src_root.setter
	def src_root(self, v):
		self.src_widget.accept_dir(v)

	@property
	def dst_root(self):
		return self.dst_widget.filepath

	@dst_root.setter
	def dst_root(self, v):
		self.dst_widget.accept_dir(v)

	def load_config(self):
		filedialog = QFileDialog(self)
		filedialog.setDefaultSuffix("mptconfig")
		filedialog.setNameFilter("Mod Packing Tool Files (*.mptconfig);;All files (*.*)")
		filedialog.setFileMode(QFileDialog.ExistingFile)
		selected = filedialog.exec()
		if selected:
			config_path = filedialog.selectedFiles()[0]
			self.load_config_file(config_path)
		else:
			logging.info("No file name selected.")
			return

	def save_config(self):
		filedialog = QFileDialog(self)
		filedialog.setDefaultSuffix("mptconfig")
		filedialog.setNameFilter("Mod Packing Tool Files (*.mptconfig);;All files (*.*)")
		filedialog.setAcceptMode(QFileDialog.AcceptSave)
		selected = filedialog.exec()
		if selected:
			cfg_path = filedialog.selectedFiles()[0]
			save_config(cfg_path, self.cfg)
		else:
			logging.info("No file name selected.")
			return

	def directory_dirty(self, watched_folder):
		# logging.info(f'Detected changes in {watched_folder}')
		# read the current folder list and add new subfolders to the watcher
		folders = self.get_non_empty_folders(watched_folder)
		self.watcher_add_folders(folders)

		rel_folder = os.path.relpath(watched_folder, self.src_root)
		if rel_folder == '.':
			return
		self.folders_to_rebuild.add(rel_folder)
		# stop any running timers
		if self.rebuild_timer.isActive():
			self.rebuild_timer.stop()
		self.rebuild_timer.start()

	def watcher_add_folders(self, folders):
		subfolders = ["/".join([self.src_root, x]) for x in folders]
		self.fs_watcher.addPaths(subfolders)

	def watcher_add_files(self, files):
		self.fs_watcher.addPaths(files)

	def watch_btn_clicked(self):
		if not self.src_root:
			logging.info('select source path to enable watch')
			self.watching = False
			return

		if not self.dst_root:
			logging.info('select destination path to enable watch')
			self.watching = False
			return

		self.cfg["watcher_enabled"] = self.watching
		if self.watching:
			logging.info("Watch enabled")
			self.fs_watcher.directoryChanged.connect(self.directory_dirty)
			# self.fs_watcher.fileChanged.connect(self.file_changed)
			self.watch_settings_changed(self.src_root)
		else:
			logging.info("Watch disabled")
			self.fs_watcher.directoryChanged.disconnect(self.directory_dirty)
		# self.fs_watcher.fileChanged.disconnect(self.file_changed)

	def watch_settings_changed(self, dirpath):
		if self.watching:
			folders = self.get_non_empty_folders(dirpath)
			self.watcher_add_folders(folders)
			self.watcher_add_files(walker.walk_type(self.src_root, extension=""))


if __name__ == '__main__':
	if len(sys.argv) == 1:
		startup(PackToolGUI,
				GuiOptions(log_name="pack_tool", size=(400, 150),
						   check_update=False  # Check update happens at top now
						   ))
	else:
		logging_setup("ovl_tool_cmd")
		PackToolCMD()