import os
import io
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from pyffi_ext.formats.fgm import FgmFormat
from util import widgets, config
from modules import extract, inject

class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "FGM Editor", )
		
		self.resize(450, 500)

		self.fgm_data = FgmFormat.Data()
		self.file_src = ""
		self.widgets = []
		self.tooltips = config.read_config("util/tooltips/fgm.txt")
		self.games = ("Jurassic World Evolution", "Planet Zoo")
		self.shaders = {}
		for game in self.games:
			self.shaders[game] = config.read_list(f"util/tooltips/fgm-shaders-{game.lower().replace(' ', '-')}.txt")
		
		mainMenu = self.menuBar() 
		fileMenu = mainMenu.addMenu('File')
		helpMenu = mainMenu.addMenu('Help')
		button_data = ( (fileMenu, "Open", self.open_fgm, "CTRL+O"), \
						(fileMenu, "Save", self.save_fgm, "CTRL+S"), \
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
		self.game_container.entry.currentIndexChanged.connect(self.game_changed)
		self.game_container.entry.setEditable(False)
		self.fgm_container = widgets.LabelEdit("FGM:")
		self.shader_container = widgets.LabelCombo("Shader:", () )
		self.shader_container.entry.activated.connect(self.shader_changed)
		self.tex_container = QtWidgets.QGroupBox("Textures")
		self.attrib_container = QtWidgets.QGroupBox("Attributes")

		vbox = QtWidgets.QVBoxLayout()
		vbox.addWidget(self.game_container)
		vbox.addWidget(self.fgm_container)
		vbox.addWidget(self.shader_container)
		vbox.addWidget(self.tex_container)
		vbox.addWidget(self.attrib_container)
		vbox.addStretch(1)
		self.widget.setLayout(vbox)

	def game_changed(self,):
		if self.file_src:
			self.shader_container.entry.clear()
			game = self.game_container.entry.currentText()
			self.shader_container.entry.addItems(self.shaders[game])
		
	def shader_changed(self,):
		"""Change the fgm data shader name if gui changes"""
		if self.file_src:
			self.fgm_data.shader_name = self.shader_container.entry.currentText()

	@property
	def fgm_name(self,):
		return self.fgm_container.entry.text()


	def open_fgm(self):
		"""Just a wrapper so we can also reload via code"""
		self.file_src = QtWidgets.QFileDialog.getOpenFileName(self, 'Load FGM', self.cfg["dir_fgms_in"], "FGM files (*.fgm)")[0]
		self.load_fgm()

	def load_fgm(self):
		if self.file_src:
			for w in self.widgets:
				w.deleteLater()
			self.cfg["dir_fgms_in"], fgm_name = os.path.split(self.file_src)
			try:
				with open(self.file_src, "rb") as fgm_stream:
					self.fgm_data.read(fgm_stream, file=self.file_src)
				game = self.fgm_data.game
				print("from game",game)
				self.game_container.setText(game)
				# also for
				self.game_changed()

				self.fgm_container.entry.setText( fgm_name )
				self.shader_container.setText(self.fgm_data.shader_name)

				# delete existing widgets
				if self.tex_container.layout():
					d = QtWidgets.QWidget()
					d.setLayout( self.tex_container.layout() )
				if self.attrib_container.layout():
					d = QtWidgets.QWidget()
					d.setLayout( self.attrib_container.layout() )

				qgrid = QtWidgets.QGridLayout()
				qgrid.setHorizontalSpacing(3)
				qgrid.setVerticalSpacing(0)
				line_i = 0
				for tex in self.fgm_data.fgm_header.textures:
					# w = widgets.VectorEntry(attrib)
					# form.addRow(w.label, w.data)
					w = QtWidgets.QLabel(tex.name)
					line_i += 1
					qgrid.addWidget(w, line_i, 0)
					# qgrid.addWidget(w.label, line_i, 0)
					# qgrid.addWidget(w.data, line_i, 1)
								
				self.tex_container.setLayout(qgrid)
				

				qgrid = QtWidgets.QGridLayout()
				qgrid.setHorizontalSpacing(3)
				qgrid.setVerticalSpacing(0)
				line_i = 0
				for attrib in self.fgm_data.fgm_header.attributes:
					w = widgets.VectorEntry(attrib, self.tooltips)
					line_i += 1
					qgrid.addWidget(w.label, line_i, 0)
					qgrid.addWidget(w.data, line_i, 1)
								
				self.attrib_container.setLayout(qgrid)
				
			except Exception as ex:
				widgets.showdialog( str(ex) )
				print(ex)
			print("Done!")
		
	def save_fgm(self):
		if self.file_src:
			file_out = QtWidgets.QFileDialog.getSaveFileName(self, 'Save FGM', os.path.join(self.cfg["dir_fgms_out"], self.fgm_name), "FGM files (*.fgm)",)[0]
			if file_out:
				self.cfg["dir_fgms_out"], fgm_name = os.path.split(file_out)
				# just a dummy stream
				with open(file_out, "wb") as fgm_stream:
					self.fgm_data.write(fgm_stream)
				print("Done!")
			
	
if __name__ == '__main__':
	widgets.startup( MainWindow )