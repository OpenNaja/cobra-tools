import os
import shutil
import sys
import time
import traceback
import logging
import tempfile


try:
	import numpy as np
	from PyQt5 import QtWidgets, QtGui, QtCore

	from ovl_util.config import logging_setup, get_version_str, get_commit_str

	logging_setup("ovl_tool_gui")

	logging.info(f"Running python {sys.version}")
	logging.info(f"Running cobra-tools {get_version_str()}, {get_commit_str()}")

	from ovl_util import widgets, interaction

	from generated.formats.bnk import BnkFile, AuxFile
	from ovl_util.texconv import write_riff_file
	# from root_path import root_dir
except Exception as err:
	traceback.print_exc()
	time.sleep(15)


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "BNK Editor", )
		self.resize(800, 600)

		self.bnk_file = BnkFile()

		self.filter = "Supported files ({})".format(" ".join("*" + t for t in (".wav", ".wem",)))

		self.file_widget = widgets.FileWidget(self, self.cfg, dtype="BNK")
		self.file_widget.setToolTip("The name of the OVL file that is currently open")

		header_names = ["Name", "File Type", "djb2"]

		# create the table
		self.files_container = widgets.SortableTable(header_names, ())
		# connect the interaction functions
		# self.files_container.table.model.member_renamed.connect(self.rename_handle)
		self.files_container.table.files_dragged.connect(self.drag_files)
		self.files_container.table.files_dropped.connect(self.inject_files)

		right_frame = QtWidgets.QWidget()
		hbox = QtWidgets.QVBoxLayout()
		hbox.addWidget(self.file_widget)
		hbox.addWidget(self.files_container)
		right_frame.setLayout(hbox)

		self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		# self.splitter.addWidget(self.dirs_container)
		self.splitter.addWidget(right_frame)
		self.splitter.setSizes([200, 400])
		self.splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

		self.qgrid = QtWidgets.QGridLayout()

		self.qgrid.addWidget(self.splitter, 5, 0, 1, 5)
		self.qgrid.addWidget(self.p_action, 6, 0, 1, 5)
		self.qgrid.addWidget(self.t_action, 7, 0, 1, 5)

		self.central_widget.setLayout(self.qgrid)

		main_menu = self.menuBar()
		file_menu = main_menu.addMenu('File')
		edit_menu = main_menu.addMenu('Edit')
		button_data = (
			(file_menu, "Open", self.file_widget.ask_open, "CTRL+O", "dir"),
			(file_menu, "Save", self.save_bnk, "CTRL+S", "save"),
			(file_menu, "Save As", self.save_as_bnk, "CTRL+SHIFT+S", "save"),
			(file_menu, "Exit", self.close, "", "exit"),
			(edit_menu, "Unpack", self.extract_all, "CTRL+U", "extract"),
			(edit_menu, "Inject", self.inject_ask, "CTRL+I", "inject")
		)
		self.add_to_menu(button_data)

	def extract_audio(self, out_dir):
		out_files = []

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(out_dir, n))
		# alternatively, bnk_name from bnk header
		bnk_dir, bnk_name = os.path.split(self.file_widget.filepath)
		bnk_name_bare = os.path.splitext(bnk_name)[0]
		for suffix in ("s", "b"):
			# no way of knowing the ovl prefix here
			ovl_basename = ""
			end_str = f"{ovl_basename}_{bnk_name_bare}_bnk_{suffix}.aux"
			logging.info(f"Looking for {end_str} in {bnk_dir}")
			aux_file_names = [f for f in os.listdir(bnk_dir) if f.lower().endswith(end_str)]
			print(os.listdir(bnk_dir))
			print(aux_file_names)
			# aux_path = os.path.join(bnk_dir, f"{ovl_basename}_{bnk_name}_bnk_{suffix}.aux")
			if not aux_file_names:
				logging.warning(f"AUX file expected in {bnk_dir}!")
				continue
			if len(aux_file_names) > 1:
				logging.warning(f"Multiple aux files qualified!")
			aux_file_name = aux_file_names[0]
			aux_file_name_bare = os.path.splitext(aux_file_name)[0]
			aux_path = os.path.join(bnk_dir, aux_file_name)
			if suffix == "s":
				with open(aux_path, "rb") as f:
					for i, stream_info in enumerate(self.bnk_file.bnk_header.stream_infos):
						self.update_progress("Extracting stream", value=i, vmax=len(self.bnk_file.bnk_header.stream_infos))
						f.seek(stream_info.offset)
						d = f.read(stream_info.size)
						out_file = write_riff_file(d, out_dir_func(f"{aux_file_name_bare}_{i}"))
						if out_file:
							out_files.append(out_file)
			if suffix == "b":
				aux = AuxFile()
				aux.load(aux_path)
				out_files.extend(aux.extract_audio(out_dir_func, aux_file_name_bare, self.update_progress))
		return out_files

	def inject_wem(self, wem_file_paths):
		bnk_dir, bnk_name = os.path.split(self.file_widget.filepath)
		for wem_file_path in wem_file_paths:
			logging.info(f"Trying to inject {wem_file_path}")
			aux_path_bare, wem_id = os.path.splitext(wem_file_path)[0].rsplit("_", 1)
			logging.info(f"WEM id: {wem_id} into aux {aux_path_bare}")

			aux_path = f"{aux_path_bare}.aux"
			# check if target aux file exists
			# if os.path.isfile(aux_path):
			# 	pass
			# get the names of the bnk files and make sure they match the input
			media_bnk = self.bnk_file.bnk_header.name
			assert "_media_" in aux_path_bare.lower()
			assert media_bnk.lower() in aux_path_bare.lower()
			events_bnk = f"{media_bnk.rsplit('_', 1)[0]}_events"
			logging.info(f"Media: {media_bnk}, Events: {events_bnk}")
			# aux_path_bare
			# for base_dir in (self.ovl.dir, os.path.dirname(wem_file_path)):

			ovl_basename = os.path.basename(aux_path_bare).lower().split(media_bnk.lower())[0][:-1]
			print(ovl_basename)
			media_path = os.path.join(bnk_dir, f"{ovl_basename}_{media_bnk}_bnk_b.aux")
			events_path = os.path.join(bnk_dir, f"{ovl_basename}_{events_bnk}_bnk_b.aux")
			print(media_path)
			print(events_path)
			if os.path.isfile(media_path) and os.path.isfile(events_path):
				media = AuxFile()
				media.load(media_path)
				media.inject_audio(wem_file_path, wem_id)
				media.save(media_path)

				events = AuxFile()
				events.load(events_path)
				events.inject_hirc(wem_file_path, wem_id)
				events.save(events_path)
				# todo update self.bnk_file.bnk_header.size_b

				logging.info(f"Injected {wem_file_path} {wem_id}")

	def drag_files(self, file_names):
		logging.info(f"DRAGGING {file_names}")
		drag = QtGui.QDrag(self)
		temp_dir = tempfile.mkdtemp("-cobra")
		try:
			out_paths, errors = self.bnk_file.extract(temp_dir, only_names=file_names, show_temp_files=self.show_temp_files)

			data = QtCore.QMimeData()
			data.setUrls([QtCore.QUrl.fromLocalFile(path) for path in out_paths])
			drag.setMimeData(data)
			drag.exec_()
			logging.info(f"Tried to extract {len(file_names)} files, got {len(errors)} errors")
		except:
			self.handle_error("Extraction failed, see log!")
		shutil.rmtree(temp_dir)

	def load(self):
		if self.file_widget.filepath:
			self.file_widget.dirty = False
			try:
				self.bnk_file.load(self.file_widget.filepath)
				print(self.bnk_file)
			except:
				self.handle_error("Loading failed, see log!")
				print(self.bnk_file)
			# self.update_gui_table()

	def is_open_bnk(self):
		if not self.file_widget.filename:
			interaction.showdialog("You must open a BNK file first!")
		else:
			return True

	def update_gui_table(self, ):
		start_time = time.time()
		logging.info(f"Loading {len(self.bnk_file.files)} files into gui")
		self.files_container.set_data([[f.name, f.ext, f.file_hash] for f in self.bnk_file.files])
		self.included_ovls_view.set_data(self.bnk_file.included_ovl_names)
		logging.info(f"Loaded GUI in {time.time() - start_time:.2f} seconds")
		self.update_progress("Operation completed!", value=1, vmax=1)

	def save_as_bnk(self):
		if self.is_open_bnk():
			filepath = QtWidgets.QFileDialog.getSaveFileName(
				self, 'Save BNK', os.path.join(self.cfg.get("dir_ovls_out", "C://"), self.file_widget.filename),
				"BNK files (*.bnk)", )[0]
			if filepath:
				self.cfg["dir_bnks_out"], ovl_name = os.path.split(filepath)
				self._save_bnk(filepath)

	def save_bnk(self):
		if self.is_open_bnk():
			self._save_bnk(self.file_widget.filepath)

	def _save_bnk(self, filepath):
		try:
			ext_path = self.dat_widget.filepath if self.use_ext_dat else ""
			self.bnk_file.save(filepath, ext_path)
			self.file_widget.dirty = False
			self.update_progress(f"Saved {self.bnk_file.basename}", value=1, vmax=1)
		except:
			self.handle_error("Loading failed, see log!")

	def extract_all(self):
		out_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg.get("dir_extract", "C://"), )
		if out_dir:
			self.cfg["dir_extract"] = out_dir
			error_files = []
			try:
				out_files = self.extract_audio(out_dir)
			except:
				self.handle_error("Extracting failed, see log!")
			interaction.extract_error_warning(error_files)

	def inject_ask(self):
		if self.is_open_bnk():
			files = QtWidgets.QFileDialog.getOpenFileNames(
				self, 'Inject files', self.cfg.get("dir_inject", "C://"), self.filter)[0]
			self.inject_files(files)

	def inject_files(self, files):
		"""Tries to inject files into self.bnk_file"""
		if files:
			self.cfg["dir_inject"] = os.path.dirname(files[0])
			try:
				# error_files, foreign_files = self.bnk_file.inject(files, self.show_temp_files)
				error_files = self.inject_wem(files)
				self.file_widget.dirty = True
				# if error_files:
				# 	interaction.showdialog(f"Injection caused errors on {len(error_files)} files, see console for details!")
				self.update_progress("Injection completed", value=1, vmax=1)
			except:
				self.handle_error("Injecting failed, see log!")


if __name__ == '__main__':
	widgets.startup(MainWindow)
