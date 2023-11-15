import os
import shutil
import sys
import logging
from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from gui.widgets import Reporter
from ovl_util.logs import HtmlFormatter, AnsiFormatter, get_stdout_handler
from generated.formats.ovl import games, OvlFile
from generated.formats.ovl_base.enums.Compression import Compression
from PyQt5 import QtWidgets, QtGui, QtCore
from typing import Any, Optional

class MainWindow(widgets.MainWindow):

	def __init__(self, opts: GuiOptions):
		widgets.MainWindow.__init__(self, "LOC Tool", opts=opts)
		self.resize(1200, 600)
		self.setAcceptDrops(True)

		self.reporter = Reporter()
		self.ovl_data = OvlFile()
		self.ovl_data.reporter = self.reporter

		self.game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False, changed_fn=self.game_changed)

		self.compression_choice = widgets.LabelCombo("Compression", [c.name for c in Compression], editable=False, changed_fn=self.compression_changed)

		if "games" not in self.cfg:
			self.cfg["games"] = {}
		self.installed_games = widgets.GamesWidget(self, game_chosen_fn=self.populate_game, file_dbl_click_fn=self.open_clicked_file)

		self.files_container = widgets.SortableTable(["ID", "Localisation"], {}, ignore_drop_type="OVL", opt_hide=True, min_width=30)

		left_frame = QtWidgets.QWidget()
		hbox = QtWidgets.QVBoxLayout()
		hbox.addWidget(self.game_choice)
		hbox.addWidget(self.compression_choice)
		hbox.addWidget(self.installed_games)
		hbox.addWidget(self.installed_games.dirs)
		hbox.setContentsMargins(0, 0, 1, 0)
		hbox.setSizeConstraint(QtWidgets.QVBoxLayout.SizeConstraint.SetNoConstraint)
		left_frame.setLayout(hbox)

		right_frame = QtWidgets.QWidget()
		hbox = QtWidgets.QVBoxLayout()
		hbox.setContentsMargins(3, 0, 0, 0)
		hbox.addWidget(self.files_container)		
		hbox.setSizeConstraint(QtWidgets.QVBoxLayout.SizeConstraint.SetNoConstraint)
		right_frame.setLayout(hbox)

		self.file_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
		self.file_splitter.addWidget(left_frame)
		self.file_splitter.addWidget(right_frame)
		self.file_splitter.setSizes([100, 500])
		self.file_splitter.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
		self.file_splitter.setContentsMargins(0, 0, 0, 0)

		grid = QtWidgets.QGridLayout()

		self.stdout_handler = get_stdout_handler("loc_tool_gui")  # self.log_name not set until after init
		# Setup Logger
		# TODO: From cfg
		orientation = QtCore.Qt.Orientation.Vertical
		# TODO: From cfg
		show_logger = True
		topleft = self.file_splitter
		if orientation == QtCore.Qt.Orientation.Vertical:
			self.file_splitter.setContentsMargins(5, 0, 5, 0)
			grid.setContentsMargins(5, 0, 5, 5)
			self.central_layout.addLayout(grid)
			self.central_layout.setSpacing(5)
		else:
			topleft = QtWidgets.QWidget()
			box = QtWidgets.QVBoxLayout()
			box.addLayout(grid)
			box.addWidget(self.file_splitter)
			topleft.setLayout(box)
		# Layout Logger
		if show_logger:
			self.layout_logger(topleft, orientation)
		else:
			self.central_layout.addWidget(topleft)

		# Setup Menus
		main_menu = self.menu_bar
		file_menu = main_menu.addMenu('File')
		edit_menu = main_menu.addMenu('Edit')
		util_menu = main_menu.addMenu('Util')
		help_menu = main_menu.addMenu('Help')
		button_data = (
			(help_menu, "Report Bug", self.report_bug, "", "report"),
			(help_menu, "Documentation", self.online_support, "", "manual"))
		self.add_to_menu(button_data)


	def populate_game(self, current_game=None):
		if current_game is None:
			current_game = self.cfg.get("current_game")
		logging.debug(f"Setting Current Game to {current_game}")
		if self.installed_games.set_selected_game(current_game):
			self.game_choice.entry.setText(current_game)

	def open_clicked_file(self, filepath: str):
		# handle double clicked file paths
		try:
			if filepath.lower().endswith(".ovl"):
				self.file_widget.open_file(filepath)
		except:
			self.handle_error("Clicked dir failed, see log!")

	def game_changed(self, game: Optional[str] = None):
		if game is None:
			game = self.game_choice.entry.currentText()
		logging.info(f"Setting OVL version to {game}")
		self.ovl_data.game = game

	def compression_changed(self, compression: str):
		compression_value = Compression[compression]
		self.ovl_data.user_version.compression = compression_value

if __name__ == '__main__':
	startup(MainWindow, GuiOptions(log_name="loc_tool_gui"))