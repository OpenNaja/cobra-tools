import logging
import os
from PyQt5 import QtWidgets, QtCore

from generated.formats.matcol.compounds.MatcolRoot import MatcolRoot
from generated.formats.ovl_base import OvlContext
from ovl_util import widgets, config


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "Matcol Editor", )
		
		self.resize(450, 500)

		self.context = OvlContext()
		self.matcol_data = MatcolRoot(self.context)
		self.file_src = ""
		self.widgets = []
		self.tooltips = config.read_config("ovl_util/tooltips/matcol.txt")
		self.games = ("Jurassic World Evolution", "Planet Zoo")
		self.default_fgms = config.read_list("ovl_util/tooltips/matcol-fgm-names.txt")

		mainMenu = self.menuBar() 
		fileMenu = mainMenu.addMenu('File')
		helpMenu = mainMenu.addMenu('Help')
		button_data = ( (fileMenu, "Open", self.open_materialcollection, "CTRL+O", ""), \
						(fileMenu, "Save", self.save_materialcollection, "CTRL+S", ""), \
						(fileMenu, "Exit", self.close, "", ""), \
						(helpMenu, "Report Bug", self.report_bug, "", ""), \
						(helpMenu, "Documentation", self.online_support, "", ""), \
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
		self.tex_container = QtWidgets.QGroupBox("Slots")
		self.attrib_container = QtWidgets.QGroupBox("Attributes")

		self.vbox = QtWidgets.QVBoxLayout()
		self.vbox.addWidget(self.game_container)
		self.vbox.addWidget(self.materialcollection_container)
		self.vbox.addWidget(self.tex_container)
		self.vbox.addWidget(self.attrib_container)
		self.vbox.addStretch(1)
		self.widget.setLayout(self.vbox)

		self.tex_grid = self.create_grid()
		self.attrib_grid = self.create_grid()

		self.tex_container.setLayout(self.tex_grid)
		self.attrib_container.setLayout(self.attrib_grid)
		
	def game_changed(self,):
		if self.file_src:
			self.shader_container.entry.clear()
			game = self.game_container.entry.currentText()
			self.shader_container.entry.addItems(self.shaders[game])

	@property
	def materialcollection_name(self,):
		return self.materialcollection_container.entry.text()

	def open_materialcollection(self):
		"""Just a wrapper so we can also reload via code"""
		self.file_src = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Matcol', self.cfg.get("dir_materialcollections_in", "C://"), "matcol files (*.materialcollection)")[0]
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
				self.matcol_data = self.matcol_data.from_xml_file(self.file_src, self.context)
				# game = get_game(self.matcol_data)[0]
				# print("from game", game)
				# self.game_container.entry.setText(game.value)

				self.materialcollection_container.entry.setText(materialcollection_name)

				# delete existing widgets
				self.clear_layout(self.tex_grid)
				self.clear_layout(self.attrib_grid)

				self.tex_grid = self.create_grid()
				self.attrib_grid = self.create_grid()

				self.tex_container.setLayout(self.tex_grid)
				self.attrib_container.setLayout(self.attrib_grid)
				main = self.matcol_data.main.data
				line_i = 0
				for i, tex in enumerate(main.textures.data):
					box = widgets.CollapsibleBox(f"Slot {i}")
					self.tex_grid.addWidget(box, line_i, 0)
					line_i += 1
					lay = self.create_grid()
					a = QtWidgets.QLabel("texture type")
					b = QtWidgets.QLabel("texture suffix")
					x = QtWidgets.QLineEdit(tex.texture_type.data)
					y = QtWidgets.QLineEdit(tex.texture_suffix.data)
					combo = widgets.LabelCombo("First FGM:", self.default_fgms)
					combo.entry.setText(tex.fgm_name.data)
					lay.addWidget(a, 0, 0)
					lay.addWidget(b, 1, 0)
					lay.addWidget(x, 0, 1)
					lay.addWidget(y, 1, 1)
					lay.addWidget(combo.label, 2, 0)
					lay.addWidget(combo.entry, 2, 1)
					box.setLayout(lay)

				line_i = 0
				for i, attrib in enumerate(main.materials.data):
					box = widgets.CollapsibleBox(f"Slot {i}")
					self.attrib_grid.addWidget(box, line_i, 0)
					line_i += 1
					lay = self.create_grid()
					combo = widgets.LabelCombo("FGM:", self.default_fgms)
					combo.entry.setText(attrib.layer_name.data)
					lay.addWidget(combo.label, 0, 0)
					lay.addWidget(combo.entry, 0, 1)
					sub_line_i = 1
					for infow in attrib.infos.data:
						w = widgets.MatcolInfo(infow, self.tooltips)
						lay.addWidget(w.label, sub_line_i, 0)
						lay.addWidget(w.data, sub_line_i, 1)
						sub_line_i += 1
					box.setLayout(lay)
			except:
				logging.exception(f"Something went wrong")
			logging.info("Done!")
		
	def save_materialcollection(self):
		if self.file_src:
			file_out = QtWidgets.QFileDialog.getSaveFileName(self, 'Save materialcollection', os.path.join(self.cfg.get("dir_materialcollections_out", "C://"), self.materialcollection_name), "matcol files (*.materialcollection)",)[0]
			if file_out:
				self.cfg["dir_materialcollections_out"], materialcollection_name = os.path.split(file_out)
				self.matcol_data.save(file_out)
				logging.info("Done!")
			
	
if __name__ == '__main__':
	widgets.startup(MainWindow)
