import logging
import os
import traceback

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor

import hashes.fgm_pz as fgm_dict
import ovl_util.interaction
from generated.formats.fgm import FgmFile
from generated.formats.ovl.versions import *
from ovl_util import widgets, config, interaction
from ovl_util.widgets import QColorButton, MySwitch, MAX_UINT

from ovl_util.config import logging_setup

logging_setup("fgm_editor")


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "FGM Editor", )
		
		self.resize(800, 600)

		self.fgm_data = FgmFile()
		self.tooltips = config.read_config("ovl_util/tooltips/fgm.txt")
		self.games = [g.value for g in games]

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
		self.file_widget = widgets.FileWidget(self, self.cfg, dtype="FGM")

		self.shader_choice = widgets.LabelCombo("Shader:", ())
		self.shader_choice.entry.activated.connect(self.shader_changed)
		self.attribute_choice = widgets.LabelCombo("Attribute:", ())
		self.texture_choice = widgets.LabelCombo("Texture:", ())
		self.attribute_add = QtWidgets.QPushButton("Add Attribute")
		self.attribute_add.clicked.connect(self.add_attribute)
		self.texture_add = QtWidgets.QPushButton("Add Texture")
		self.texture_add.clicked.connect(self.add_texture)

		self.tex_container = ProptertyContainer(self, "Textures")
		self.attrib_container = ProptertyContainer(self, "Attributes")

		self.populate_choices()

		vbox = QtWidgets.QVBoxLayout()
		vbox.addWidget(self.file_widget)
		vbox.addWidget(self.game_container)
		vbox.addWidget(self.shader_choice)
		vbox.addWidget(self.attribute_choice)
		vbox.addWidget(self.attribute_add)
		vbox.addWidget(self.texture_choice)
		vbox.addWidget(self.texture_add)
		vbox.addWidget(self.tex_container)
		vbox.addWidget(self.attrib_container)
		vbox.addStretch(1)
		self.widget.setLayout(vbox)

		self.attrib_grid = self.create_grid()

		self.attrib_container.setLayout(self.attrib_grid)

		main_menu = self.menuBar()
		file_menu = main_menu.addMenu('File')
		help_menu = main_menu.addMenu('Help')
		button_data = (
			(file_menu, "Open", self.file_widget.ask_open, "CTRL+O", ""),
			(file_menu, "Save", self.save_fgm, "CTRL+S", ""),
			(file_menu, "Exit", self.close, "", ""),
			(help_menu, "Report Bug", self.report_bug, "", ""),
			(help_menu, "Documentation", self.online_support, "", ""),
		)
		self.add_to_menu(button_data)

	def game_changed(self,):
		game = self.game_container.entry.currentText()
		# self.populate_choices(game)

	def populate_choices(self, game=None):
		# todo - make version dependant
		self.shader_choice.entry.clear()
		self.shader_choice.entry.addItems(sorted(fgm_dict.shaders))
		self.attribute_choice.entry.clear()
		self.attribute_choice.entry.addItems(sorted(fgm_dict.attributes))
		self.texture_choice.entry.clear()
		self.texture_choice.entry.addItems(sorted(fgm_dict.textures))
		
	def shader_changed(self,):
		self.fgm_data.shader_name = self.shader_choice.entry.currentText()

	def add_attribute(self,):
		self.fgm_data.shader_name = self.shader_choice.entry.currentText()

	def add_texture(self,):
		self.fgm_data.shader_name = self.shader_choice.entry.currentText()

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
			try:
				self.fgm_data.load(self.file_widget.filepath)
				game = get_game(self.fgm_data)[0]
				logging.debug(f"from game {game}")
				self.game_container.entry.setText(game.value)
				self.game_changed()
				self.shader_choice.entry.setText(self.fgm_data.shader_name)
				self.tex_container.update_gui(self.fgm_data.textures)
				self.attrib_container.update_gui(self.fgm_data.attributes)

			except Exception as ex:
				traceback.print_exc()
				ovl_util.interaction.showdialog(str(ex))
				logging.warning(ex)
			logging.info("Done!")

	def save_fgm(self):
		if self.file_widget.filepath:
			file_out = QtWidgets.QFileDialog.getSaveFileName(self, 'Save FGM', os.path.join(self.cfg.get("dir_fgms_out", "C://"), self.fgm_name), "FGM files (*.fgm)",)[0]
			if file_out:
				self.cfg["dir_fgms_out"], fgm_name = os.path.split(file_out)
				try:
					self.fgm_data.save(file_out)
				except BaseException as err:
					traceback.print_exc()
					interaction.showdialog(str(err))
					logging.error(err)
				logging.info("Done!")


