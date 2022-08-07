import os
import sys
import time
import traceback
import logging


try:
	from ovl_util.config import logging_setup, get_version_str, get_commit_str
	logging_setup("ms2_tool_gui")
	logging.info(f"Running python {sys.version}")
	logging.info(f"Running cobra-tools {get_version_str()}, {get_commit_str()}")

	import numpy as np
	from PyQt5 import QtWidgets, QtGui, QtCore
	from ovl_util import widgets, interaction
	from generated.formats.ms2 import Ms2File
except Exception as err:
	traceback.print_exc()
	time.sleep(15)


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "MS2 Editor", )
		self.resize(600, 600)

		self.ms2_file = Ms2File()

		self.filter = "Supported files (*ms2)"

		self.file_widget = widgets.FileWidget(self, self.cfg, dtype="MS2")
		self.file_widget.setToolTip("The name of the MS2 file that is currently open")

		header_names = ["Name", "File Type", "LODs", "Objects", "Meshes", "Materials"]

		# create the table
		self.files_container = widgets.SortableTable(header_names, ())
		# connect the interaction functions
		self.files_container.table.model.member_renamed.connect(self.rename_handle)
		self.files_container.table.hideColumn(1)

		# Configure table button row
		self.btn_duplicate = QtWidgets.QPushButton()
		self.btn_duplicate.setIcon(widgets.get_icon("duplicate_mesh"))
		self.btn_duplicate.clicked.connect(self.duplicate)
		self.btn_duplicate.setToolTip("Duplicate Selected Meshes")
		self.btn_delete = QtWidgets.QPushButton()
		self.btn_delete.setIcon(widgets.get_icon("delete_mesh"))
		self.btn_delete.clicked.connect(self.remove)
		self.btn_delete.setToolTip("Delete Selected Meshes")
		# Add buttons to table
		self.files_container.add_button(self.btn_duplicate)
		self.files_container.add_button(self.btn_delete)

		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.file_widget, 0, 0)
		self.qgrid.addWidget(self.files_container, 1, 0)
		self.qgrid.addWidget(self.p_action, 2, 0)
		self.qgrid.addWidget(self.t_action, 3, 0)
		self.central_widget.setLayout(self.qgrid)

		main_menu = self.menuBar()
		file_menu = main_menu.addMenu('File')
		edit_menu = main_menu.addMenu('Edit')
		button_data = (
			(file_menu, "Open", self.file_widget.ask_open, "CTRL+O", "dir"),
			(file_menu, "Save", self.save_ms2, "CTRL+S", "save"),
			(file_menu, "Save As", self.save_as_ms2, "CTRL+SHIFT+S", "save"),
			(file_menu, "Exit", self.close, "", "exit"),
			(edit_menu, "Duplicate Selected", self.duplicate, "SHIFT+D", "duplicate_mesh"),
			(edit_menu, "Remove Selected", self.remove, "DEL", "delete_mesh"),
		)
		self.add_to_menu(button_data)

	def rename_handle(self, old_name, new_name):
		"""this manages the renaming of a single entry"""
		new_name = new_name.lower()
		try:
			# force new name to be lowercase
			for model_info in self.ms2_file.model_infos:
				if model_info.name == new_name:
					interaction.showdialog(f"Model {new_name} already exists in ms2!")
					break
			# none was found, new name is new
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

	def load(self):
		if self.file_widget.filepath:
			self.file_widget.dirty = False
			try:
				self.ms2_file.load(self.file_widget.filepath, read_editable=True)
			except:
				self.handle_error("Loading failed, see log!")
			self.update_gui_table()

	def is_open_ms2(self):
		if not self.file_widget.filename:
			interaction.showdialog("You must open a MS2 file first!")
		else:
			return True

	def update_gui_table(self, ):
		start_time = time.time()
		try:
			logging.info(f"Loading {len(self.ms2_file.mdl_2_names)} files into gui")
			self.files_container.set_data([[m.name, ".mdl2", m.num_lods, m.num_objects, m.num_meshes, m.num_materials] for m in self.ms2_file.model_infos])
			logging.info(f"Loaded GUI in {time.time() - start_time:.2f} seconds")
			self.update_progress("Operation completed!", value=1, vmax=1)
		except:
			self.handle_error("GUI update failed, see log!")

	def save_as_ms2(self):
		if self.is_open_ms2():
			filepath = QtWidgets.QFileDialog.getSaveFileName(
				self, 'Save MS2', os.path.join(self.cfg.get("dir_ms2s_out", "C://"), self.file_widget.filename),
				"MS2 files (*.ms2)", )[0]
			if filepath:
				self.cfg["dir_ms2s_out"], ms2_name = os.path.split(filepath)
				self.file_widget._set_file_path(filepath)
				self._save_ms2()

	def save_ms2(self):
		if self.is_open_ms2():
			self._save_ms2()

	def _save_ms2(self, ):
		try:
			self.ms2_file.save(self.file_widget.filepath)
			self.file_widget.dirty = False
			self.update_progress(f"Saved {self.ms2_file.name}", value=1, vmax=1)
		except:
			self.handle_error("Saving OVL failed, see log!")


if __name__ == '__main__':
	widgets.startup(MainWindow)
