import os
import io
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from pyffi.formats.ovl import OvlFormat
from util import widgets, config
from modules import extract, inject

class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "OVL Tool", )
		
		self.ovl_data = OvlFormat.Data()

		supported_types = ("DDS", "PNG", "MDL2", "TXT")
		self.filter = "Supported files ({})".format( " ".join("*."+t for t in supported_types) )
		
		self.b_open = QtWidgets.QPushButton('Open OVL')
		self.b_open.setToolTip("Load an ovl archive whose files you want to modify.")
		self.b_open.clicked.connect(self.open_ovl)
		
		self.b_save = QtWidgets.QPushButton('Save OVL')
		self.b_save.setToolTip("Save the ovl file you do not want to merge.")
		self.b_save.clicked.connect(self.save_ovl)
		
		self.b_unpack = QtWidgets.QPushButton('Unpack')
		self.b_unpack.setToolTip("Unpack all known files from the OVL into the selected folder.")
		self.b_unpack.clicked.connect(self.extract_all)
		
		self.b_inject = QtWidgets.QPushButton('Inject')
		self.b_inject.setToolTip("Load files to inject into the opened ovl archive.")
		self.b_inject.clicked.connect(self.inject)

		self.e_ovl_name = QtWidgets.QLineEdit(self)
		self.e_ovl_name.setToolTip("The name of the OVL file that is currently open.")
		self.e_ovl_name.setReadOnly(True)
		
		self.t_reverse = QtWidgets.QCheckBox("Reverse Sets")
		self.t_reverse.setToolTip("Most models need their sets to be read in revers. Uncheck only if issues ocur.")
		self.t_reverse.setChecked(True)
		
		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.b_open, 0, 0)
		self.qgrid.addWidget(self.b_save, 0, 1)
		self.qgrid.addWidget(self.b_unpack, 0, 2)
		self.qgrid.addWidget(self.b_inject, 0, 3)
		self.qgrid.addWidget(self.t_reverse, 0, 4)
		self.qgrid.addWidget(self.e_ovl_name, 1, 0, 1, 5)
		
		self.central_widget.setLayout(self.qgrid)
	
	@property
	def ovl_name(self,):
		return self.e_ovl_name.text()
		
	@property
	def reverse_sets(self,):
		return self.t_reverse.isChecked()
	
	def open_ovl(self):
		file_src = QtWidgets.QFileDialog.getOpenFileName(self, 'Load OVL', self.cfg["dir_ovls_in"], "OVL files (*.ovl)")[0]
		if file_src:
			self.cfg["dir_ovls_in"], ovl_name = os.path.split(file_src)
			try:
				with open(file_src, "rb") as nif_stream:
					self.ovl_data.read(nif_stream, file=file_src, reverse_sets=self.reverse_sets)
				self.e_ovl_name.setText(ovl_name)
			except Exception as ex:
				widgets.showdialog( str(ex) )
				print(ex)
			print("Done!")
		
	def save_ovl(self):
		if self.ovl_name:
			file_src = QtWidgets.QFileDialog.getSaveFileName(self, 'Save OVL', os.path.join(self.cfg["dir_ovls_out"], self.ovl_name), "OVL files (*.ovl)",)[0]
			if file_src:
				self.cfg["dir_ovls_out"], ovl_name = os.path.split(file_src)
				# just a dummy stream
				with io.BytesIO() as nif_stream:
					self.ovl_data.write(nif_stream, file_path=file_src)
				print("Done!")
			
	def extract_all(self):
		if self.ovl_name:
			self.cfg["dir_extract"] = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg["dir_extract"], )
			if self.cfg["dir_extract"]:
				# self.ovl_data.extract_all(self.cfg["dir_extract"])
				dir = self.cfg["dir_extract"]
				# create output dir
				os.makedirs(dir, exist_ok=True)
				for archive in self.ovl_data.archives:
					archive.dir = dir
					extract.extract(archive)
				print("Done!")
			
	def inject(self):
		if self.ovl_name:
			files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Inject files', self.cfg["dir_inject"], self.filter)[0]
			if files:
				self.cfg["dir_inject"] = os.path.dirname(files[0])
			# self.ovl_data.inject( files )
			try:
				inject.inject( self.ovl_data, files )
			except Exception as ex:
				widgets.showdialog( str(ex) )
			print("Done!")
	
	
if __name__ == '__main__':
	widgets.startup( MainWindow )