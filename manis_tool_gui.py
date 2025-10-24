import contextlib
import time
import logging

from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from gui.widgets import MenuItem, SeparatorMenuItem
from generated.formats.manis import ManisFile
from generated.formats.manis.versions import games
from typing import Optional
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from matplotlib import pyplot as plt
plt.set_loglevel(level='warning')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar


from gui.widgets import get_icon


class MainWindow(widgets.MainWindow):

	def __init__(self, opts: GuiOptions):
		widgets.MainWindow.__init__(self, "Manis Editor", opts=opts)
		self.setAcceptDrops(True)

		self.manis_file = ManisFile()

		self.filter = "Supported files (*manis)"

		self.file_widget = self.make_file_widget(ftype="MANIS")

		self.game_choice = widgets.LabelCombo("Game", [g.value for g in games], editable=False,
											  changed_fn=self.game_changed)

		self.stream_entry = QtWidgets.QLineEdit()
		self.stream_entry.setPlaceholderText("Stream")
		self.stream_entry.setToolTip("OVS stream that holds this manis' data")
		# create the table
		self.header_labels = ["Name", "Num", "Compressed", "Duration", "Frames"]

		# tree
		self.tree = QtWidgets.QTreeWidget(self)
		self.tree.setColumnCount(2)
		self.tree.setHeaderLabels(self.header_labels)
		self.tree.setAlternatingRowColors(True)
		self.tree.itemChanged.connect(self.edit_handle)
		self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tree.customContextMenuRequested.connect(self.context_menu)
		self.tree.itemSelectionChanged.connect(self.selection_change)

		self.setup_plot()
		splitter = QtWidgets.QSplitter()
		splitter.addWidget(self.tree)

		toolbar = NavigationToolbar(self.fig.canvas, self)

		plot = widgets.pack_in_box(toolbar, self.fig.canvas)
		self.fig.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		plot.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		splitter.addWidget(plot)
		splitter.setSizes([30, 50])
		splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		hbox = QtWidgets.QHBoxLayout()
		hbox.addWidget(self.file_widget)
		hbox.addWidget(self.stream_entry)
		hbox.addWidget(self.game_choice)
		self.qgrid = QtWidgets.QVBoxLayout()
		self.qgrid.addLayout(hbox)
		self.qgrid.addWidget(splitter)

		self.qgrid.addWidget(self.progress)
		self.central_widget.setLayout(self.qgrid)

		self.build_menus({
			widgets.FILE_MENU: self.file_menu_items,
			widgets.EDIT_MENU: [
				MenuItem("Append", self.append, icon="append"),
				MenuItem("Duplicate Selected", self.duplicate, shortcut="SHIFT+D", icon="duplicate_mesh"),
				MenuItem("Remove Selected", self.remove, shortcut="DEL", icon="delete_mesh"),
			],
			widgets.HELP_MENU: self.help_menu_items
		})

	def setup_plot(self):
		# a figure instance to plot on
		self.setPalette(self.get_palette_from_cfg())
		text_color = self.get_palette_color(self.palette().text())
		text2_color = self.get_palette_color(self.palette().dark())
		self.fig, self.ax = plt.subplots(nrows=1, ncols=1, layout="tight", facecolor=text_color)
		# self.ax.set_xlabel('Frame', color=text_color)
		# self.ax.set_ylabel('Value', color=text_color)
		self.ax.spines['bottom'].set_color(text2_color)
		self.ax.spines['top'].set_color(text2_color)
		self.ax.spines['right'].set_color(text2_color)
		self.ax.spines['left'].set_color(text2_color)
		self.ax.tick_params(axis='x', colors=text2_color)
		self.ax.tick_params(axis='y', colors=text2_color)

		# the range is not automatically fixed
		self.fig.patch.set_facecolor(self.get_palette_color(self.palette().base()))
		self.ax.set_facecolor(self.get_palette_color(self.palette().alternateBase()))

	def get_palette_color(self, input_color):
		col = input_color.color().toRgb()
		col_rgb = (col.red() / 255, col.green() / 255, col.blue() / 255)
		return col_rgb

	@contextlib.contextmanager
	def update_plot(self):
		# discards the old graph
		self.ax.clear()
		yield
		# self.ax.set_xlabel('Frame')
		# self.ax.set_ylabel('Value')
		# refresh canvas
		self.fig.canvas.draw()

	def selection_change(self):
		for item in self.tree.selectedItems():
			names = self.get_parents(item)
			if len(names) == 1:
				mani_name, = names
			elif len(names) == 3:
				mani_name, dtype, bone_name = names

				with self.update_plot():
					try:
						self.manis_file.show_keys_by_dtype(mani_name, dtype, bone_name, self.ax)
					except:
						logging.exception(f"failed")

	def context_menu(self, pos):
		item = self.tree.itemAt(pos)
		if item:
			names = self.get_parents(item)
			if len(names) == 1:
				mani_name, = names
			elif len(names) == 3:
				mani_name, dtype, bone_name = names
				menu = QtWidgets.QMenu("Test", self.tree)
				show_keys = QtWidgets.QAction("Show Keys")

				def show_keys_cb(checked):
					with self.update_plot():
						try:
							self.manis_file.show_keys_by_dtype(mani_name, dtype, bone_name, self.ax)
						except:
							logging.exception(f"failed")
				show_keys.triggered.connect(show_keys_cb)
				menu.addAction(show_keys)
				delete = QtWidgets.QAction(f"Delete {bone_name}")
				menu.addAction(delete)
				menu.exec(self.tree.mapToGlobal(pos))

	def get_parents(self, item):
		names = [item.text(0), ]
		while item.parent():
			item = item.parent()
			names.insert(0, item.text(0))
		return names

	def game_changed(self, game: Optional[str] = None):
		if game is None:
			game = self.game_choice.entry.currentText()
		logging.info(f"Setting Manis version to {game}")
		self.manis_file.game = game

	def edit_handle(self, item, col):
		ix = self.tree.indexOfTopLevelItem(item)
		mani_info = self.manis_file.mani_infos[ix]
		new_val = item.text(col)
		dtype = self.header_labels[col]
		logging.info(f"Editing {mani_info.name}.{dtype} = {new_val}")
		try:
			if dtype == "Name":
				# force new name to be lowercase
				new_name = new_val.lower()
				try:
					if self.manis_file.name_used(new_name):
						self.showwarning(f"Model {new_name} already exists in MANIS!")
					# new name is new
					else:
						self.manis_file.rename_file(mani_info.name, new_name)
						self.set_file_modified(True)
				except:
					self.handle_error("Renaming failed, see log!")
				self.update_gui_table()
			elif dtype == "Compressed":
				if mani_info.dtype.compression == 1 and new_val == "0":
					logging.info(f"Decompressing")
					self.manis_file.decompress(mani_info, dump=False)
					mani_info.dtype.compression = 0
					mani_info.dtype.has_list = 0
					k = mani_info.keys
					ck = mani_info.keys.compressed
					# mani_info.keys.set_defaults()
					k.reset_field("pos_bones")
					k.reset_field("ori_bones")
					k.pos_bones[:] = ck.pos_bones
					k.ori_bones[:] = ck.ori_bones
					# k.scl_bones[:] = ck.scl_bones
			elif dtype == "Duration":
				logging.info(f"Changing duration to {new_val}")
				mani_info.duration = float(new_val)
		except:
			logging.exception("edit_handle")

	def remove(self):
		for item in self.tree.selectedItems():
			names = self.get_parents(item)
			if len(names) == 1:
				mani_name, = names
				try:
					self.manis_file.remove((mani_name, ))
					self.set_file_modified(True)
				except:
					self.handle_error("Removing file failed, see log!")
			elif len(names) == 3:
				mani_name, dtype, bone_name = names
		self.update_gui_table()

	def duplicate(self):
		for item in self.tree.selectedItems():
			names = self.get_parents(item)
			if len(names) == 1:
				mani_name, = names
				try:
					self.manis_file.duplicate((mani_name, ))
					self.set_file_modified(True)
				except:
					self.handle_error("Duplicating file failed, see log!")
			elif len(names) == 3:
				mani_name, dtype, bone_name = names
		self.update_gui_table()

	def open(self, filepath):
		if filepath:
			self.set_file_modified(False)
			try:
				self.manis_file.load(filepath)
				# print(self.manis_file)
			except:
				self.handle_error("Loading failed, see log!")
			self.update_gui_table()

	def append(self):
		if self.file_widget.is_open():
			append_path = self.file_widget.get_open_file_name(f'Append MANIS')
			if append_path:
				try:
					other_manis_file = ManisFile()
					other_manis_file.load(append_path)
					# ensure that there are no name collisions
					for mani_info in other_manis_file.mani_infos:
						self.manis_file.make_name_unique(mani_info)
						self.manis_file.mani_infos.append(mani_info)
						# update context reference on everything do that indexing happens using the correct reference
						mani_info.set_context(self.manis_file.context)
						mani_info.keys.set_context(self.manis_file.context)
					self.set_file_modified(True)
				except:
					self.handle_error("Appending failed, see log!")
				self.update_gui_table()

	def update_gui_table(self, ):
		start_time = time.time()
		try:
			logging.info(f"Loading {len(self.manis_file.mani_infos)} files into GUI")
			self.tree.clear()
			self.tree.itemChanged.disconnect(self.edit_handle)
			# addition data to the tree
			for m in self.manis_file.mani_infos:
				mani_item = QtWidgets.QTreeWidgetItem(self.tree)
				mani_item.setText(0, m.name)
				mani_item.setIcon(0, get_icon("mani"))
				mani_item.setText(2, str(m.dtype.compression))
				mani_item.setText(3, f"{m.duration:.4f}")
				mani_item.setText(4, str(m.frame_count))
				mani_item.setFlags(mani_item.flags() | Qt.ItemIsEditable)
				for dtype in ("pos_bones", "ori_bones", "scl_bones", "floats"):
					dtype_array = getattr(m.keys, f"{dtype}_names")
					if len(dtype_array):
						dtype_item = QtWidgets.QTreeWidgetItem(mani_item)
						dtype_item.setIcon(0, get_icon(dtype))
						dtype_item.setText(0, dtype)
						dtype_item.setText(1, str(len(dtype_array)))
						for i, bone_name in enumerate(dtype_array):
							bone_item = QtWidgets.QTreeWidgetItem(dtype_item)
							bone_item.setIcon(0, get_icon(dtype))
							bone_item.setText(0, bone_name)
							bone_item.setText(1, str(i))
			header = self.tree.header()
			header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
			self.tree.itemChanged.connect(self.edit_handle)
			self.game_choice.entry.setText(self.manis_file.game)
			self.stream_entry.setText(self.manis_file.stream)
			logging.info(f"Loaded GUI in {time.time() - start_time:.2f} seconds")
			self.set_progress_message("Operation completed!")
		except:
			self.handle_error("GUI update failed, see log!")

	def save(self, filepath) -> None:
		try:
			self.manis_file.stream = self.stream_entry.text()
			self.manis_file.save(filepath)
			self.set_file_modified(False)
			self.set_progress_message(f"Saved {self.manis_file.name}")
		except:
			self.handle_error("Saving MANIS failed, see log!")


if __name__ == '__main__':
	startup(MainWindow, GuiOptions(log_name="manis_tool_gui", size=(900, 600)))
