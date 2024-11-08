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

		self.game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False,
											  changed_fn=self.game_changed)

		self.stream_entry = QtWidgets.QLineEdit()
		self.stream_entry.setPlaceholderText("Stream")
		self.stream_entry.setToolTip("OVS stream that holds this manis' data")
		# create the table
		header_names = ["Name", "File Type", "Compressed", "Duration", "Frames", "Loc", "Rot", "Scale", "Float"]
		self.files_container = widgets.SortableTable(header_names, (), ignore_drop_type="MANIS", editable_columns=("Name", "Duration", "Compressed"))
		# connect the interaction functions
		self.files_container.table.table_model.member_renamed.connect(self.rename_handle)
		self.files_container.table.table_model.value_edited.connect(self.edit_handle)
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

		self.qgrid = QtWidgets.QVBoxLayout()
		self.qgrid.addWidget(self.file_widget)
		self.qgrid.addWidget(self.game_choice)
		self.qgrid.addWidget(self.stream_entry)
		self.qgrid.addWidget(self.files_container)
		self.qgrid.addWidget(self.progress)
		self.central_widget.setLayout(self.qgrid)

		self.add_to_menu(
			*self.file_menu_functions,
			(widgets.EDIT_MENU, "Append", self.append, "", "append"),
			(widgets.EDIT_MENU, "Duplicate Selected", self.duplicate, "SHIFT+D", "duplicate_mesh"),
			(widgets.EDIT_MENU, "Remove Selected", self.remove, "DEL", "delete_mesh"),
			(widgets.EDIT_MENU, "Show Keys", self.show_keys, "", ""),
			*self.help_menu_functions,
		)

	def game_changed(self, game: Optional[str] = None):
		if game is None:
			game = self.game_choice.entry.currentText()
		logging.info(f"Setting Manis version to {game}")
		self.manis_file.game = game

	def edit_handle(self, name, dtype, new_val):
		logging.debug(f"Editing {dtype} = {new_val} for {name}")
		try:
			mani_info = self.manis_file.get_mani(name)
			logging.info(f"Editing {name}")
			if dtype == "Compressed":
				if mani_info.dtype.compression == 1 and new_val == 0:
					logging.info(f"Decompressing")
					self.manis_file.decompress(mani_info, dump=False)
					mani_info.dtype.compression = 0
					mani_info.dtype.has_list = 0
					k = mani_info.keys
					ck = mani_info.keys.compressed
					# mani_info.keys.set_defaults()
					k.reset_field("pos_bones")
					k.reset_field("ori_bones")
					k.pos_bones[:] = ck.pos_bones
					k.ori_bones[:] = ck.ori_bones
					# k.scl_bones[:] = ck.scl_bones
			if dtype == "Duration":
				logging.info(f"Changing duration to {new_val}")
				mani_info.duration = new_val
		except:
			logging.exception("test")

	def show_keys(self,):
		selected_file_names = self.files_container.table.get_selected_files()
		if selected_file_names:
			for name in selected_file_names:
				mani_info = self.manis_file.get_mani(name)
				self.manis_file.show_floats(mani_info, name_filter="")

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
				print(self.manis_file)
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
						# update context reference on everything do that indexing happens using the correct reference
						mani_info.set_context(self.manis_file.context)
						mani_info.keys.set_context(self.manis_file.context)
					self.set_file_modified(True)
				except:
					self.handle_error("Appending failed, see log!")
				self.update_gui_table()

	def update_gui_table(self, ):
		start_time = time.time()
		try:
			logging.info(f"Loading {len(self.manis_file.mani_infos)} files into GUI")
			self.files_container.set_data([[m.name, ".manis", m.dtype.compression, m.duration, m.frame_count, m.pos_bone_count, m.ori_bone_count, m.scl_bone_count, m.float_count] for m in self.manis_file.mani_infos])
			self.game_choice.entry.setText(self.manis_file.game)
			self.stream_entry.setText(self.manis_file.stream)
			logging.info(f"Loaded GUI in {time.time() - start_time:.2f} seconds")
			self.set_msg_temporarily("Operation completed!")
		except:
			self.handle_error("GUI update failed, see log!")

	def save(self, filepath) -> None:
		try:
			self.manis_file.stream = self.stream_entry.text()
			self.manis_file.save(filepath)
			self.set_file_modified(False)
			self.set_msg_temporarily(f"Saved {self.manis_file.name}")
		except:
			self.handle_error("Saving MANIS failed, see log!")


if __name__ == '__main__':
	startup(MainWindow, GuiOptions(log_name="manis_tool_gui"))
