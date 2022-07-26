import logging
import os
import traceback

import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor, QIcon

from generated.formats.fgm.enum.FgmDtype import FgmDtype
from generated.formats.ovl_base import OvlContext
from hashes import fgm_pz, fgm_jwe2
import ovl_util.interaction
from generated.formats.fgm.compound.FgmHeader import FgmHeader
from generated.formats.fgm.compound.TexIndex import TexIndex
from generated.formats.fgm.compound.TextureInfo import TextureInfo
from generated.formats.fgm.compound.DependencyInfo import DependencyInfo
from generated.formats.fgm.compound.AttributeInfo import AttributeInfo
from generated.formats.fgm.compound.AttribData import AttribData
from generated.array import Array
from generated.formats.ovl.versions import *
from ovl_util import widgets, config, interaction
from ovl_util.widgets import QColorButton, MySwitch, MAX_UINT

from ovl_util.config import logging_setup

logging_setup("fgm_editor")

attrib_sizes = {
	0: 4, # FgmDtype.Float
	1: 8, # FgmDtype.Float2
	2: 12, # FgmDtype.Float3
	3: 16, # FgmDtype.Float4
	5: 4, # FgmDtype.Int
	6: 4, # FgmDtype.Bool
}

# Because FgmDtype does not have a from int
attrib_dtypes = {
	0: FgmDtype.Float,
	1: FgmDtype.Float2,
	2: FgmDtype.Float3,
	3: FgmDtype.Float4,
	5: FgmDtype.Int,
	6: FgmDtype.Bool,
}

