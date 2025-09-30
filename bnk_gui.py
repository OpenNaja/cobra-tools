import os
import shutil
import logging
import tempfile


from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from gui.app_utils import get_icon
from gui.widgets import MenuItem, GameSelectorWidget
from generated.formats.bnk import BnkFile
from generated.formats.ovl import OvlFile
from constants import ConstantsProvider
from generated.formats.bnk.enums.HircType import HircType
from ovl_util.texconv import write_riff_file
from modules.formats.shared import fmt_hash

from PyQt5 import QtWidgets, QtGui, QtCore


suffices = ("_Media", "_Events", "_DistMedia")

class EventTree(QtWidgets.QTreeWidget):
	files_dropped = QtCore.pyqtSignal(list)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setAcceptDrops(True)
		self.ignore_drop_type = ""

	def accept_ignore(self, e: QtGui.QDropEvent) -> None:
		if not self.ignore_drop_type:
			e.accept()
			return
		path = e.mimeData().urls()[0].toLocalFile() if e.mimeData().hasUrls() else ""
		if not path.lower().endswith(f".{self.ignore_drop_type.lower()}"):
			e.accept()
		else:
			e.ignore()

	def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
		self.accept_ignore(event)

	def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
		self.accept_ignore(event)

	def dropEvent(self, event: QtGui.QDropEvent) -> None:
		data = event.mimeData()
		urls = data.urls()
		if urls and urls[0].scheme() == 'file':
			file_paths = [str(url.path())[1:] for url in urls]
			self.files_dropped.emit(file_paths)
			event.accept()


