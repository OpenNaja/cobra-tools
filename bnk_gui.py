import os
import shutil
import logging
import tempfile

from gui import widgets, startup, GuiOptions  # Import widgets before everything except built-ins!
from gui.app_utils import get_icon
from gui.widgets import MenuItem, GameSelectorWidget
from generated.formats.bnk import BnkFile, AuxFile
from generated.formats.ovl import OvlFile
from constants import ConstantsProvider
from generated.formats.bnk.enums.HircType import HircType
from ovl_util.texconv import write_riff_file
from modules.formats.shared import fmt_hash

from PyQt5 import QtWidgets, QtGui, QtCore

suffices = ("_Media", "_Events", "_DistMedia")


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

		header_names = ["Name", "Event Name", "File Type", "File Size"]

		# create the table
		self.files_container = widgets.SortableTable(header_names, ())
		# connect the interaction functions
		# self.files_container.table.table_model.member_renamed.connect(self.rename_handle)
		self.files_container.table.files_dragged.connect(self.drag_files)
		self.files_container.table.files_dropped.connect(self.inject_files)

		self.bnk_map = {}
		self.bnks_tree = QtWidgets.QTreeWidget(self)
		self.bnks_tree.setColumnCount(1)
		self.bnks_tree.setHeaderHidden(True)
		self.bnks_tree.itemDoubleClicked.connect(self.bnk_selected)

		self.events_tree = QtWidgets.QTreeWidget(self)
		self.events_tree.setColumnCount(1)
		self.events_tree.setHeaderHidden(True)
		# self.events_tree.itemDoubleClicked.connect(self.bnk_selected)
		
		
		self.game_choice = GameSelectorWidget(self)
		self.game_choice.installed_game_chosen.connect(self.fill_bnks)

		right_frame = widgets.pack_in_box(
			self.files_container,
			self.events_tree,
			layout=QtWidgets.QHBoxLayout)

		left_frame = widgets.pack_in_box(
			self.bnks_tree,
			self.game_choice
		)

		splitter = QtWidgets.QSplitter()
		splitter.addWidget(left_frame)
		splitter.addWidget(right_frame)
		splitter.setSizes([20, 50])
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
								self.store_bnk_ref(ovl_path, bnk_name, cp_map)
					else:
						# ovls directly in audio dir
						for ovl_path in self.get_ovl_files(audio_dir):
							bnk_name = os.path.splitext(os.path.basename(ovl_path))[0]
							self.store_bnk_ref(ovl_path, bnk_name, cp_map)
		for cp_name, cp_map in sorted(self.bnk_map.items()):
			cp_item = QtWidgets.QTreeWidgetItem(self.bnks_tree)
			cp_item.setText(0, cp_name)
			cp_item.setIcon(0, get_icon("dir"))
			for bnk_name in sorted(cp_map.keys()):
				bnk_item = QtWidgets.QTreeWidgetItem(cp_item)
				bnk_item.setText(0, bnk_name)
				bnk_item.setIcon(0, get_icon("bnk"))

	def store_bnk_ref(self, ovl_path, bnk_name, cp_map):
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
			cp = names[0]
			bnk = names[-1]
			self.clear_tmp_dir()
			self.setWindowTitle("BNK Editor", file=bnk)
			ovl_paths = self.bnk_map[cp][bnk]
			for ovl_path in ovl_paths:
				ovl_data = OvlFile()
				ovl_data.load(ovl_path, {"game": self.game_choice.entry.currentText(), })
				for fp in ovl_data.extract(self.tmp_dir):
					if fp.endswith(".bnk"):
						if "_events" in fp.lower():
							self.filepath_events = fp
						if "_media" in fp.lower():
							self.filepath_media = fp
			self.open("")

	def extract_audio(self, out_dir, hashes=()):
		out_files = []

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(out_dir, n))
		if not hashes:
			hashes = self.bnk_media.data_map.keys()
		for id_hash in hashes:
			data, aux_name = self.bnk_media.data_map[id_hash]
			out_file = write_riff_file(data, out_dir_func(f"{aux_name}_{id_hash}"))
			if out_file:
				out_files.append(out_file)
		return out_files

	def inject_wem(self, wem_file_paths):
		bnk_dir, bnk_name = os.path.split(self.filepath_media)
		for wem_file_path in wem_file_paths:
			logging.info(f"Trying to inject {wem_file_path}")
			aux_path_bare, wem_id = os.path.splitext(wem_file_path)[0].rsplit("_", 1)
			logging.info(f"WEM id: {wem_id} into aux {aux_path_bare}")

			aux_path = f"{aux_path_bare}.aux"
			# check if target aux file exists
			# if os.path.isfile(aux_path):
			# 	pass
			# get the names of the bnk files and make sure they match the input
			media_bnk = self.bnk_media.bnk_header.name
			assert "_media_" in aux_path_bare.lower()
			assert media_bnk.lower() in aux_path_bare.lower()
			events_bnk = f"{media_bnk.rsplit('_', 1)[0]}_events"
			logging.info(f"Media: {media_bnk}, Events: {events_bnk}")
			# aux_path_bare
			# for base_dir in (self.ovl.dir, os.path.dirname(wem_file_path)):

			ovl_basename = os.path.basename(aux_path_bare).lower().split(media_bnk.lower())[0][:-1]
			print(ovl_basename)
			media_path = os.path.join(bnk_dir, f"{ovl_basename}_{media_bnk}_bnk_b.aux")
			events_path = os.path.join(bnk_dir, f"{ovl_basename}_{events_bnk}_bnk_b.aux")
			print(media_path)
			print(events_path)
			if os.path.isfile(media_path) and os.path.isfile(events_path):
				media = AuxFile()
				media.load(media_path)
				media.inject_audio(wem_file_path, wem_id)
				media.save(media_path)

				events = AuxFile()
				events.load(events_path)
				events.inject_hirc(wem_file_path, wem_id)
				events.save(events_path)

				logging.info(f"Injected {wem_file_path} {wem_id}")

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

	def open(self, dummy_filepath):
		if self.filepath_media:
			self.set_file_modified(False)
			try:
				self.bnk_media.load(self.filepath_media)
				self.bnk_events.load(self.filepath_events)
				logging.info(self.bnk_events.aux_b)
				# print(self.bnk_media)
				# print(self.bnk_media.aux_b)
				if not self.bnk_events.aux_b.hirc:
					logging.warning("No hirc found")
					return
				sid_2_hirc = {hirc.data.id: hirc for hirc in self.bnk_events.aux_b.hirc.hirc_pointers}
				game_obj_2_hirc = {}
				# get the lut of fnv1 of the sound names
				lut = self.constants[self.game_choice.get_selected_game()].get("audio", {})
				# propagate names
				for hirc in self.bnk_events.aux_b.hirc.hirc_pointers:
					hirc.name = None
				for hirc in self.bnk_events.aux_b.hirc.hirc_pointers:
					if hirc.id == HircType.EVENT:
						# map to actions
						hirc.name = lut.get(hirc.data.id, f"0x{fmt_hash(hirc.data.id)}")
						# print(name)
						for action_id in hirc.data.action_ids:
							action = sid_2_hirc[action_id]
							action.name = hirc.name
							# print(f"action.name {action.name}")
					if hirc.id == HircType.EVENT_ACTION:
						# map by game obj
						print(sid_2_hirc.get(hirc.data.game_obj))
						game_obj_2_hirc[hirc.data.game_obj] = hirc
						# action = sid_2_hirc[hirc.data.extra_id]
						# action.name = hirc.name
				for hirc in self.bnk_events.aux_b.hirc.hirc_pointers:
					if hirc.id == HircType.RANDOM_OR_SEQUENCE_CONTAINER:
						pid = hirc.data.node_base_params.direct_parent_i_d
						if pid in game_obj_2_hirc:
							hirc.name = game_obj_2_hirc[pid].name
						# else:
						# 	logging.warning(f"Parent {pid} not found")
						for child_id in hirc.data.children:
							child = sid_2_hirc[child_id]
							child.name = hirc.name
							# print(f"child.name {child.name}")
				# print(game_obj_2_hirc)
				# map the hirc to the wem id from events bnk
				hirc_map = {hirc.data.ak_bank_source_data.ak_media_information.source_i_d: hirc for hirc in self.bnk_events.aux_b.hirc.hirc_pointers if hirc.id == HircType.SOUND}
				# print(hirc_map)
				# print(lut)
				def get_name(hirc):
					if hirc.name:
						return hirc.name
					# return f"0x{fmt_hash(hirc.data.id)}"
					return f""
				print([pointer.wem_id for pointer in self.bnk_media.aux_b.didx.data_pointers])
				f_list = [(fmt_hash(stream_info.event_id), get_name(hirc_map[stream_info.event_id]), "s", stream_info.size) for stream_info in self.bnk_media.bnk_header.streams]
				if self.bnk_media.aux_b and self.bnk_media.aux_b.didx:
					f_list.extend([(fmt_hash(pointer.wem_id), get_name(hirc_map[pointer.wem_id]), "b", pointer.wem_filesize) for pointer in self.bnk_media.aux_b.didx.data_pointers])
				f_list.sort(key=lambda t: (t[1], t[0]))
				self.files_container.set_data(f_list)

				self.events_tree.clear()
				for hirc in self.bnk_events.aux_b.hirc.hirc_pointers:
					if hirc.id == HircType.EVENT:
						# cp_name = os.path.basename(cp)
						event_item = QtWidgets.QTreeWidgetItem(self.events_tree)
						event_item.setText(0, hirc.name)
						event_item.setIcon(0, get_icon("dir"))
							# cp_map = {}
							# self.bnk_map[cp_name] = cp_map
							# for bnk_dir in self.get_subfolders(audio_dir):
							# 	bnk_name = os.path.basename(bnk_dir)
							# 	for s in suffices:
							# 		bnk_name = bnk_name.removesuffix(s)
							# 		bnk_name = bnk_name.removesuffix(s.lower())
							# 	if bnk_name not in cp_map:
							# 		cp_map[bnk_name] = []
							# 	cp_map[bnk_name].append(bnk_dir)
							# for bnk_name in sorted(cp_map.keys()):
							# 	bnk_item = QtWidgets.QTreeWidgetItem(event_item)
							# 	bnk_item.setText(0, bnk_name)
							# 	bnk_item.setIcon(0, get_icon("bnk"))
			except:
				self.handle_error("Loading failed, see log!")

	def is_open_bnk(self):
		if not self.filepath_media:
			self.showwarning("You must open a BNK file first!")
		else:
			return True

	def save(self, filepath) -> None:
		try:
			self.bnk_media.save(filepath)
			self.set_file_modified(False)
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
		if self.is_open_bnk():
			files = QtWidgets.QFileDialog.getOpenFileNames(
				self, 'Inject files', self.cfg.get("dir_inject", "C://"), self.filter)[0]
			self.inject_files(files)

	def inject_files(self, files):
		"""Tries to inject files into self.bnk_media"""
		if files:
			self.cfg["dir_inject"] = os.path.dirname(files[0])
			try:
				error_files = self.inject_wem(files)
				self.set_file_modified(True)
				self.set_progress_message("Injection completed")
			except:
				self.handle_error("Injecting failed, see log!")


if __name__ == '__main__':
	startup(MainWindow, GuiOptions("bnk_gui"))