class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "FGM Editor", )
		
		self.resize(800, 600)
		self.setAcceptDrops(True)

		self.context = OvlContext()
		self.header = FgmHeader(self.context)
		self.tooltips = config.read_config("ovl_util/tooltips/fgm.txt")
		self.games = [g.value for g in games]
		self.fgm_dict = None
		self.import_header = None

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

		self.lock_attrs = QtWidgets.QCheckBox("Lock Attributes")
		self.lock_attrs.setLayoutDirection(QtCore.Qt.RightToLeft)
		self.lock_attrs.setChecked(True)

		self.skip_color = QtWidgets.QCheckBox("Disable Float3 Color Widgets")
		self.skip_color.setLayoutDirection(QtCore.Qt.RightToLeft)
		self.skip_color.setToolTip("Some Float3 colors can go above 1.0 or below 0.0 to achieve certain effects")

		self.shader_choice = widgets.LabelCombo("Shader:", ())
		self.shader_choice.entry.activated.connect(self.shader_changed)
		self.attribute_choice = widgets.LabelCombo("Attribute:", ())
		self.texture_choice = widgets.LabelCombo("Texture:", ())
		self.attribute_add = QtWidgets.QPushButton("Add Attribute")
		self.attribute_add.clicked.connect(self.add_attribute_clicked)
		self.texture_add = QtWidgets.QPushButton("Add Texture")
		self.texture_add.clicked.connect(self.add_texture_clicked)
		self.lock_attrs.toggled.connect(self.attribute_choice.setHidden)
		self.lock_attrs.toggled.connect(self.attribute_add.setHidden)

		self.tex_container = PropertyContainer(self, "Textures")
		self.attrib_container = PropertyContainer(self, "Attributes")

		self.game_changed()

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
		vbox.addWidget(self.skip_color)
		vbox.addWidget(self.lock_attrs)
		vbox.addStretch(1)
		self.widget.setLayout(vbox)

		main_menu = self.menuBar()
		file_menu = main_menu.addMenu('File')
		edit_menu = main_menu.addMenu('Edit')
		help_menu = main_menu.addMenu('Help')
		button_data = (
			(file_menu, "Open", self.file_widget.ask_open, "CTRL+O", "dir"),
			(file_menu, "Save", self.save_fgm, "CTRL+S", "save"),
			(file_menu, "Save As", self.save_as_fgm, "CTRL+SHIFT+S", "save"),
			(file_menu, "Exit", self.close, "", "exit"),
			(edit_menu, "Import Texture Values", self.import_tex, "", ""),
			(edit_menu, "Import Attribute Values", self.import_att, "", ""),
			(help_menu, "Report Bug", self.report_bug, "", "report"),
			(help_menu, "Documentation", self.online_support, "", "manual")
		)
		self.add_to_menu(button_data)

		if self.lock_attrs.isChecked():
			self.attribute_choice.hide()
			self.attribute_add.hide()

	@staticmethod
	def get_icon(name, format="png"):
		base_dir = os.path.dirname(os.path.realpath(__file__))
		return QIcon(os.path.join(base_dir, f'icons/{name}.{format}'))

	def dragEnterEvent(self, e):
		path = e.mimeData().urls()[0].toLocalFile() if e.mimeData().hasUrls() else ""
		if path.lower().endswith(".fgm"):
			e.accept()
		else:
			e.ignore()

	def dropEvent(self, e):
		path = e.mimeData().urls()[0].toLocalFile() if e.mimeData().hasUrls() else ""
		if path:
			self.file_widget.decide_open(path)

	def game_changed(self,):
		game = self.game_container.entry.currentText()
		logging.info(f"Changed game to {game}")
		try:
			set_game(self.header.context, game)
			# set_game(self.header, game)
		except BaseException as err:
			print(err)

		if is_jwe2(self.header.context):
			self.fgm_dict = fgm_jwe2
		elif is_pz16(self.header.context) or is_pz(self.header.context):
			self.fgm_dict = fgm_pz
		else:
			self.fgm_dict = None
		if self.fgm_dict:
			self.shader_choice.entry.clear()
			self.shader_choice.entry.addItems(sorted(self.fgm_dict.shaders))

	def set_tex_count(self, count=None):
		self.header.texture_count = count if count is not None else len(self.header.textures.data)

	def set_attrib_count(self, count=None):
		self.header.attribute_count = count if count is not None else len(self.header.attributes.data)

	def update_choices(self):
		shader_name = self.shader_choice.entry.currentText()
		if self.fgm_dict and shader_name:
			self.texture_choice.entry.clear()
			self.texture_choice.entry.addItems(sorted(self.fgm_dict.shader_textures[shader_name]))
			self.attribute_choice.entry.clear()
			self.attribute_choice.entry.addItems(sorted(self.fgm_dict.shader_attribs[shader_name]))

	def update_shader(self, name):
		self.shader_choice.entry.setText(name)
		self.update_choices()

	def import_tex(self):
		self.import_fgm()
		if self.import_header:
			try:
				self.merge_textures((self.import_header.textures.data, self.import_header.dependencies.data), 
									(self.header.textures.data, self.header.dependencies.data))
				logging.info("Finished importing texture values")
			except:
				logging.error("Error importing texture values")
				traceback.print_exc()

	def import_att(self):
		self.import_fgm()
		if self.import_header:
			try:
				self.merge_attributes((self.import_header.attributes.data, self.import_header.data_lib.data),
									(self.header.attributes.data, self.header.data_lib.data))
				logging.info("Finished importing attribute values")
			except:
				logging.error("Error importing attribute values")
				traceback.print_exc()

	def merge_textures(self, data_old, data_new):
		try:
			tex_old, dep_old = data_old
			tex_new, dep_new = data_new
			for i, t_old in enumerate(tex_old):
				for j, t_new in enumerate(tex_new):
					if t_old.name == t_new.name:
						t_new.dtype = t_old.dtype
						t_new.value = t_old.value
						dep_new[j].dependency_name.data = dep_old[i].dependency_name.data
						break
		except:
			logging.error("Error merging texture values")
			traceback.print_exc()
		finally:
			# Fix indices again after merge
			self.fix_tex_indices(self.header.textures.data)
			self.tex_container.update_gui(self.header.textures.data, self.header.dependencies.data)

	def merge_attributes(self, data_old, data_new):
		try:
			att_old, lib_old = data_old
			att_new, lib_new = data_new
			for i, a_old in enumerate(att_old):
				for j, a_new in enumerate(att_new):
					if a_old.name == a_new.name:
						assert a_new.dtype == a_old.dtype
						lib_new[j].value = lib_old[i].value
						break
		except:
			logging.error("Error merging attribute values")
			traceback.print_exc()
		finally:
			self.attrib_container.update_gui(self.header.attributes.data, self.header.data_lib.data)

	def shader_changed(self,):
		"""Run only during user activation"""
		self.header.shader_name = self.shader_choice.entry.currentText()
		self.update_choices()

		tex_data_old = (self.header.textures.data.copy(), self.header.dependencies.data.copy())
		attrib_data_old = (self.header.attributes.data.copy(), self.header.data_lib.data.copy())

		self.header.textures.data = Array((1,), self.header.textures.template, self.context, set_default=False)
		self.header.attributes.data = Array((1,), self.header.attributes.template, self.context, set_default=False)
		self.header.dependencies.data = Array((1,), self.header.dependencies.template, self.context, set_default=False)
		self.header.data_lib.data = Array((1,), self.header.data_lib.template, self.context, set_default=False)

		for tex in self.fgm_dict.shader_textures[self.header.shader_name]:
			self.add_texture(tex)
		
		for att in self.fgm_dict.shader_attribs[self.header.shader_name]:
			self.add_attribute(att)

		# Preserve old values when possible
		self.merge_textures(tex_data_old, (self.header.textures.data, self.header.dependencies.data))
		self.merge_attributes(attrib_data_old, (self.header.attributes.data, self.header.data_lib.data))

	def create_tex_name(self, prefix, suffix):
		return f'{prefix.replace(".fgm", "")}.{suffix.lower()}.tex'

	def fix_tex_indices(self, textures):
		for i, tex in enumerate([t for t in textures if t.dtype == FgmDtype.Texture]):
			tex.value[0].index = i

	def fix_dependencies(self, deps):
		for i, dep in enumerate(deps):
			tex_dtype = self.header.textures.data[i].dtype
			if tex_dtype == FgmDtype.RGBA:
				dep.dependency_name.data = ''

	def sort_textures(self):
		textures = self.header.textures.data
		deps = self.header.dependencies.data
		textures[:], deps[:] = zip(*sorted(zip(textures, deps), key=lambda p: p[0].name))
		self.fix_tex_indices(textures)
		return textures, deps

	def add_texture_clicked(self):
		self.add_texture(self.texture_choice.entry.currentText(), update_gui=True)

	def add_texture(self, tex_name, update_gui=False):
		textures = self.header.textures.data
		for tex in textures:
			if tex.name == tex_name:
				logging.warning(f"Texture '{tex_name}' already exists. Ignoring.")
				return

		tex_index = TexIndex(self.context, set_default=False)
		tex_index.set_defaults()

		tex = TextureInfo(self.context, set_default=False)
		tex.dtype = FgmDtype.Texture
		tex.set_defaults()
		tex.name = tex_name
		tex.value[:] = [tex_index]
		textures.append(tex)

		deps = self.header.dependencies.data
		dep = DependencyInfo(self.context, arg=tex, set_default=False)
		dep.set_defaults()
		dep.dependency_name.data = ''
		deps.append(dep)

		self.header.textures.data[:], self.header.dependencies.data[:] = self.sort_textures()
		self.set_tex_count()

		if update_gui:
			self.tex_container.update_gui(self.header.textures.data, self.header.dependencies.data)

	def add_attribute_clicked(self):
		self.add_attribute(self.attribute_choice.entry.currentText(), update_gui=True)

	def fix_att_offsets(self, attributes):
		for i, att in enumerate(attributes):
			att.value_offset = self.offset_for_index(i)

	def offset_for_index(self, index):
		return attrib_sizes[int(self.header.attributes.data[index-1].dtype)] + self.header.attributes.data[index-1].value_offset if index > 0 else 0

	def add_attribute(self, att_name, update_gui=False):
		attributes = self.header.attributes.data
		for attrib in attributes:
			if attrib.name == att_name:
				logging.warning(f"Attribute '{att_name}' already exists. Ignoring.")
				return

		att = AttributeInfo(self.context, set_default=False)
		att.dtype = attrib_dtypes[self.fgm_dict.attributes[att_name][0]]
		att.name = att_name
		att.value_offset = self.offset_for_index(len(self.header.attributes.data))
		attributes.append(att)

		self.header.attributes.data[:] = attributes

		data_lib = self.header.data_lib.data
		data = AttribData(self.context, arg=att, set_default=False)
		data.set_defaults()
		# Assign default value from attributes dict
		if self.fgm_dict.attributes.get(att.name):
			data.value = np.array(self.fgm_dict.attributes[att.name][1][0][0], data.value.dtype)
		data_lib.append(data)

		self.header.data_lib.data[:] = data_lib
		self.set_attrib_count()

		if update_gui:
			self.attrib_container.update_gui(self.header.attributes.data, self.header.data_lib.data)

	@property
	def fgm_name(self,):
		return self.file_widget.entry.text()

	@property
	def fgm_path(self,):
		return os.path.split(self.file_widget.filepath)[0]

	def create_grid(self,):
		g = QtWidgets.QGridLayout()
		g.setContentsMargins(8, 0, 0, 0)
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
				self.header = FgmHeader.from_xml_file(self.file_widget.filepath, self.context)
				enum_name, member_name = self.header.game.split(".")
				game = games[member_name]
				logging.debug(f"from game {game}")
				self.game_container.entry.setText(game.value)
				self.game_changed()
				self.update_shader(self.header.shader_name)
				self.tex_container.update_gui(self.header.textures.data, self.header.dependencies.data)
				self.attrib_container.update_gui(self.header.attributes.data, self.header.data_lib.data)

			except Exception as ex:
				traceback.print_exc()
				ovl_util.interaction.showdialog(str(ex))
				logging.warning(ex)
			logging.info("Done!")

	def import_fgm(self):
		file_in = QtWidgets.QFileDialog.getOpenFileName(self, 'Import FGM', self.cfg.get("dir_fgms_in", "C://"), "FGM files (*.fgm)")[0]
		if file_in:
			try:
				self.cfg["dir_fgms_in"], _ = os.path.split(file_in)
				self.import_header = FgmHeader.from_xml_file(file_in, self.context)
				logging.info(f"Importing {file_in}")
			except Exception as ex:
				traceback.print_exc()
				ovl_util.interaction.showdialog(str(ex))
				logging.warning(ex)

	def _save_fgm(self, filepath):
		if filepath:
			try:
				self.header.to_xml_file(filepath)
			except BaseException as err:
				traceback.print_exc()
				interaction.showdialog(str(err))
				logging.error(err)
			logging.info("Done!")

	def save_fgm(self):
		self._save_fgm(self.file_widget.filepath)

	def save_as_fgm(self):
		file_out = QtWidgets.QFileDialog.getSaveFileName(self, 'Save FGM', os.path.join(self.cfg.get("dir_fgms_out", "C://"), self.fgm_name), "FGM files (*.fgm)",)[0]
		if file_out:
			self.cfg["dir_fgms_out"], fgm_name = os.path.split(file_out)
			self._save_fgm(file_out)
			self.file_widget.set_file_path(file_out)


