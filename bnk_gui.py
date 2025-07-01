import os
import shutil
import logging
import tempfile
from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from gui.widgets import MenuItem
from generated.formats.bnk import BnkFile, AuxFile
from ovl_util.texconv import write_riff_file
from modules.formats.shared import fmt_hash

from PyQt5 import QtWidgets, QtGui, QtCore


class MainWindow(widgets.MainWindow):

	def __init__(self, opts: GuiOptions):
		widgets.MainWindow.__init__(self, "BNK Editor", opts=opts)
		self.bnk_file = BnkFile()

		self.filter = "Supported files ({})".format(" ".join("*" + t for t in (".wav", ".wem",)))

		self.file_widget = self.make_file_widget(ftype="BNK")

		header_names = ["Name", "File Type", "File Size"]

		# create the table
		self.files_container = widgets.SortableTable(header_names, ())
		# connect the interaction functions
		# self.files_container.table.table_model.member_renamed.connect(self.rename_handle)
		self.files_container.table.files_dragged.connect(self.drag_files)
		self.files_container.table.files_dropped.connect(self.inject_files)

		right_frame = QtWidgets.QWidget()
		hbox = QtWidgets.QVBoxLayout()
		hbox.addWidget(self.file_widget)
		hbox.addWidget(self.files_container)
		right_frame.setLayout(hbox)

		self.qgrid = QtWidgets.QGridLayout()

		self.qgrid.addWidget(right_frame, 5, 0, 1, 5)
		self.qgrid.addWidget(self.progress, 6, 0, 1, 5)

		self.central_widget.setLayout(self.qgrid)

		self.build_menus({
			widgets.FILE_MENU: self.file_menu_items,
			widgets.EDIT_MENU: [
				MenuItem("Unpack", self.extract_all, shortcut="CTRL+U", icon="extract"),
				MenuItem("Inject", self.inject_ask, shortcut="CTRL+I", icon="inject"),
			],
			widgets.HELP_MENU: self.help_menu_items
		})

	def extract_audio(self, out_dir, hashes=()):
		out_files = []

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(out_dir, n))
		if not hashes:
			hashes = self.bnk_file.data_map.keys()
		for id_hash in hashes:
			data, aux_name = self.bnk_file.data_map[id_hash]
			out_file = write_riff_file(data, out_dir_func(f"{aux_name}_{id_hash}"))
			if out_file:
				out_files.append(out_file)
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

				logging.info(f"Injected {wem_file_path} {wem_id}")

	def drag_files(self, file_names):
		drag = QtGui.QDrag(self)
		temp_dir = tempfile.mkdtemp("-cobra")
		try:
			out_paths = self.extract_audio(temp_dir, file_names)

			data = QtCore.QMimeData()
			data.setUrls([QtCore.QUrl.fromLocalFile(path) for path in out_paths])
			drag.setMimeData(data)
			drag.exec_()
			logging.info(f"Tried to extract {len(file_names)} files")
		except:
			self.handle_error("Extraction failed, see log!")
		shutil.rmtree(temp_dir)

	def open(self, filepath):
		if filepath:
			self.set_file_modified(False)
			try:
				self.bnk_file.load(filepath)
				print(self.bnk_file)
				print(self.bnk_file.aux_b)
				f_list = [(fmt_hash(stream_info.event_id), "s", stream_info.size) for stream_info in self.bnk_file.bnk_header.streams]
				if self.bnk_file.aux_b and self.bnk_file.aux_b.didx:
					f_list.extend([(pointer.hash, "b", pointer.wem_filesize) for pointer in self.bnk_file.aux_b.didx.data_pointers])
				f_list.sort(key=lambda t: (t[1], t[0]))
				self.files_container.set_data(f_list)
			except:
				self.handle_error("Loading failed, see log!")
				# print(self.bnk_file)

	def is_open_bnk(self):
		if not self.file_widget.filename:
			self.showwarning("You must open a BNK file first!")
		else:
			return True

	def save(self, filepath) -> None:
		try:
			self.bnk_file.save(filepath)
			self.set_file_modified(False)
			self.set_progress_message(f"Saved {self.bnk_file.bnk_name}")
		except:
			self.handle_error("Loading failed, see log!")

	def extract_all(self):
		out_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg.get("dir_extract", "C://"), )
		if out_dir:
			self.cfg["dir_extract"] = out_dir
			try:
				out_files = self.extract_audio(out_dir)
			except:
				self.handle_error("Extracting failed, see log!")

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
				error_files = self.inject_wem(files)
				self.set_file_modified(True)
				self.set_progress_message("Injection completed")
			except:
				self.handle_error("Injecting failed, see log!")


if __name__ == '__main__':
	startup(MainWindow, GuiOptions("bnk_gui"))
