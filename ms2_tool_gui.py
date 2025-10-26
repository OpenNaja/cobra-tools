import time
import logging

from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from gui.widgets import window, MenuItem
from generated.formats.ms2 import Ms2File
from generated.formats.ms2.versions import games
from typing import Optional
from PyQt5 import QtWidgets


class MainWindow(window.MainWindow):

	def __init__(self, opts: GuiOptions):
		window.MainWindow.__init__(self, "MS2 Editor", opts=opts)
		self.setAcceptDrops(True)

		self.ms2_file = Ms2File()

		self.filter = "Supported files (*ms2)"

		self.file_widget = self.make_file_widget(ftype="MS2")

		header_names = ["Name", "File Type", "LODs", "Objects", "Meshes", "Materials"]
		self.game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False,
											  changed_fn=self.game_changed)

		# create the table
		self.files_container = widgets.SortableTable(header_names, (), ignore_drop_type="MS2")
		# connect the interaction functions
		self.files_container.table.table_model.member_renamed.connect(self.rename_handle)
		self.files_container.table.hideColumn(1)

		# Configure table button row
		self.btn_duplicate = widgets.SelectedItemsButton(self, icon=widgets.get_icon("duplicate_mesh"))
		self.btn_duplicate.clicked.connect(self.duplicate)
		self.btn_duplicate.setToolTip("Duplicate Selected Meshes")
		self.btn_delete = widgets.SelectedItemsButton(self, icon=widgets.get_icon("delete_mesh"))
		self.btn_delete.clicked.connect(self.remove)
		self.btn_delete.setToolTip("Delete Selected Meshes")
		# Add buttons to table
		self.files_container.add_button(self.btn_duplicate)
		self.files_container.add_button(self.btn_delete)

		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.file_widget, 0, 0)
		self.qgrid.addWidget(self.game_choice, 1, 0)
		self.qgrid.addWidget(self.files_container, 2, 0)
		self.qgrid.addWidget(self.progress, 3, 0)
		self.central_widget.setLayout(self.qgrid)

		# Setup Menus
		self.build_menus({
			widgets.FILE_MENU: self.file_menu_items,
			widgets.EDIT_MENU: [
				MenuItem("Append", self.append, icon="append"),
				MenuItem("Duplicate Selected", self.duplicate, shortcut="SHIFT+D", icon="duplicate_mesh"),
				MenuItem("Remove Selected", self.remove, shortcut="DEL", icon="delete_mesh"),
			],
			widgets.HELP_MENU: self.help_menu_items
		})

	def game_changed(self, game: Optional[str] = None):
		if game is None:
			game = self.game_choice.entry.currentText()
		logging.info(f"Setting MS2 version to {game}")
		self.ms2_file.game = game

	def rename_handle(self, old_name, new_name):
		"""this manages the renaming of a single entry"""
		# force new name to be lowercase
		new_name = new_name.lower()
		try:
			if self.ms2_file.name_used(new_name):
				self.showwarning(f"Model {new_name} already exists in ms2!")
			# new name is new
			else:
				self.ms2_file.rename_file(old_name, new_name)
				self.set_file_modified(True)
		except:
			self.handle_error("Renaming failed, see log!")
		self.update_gui_table()

	def remove(self):
		selected_file_names = self.files_container.table.get_selected_files()
		if selected_file_names:
			try:
				self.ms2_file.remove(selected_file_names)
				self.set_file_modified(True)
			except:
				self.handle_error("Removing file failed, see log!")
			self.update_gui_table()

	def duplicate(self):
		selected_file_names = self.files_container.table.get_selected_files()
		if selected_file_names:
			try:
				self.ms2_file.duplicate(selected_file_names)
				self.set_file_modified(True)
			except:
				self.handle_error("Duplicating file failed, see log!")
			self.update_gui_table()

	def open(self, filepath):
		if filepath:
			self.set_file_modified(False)
			try:
				# self.ms2_file.load(filepath, read_editable=True, dump=True)
				self.ms2_file.load(filepath, read_editable=True)
				# print(self.ms2_file)
				# for model_info in self.ms2_file.model_infos:
				# 	# model_info.
				# 	model = model_info.model
				# 	for m in model.meshes:
				# 		print(m.mesh.vert_chunks)
				# 		print(m.mesh.tri_chunks)
				# 	break
			except:
				self.handle_error("Loading failed, see log!")
			self.update_gui_table()

	def append(self):
		if self.file_widget.is_open():
			append_path = self.file_widget.get_open_file_name(f'Append MS2')
			if append_path:
				try:
					other_ms2_file = Ms2File()
					other_ms2_file.load(append_path, read_editable=True)
					# ensure that there are no name collisions
					for model in other_ms2_file.model_infos:
						self.ms2_file.make_name_unique(model)
						self.ms2_file.model_infos.append(model)
					self.set_file_modified(True)
				except:
					self.handle_error("Appending failed, see log!")
				self.update_gui_table()

	def update_gui_table(self, ):
		start_time = time.time()
		try:
			logging.info(f"Loading {len(self.ms2_file.mdl_2_names)} files into GUI")
			self.files_container.set_data([[m.name, ".mdl2", m.num_lods, m.num_objects, m.num_meshes, m.num_materials] for m in self.ms2_file.model_infos])
			self.game_choice.entry.setText(self.ms2_file.game)
			logging.info(f"Loaded GUI in {time.time() - start_time:.2f} seconds")
			self.set_progress_message("Operation completed!")
		except:
			self.handle_error("GUI update failed, see log!")

	def save(self, filepath) -> None:
		try:
			self.ms2_file.save(filepath)
			self.set_file_modified(False)
			self.set_progress_message(f"Saved {self.ms2_file.name}")
		except:
			self.handle_error("Saving MS2 failed, see log!")


if __name__ == '__main__':
	startup(MainWindow, GuiOptions(log_name="ms2_tool_gui", size=(600, 600)))