class PropertyContainer(QtWidgets.QGroupBox):
	def __init__(self, gui, name):
		super().__init__(name)
		self.gui = gui
		self.entry_list = []
		self.data_list = []
		self.widgets = []

	def update_gui(self, entry_list, data_list):
		logging.debug(f"Populating table with {len(entry_list)} entries")
		assert len(entry_list) == len(data_list)
		self.entry_list = entry_list
		self.data_list = data_list
		self.clear_layout()
		grid = self.gui.create_grid()
		grid.setColumnStretch(1, 3)
		grid.setColumnStretch(2, 1)
		grid.setColumnStretch(3, 4)
		self.setLayout(grid)
		self.widgets = []
		for line_i, (entry, data) in enumerate(zip(self.entry_list, self.data_list)):
			w = TextureVisual(self, entry, data)
			self.widgets.append(w)
			grid.addWidget(w.b_delete, line_i, 0)
			grid.addWidget(w.w_label, line_i, 1)
			grid.addWidget(w.w_dtype, line_i, 2)
			grid.addWidget(w.w_data, line_i, 3)
			if self.title() == "Attributes":
				w.b_delete.setHidden(self.gui.lock_attrs.isChecked())
				self.gui.lock_attrs.toggled.connect(w.b_delete.setHidden)

	def clear_layout(self):
		layout = self.layout()
		if layout is not None:
			w = QtWidgets.QWidget()
			w.setLayout(layout)