class ProptertyContainer(QtWidgets.QGroupBox):
	def __init__(self, gui, name):
		super().__init__(name)
		self.gui = gui
		self.data_list = []
		self.widgets = []

	def update_gui(self, data_list):
		logging.debug(f"Populating table with {len(data_list)} entries")
		self.data_list = data_list
		self.clear_layout()
		grid = self.gui.create_grid()
		grid.setColumnStretch(1, 3)
		grid.setColumnStretch(2, 3)
		self.setLayout(grid)
		self.widgets = []
		for line_i, tex in enumerate(self.data_list):
			w = TextureVisual(self, tex)
			self.widgets.append(w)
			grid.addWidget(w.delete_btn, line_i, 0)
			grid.addWidget(w.entry, line_i, 1)
			grid.addWidget(w.data, line_i, 2)

	def clear_layout(self):
		layout = self.layout()
		if layout is not None:
			w = QtWidgets.QWidget()
			w.setLayout(layout)


class TextureVisual:
	def __init__(self, container, property):
		self.container = container
		self.property = property
		self.entry = QtWidgets.QLineEdit(property.name)
		self.entry.textEdited.connect(self.update_name)
		self.delete_btn = QtWidgets.QPushButton("x")
		self.delete_btn.setMaximumWidth(15)
		self.delete_btn.clicked.connect(self.delete)
		self.data = QtWidgets.QWidget()
		layout = QtWidgets.QHBoxLayout()
		self.fields = self.create_fields()
		for button in self.fields:
			layout.addWidget(button)
		self.data.setLayout(layout)

		# get tooltip
		tooltip = self.container.gui.tooltips.get(self.property.name, "Undocumented textureute.")
		self.data.setToolTip(tooltip)
		self.entry.setToolTip(tooltip)

	def delete(self):
		self.container.data_list.remove(self.property)
		self.container.update_gui(self.container.data_list)

	def update_name(self, name):
		self.property.name = name

	def update_file(self, file):
		self.property.file = file

	def create_fields(self):
		if hasattr(self.property, "file") and self.property.file:
			self.file_w = QtWidgets.QLineEdit(self.property.file)
			self.file_w.textEdited.connect(self.update_file)
			return self.file_w,
		elif "_RGB" in self.property.name:
			return self.create_rgb_field(),
		else:
			return [self.create_field(i) for i in range(len(self.property.value))]

	def update_rgb_field(self, c):
		self.property.value = [x / 255 for x in c.getRgb()[:3]]

	def create_rgb_field(self):
		field = QColorButton()
		field.colorChanged.connect(self.update_rgb_field)
		d = [x * 255 for x in self.property.value]
		c = QColor(*d, 255)
		field.setColor(c)
		return field

	def create_field(self, ind):
		default = self.property.value[ind]

		def update_ind_color(c):
			# use a closure to remember index
			color = self.property.value[ind]
			color.r, color.g, color.b, color.a = c.getRgb()

		def update_ind(v):
			# use a closure to remember index
			# print(self.attrib, ind, v)
			self.property.value[ind] = v

		def update_ind_int(v):
			# use a closure to remember index
			# print(self.attrib, ind, v)
			self.property.value[ind] = int(v)

		t = str(type(default))
		# print(t)
		if "Color" in t:
			field = QColorButton()
			field.colorChanged.connect(update_ind_color)
		elif "float" in t:
			field = QtWidgets.QDoubleSpinBox()
			field.setDecimals(3)
			field.setRange(-10000, 10000)
			field.setSingleStep(.05)
			field.valueChanged.connect(update_ind)
		elif "bool" in t:
			field = MySwitch()
			field.clicked.connect(update_ind)
		elif "int" in t:
			default = int(default)
			field = QtWidgets.QDoubleSpinBox()
			field.setDecimals(0)
			field.setRange(-MAX_UINT, MAX_UINT)
			field.valueChanged.connect(update_ind_int)
		else:
			raise AttributeError(f"Unsupported field type {t}")
		field.setValue(default)
		field.setMinimumWidth(50)
		return field


if __name__ == '__main__':
	widgets.startup(MainWindow)
