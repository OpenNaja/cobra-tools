import os
import io
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from pyffi_ext.formats.materialcollection import MaterialcollectionFormat
from util import widgets, config
from modules import extract, inject

class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "MaterialCollection Editor", )
		
		self.resize(450, 500)

		self.materialcollection_data = MaterialcollectionFormat.Data()
		self.file_src = ""
		self.widgets = []
		# self.tooltips = config.read_config("util/tooltips/matcol.txt")
		self.tooltips = {}
		self.games = ("Jurassic World Evolution", "Planet Zoo")
		# self.shaders = {}
		# for game in self.games:
		# 	self.shaders[game] = config.read_list(f"util/tooltips/materialcollection-shaders-{game.lower().replace(' ', '-')}.txt")
		
		mainMenu = self.menuBar() 
		fileMenu = mainMenu.addMenu('File')
		helpMenu = mainMenu.addMenu('Help')
		button_data = ( (fileMenu, "Open", self.open_materialcollection, "CTRL+O"), \
						(fileMenu, "Save", self.save_materialcollection, "CTRL+S"), \
						(fileMenu, "Exit", self.close, ""), \
						(helpMenu, "Report Bug", self.report_bug, ""), \
						(helpMenu, "Documentation", self.online_support, ""), \
						)
		self.add_to_menu(button_data)

		self.cleaner = QtCore.QObjectCleanupHandler()

		self.scrollarea = QtWidgets.QScrollArea(self)
		self.scrollarea.setWidgetResizable(True)
		self.setCentralWidget(self.scrollarea)

		# the actual scrollable stuff
		self.widget = QtWidgets.QWidget()
		self.scrollarea.setWidget(self.widget)

		self.game_container = widgets.LabelCombo("Game:", self.games)
		# self.game_container.entry.currentIndexChanged.connect(self.game_changed)
		self.game_container.entry.setEditable(False)
		self.materialcollection_container = widgets.LabelEdit("MATCOL:")
		# self.shader_container = widgets.LabelCombo("Shader:", () )
		# self.shader_container.entry.activated.connect(self.shader_changed)
		self.tex_container = QtWidgets.QGroupBox("Slots")
		self.attrib_container = QtWidgets.QGroupBox("Attributes")

		vbox = QtWidgets.QVBoxLayout()
		vbox.addWidget(self.game_container)
		vbox.addWidget(self.materialcollection_container)
		# vbox.addWidget(self.shader_container)
		vbox.addWidget(self.tex_container)
		vbox.addWidget(self.attrib_container)
		vbox.addStretch(1)
		self.widget.setLayout(vbox)

		self.tex_grid = self.create_grid()
		self.attrib_grid = self.create_grid()

		self.tex_container.setLayout(self.tex_grid)
		self.attrib_container.setLayout(self.attrib_grid)
		
	def game_changed(self,):
		if self.file_src:
			self.shader_container.entry.clear()
			game = self.game_container.entry.currentText()
			self.shader_container.entry.addItems(self.shaders[game])
		
	def shader_changed(self,):
		"""Change the materialcollection data shader name if gui changes"""
		if self.file_src:
			self.materialcollection_data.shader_name = self.shader_container.entry.currentText()

	@property
	def materialcollection_name(self,):
		return self.materialcollection_container.entry.text()


	def open_materialcollection(self):
		"""Just a wrapper so we can also reload via code"""
		self.file_src = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Matcol', self.cfg["dir_materialcollections_in"], "Matcol files (*.materialcollection)")[0]
		self.load_materialcollection()

	def create_grid(self,):
		g = QtWidgets.QGridLayout()
		g.setHorizontalSpacing(3)
		g.setVerticalSpacing(3)
		return g

	def clear_layout(self, layout):
		w = QtWidgets.QWidget()
		w.setLayout(layout)
		while layout.count():
			item = layout.takeAt(0)
			widget = item.widget()
			# if widget has some id attributes you need to
			# save in a list to maintain order, you can do that here
			# i.e.:   aList.append(widget.someId)
			widget.deleteLater()

	def load_materialcollection(self):
		if self.file_src:
			for w in self.widgets:
				w.deleteLater()
			self.cfg["dir_materialcollections_in"], materialcollection_name = os.path.split(self.file_src)
			try:
				with open(self.file_src, "rb") as materialcollection_stream:
					self.materialcollection_data.read(materialcollection_stream)
				game = self.materialcollection_data.game
				print("from game",game)
				self.game_container.setText(game)

				self.materialcollection_container.entry.setText( materialcollection_name )

				# delete existing widgets
				self.clear_layout(self.tex_grid)
				self.clear_layout(self.attrib_grid)

				self.tex_grid = self.create_grid()
				self.attrib_grid = self.create_grid()

				self.tex_container.setLayout(self.tex_grid)
				self.attrib_container.setLayout(self.attrib_grid)
				line_i = 0
				for i, tex in enumerate(self.materialcollection_data.header.texture_wrapper.textures):
					# w = widgets.VectorEntry(tex, self.tooltips)
					# form.addRow(w.label, w.data)
					box = widgets.CollapsibleBox(f"Slot {i}")
					# box = QtWidgets.QGroupBox(f"Slot {i}")
					self.tex_grid.addWidget(box, line_i, 0)
					line_i += 1
					lay = self.create_grid()
					a = QtWidgets.QLabel("texture type")
					b = QtWidgets.QLabel("texture suffix")
					c = QtWidgets.QLabel("fgm name")
					x = QtWidgets.QLineEdit(tex.texture_type)
					y = QtWidgets.QLineEdit(tex.texture_suffix)
					z = QtWidgets.QLineEdit(tex.fgm_name)
					lay.addWidget(a, 0, 0)
					lay.addWidget(b, 1, 0)
					lay.addWidget(c, 2, 0)
					lay.addWidget(x, 0, 1)
					lay.addWidget(y, 1, 1)
					lay.addWidget(z, 2, 1)
					box.setLayout(lay)
				
				line_i = 0
				for attrib in self.materialcollection_data.header.layered_wrapper.layers:
					# w = widgets.VectorEntry(attrib, self.tooltips)
					# self.attrib_grid.addWidget(w.label, line_i, 0)
					# self.attrib_grid.addWidget(w.data, line_i, 1)
					# w = QtWidgets.QLabel(attrib.name)
					# self.attrib_grid.addWidget(w, line_i, 0)
					# line_i += 1
					# for infow in attrib.infos:
					# 	w = widgets.MatcolInfo(infow, self.tooltips)
					# 	self.attrib_grid.addWidget(w.label, line_i, 0)
					# 	self.attrib_grid.addWidget(w.data, line_i, 1)
					# 	line_i += 1
					box = widgets.CollapsibleBox(attrib.name)
					# box = QtWidgets.QGroupBox(attrib.name)
					self.attrib_grid.addWidget(box, line_i, 0)
					line_i += 1
					lay = self.create_grid()
					l = 0
					for infow in attrib.infos:
						w = widgets.MatcolInfo(infow, self.tooltips)
						lay.addWidget(w.label, l, 0)
						lay.addWidget(w.data, l, 1)
						l+=1
					box.setLayout(lay)
				
				line_i = 0
				for zstr in self.materialcollection_data.header.variant_wrapper.materials:

					a = QtWidgets.QLabel("variant fgm")
					b = QtWidgets.QLineEdit(zstr)
					self.attrib_grid.addWidget(a, line_i, 0)
					self.attrib_grid.addWidget(b, line_i, 1)
					line_i += 1
				
			except Exception as ex:
				widgets.showdialog( str(ex) )
				print(ex)
			print("Done!")
		
	def save_materialcollection(self):
		if self.file_src:
			file_out = QtWidgets.QFileDialog.getSaveFileName(self, 'Save materialcollection', os.path.join(self.cfg["dir_materialcollections_out"], self.materialcollection_name), "materialcollection files (*.materialcollection)",)[0]
			if file_out:
				self.cfg["dir_materialcollections_out"], materialcollection_name = os.path.split(file_out)
				with open(file_out, "wb") as materialcollection_stream:
					self.materialcollection_data.write(materialcollection_stream)
				print("Done!")
			
	
if __name__ == '__main__':
	widgets.startup( MainWindow )