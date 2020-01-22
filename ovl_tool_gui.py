import os
import io
import sys
import traceback
import time
from PyQt5 import QtWidgets
import numpy as np

from pyffi_ext.formats.ovl import OvlFormat
from pyffi_ext.formats.ms2 import Ms2Format
from util import widgets
from modules import extract, inject, hasher, walker


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "OVL Tool", )
		
		self.ovl_data = OvlFormat.Data()

		supported_types = ("DDS", "PNG", "MDL2", "TXT", "FGM", "FDB", "MATCOL", "XMLCONFIG", "ASSETPKG", "LUA")
		self.filter = "Supported files ({})".format( " ".join("*."+t for t in supported_types) )

		self.file_widget = widgets.FileWidget(self, self.cfg)
		self.file_widget.setToolTip("The name of the OVL file that is currently open.")

		self.e_name_pairs = [ (QtWidgets.QLineEdit("old"), QtWidgets.QLineEdit("new")) for i in range(3) ]

		# toggles
		self.t_write_dds = QtWidgets.QCheckBox("Save DDS")
		self.t_write_dds.setToolTip("By default, DDS files are converted to PNG and back on the fly.")
		self.t_write_dds.setChecked(False)
		
		self.t_write_dat = QtWidgets.QCheckBox("Save DAT")
		self.t_write_dat.setToolTip("Writes decompressed archive streams to DAT files for debugging.")
		self.t_write_dat.setChecked(False)
		self.t_write_dat.stateChanged.connect(self.load_ovl)

		self.t_write_frag_log = QtWidgets.QCheckBox("Save Frag Log")
		self.t_write_frag_log.setToolTip("For devs.")
		self.t_write_frag_log.setChecked(False)
		self.t_write_frag_log.stateChanged.connect(self.load_ovl)

		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.file_widget, 0, 0, 1, 2)
		self.qgrid.addWidget(self.t_write_dds, 1, 0)
		self.qgrid.addWidget(self.t_write_dat, 2, 0)
		self.qgrid.addWidget(self.t_write_frag_log, 3, 0)
		start = 4
		for i, (old, new) in enumerate(self.e_name_pairs):
			self.qgrid.addWidget(old, start+i, 0)
			self.qgrid.addWidget(new, start+i, 1)

		self.central_widget.setLayout(self.qgrid)

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('File')
		editMenu = mainMenu.addMenu('Edit')
		helpMenu = mainMenu.addMenu('Help')
		button_data = ((fileMenu, "Open", self.file_widget.ask_open, "CTRL+O"),
					   (fileMenu, "Save", self.save_ovl, "CTRL+S"),
					   (fileMenu, "Exit", self.close, ""),
					   (editMenu, "Unpack", self.extract_all, "CTRL+U"),
					   (editMenu, "Inject", self.inject, "CTRL+I"),
					   (editMenu, "Hash", self.hasher, "CTRL+H"),
					   (editMenu, "Walk", self.walker, ""),
					   (helpMenu, "Report Bug", self.report_bug, ""),
					   (helpMenu, "Documentation", self.online_support, ""))
		self.add_to_menu(button_data)
		self.check_version()

	@property
	def commands(self,):
		# get those commands that are set to True
		return [ x for x in ("write_dat", "write_frag_log") if getattr(self, x)]
	
	def update_commands(self):
		# at some point, just set commands to archive and trigger changes there
		if self.ovl_name:
			self.ovl_data.commands = self.commands

	@property
	def ovl_name(self,):
		return self.file_widget.text()

	@property
	def write_dds(self,):
		return self.t_write_dds.isChecked()
	
	@property
	def write_dat(self,):
		return self.t_write_dat.isChecked()

	@property
	def write_frag_log(self,):
		return self.t_write_frag_log.isChecked()

	def load_ovl(self):
		if self.file_widget.filepath:
			self.file_widget.dirty = False
			self.cfg["dir_ovls_in"], ovl_name = os.path.split(self.file_widget.filepath)
			start_time = time.time()
			try:
				with open(self.file_widget.filepath, "rb") as ovl_stream:
					self.ovl_data.read(ovl_stream, file=self.file_widget.filepath, commands=self.commands)
				self.file_widget.setText(ovl_name)
			except Exception as ex:
				traceback.print_exc()
				widgets.showdialog( str(ex) )
				print(ex)
			print(f"Done in {time.time()-start_time:.2f} seconds!")
		
	def save_ovl(self):
		if self.ovl_name:
			file_src = QtWidgets.QFileDialog.getSaveFileName(self, 'Save OVL', os.path.join(self.cfg["dir_ovls_out"], self.ovl_name), "OVL files (*.ovl)",)[0]
			if file_src:
				self.cfg["dir_ovls_out"], ovl_name = os.path.split(file_src)
				# just a dummy stream
				with io.BytesIO() as ovl_stream:
					self.ovl_data.write(ovl_stream, file_path=file_src)
				self.file_widget.dirty = False
				print("Done!")
			
	def extract_all(self):
		if self.ovl_name:
			self.cfg["dir_extract"] = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg["dir_extract"], )
			if self.cfg["dir_extract"]:
				dir = self.cfg["dir_extract"]
				# create output dir
				try:
					os.makedirs(dir, exist_ok=True)
					for archive in self.ovl_data.archives:
						archive.dir = dir
						extract.extract(archive, self.write_dds)
					print("Done!")
				except Exception as ex:
					traceback.print_exc()
					widgets.showdialog( str(ex) )
					print(ex)
		else:
			widgets.showdialog( "You must open an OVL file before you can extract files!" )
			
	def inject(self):
		if self.ovl_name:
			files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Inject files', self.cfg["dir_inject"], self.filter)[0]
			if files:
				self.cfg["dir_inject"] = os.path.dirname(files[0])
			try:
				inject.inject( self.ovl_data, files, self.write_dds )
				self.file_widget.dirty = True
			except Exception as ex:
				traceback.print_exc()
				widgets.showdialog( str(ex) )
			print("Done!")
		else:
			widgets.showdialog( "You must open an OVL file before you can inject files!" )

	def hasher(self):
		if self.ovl_name:
			names = [ (tup[0].text(), tup[1].text()) for tup in self.e_name_pairs ]
			for archive in self.ovl_data.archives:
				hasher.dat_hasher(archive, names, self.ovl_data.header.files,self.ovl_data.header.textures)
		else:
			widgets.showdialog( "You must open an OVL file before you can extract files!" )

	def walker(self, dummy=False, walk_ovls=True, walk_models=True):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg["dir_ovls_in"], )
		errors = []
		# holds different types of flag - list of byte maps pairs
		type_dic = {}
		if start_dir:
			export_dir = os.path.join(start_dir, "walker_export")
			# don't use internal data
			ovl_data = OvlFormat.Data()
			mdl2_data = Ms2Format.Data()
			if walk_ovls:
				for ovl_path in walker.walk_type(start_dir, extension="ovl"):
					try:
						# read ovl file
						with open(ovl_path, "rb") as ovl_stream:
							ovl_data.read(ovl_stream, file=ovl_path, commands=self.commands)
						# create an output folder for it
						outdir = os.path.join(export_dir, os.path.basename(ovl_path[:-4]))
						# create output dir
						os.makedirs(outdir, exist_ok=True)
						for archive in ovl_data.archives:
							archive.dir = outdir
							extract.extract(archive, self.write_dds, only_types=["ms2",])
					except Exception as ex:
						traceback.print_exc()
						errors.append((ovl_path, ex))
			if walk_models:
				for mdl2_path in walker.walk_type(export_dir, extension="mdl2"):
					mdl2_name = os.path.basename(mdl2_path)
					try:
						with open(mdl2_path, "rb") as ovl_stream:
							mdl2_data.read(ovl_stream, file=mdl2_path, quick=True, map_bytes=True)
							for model in mdl2_data.mdl2_header.models:
								if model.flag not in type_dic:
									type_dic[model.flag] = ([], [])
								type_dic[model.flag][0].append(mdl2_name)
								type_dic[model.flag][1].append(model.bytes_map)
					except Exception as ex:
						traceback.print_exc()
						errors.append((mdl2_path, ex))
			# report
			print("\nThe following errors occured:")
			for file_path, ex in errors:
				print(file_path, str(ex))

			print("\nThe following type - map pairs were found:")
			for flag, tup in type_dic.items():
				print(flag, bin(flag))
				names, maps_list = tup
				print("Some files:", list(set(names))[:25])
				print("num models", len(maps_list))
				print("mean", np.mean(maps_list, axis=0).astype(dtype=np.ubyte))
				print("max", np.max(maps_list, axis=0))
				print()

	def closeEvent(self, event):
		if self.file_widget.dirty:
			qm = QtWidgets.QMessageBox
			quit_msg = "You will lose unsaved work on "+os.path.basename(self.file_widget.filepath)+"!"
			reply = qm.question(self, 'Quit?', quit_msg, qm.Yes, qm.No)

			if reply == qm.Yes:
				event.accept()
			else:
				event.ignore()
		else:
			event.accept()

	@staticmethod
	def check_version():
		is_64bits = sys.maxsize > 2 ** 32
		if not is_64bits:
			widgets.showdialog("Either your operating system or your python installation is not 64 bits.\n"
							   "Large OVLs will crash unexpectedly!")
		if sys.version_info[0] != 3 or sys.version_info[1] != 7 or sys.version_info[2] < 6:
			widgets.showdialog("Python 3.7.6+ x64 bit is expected!")


if __name__ == '__main__':
	print("running python", sys.version)
	widgets.startup(MainWindow)
