import logging
import sys
import time
from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from ovl_util.config import read_str_dict, read_list

from generated.formats.matcol.compounds.MatcolRoot import MatcolRoot
from generated.formats.ovl_base import OvlContext

from PyQt5 import QtWidgets


class MainWindow(widgets.MainWindow):

	def __init__(self, opts: GuiOptions):
		self.scrollarea = QtWidgets.QScrollArea()
		self.scrollarea.setWidgetResizable(True)

		# the actual scrollable stuff
		self.widget = QtWidgets.QWidget()
		self.scrollarea.setWidget(self.widget)

		widgets.MainWindow.__init__(self, "Matcol Editor", opts=opts, central_widget=self.scrollarea)

		self.context = OvlContext()
		self.matcol_data = MatcolRoot(self.context)
		self.file_widget = self.make_file_widget(ftype="materialcollection")
		self.tooltips = read_str_dict("gui/tooltips/matcol.txt")
		self.default_fgms = read_list("gui/tooltips/matcol-fgm-names.txt")

		# Setup Menus
		self.build_menus({
			widgets.FILE_MENU: self.file_menu_items,
			widgets.HELP_MENU: self.help_menu_items,
		})

		self.tex_container = QtWidgets.QGroupBox("Slots")
		self.attrib_container = QtWidgets.QGroupBox("Attributes")

		self.vbox = QtWidgets.QVBoxLayout()
		self.vbox.addWidget(self.file_widget)
		self.vbox.addWidget(self.tex_container)
		self.vbox.addWidget(self.attrib_container)
		self.vbox.addStretch(1)
		self.widget.setLayout(self.vbox)

		self.tex_grid = self.create_grid()
		self.attrib_grid = self.create_grid()

		self.tex_container.setLayout(self.tex_grid)
		self.attrib_container.setLayout(self.attrib_grid)

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
			widget.deleteLater()

	def open(self, filepath):
		if filepath:
			try:
				self.matcol_data = self.matcol_data.from_xml_file(filepath, self.context)

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
					for float_attribute in attrib.float_attributes.data:
						w = widgets.MatcolFloatAttrib(float_attribute, self.tooltips)
						lay.addWidget(w.label, sub_line_i, 0)
						lay.addWidget(w.data, sub_line_i, 1)
						sub_line_i += 1
					box.setLayout(lay)
			except:
				logging.exception(f"Something went wrong")
			logging.info("Done!")

	def save(self, filepath):
		with self.matcol_data.to_xml_file(self.matcol_data, filepath) as xml_root:
			pass
			
	
if __name__ == '__main__':
	startup(MainWindow, GuiOptions(log_name="matcol_editor_gui", size=(450, 500)))