class TextureVisual:
	def __init__(self, container, entry, data):
		self.container = container
		self.entry = entry
		self.data = data
		self.w_label = QtWidgets.QLabel(entry.name)
		dtypes = [e.name for e in FgmDtype]
		dtypes_tex = [dtypes.pop(dtypes.index("RGBA")), dtypes.pop(dtypes.index("Texture"))]

		self.w_dtype = widgets.CleverCombo(dtypes_tex if container.title() == "Textures" else dtypes)
		self.w_dtype.setText(entry.dtype.name)
		self.w_dtype.setToolTip(f"Data type of {entry.name}")
		self.w_dtype.currentIndexChanged.connect(self.update_dtype)
		if container.title() == "Attributes":
			self.container.gui.lock_attrs.toggled.connect(self.w_dtype.setDisabled)
			if self.container.gui.lock_attrs.isChecked():
				self.w_dtype.setDisabled(True)

		self.b_delete = QtWidgets.QPushButton()
		self.b_delete.setIcon(container.gui.get_icon("x", "svg"))
		self.b_delete.setFlat(True)
		self.b_delete.setIconSize(QtCore.QSize(12, 12))
		self.b_delete.setFixedSize(16, 16)
		self.b_delete.setStyleSheet(r"QPushButton {padding: 2px; margin: 2px 4px 0 0;} QPushButton:pressed { background-color: rgba(240, 30, 30, 128); }")
		self.b_delete.clicked.connect(self.delete)
		self.w_data = QtWidgets.QWidget()
		self.create_fields_w_layout()

		# get tooltip
		tooltip = self.container.gui.tooltips.get(self.entry.name, "Undocumented attribute.")
		if container.title() == "Attributes":
			most_common = [fr"{a[0]} ({a[1]})" if len(a[0]) > 1 else fr"{a[0][0]} ({a[1]})"
							for a in self.container.gui.fgm_dict.attributes.get(self.entry.name, [("No data",), 0])[1]
							if len(a) > 0]
			tooltip += fr"<br><br>Most Common Values (Usage #)<br> {'<br>'.join(most_common)}"
		self.w_data.setToolTip(tooltip)
		self.w_label.setToolTip(tooltip)
		self.b_delete.setToolTip(f"Delete {entry.name}")

	def create_fields_w_layout(self):
		self.fields = self.create_fields()
		if self.w_data.layout():
			QtWidgets.QWidget().setLayout(self.w_data.layout())
		# layout = QGridLayout(self)
		layout = QtWidgets.QHBoxLayout()
		for button in self.fields:
			button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
			layout.addWidget(button)
		self.w_data.setLayout(layout)

	def delete(self):
		try:
			self.container.entry_list.remove(self.entry)
			self.container.data_list.remove(self.data)
			self.container.gui.set_tex_count()
			self.container.gui.set_attrib_count()
			self.container.update_gui(self.container.entry_list, self.container.data_list)
		except:
			traceback.print_exc()
		finally:
			self.update()

	def update(self):
		if self.entry.dtype == FgmDtype.Texture or self.entry.dtype == FgmDtype.RGBA:
			# Update texture indices after changing texture type
			self.container.gui.fix_tex_indices(self.container.entry_list)
			self.container.gui.fix_dependencies(self.container.data_list)
		else:
			# Update attribute offsets after changing type
			self.container.gui.fix_att_offsets(self.container.entry_list)

	def update_dtype(self, ind):
		dtype_name = self.w_dtype.currentText()
		self.entry.dtype = FgmDtype[dtype_name]
		try:
			self.data.set_defaults()
			if self.entry.dtype == FgmDtype.Texture:
				self.entry.value = None
				self.data.dependency_name.data = ''

			self.entry.set_defaults()

			# Set RGBA values to middle gray
			if self.entry.dtype == FgmDtype.RGBA:
				self.entry.value[0].r = 127
				self.entry.value[0].g = 127
				self.entry.value[0].b = 127
				self.entry.value[0].a = 255
				self.entry.value[1].r = 127
				self.entry.value[1].g = 127
				self.entry.value[1].b = 127
				self.entry.value[1].a = 255

			self.create_fields_w_layout()
			self.update()

		except:
			traceback.print_exc()

	def update_file(self, file):
		self.data.dependency_name.data = file

	def create_fields(self):
		rgb_colors = ("_RGB", "Tint", "Discolour", "Colour")
		if self.entry.dtype == FgmDtype.Texture:
			assert self.data.dependency_name.data is not None
			if self.data.dependency_name.data == '':
				self.data.dependency_name.data = self.container.gui.create_tex_name(self.container.gui.fgm_name, self.entry.name)

			self.w_file = widgets.FileWidget(self.container, self.container.gui.cfg, ask_user=False,
											dtype="TEX", poll=False, editable=True, check_exists=True, root=self.container.gui.fgm_path)
			self.w_file.set_file_path(self.data.dependency_name.data)
			self.w_file.entry.textChanged.connect(self.update_file)
			return self.w_file,
		elif self.entry.dtype == FgmDtype.RGBA:
			return [self.create_field(i, self.entry.value) for i in range(len(self.entry.value))]
		elif self.entry.dtype == FgmDtype.Float3 and not self.container.gui.skip_color.isChecked() and self.entry.name.endswith(rgb_colors):
			return self.create_rgb_field(),
		else:
			return [self.create_field(i, self.data.value) for i in range(len(self.data.value))]

	def update_rgb_field(self, c):
		self.data.value = np.array([x / 255 for x in c.getRgb()[:3]])

	def create_rgb_field(self):
		field = QColorButton()
		field.colorChanged.connect(self.update_rgb_field)
		d = [int(np.rint(x * 255)) for x in self.data.value]
		c = QColor(*d, 255)
		field.setColor(c)
		return field

	def create_field(self, ind, target):
		default = target[ind]

		def update_ind_color(c):
			# use a closure to remember index
			if c:
				color = target[ind]
				color.r, color.g, color.b, color.a = c.getRgb()

		def update_ind(v):
			# use a closure to remember index
			target[ind] = v

		def update_ind_int(v):
			# use a closure to remember index
			target[ind] = int(v)

		t = self.entry.dtype.name
		if "RGBA" in t:
			field = QColorButton()
			# Create container for transparency background
			frame = QtWidgets.QFrame()
			frame.setObjectName("ColorFrame")
			frame.setContentsMargins(0, 0, 0, 0)
			layout = QtWidgets.QHBoxLayout()
			layout.addWidget(QColorButton())
			layout.setContentsMargins(0, 0, 0, 0)
			layout.setSpacing(0)
			frame.setLayout(layout)
			field = frame
			field.children()[1].colorChanged.connect(update_ind_color)
			frame.setStyleSheet((f"""QFrame#ColorFrame {{ 
				background-image: url('icon:transparency.png');
				max-height: 22px;
				max-width: 100px;
				padding: 0px;
				border: 0px;
				border-radius: 4px;
			}}"""))

		elif "Float" in t:
			field = QtWidgets.QDoubleSpinBox()
			field.setDecimals(3)
			field.setRange(-10000, 10000)
			field.setSingleStep(.05)
			field.valueChanged.connect(update_ind)
		elif "Bool" in t:
			field = MySwitch()
			field.clicked.connect(update_ind)
		elif "Int" in t:
			default = int(default)
			field = QtWidgets.QDoubleSpinBox()
			field.setDecimals(0)
			field.setRange(-MAX_UINT, MAX_UINT)
			field.valueChanged.connect(update_ind_int)
		else:
			raise AttributeError(f"Unsupported field type {t}")
		
		if "RGBA" in t:
			field.children()[1].setValue(default)
		else:
			field.setValue(default)
			
		field.setMinimumWidth(50)
		return field


if __name__ == '__main__':
	widgets.startup(MainWindow)
