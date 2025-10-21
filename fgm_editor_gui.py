import logging
import os
from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from gui.widgets import MenuItem, SeparatorMenuItem
from modules.formats.FGM import FgmContext
from ovl_util.config import read_str_dict
from typing import Any, Optional

from constants import ConstantsProvider
from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.fgm.structs.FgmHeader import FgmHeader
from generated.formats.fgm.structs.TexIndex import TexIndex
from generated.formats.fgm.structs.TextureInfo import TextureInfo
from generated.formats.fgm.structs.TextureData import TextureData
from generated.formats.fgm.structs.AttribInfo import AttribInfo
from generated.formats.fgm.structs.AttribData import AttribData
from generated.array import Array
from generated.formats.ovl.versions import *

import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor


class MainWindow(widgets.MainWindow):

	def __init__(self, opts: GuiOptions):
		self.scrollarea = QtWidgets.QScrollArea()
		self.scrollarea.setWidgetResizable(True)
		# the actual scrollable stuff
		self.widget = QtWidgets.QWidget()
		self.scrollarea.setWidget(self.widget)

		widgets.MainWindow.__init__(self, "FGM Editor", opts=opts, central_widget=self.scrollarea)

		self.setAcceptDrops(True)

		self.context = FgmContext(loader=None)
		self.constants = ConstantsProvider()
		self.header = FgmHeader(self.context)
		self.tooltips = read_str_dict("gui/tooltips/fgm.txt")
		self.games = [g.value for g in games]
		self.import_header = None

		self.game_choice = widgets.LabelCombo("Game", self.games, editable=False, activated_fn=self.game_changed)

		self.file_widget = self.make_file_widget(ftype="FGM")

		self.lock_attrs = QtWidgets.QCheckBox("Lock Data")
		self.lock_attrs.setLayoutDirection(QtCore.Qt.RightToLeft)
		self.lock_attrs.setChecked(True)

		self.skip_color = QtWidgets.QCheckBox("Disable Float3 Color Widgets")
		self.skip_color.setLayoutDirection(QtCore.Qt.RightToLeft)
		self.skip_color.setToolTip("Some Float3 colors can go above 1.0 or below 0.0 to achieve certain effects")

		self.shader_choice = widgets.LabelCombo("Shader", (), activated_fn=self.shader_changed)
		self.attribute_choice = widgets.LabelCombo("Attribute", ())
		self.texture_choice = widgets.LabelCombo("Texture", ())
		self.attribute_add = QtWidgets.QPushButton("Add Attribute")
		self.attribute_add.clicked.connect(self.add_attribute_clicked)
		self.texture_add = QtWidgets.QPushButton("Add Texture")
		self.texture_add.clicked.connect(self.add_texture_clicked)
		self.lock_attrs.toggled.connect(self.texture_choice.setHidden)
		self.lock_attrs.toggled.connect(self.texture_add.setHidden)
		self.lock_attrs.toggled.connect(self.attribute_choice.setHidden)
		self.lock_attrs.toggled.connect(self.attribute_add.setHidden)

		self.tex_container = PropertyContainer(self, "Textures")
		self.attrib_container = PropertyContainer(self, "Attributes")

		self.game_changed()

		vbox = QtWidgets.QVBoxLayout()
		
		vbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
		vbox.addWidget(self.file_widget)
		vbox.addWidget(self.game_choice)
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

		# Setup Menus
		self.build_menus({
			widgets.FILE_MENU: [
				MenuItem("New", self.new_file, shortcut="CTRL+N", icon="new"),
				SeparatorMenuItem(),
				*self.file_menu_items,
			],
			widgets.EDIT_MENU: [
				MenuItem("Import Texture Values", self.import_tex),
				MenuItem("Import Attribute Values", self.import_att),
			],
			widgets.VIEW_MENU: self.view_menu_items,
			widgets.HELP_MENU: self.help_menu_items
		})

		self.lock_attrs.toggled.emit(True)

		self.layout_logger(self.central_widget, widgets.LOGGER_BOTTOM)

	@property
	def game(self):
		return self.game_choice.entry.currentText()

	def game_changed(self, game: Optional[str] = None):
		if game is None:
			game = self.game
		else:
			logging.info(f"Changed game to {game}")
		self.header.game = game
		self.header.context.game = game
		try:
			shaders = self.constants[game]["shaders"]
			self.shader_choice.entry.clear()
			self.shader_choice.entry.addItems(sorted(shaders.keys()))
		except:
			logging.warning(f"No presets for game {game}")

	def update_choices(self):
		shader_name = self.shader_choice.entry.currentText()
		if shader_name:
			self.texture_choice.entry.clear()
			self.attribute_choice.entry.clear()
			try:
				textures, attrib_dic = self.current_shaders[shader_name]
				self.texture_choice.entry.addItems(textures)
				self.attribute_choice.entry.addItems(attrib_dic.keys())
			except:
				logging.warning(f"{self.game} shader constants missing for shader: '{shader_name}'")

	@property
	def current_shaders(self):
		try:
			return self.constants[self.game]["shaders"]
		except:
			logging.warning(f"No presets for game {self.game}")
			return {}

	def update_shader(self, name):
		self.shader_choice.entry.setText(name)
		self.update_choices()

	def import_tex(self):
		self.import_fgm()
		if self.import_header:
			try:
				self.merge_textures((self.import_header.textures.data, self.import_header.name_foreach_textures.data),
									(self.header.textures.data, self.header.name_foreach_textures.data))
				logging.info("Finished importing texture values")
			except:
				logging.exception("Error importing texture values")

	def import_att(self):
		self.import_fgm()
		if self.import_header:
			try:
				self.merge_attributes((self.import_header.attributes.data, self.import_header.value_foreach_attributes.data),
									(self.header.attributes.data, self.header.value_foreach_attributes.data))
				logging.info("Finished importing attribute values")
			except:
				logging.exception("Error importing attribute values")

	def merge_textures(self, data_old, data_new):
		try:
			if data_old and data_new:
				tex_old, dep_old = data_old
				tex_new, dep_new = data_new
				for i, t_old in enumerate(tex_old):
					for j, t_new in enumerate(tex_new):
						if t_old.name == t_new.name:
							t_new.dtype = t_old.dtype
							t_new.reset_field("value")
							t_new.value = t_old.value
							dep_new[j].dependency_name.data = dep_old[i].dependency_name.data
							break
		except:
			logging.exception("Could not merge texture values")
		finally:
			# Fix indices again after merge
			self.tex_container.update_gui(self.header.textures.data, self.header.name_foreach_textures.data)
			self.set_dirty()

	def merge_attributes(self, data_old, data_new):
		try:
			if data_old and data_new:
				att_old, lib_old = data_old
				att_new, lib_new = data_new
				for i, a_old in enumerate(att_old):
					for j, a_new in enumerate(att_new):
						if a_old.name == a_new.name:
							assert a_new.dtype == a_old.dtype
							lib_new[j].value = lib_old[i].value
							break
		except:
			logging.exception("Could not merge attribute values")
		finally:
			self.attrib_container.update_gui(self.header.attributes.data, self.header.value_foreach_attributes.data)
			self.set_dirty()

	def has_data(self):
		return self.header.textures.data and self.header.name_foreach_textures.data and self.header.attributes.data and self.header.value_foreach_attributes.data

	def shader_changed(self, name: str):
		"""Run only during user activation"""
		self.header.shader_name = name
		self.update_choices()
		try:
			tex_data_old = (self.header.textures.data.copy(), self.header.name_foreach_textures.data.copy()) if self.has_data() else None
			attrib_data_old = (self.header.attributes.data.copy(), self.header.value_foreach_attributes.data.copy()) if self.has_data() else None
			self.set_dirty()

			self.header.textures.data = Array(self.context, 0, None, (0,), self.header.textures.template)
			self.header.attributes.data = Array(self.context, 0, None, (0,), self.header.attributes.template)
			self.header.name_foreach_textures.data = Array(self.context, self.header.textures, None, (0,), self.header.name_foreach_textures.template)
			self.header.value_foreach_attributes.data = Array(self.context, self.header.attributes, None, (0,), self.header.value_foreach_attributes.template)

			textures, attrib_dic = self.current_shaders[self.header.shader_name]
			for tex_name in textures:
				self.add_texture(tex_name)

			for att_name in attrib_dic.keys():
				self.add_attribute(att_name)

			# Preserve old values when possible
			self.merge_textures(tex_data_old, (self.header.textures.data, self.header.name_foreach_textures.data))
			self.merge_attributes(attrib_data_old, (self.header.attributes.data, self.header.value_foreach_attributes.data))
		except:
			logging.exception(f"Shader change failed")

	def create_tex_name(self, prefix, suffix):
		return f'{prefix.replace(".fgm", "")}.{suffix.lower()}.tex'

	def fix_dependencies(self, deps):
		for i, dep in enumerate(deps):
			tex_dtype = self.header.textures.data[i].dtype
			if tex_dtype == FgmDtype.RGBA:
				dep.dependency_name.data = ''

	def sort_textures(self):
		textures = self.header.textures.data
		deps = self.header.name_foreach_textures.data
		self.header.textures.data[:], self.header.name_foreach_textures.data[:] = zip(*sorted(zip(textures, deps), key=lambda p: p[0].name))

	def add_texture_clicked(self):
		self.add_texture(self.texture_choice.entry.currentText(), update_gui=True)

	def add_texture(self, tex_name, update_gui=False):
		try:
			if self.header.textures.data is None:
				self.header.textures.data = Array(self.context, 0, None, (0,), TextureInfo)
			if self.header.name_foreach_textures.data is None:
				self.header.name_foreach_textures.data = Array(self.context, self.header.textures, None, (0,), TextureData)
			textures = self.header.textures.data
			for tex in textures:
				if tex.name == tex_name:
					logging.warning(f"Texture '{tex_name}' already exists. Ignoring.")
					return

			tex_index = TexIndex(self.context)

			tex = TextureInfo(self.context)
			tex.dtype = FgmDtype.TEXTURE
			tex.name = tex_name
			tex.reset_field("value")
			tex.value[:] = [tex_index]
			textures.append(tex)

			dep = TextureData(self.context, arg=tex)
			dep.dependency_name.data = ''
			self.header.name_foreach_textures.data.append(dep)

			self.sort_textures()

			if update_gui:
				self.tex_container.update_gui(self.header.textures.data, self.header.name_foreach_textures.data)
		except:
			logging.exception(f"Tex failed")

	def sort_attributes(self):
		attribs = self.header.attributes.data
		data = self.header.value_foreach_attributes.data
		attribs[:], data[:] = zip(*sorted(zip(attribs, data), key=lambda p: p[0].name))
		return attribs, data

	def add_attribute_clicked(self):
		self.add_attribute(self.attribute_choice.entry.currentText(), update_gui=True)

	def add_attribute(self, att_name, update_gui=False):
		attributes = self.header.attributes.data
		for attrib in attributes:
			if attrib.name == att_name:
				logging.warning(f"Attribute '{att_name}' already exists. Ignoring.")
				return

		att = AttribInfo(self.context)
		_, attrib_dict = self.current_shaders[self.header.shader_name]
		attr_data = attrib_dict[att_name]
		att.dtype = FgmDtype.from_value(attr_data[0])
		att.name = att_name
		attributes.append(att)

		data_lib = self.header.value_foreach_attributes.data
		data = AttribData(self.context, arg=att)
		# Assign default value from attributes dict
		data.value = np.array(attr_data[1][0][0], data.value.dtype)
		data_lib.append(data)

		self.header.attributes.data[:], self.header.value_foreach_attributes.data[:] = self.sort_attributes()

		if update_gui:
			self.attrib_container.update_gui(self.header.attributes.data, self.header.value_foreach_attributes.data)

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

	def new_file(self):
		self.file_widget.set_file_path("")

	def open(self, filepath):
		if filepath:
			try:
				self.header: FgmHeader = FgmHeader.from_xml_file(filepath, self.context)
				logging.debug(f"from game {self.header.game}")
				self.game_choice.entry.setText(self.header.game)
				self.game_changed()
				self.update_shader(self.header.shader_name)
				self.tex_container.update_gui(self.header.textures.data, self.header.name_foreach_textures.data)
				self.attrib_container.update_gui(self.header.attributes.data, self.header.value_foreach_attributes.data)
				self.set_clean()
				logging.info(f"Opened {filepath}")
			except:
				self.handle_error("Opening failed, see log!")

	def import_fgm(self):
		file_in = self.file_widget.get_open_file_name(f'Import FGM')
		if file_in:
			try:
				self.cfg["dir_fgms_in"], _ = os.path.split(file_in)
				self.import_header = FgmHeader.from_xml_file(file_in, self.context)
				logging.info(f"Importing {file_in}")
			except:
				self.handle_error("Importing failed, see log!")

	def save(self, filepath) -> None:
		try:
			with self.header.to_xml_file(self.header, filepath):
				# got to use context manager, but there's no need to do any post-write cleanup here
				pass
			self.set_clean()
			logging.info(f"Saved {filepath}")
		except:
			self.handle_error("Saving failed, see log!")


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
		dtypes_tex = [dtypes.pop(dtypes.index("RGBA")), dtypes.pop(dtypes.index("TEXTURE"))]

		self.w_dtype = widgets.CleverCombo(self.container, options=dtypes_tex if container.title() == "Textures" else dtypes)
		self.w_dtype.setText(entry.dtype.name)
		self.w_dtype.setToolTip(f"Data type of {entry.name}")
		self.w_dtype.currentIndexChanged.connect(self.update_dtype)
		if container.title() == "Attributes":
			self.container.gui.lock_attrs.toggled.connect(self.w_dtype.setDisabled)
			if self.container.gui.lock_attrs.isChecked():
				self.w_dtype.setDisabled(True)

		self.b_delete = QtWidgets.QPushButton()
		self.b_delete.setIcon(widgets.get_icon("x"))
		self.b_delete.setFlat(True)
		self.b_delete.setIconSize(QtCore.QSize(12, 12))
		self.b_delete.setFixedSize(16, 16)
		self.b_delete.setStyleSheet(r"QPushButton {padding: 2px; margin: 2px 4px 0 0;} QPushButton:pressed { background-color: rgba(240, 30, 30, 128); }")
		self.b_delete.clicked.connect(self.delete)
		self.w_data = QtWidgets.QWidget()
		self.create_fields_w_layout()

		# get tooltip from fgm dict
		tooltip = self.container.gui.tooltips.get(self.entry.name, "Undocumented attribute.")
		if container.title() == "Attributes":
			most_common = []
			try:
				gui = self.container.gui
				tex, attr_dict = gui.current_shaders[gui.header.shader_name]
				dtype, data_dist = attr_dict.get(self.entry.name, (0, [((0,), 0)]))
				most_common = [fr"{a[0]} ({a[1]})" if len(a[0]) > 1 else fr"{a[0][0]} ({a[1]})"
								for a in data_dist if len(a) > 0]
			except:
				logging.debug(f"Attribute tooltip for {self.entry.name} failed")
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
			self.container.update_gui(self.container.entry_list, self.container.data_list)
		except:
			logging.exception("Deleting errored")
		finally:
			self.update()

	def update(self):
		if self.entry.dtype == FgmDtype.TEXTURE or self.entry.dtype == FgmDtype.RGBA:
			# Update texture indices after changing texture type
			self.container.gui.fix_dependencies(self.container.data_list)
		self.container.gui.set_dirty()

	def update_dtype(self, ind):
		dtype_name = self.w_dtype.currentText()
		self.entry.set_defaults()
		self.entry.dtype = FgmDtype[dtype_name]
		try:
			self.data.set_defaults()
			if self.entry.dtype == FgmDtype.TEXTURE:
				self.entry.value = None
				self.data.dependency_name.data = ''
			self.entry.reset_field("value")
			# Set RGBA values to middle gray
			if self.entry.dtype == FgmDtype.RGBA:
				for v in self.entry.value:
					v.r = v.g = v.b = 127
					v.a = 255
			self.create_fields_w_layout()
			# self.w_tile.setVisible(self.entry.dtype == FgmDtype.TEXTURE)
			self.update()
		except:
			logging.exception("Updating dtype errored")

	def update_file(self, file):
		self.data.dependency_name.data = file
		self.container.gui.set_dirty()

	def update_tile_i(self, tile_i):
		self.entry.value[0].array_index = tile_i
		self.container.gui.set_dirty()

	def create_fields(self):
		rgb_colors = ("_RGB", "Tint", "Discolour", "Colour")
		if self.entry.dtype == FgmDtype.TEXTURE:
			assert self.data.dependency_name.data is not None
			if self.data.dependency_name.data == '':
				self.data.dependency_name.data = self.container.gui.create_tex_name(self.container.gui.fgm_name, self.entry.name)

			self.w_file = widgets.FileWidget(self.container, self.container.gui.cfg, ftype="TEX", ask_user=False,
											 editable=True, check_exists=True, root=self.container.gui.fgm_path)
			self.w_file.set_file_path(self.data.dependency_name.data)
			self.w_file.entry.textChanged.connect(self.update_file)
			self.w_tile = QtWidgets.QSpinBox(self.container)
			self.w_tile.setMaximumWidth(36)
			self.w_tile.setToolTip("Array Tile Index")
			self.w_tile.setRange(0, 2147483647)
			self.w_tile.setValue(self.entry.value[0].array_index)
			self.w_tile.valueChanged.connect(self.update_tile_i)
			self.w_tile.setVisible(self.entry.dtype == FgmDtype.TEXTURE)
			return self.w_file, self.w_tile
		elif self.entry.dtype == FgmDtype.RGBA:
			return [self.create_field(i, self.entry.value) for i in range(len(self.entry.value))]
		elif self.entry.dtype == FgmDtype.FLOAT_3 and not self.container.gui.skip_color.isChecked() and self.entry.name.endswith(rgb_colors):
			return self.create_rgb_field(),
		else:
			return [self.create_field(i, self.data.value) for i in range(len(self.data.value))]

	def update_rgb_field(self, c):
		self.data.value = np.array([x / 255 for x in c.getRgb()[:3]])
		self.container.gui.set_dirty()

	def create_rgb_field(self):
		field = widgets.QColorButton()
		d = [int(np.rint(x * 255)) for x in self.data.value]
		c = QColor(*d, 255)
		field.setColor(c)
		field.colorChanged.connect(self.update_rgb_field)
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

		t = self.entry.dtype.name.lower()
		if "rgba" in t:
			field = widgets.QColorButton()
			# Create container for transparency background
			frame = QtWidgets.QFrame()
			frame.setObjectName("ColorFrame")
			frame.setContentsMargins(0, 0, 0, 0)
			layout = QtWidgets.QHBoxLayout()
			layout.addWidget(widgets.QColorButton())
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

		elif "float" in t:
			field = widgets.NoScrollDoubleSpinBox()
			field.setDecimals(3)
			field.setRange(-10000, 10000)
			field.setSingleStep(.05)
			field.valueChanged.connect(update_ind)
		elif "bool" in t:
			field = widgets.OnOffSwitch()
			field.clicked.connect(update_ind)
		elif "int" in t:
			default = int(default)
			field = widgets.NoScrollDoubleSpinBox()
			field.setDecimals(0)
			field.setRange(-widgets.MAX_UINT, widgets.MAX_UINT)
			field.valueChanged.connect(update_ind_int)
		else:
			raise AttributeError(f"Unsupported field type {t}")

		if "rgba" in t:
			field.children()[1].setValue(default)
		else:
			field.setValue(default)

		# Connect *after* setting initial value
		if "rgba" in t:
			field.children()[1].colorChanged.connect(self.container.gui.set_dirty)
		elif "float" in t:
			field.valueChanged.connect(self.container.gui.set_dirty)
		elif "bool" in t:
			field.clicked.connect(self.container.gui.set_dirty)
		elif "int" in t:
			field.valueChanged.connect(self.container.gui.set_dirty)

		field.setMinimumWidth(50)
		return field


if __name__ == '__main__':
	startup(MainWindow, GuiOptions(log_name="fgm_editor_gui"))
