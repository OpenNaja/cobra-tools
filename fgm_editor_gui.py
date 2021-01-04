import os
from PyQt5 import QtWidgets, QtCore

import modules.formats.shared
import util.interaction
from generated.formats.fgm import FgmFile
from generated.formats.ovl.versions import *
from util import widgets, config


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "FGM Editor", )
		
		self.resize(450, 500)

		self.fgm_data = FgmFile()
		self.widgets = []
		self.tooltips = config.read_config("util/tooltips/fgm.txt")
		self.shaders = {}
		for game in games:
			self.shaders[game] = config.read_list(f"util/tooltips/fgm-shaders-{game.lower().replace(' ', '-')}.txt")

		self.cleaner = QtCore.QObjectCleanupHandler()

		self.scrollarea = QtWidgets.QScrollArea(self)
		self.scrollarea.setWidgetResizable(True)
		self.setCentralWidget(self.scrollarea)

		# the actual scrollable stuff
		self.widget = QtWidgets.QWidget()
		self.scrollarea.setWidget(self.widget)

		self.game_container = widgets.LabelCombo("Game:", games)
		self.game_container.entry.currentIndexChanged.connect(self.game_changed)
		self.game_container.entry.setEditable(False)
		self.file_widget = widgets.FileWidget(self, self.cfg, dtype="FGM")
		self.shader_container = widgets.LabelCombo("Shader:", ())
		self.shader_container.entry.activated.connect(self.shader_changed)
		self.tex_container = QtWidgets.QGroupBox("Textures")
		self.attrib_container = QtWidgets.QGroupBox("Attributes")

		vbox = QtWidgets.QVBoxLayout()
		vbox.addWidget(self.file_widget)
		vbox.addWidget(self.game_container)
		vbox.addWidget(self.shader_container)
		vbox.addWidget(self.tex_container)
		vbox.addWidget(self.attrib_container)
		vbox.addStretch(1)
		self.widget.setLayout(vbox)

		self.tex_grid = self.create_grid()
		self.attrib_grid = self.create_grid()

		self.tex_container.setLayout(self.tex_grid)
		self.attrib_container.setLayout(self.attrib_grid)

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('File')
		helpMenu = mainMenu.addMenu('Help')
		button_data = ( (fileMenu, "Open", self.file_widget.ask_open, "CTRL+O", ""), \
						(fileMenu, "Save", self.save_fgm, "CTRL+S", ""), \
						(fileMenu, "Exit", self.close, "", ""), \
						(helpMenu, "Report Bug", self.report_bug, "", ""), \
						(helpMenu, "Documentation", self.online_support, "", ""), \
						)
		self.add_to_menu(button_data)

	def game_changed(self,):
		if self.file_widget.filepath:
			self.shader_container.entry.clear()
			game = self.game_container.entry.currentText()
			self.shader_container.entry.addItems(self.shaders[game])
		
	def shader_changed(self,):
		"""Change the fgm data shader name if gui changes"""
		if self.file_widget.filepath:
			self.fgm_data.shader_name = self.shader_container.entry.currentText()

	@property
	def fgm_name(self,):
		return self.file_widget.entry.text()

	def create_grid(self,):
		g = QtWidgets.QGridLayout()
		g.setHorizontalSpacing(3)
		g.setVerticalSpacing(0)
		return g

	def clear_layout(self, layout):
		w = QtWidgets.QWidget()
		w.setLayout(layout)
		# while layout.count():
		# 	item = layout.takeAt(0)
		# 	widget = item.widget()
		# 	# if widget has some id attributes you need to
		# 	# save in a list to maintain order, you can do that here
		# 	# i.e.:   aList.append(widget.someId)
		# 	widget.deleteLater()

	def load(self):
		if self.file_widget.filepath:
			for w in self.widgets:
				w.deleteLater()
			try:
				self.fgm_data.load(self.file_widget.filepath)
				game = get_game(self.fgm_data)
				print("from game", game)
				self.game_container.entry.setText(game)
				# also for
				self.game_changed()
				self.shader_container.entry.setText(self.fgm_data.shader_name)

				# delete existing widgets
				self.clear_layout(self.tex_grid)
				self.clear_layout(self.attrib_grid)

				self.tex_grid = self.create_grid()
				self.attrib_grid = self.create_grid()

				self.tex_container.setLayout(self.tex_grid)
				self.attrib_container.setLayout(self.attrib_grid)
				for line_i, tex in enumerate(self.fgm_data.textures):
					w = widgets.VectorEntry(tex, self.tooltips)
					self.tex_grid.addWidget(w.delete, line_i, 0)
					self.tex_grid.addWidget(w.label, line_i, 1)
					self.tex_grid.addWidget(w.data, line_i, 2)

				for line_i, attrib in enumerate(self.fgm_data.attributes):
					w = widgets.VectorEntry(attrib, self.tooltips)
					self.attrib_grid.addWidget(w.delete, line_i, 0)
					self.attrib_grid.addWidget(w.label, line_i, 1)
					self.attrib_grid.addWidget(w.data, line_i, 2)

			except Exception as ex:
				util.interaction.showdialog(str(ex))
				print(ex)
			print("Done!")
		
	def save_fgm(self):
		if self.file_widget.filepath:
			file_out = QtWidgets.QFileDialog.getSaveFileName(self, 'Save FGM', os.path.join(self.cfg.get("dir_fgms_out", "C://"), self.fgm_name), "FGM files (*.fgm)",)[0]
			if file_out:
				self.cfg["dir_fgms_out"], fgm_name = os.path.split(file_out)
				self.fgm_data.save(file_out)
				print("Done!")
			
	
if __name__ == '__main__':
	widgets.startup(MainWindow)