class MainWindow(widgets.MainWindow):

	def __init__(self, opts: GuiOptions):
		widgets.MainWindow.__init__(self, "BNK Editor", opts=opts)
		self.bnk_media = BnkFile()
		self.bnk_events = BnkFile()
		self.tmp_dir = os.path.join(os.path.dirname(__file__), "bnk")
		os.makedirs(self.tmp_dir, exist_ok=True)

		self.constants = ConstantsProvider()

		self.filter = "Supported files ({})".format(" ".join("*" + t for t in (".wav", ".wem",)))

		self.file_widget = self.make_file_widget(ftype="BNK")
		self.file_widget.setHidden(True)

		self.bnk_name = ""
		self.cp_name = ""
		self.filepath_events = None
		self.filepath_media = None
		self.bnk_map = {}
		self.bnks_tree = QtWidgets.QTreeWidget(self)
		self.bnks_tree.setColumnCount(1)
		self.bnks_tree.setHeaderHidden(True)
		self.bnks_tree.itemDoubleClicked.connect(self.bnk_selected)

		self.events_tree = EventTree(self)
		self.events_tree.setColumnCount(3)
		self.events_tree.setHeaderLabels(("Name", "File Type", "Size"))
		self.events_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.events_tree.customContextMenuRequested.connect(self.context_menu)
		self.events_tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.events_tree.files_dropped.connect(self.inject_wem)
		# self.events_tree.itemDoubleClicked.connect(self.bnk_selected)

		
		self.game_choice = GameSelectorWidget(self)
		self.game_choice.installed_game_chosen.connect(self.fill_bnks)

		left_frame = widgets.pack_in_box(self.bnks_tree, self.game_choice)

		splitter = QtWidgets.QSplitter()
		splitter.addWidget(left_frame)
		splitter.addWidget(self.events_tree)
		splitter.setStretchFactor(0, 1)
		splitter.setStretchFactor(1, 3)
		splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

		self.qgrid = QtWidgets.QVBoxLayout()
		self.qgrid.addWidget(splitter)
		self.qgrid.addWidget(self.progress)
		self.central_widget.setLayout(self.qgrid)

		self.build_menus({
			widgets.FILE_MENU: self.file_menu_items,
			widgets.EDIT_MENU: [
				MenuItem("Unpack", self.extract_all, shortcut="CTRL+U", icon="extract"),
				MenuItem("Inject", self.inject_ask, shortcut="CTRL+I", icon="inject"),
			],
			widgets.HELP_MENU: self.help_menu_items
		})

		self.fill_bnks()

	def context_menu(self, pos):
		item = self.events_tree.itemAt(pos)
		if item:
			if "WEM" in item.text(1):
				menu = QtWidgets.QMenu("Test", self.events_tree)
				extract = QtWidgets.QAction("Extract")
				wem_hash = item.text(0)[2:]

				def extract_cb(checked):
					out_dir = QtWidgets.QFileDialog.getExistingDirectory(directory=self.cfg.get("dir_extract"))
					logging.info(f"extracting {wem_hash}")
					self.extract_audio(out_dir, hashes=(wem_hash,))

				extract.triggered.connect(extract_cb)
				menu.addAction(extract)
				# delete = QtWidgets.QAction(f"Delete {bone_name}")
				# menu.addAction(delete)
				menu.exec(self.events_tree.mapToGlobal(pos))
	
	def get_subfolders(self, dir_path):
		for name in os.listdir(dir_path):
			sub_dir_path = os.path.join(dir_path, name)
			if os.path.isdir(sub_dir_path):
				yield sub_dir_path

	def get_ovl_files(self, dir_path):
		for name in os.listdir(dir_path):
			file_path = os.path.join(dir_path, name)
			if os.path.isfile(file_path) and file_path.endswith(".ovl"):
				yield file_path

	def clear_tmp_dir(self):
		for fp in os.listdir(self.tmp_dir):
			os.remove(os.path.join(self.tmp_dir, fp))

	def fill_bnks(self):
		self.bnks_tree.clear()
		self.bnk_map = {}
		game = self.game_choice.get_selected_game()
		if game:
			game_dir = self.cfg.get("games").get(game)
			# content packs
			for cp in self.get_subfolders(game_dir):
				audio_dir = os.path.join(cp, "Audio")
				if os.path.isdir(audio_dir):
					cp_map = {}
					cp_name = os.path.basename(cp)
					self.bnk_map[cp_name] = cp_map
					if game == "Planet Coaster 2":
						# todo better logic for finding paths
						# PC2: misses loc ovls?
						# subfolder and separate ovls
						for bnk_dir in self.get_subfolders(audio_dir):
							bnk_name = os.path.basename(bnk_dir)
							for s in suffices:
								bnk_name = bnk_name.removesuffix(s)
								bnk_name = bnk_name.removesuffix(s.lower())
							for ovl_path in self.get_ovl_files(bnk_dir):
								self.store_ovl_paths(ovl_path, bnk_name, cp_map)
					else:
						# ovls directly in audio dir
						for ovl_path in self.get_ovl_files(audio_dir):
							bnk_name = os.path.splitext(os.path.basename(ovl_path))[0]
							self.store_ovl_paths(ovl_path, bnk_name, cp_map)
		for cp_name, cp_map in sorted(self.bnk_map.items()):
			cp_item = QtWidgets.QTreeWidgetItem(self.bnks_tree)
			cp_item.setText(0, cp_name)
			cp_item.setIcon(0, get_icon("dir"))
			for bnk_name in sorted(cp_map.keys()):
				bnk_item = QtWidgets.QTreeWidgetItem(cp_item)
				bnk_item.setText(0, bnk_name)
				bnk_item.setIcon(0, get_icon("bnk"))

	def store_ovl_paths(self, ovl_path, bnk_name, cp_map):
		if bnk_name not in cp_map:
			cp_map[bnk_name] = []
		cp_map[bnk_name].append(ovl_path)

	def get_parents(self, item):
		names = [item.text(0), ]
		while item.parent():
			item = item.parent()
			names.insert(0, item.text(0))
		return names

	def bnk_selected(self, item):
		names = self.get_parents(item)
		if len(names) > 1:
			self.filepath_events = None
			self.filepath_media = None
			self.cp_name = names[0]
			self.bnk_name = names[-1]
			self.clear_tmp_dir()
			self.setWindowTitle("BNK Editor", file=self.bnk_name)
			ovl_paths = self.bnk_map[self.cp_name][self.bnk_name]
			for ovl_path in ovl_paths:
				ovl_data = OvlFile()
				ovl_data.load(ovl_path, {"game": self.game_choice.entry.currentText(), })
				for fp in ovl_data.extract(self.tmp_dir):
					if fp.endswith(".bnk"):
						if "_events" in fp.lower():
							self.filepath_events = fp
						if "_media" in fp.lower():
							self.filepath_media = fp
			if self.filepath_media and self.filepath_events:
				# set a dummy path so file_widget knows a file is open
				# self.file_widget.filepath = self.filepath_media
				# self.open("")
				self.file_widget.open_file(f"//{self.bnk_name}")

	def extract_audio(self, out_dir, hashes=()):
		out_files = []

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(out_dir, n))
		if not hashes:
			hashes = self.bnk_media.data_map.keys()
		for id_hash in hashes:
			try:
				data, aux_name = self.bnk_media.data_map[id_hash]
				out_file = write_riff_file(data, out_dir_func(f"{aux_name}_{id_hash}"))
				if out_file:
					out_files.append(out_file)
			except:
				logging.exception(f"Failed to extract audio for {id_hash}")
		return out_files

	def inject_wem(self, wem_file_paths):
		if self.filepath_media:
			assert os.path.isfile(self.filepath_media)
			assert os.path.isfile(self.filepath_events)
			for wem_file_path in wem_file_paths:
				if not wem_file_path.lower().endswith(".wem"):
					logging.warning(f"Wrong file format, ignoring {wem_file_path}")
					continue
				logging.info(f"Trying to inject {wem_file_path}")
				try:
					aux_path_bare, wem_id = os.path.splitext(wem_file_path)[0].rsplit("_", 1)
					logging.info(f"WEM id: {wem_id} into aux {aux_path_bare}")

					# get the names of the bnk files and make sure they match the input
					media_bnk = self.bnk_media.bnk_header.name
					assert "_media_" in aux_path_bare.lower()
					assert media_bnk.lower() in aux_path_bare.lower()
					events_bnk = f"{media_bnk.rsplit('_', 1)[0]}_events"
					logging.info(f"Media: {media_bnk}, Events: {events_bnk}")

					ovl_basename = os.path.basename(aux_path_bare).lower().split(media_bnk.lower())[0][:-1]

					self.bnk_media.aux_b.inject_audio(wem_file_path, wem_id)
					self.bnk_events.aux_b.inject_hirc(wem_file_path, wem_id)
					self.set_dirty()
					logging.info(f"Injected {wem_file_path} {wem_id}")
				except BaseException:
					logging.exception(f"Failed to inject {wem_file_path}")

	def drag_files(self, file_names):
		drag = QtGui.QDrag(self)
		temp_dir = tempfile.mkdtemp("-cobra")
		try:
			out_paths = self.extract_audio(temp_dir, file_names)

			data = QtCore.QMimeData()
			data.setUrls([QtCore.QUrl.fromLocalFile(path) for path in out_paths])
			drag.setMimeData(data)
			drag.exec_()
			logging.info(f"Tried to extract {len(file_names)} files")
		except:
			self.handle_error("Extraction failed, see log!")
		shutil.rmbnks_tree(temp_dir)

	def show_node(self, hirc, qt_parent, sid_2_hirc, lut):
		hirc_item = QtWidgets.QTreeWidgetItem(qt_parent)
		name = lut.get(hirc.data.id, f"0x{fmt_hash(hirc.data.id)}")
		hirc_item.setText(0, name)
		hirc_item.setIcon(0, get_icon("dir"))
		hirc_item.setText(1, hirc.id.name)
		if hasattr(hirc.data, "children"):
			hirc_item.setText(2, str(len(hirc.data.children)))
			for child_id in hirc.data.children:
				child = sid_2_hirc.get(child_id)
				if not child:
					logging.warning(f"Child {child_id} not found")
					continue
				self.show_node(child, hirc_item, sid_2_hirc, lut)
		if hirc.id == HircType.SOUND:
			sbi = hirc.data.ak_bank_source_data
			info = sbi.ak_media_information
			wem_hash = fmt_hash(info.source_i_d)
			src_item = QtWidgets.QTreeWidgetItem(hirc_item)
			src_item.setText(0, f"0x{wem_hash}")
			icon = get_icon("bnk")
			src_item.setIcon(0, icon)
			src_item.setText(1, f"WEM {sbi.stream_type.name}")
			src_item.setText(2, f"{info.u_in_memory_media_size} bytes")
			# external sound from another bnk file
			if wem_hash not in self.bnk_media.data_map:
				src_item.setDisabled(True)
	
	def open(self, dummy_filepath):
		if self.filepath_media:
			self.set_clean()
			try:
				self.bnk_media.load(self.filepath_media)
				self.bnk_events.load(self.filepath_events)
				# logging.info(self.bnk_events.aux_b)
				# print(self.bnk_media)
				# print(self.bnk_media.aux_b)
				if not self.bnk_events.aux_b.hirc:
					logging.warning("No hirc found")
					return
				sid_2_hirc = {hirc.data.id: hirc for hirc in self.bnk_events.aux_b.hirc.hirc_pointers}
				# get the lut of fnv1 of the sound names
				lut = self.constants[self.game_choice.get_selected_game()].get("audio", {})

				self.events_tree.clear()
				for hirc in self.bnk_events.aux_b.hirc.hirc_pointers:
					if hirc.id == HircType.EVENT:
						self.show_node(hirc, self.events_tree, sid_2_hirc, lut)
				self.events_tree.expandAll()
				self.events_tree.sortItems(0, QtCore.Qt.AscendingOrder)
				self.events_tree.resizeColumnToContents(0)
				self.events_tree.resizeColumnToContents(1)
				self.events_tree.resizeColumnToContents(2)
			except:
				self.handle_error("Loading failed, see log!")

	def save(self, filepath) -> None:
		try:
			# save aux
			self.bnk_media.aux_b.save(self.filepath_media)
			self.bnk_events.aux_b.save(self.filepath_events)
			# save bnk
			self.bnk_media.save(self.filepath_media)
			self.bnk_events.save(self.filepath_events)
			# inject into the ovls
			ovl_paths = self.bnk_map[self.cp_name][self.bnk_name]
			for ovl_path in ovl_paths:
				ovl_data = OvlFile()
				ovl_data.load_hash_table()
				ovl_data.load(ovl_path, commands={"game": self.game_choice.entry.currentText(), })
				file_paths = [os.path.join(self.tmp_dir, filename) for filename in ovl_data.loaders]
				# inject
				ovl_data.add_files(file_paths, common_root_dir=self.tmp_dir)
				ovl_data.save(ovl_path, commands={})
			self.set_clean()
			self.set_progress_message(f"Saved {self.bnk_media.bnk_name}")
		except:
			self.handle_error("Loading failed, see log!")

	def extract_all(self):
		out_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg.get("dir_extract", "C://"), )
		if out_dir:
			self.cfg["dir_extract"] = out_dir
			try:
				out_files = self.extract_audio(out_dir)
			except:
				self.handle_error("Extracting failed, see log!")

	def inject_ask(self):
		if self.file_widget.is_open():
			files = QtWidgets.QFileDialog.getOpenFileNames(
				self, 'Inject files', self.cfg.get("dir_inject", "C://"), self.filter)[0]
			self.inject_files(files)

	def inject_files(self, files):
		"""Tries to inject files into self.bnk_media"""
		if files:
			self.cfg["dir_inject"] = os.path.dirname(files[0])
			try:
				error_files = self.inject_wem(files)
				self.set_progress_message("Injection completed")
			except:
				self.handle_error("Injecting failed, see log!")


if __name__ == '__main__':
	startup(MainWindow, GuiOptions("bnk_gui"))
