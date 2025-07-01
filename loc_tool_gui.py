import os
import shutil
import sys
import logging
from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from gui.widgets import Reporter
from ovl_util.logs import get_stdout_handler
from generated.formats.ovl import games, OvlFile
from generated.formats.ovl_base.enums.Compression import Compression
from PyQt5 import QtWidgets, QtGui, QtCore
from typing import Any, Optional


class MainWindow(widgets.MainWindow):

	def __init__(self, opts: GuiOptions):
		widgets.MainWindow.__init__(self, "LOC Tool", opts=opts)
		self.setAcceptDrops(True)

		self.reporter = Reporter()
		self.ovl_data = OvlFile()
		self.ovl_data.reporter = self.reporter

		self.game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False, changed_fn=self.game_changed)

		self.compression_choice = widgets.LabelCombo("Compression", [c.name for c in Compression], editable=False, changed_fn=self.compression_changed)

		if "games" not in self.cfg:
			self.cfg["games"] = {}
		self.installed_games = widgets.GamesWidget(self, game_chosen_fn=self.populate_game, file_dbl_click_fn=self.open_clicked_file)

		self.files_container = widgets.SortableTable(["ID", "Localisation"], {}, ignore_drop_type="OVL", opt_hide=True)

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

		grid = QtWidgets.QGridLayout()

		self.stdout_handler = get_stdout_handler("loc_tool_gui")  # self.log_name not set until after init
		self.layout_splitter(grid, left_frame, right_frame)

		# Setup Menus
		self.build_menus({
			widgets.HELP_MENU: self.help_menu_items,
		})

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
	startup(MainWindow, GuiOptions(log_name="loc_tool_gui", size=(1200, 600)))
