import sys
import time
import logging

try:
	from ovl_util.config import logging_setup, get_version_str, get_commit_str
	logging_setup("ms2_tool_gui")
	logging.info(f"Running python {sys.version}")
	logging.info(f"Running cobra-tools {get_version_str()}, {get_commit_str()}")

	# Import widgets before everything except Python built-ins and ovl_util.config!
	from ovl_util import widgets, interaction
	from ovl_util.widgets import get_icon
	from generated.formats.ms2 import Ms2File
	from PyQt5 import QtWidgets, QtGui, QtCore
except:
	logging.exception(f"Some modules could not be imported; make sure you install the required dependencies with pip!")
	time.sleep(15)


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "MS2 Editor", )
		self.resize(600, 600)
		self.setAcceptDrops(True)

		self.ms2_file = Ms2File()

		self.filter = "Supported files (*ms2)"

		self.file_widget = self.make_file_widget(dtype="MS2")

		header_names = ["Name", "File Type", "LODs", "Objects", "Meshes", "Materials"]

		# create the table
		self.files_container = widgets.SortableTable(header_names, (), ignore_drop_type="MS2")
		# connect the interaction functions
		self.files_container.table.table_model.member_renamed.connect(self.rename_handle)
		self.files_container.table.hideColumn(1)

		# Configure table button row
		self.btn_duplicate = widgets.SelectedItemsButton(self, icon=get_icon("duplicate_mesh"))
		self.btn_duplicate.clicked.connect(self.duplicate)
		self.btn_duplicate.setToolTip("Duplicate Selected Meshes")
		self.btn_delete = widgets.SelectedItemsButton(self, icon=get_icon("delete_mesh"))
		self.btn_delete.clicked.connect(self.remove)
		self.btn_delete.setToolTip("Delete Selected Meshes")
		# Add buttons to table
		self.files_container.add_button(self.btn_duplicate)
		self.files_container.add_button(self.btn_delete)

		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.file_widget, 0, 0)
		self.qgrid.addWidget(self.files_container, 1, 0)
		self.qgrid.addWidget(self.p_action, 2, 0)
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

	def rename_handle(self, old_name, new_name):
		"""this manages the renaming of a single entry"""
		# force new name to be lowercase
		new_name = new_name.lower()
		try:
			if self.ms2_file.name_used(new_name):
				interaction.showwarning(f"Model {new_name} already exists in ms2!")
			# new name is new
			else:
				self.ms2_file.rename_file(old_name, new_name)
				self.file_widget.dirty = True
		except:
			self.handle_error("Renaming failed, see log!")
		self.update_gui_table()

	def remove(self):
		selected_file_names = self.files_container.table.get_selected_files()
		if selected_file_names:
			try:
				self.ms2_file.remove(selected_file_names)
				self.file_widget.dirty = True
			except:
				self.handle_error("Removing file failed, see log!")
			self.update_gui_table()

	def duplicate(self):
		selected_file_names = self.files_container.table.get_selected_files()
		if selected_file_names:
			try:
				self.ms2_file.duplicate(selected_file_names)
				self.file_widget.dirty = True
			except:
				self.handle_error("Duplicating file failed, see log!")
			self.update_gui_table()

	def load(self, filepath):
		if filepath:
			self.file_widget.dirty = False
			try:
				self.ms2_file.load(filepath, read_editable=True)
			except:
				self.handle_error("Loading failed, see log!")
			self.update_gui_table()

	def append(self):
		if self.file_widget.is_open():
			append_path = QtWidgets.QFileDialog.getOpenFileName(
				self, f'Append MS2', self.cfg.get(f"dir_ms2s_in", "C://"), self.file_widget.files_filter_str)[0]
			if append_path:
				try:
					other_ms2_file = Ms2File()
					other_ms2_file.load(append_path, read_editable=True)
					# ensure that there are no name collisions
					for model in other_ms2_file.model_infos:
						self.ms2_file.make_name_unique(model)
						self.ms2_file.model_infos.append(model)
					self.file_widget.dirty = True
				except:
					self.handle_error("Appending failed, see log!")
				self.update_gui_table()

	def update_gui_table(self, ):
		start_time = time.time()
		try:
			logging.info(f"Loading {len(self.ms2_file.mdl_2_names)} files into gui")
			self.files_container.set_data([[m.name, ".mdl2", m.num_lods, m.num_objects, m.num_meshes, m.num_materials] for m in self.ms2_file.model_infos])
			logging.info(f"Loaded GUI in {time.time() - start_time:.2f} seconds")
			self.update_progress("Operation completed!", value=100, vmax=100)
		except:
			self.handle_error("GUI update failed, see log!")

	def _save(self, ):
		try:
			self.ms2_file.save(self.file_widget.filepath)
			self.file_widget.dirty = False
			self.update_progress(f"Saved {self.ms2_file.name}", value=100, vmax=100)
		except:
			self.handle_error("Saving MS2 failed, see log!")


if __name__ == '__main__':
	widgets.startup(MainWindow)
