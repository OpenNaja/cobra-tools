import time
import logging

from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from generated.formats.manis import ManisFile
from generated.formats.manis.versions import games
from typing import Optional
from PyQt5 import QtWidgets


class MainWindow(widgets.MainWindow):

	def __init__(self, opts: GuiOptions):
		widgets.MainWindow.__init__(self, "Manis Editor", opts=opts)
		self.resize(900, 600)
		self.setAcceptDrops(True)

		self.manis_file = ManisFile()

		self.filter = "Supported files (*manis)"

		self.file_widget = self.make_file_widget(ftype="MANIS")

		header_names = ["Name", "File Type", "Stream", "Compressed", "Frames", "Duration", "Loc", "Rot", "Scale", "Float"]
		self.game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False,
											  changed_fn=self.game_changed)

		# create the table
		self.files_container = widgets.SortableTable(header_names, (), ignore_drop_type="MANIS")
		# connect the interaction functions
		self.files_container.table.table_model.member_renamed.connect(self.rename_handle)
		self.files_container.table.hideColumn(1)

		# Configure table button row
		self.btn_duplicate = widgets.SelectedItemsButton(self, icon=widgets.get_icon("duplicate_mesh"))
		self.btn_duplicate.clicked.connect(self.duplicate)
		self.btn_duplicate.setToolTip("Duplicate Selected Mani")
		self.btn_delete = widgets.SelectedItemsButton(self, icon=widgets.get_icon("delete_mesh"))
		self.btn_delete.clicked.connect(self.remove)
		self.btn_delete.setToolTip("Delete Selected Mani")
		# Add buttons to table
		self.files_container.add_button(self.btn_duplicate)
		self.files_container.add_button(self.btn_delete)

		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.file_widget, 0, 0)
		self.qgrid.addWidget(self.game_choice, 1, 0)
		self.qgrid.addWidget(self.files_container, 2, 0)
		self.qgrid.addWidget(self.progress, 3, 0)
		self.central_widget.setLayout(self.qgrid)

		main_menu = self.menu_bar
		file_menu = main_menu.addMenu('File')
		edit_menu = main_menu.addMenu('Edit')
		button_data = (
			(file_menu, "Open", self.file_widget.ask_open, "CTRL+O", "dir"),
			(file_menu, "Append", self.append, "", "append"),
			(file_menu, "Save", self.file_widget.ask_save, "CTRL+S", "save"),
			(file_menu, "Save As", self.file_widget.ask_save_as, "CTRL+SHIFT+S", "save"),
			(file_menu, "Exit", self.close, "", "exit"),
			(edit_menu, "Duplicate Selected", self.duplicate, "SHIFT+D", "duplicate_mesh"),
			(edit_menu, "Remove Selected", self.remove, "DEL", "delete_mesh"),
		)
		self.add_to_menu(button_data)

	def game_changed(self, game: Optional[str] = None):
		if game is None:
			game = self.game_choice.entry.currentText()
		logging.info(f"Setting Manis version to {game}")
		self.manis_file.game = game

	def rename_handle(self, old_name, new_name):
		"""this manages the renaming of a single entry"""
		# force new name to be lowercase
		new_name = new_name.lower()
		try:
			if self.manis_file.name_used(new_name):
				self.showwarning(f"Model {new_name} already exists in MANIS!")
			# new name is new
			else:
				self.manis_file.rename_file(old_name, new_name)
				self.set_file_modified(True)
		except:
			self.handle_error("Renaming failed, see log!")
		self.update_gui_table()

	def remove(self):
		selected_file_names = self.files_container.table.get_selected_files()
		if selected_file_names:
			try:
				self.manis_file.remove(selected_file_names)
				self.set_file_modified(True)
			except:
				self.handle_error("Removing file failed, see log!")
			self.update_gui_table()

	def duplicate(self):
		selected_file_names = self.files_container.table.get_selected_files()
		if selected_file_names:
			try:
				self.manis_file.duplicate(selected_file_names)
				self.set_file_modified(True)
			except:
				self.handle_error("Duplicating file failed, see log!")
			self.update_gui_table()

	def open(self, filepath):
		if filepath:
			self.set_file_modified(False)
			try:
				self.manis_file.load(filepath)
				# print(self.manis_file)
			except:
				self.handle_error("Loading failed, see log!")
			self.update_gui_table()

	def append(self):
		if self.file_widget.is_open():
			append_path = self.file_widget.get_open_file_name(f'Append MANIS')
			if append_path:
				try:
					other_manis_file = ManisFile()
					other_manis_file.load(append_path)
					# ensure that there are no name collisions
					for mani_info in other_manis_file.mani_infos:
						self.manis_file.make_name_unique(mani_info)
						self.manis_file.mani_infos.append(mani_info)
					self.set_file_modified(True)
				except:
					self.handle_error("Appending failed, see log!")
				self.update_gui_table()

	def update_gui_table(self, ):
		start_time = time.time()
		try:
			logging.info(f"Loading {len(self.manis_file.mani_infos)} files into GUI")
			self.files_container.set_data([[m.name, ".manis", self.manis_file.stream, m.dtype.compression, m.frame_count, m.duration, m.pos_bone_count, m.ori_bone_count, m.scl_bone_count, m.float_count] for m in self.manis_file.mani_infos])
			self.game_choice.entry.setText(self.manis_file.game)
			logging.info(f"Loaded GUI in {time.time() - start_time:.2f} seconds")
			self.set_msg_temporarily("Operation completed!")
		except:
			self.handle_error("GUI update failed, see log!")

	def save(self, filepath) -> None:
		try:
			self.manis_file.save(filepath)
			self.set_file_modified(False)
			self.set_msg_temporarily(f"Saved {self.manis_file.name}")
		except:
			self.handle_error("Saving MANIS failed, see log!")


if __name__ == '__main__':
	startup(MainWindow, GuiOptions(log_name="manis_tool_gui"))
