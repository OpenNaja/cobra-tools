import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

import ms2_merger
from util import widgets, config

class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "MS2 Merger", )
		
		self.mdl2_names = []
		self.names_to_full_paths = {}
		self.mdl2_to_ms2 = {}

		self.b_add = QtWidgets.QPushButton('Load MDL2s')
		self.b_add.setToolTip("Load mdl2 files whose MS2 buffers you want to merge.")
		self.b_add.clicked.connect(self.add_mdl2s)
		
		self.b_remove = QtWidgets.QPushButton('Remove MDL2s')
		self.b_remove.setToolTip("Remove mdl2 files you do not want to merge.")
		self.b_remove.clicked.connect(self.remove_mdl2s)
		
		self.b_merge = QtWidgets.QPushButton('Merge')
		self.b_merge.setToolTip("Merge these files according to the current settings.")
		self.b_merge.clicked.connect(self.run)

		self.c_ms2 = QtWidgets.QLineEdit(self)
		self.c_ms2.setToolTip("Select the master MS2. This determines how many keys you may use.")
		self.c_ms2.setText(self.cfg["ms2_name"])
		self.c_ms2.textChanged.connect(self.update_cfg_ms2_name)
		
		self.mdl2_widget = QtWidgets.QListWidget()
		self.mdl2_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		
		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.setHorizontalSpacing(0)
		self.qgrid.setVerticalSpacing(0)
		self.qgrid.addWidget(self.b_add, 0, 0)
		self.qgrid.addWidget(self.b_remove, 0, 1)
		self.qgrid.addWidget(self.b_merge, 0, 2)
		self.qgrid.addWidget(self.c_ms2, 0, 3)
		self.qgrid.addWidget(self.mdl2_widget, 1, 0, 1, 4)
		
		self.central_widget.setLayout(self.qgrid)
		
	def run(self):
		self.cfg["dir_models_out"] = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg["dir_models_out"], )
		if self.cfg["dir_models_out"]:
			ms2_merger.merge_mdl2s([ self.names_to_full_paths[mdl2_name] for mdl2_name in self.mdl2_names], self.cfg["dir_models_out"], self.cfg["ms2_name"])
			print("Done!")
	
	def update_cfg_ms2_name(self):
		self.cfg["ms2_name"] = self.c_ms2.text()
	
	def add_mdl2s(self):
		file_src = QtWidgets.QFileDialog.getOpenFileNames(self, 'Load MDL2s', self.cfg["dir_models_in"], "mdl2 files (*.mdl2)")[0]
		for mdl2_path in file_src:
			self.cfg["dir_models_in"], mdl2_name = os.path.split(mdl2_path[:-5])
			if mdl2_name not in self.mdl2_names:
				self.mdl2_names.append(mdl2_name)
				self.mdl2_widget.addItem(mdl2_name)
				self.names_to_full_paths[mdl2_name] = mdl2_path
				# update ms2 info field
				self.cfg["ms2_name"] = ms2_merger.get_ms2_name(mdl2_path)
				self.c_ms2.setText(self.cfg["ms2_name"])
		
	def remove_mdl2s(self):
		for item in self.mdl2_widget.selectedItems():
			mdl2_name = item.text()
			for i in reversed(range(0, len(self.mdl2_names))):
				if self.mdl2_names[i] == mdl2_name:
					self.mdl2_names.pop(i)
			self.mdl2_widget.takeItem(self.mdl2_widget.row(item))

if __name__ == '__main__':
	widgets.startup( MainWindow )