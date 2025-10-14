from generated.formats.bnk.compounds.AuxFileContainer import AuxFileContainer
from generated.formats.bnk.compounds.BnkFileContainer import BnkFileContainer
from generated.formats.ovl_base import OvlContext
from generated.io import IoFile

import os
import logging

from modules.formats.shared import fmt_hash


class BnkFile(BnkFileContainer, IoFile):

	def __init__(self):
		super().__init__(OvlContext())
		self.aux_b = AuxFile()
		self.aux_b_name_bare = self.aux_b_path = self.aux_s_name_bare = self.aux_s_path = self.bnk_name_bare = self.bnk_dir = self.bnk_name = None
		self.ptr_map = {}

	def load(self, filepath):
		with open(filepath, "rb") as stream:
			self.read_fields(stream, self)
		self.ptr_map = {}
		# alternatively, bnk_name from bnk header
		self.bnk_dir, self.bnk_name = os.path.split(filepath)
		self.bnk_name_bare = os.path.splitext(self.bnk_name)[0]
		if self.bnk_header.external_s_suffix:
			self.aux_s_name_bare, self.aux_s_path = self.get_aux_path("s")
			with open(self.aux_s_path, "rb") as f:
				for stream_info in self.bnk_header.streams:
					f.seek(stream_info.offset)
					stream_info.data = f.read(stream_info.size)
					id_hash = fmt_hash(stream_info.event_id)
					self.ptr_map[id_hash] = stream_info
		# since the b aux can be originally internal as a buffer, or an external file, we just check if the file now exists
		self.aux_b_name_bare, self.aux_b_path = self.get_aux_path("b")
		if self.aux_b_name_bare:
			self.aux_b.load(self.aux_b_path)
			if self.aux_b.didx:
				for pointer in self.aux_b.didx.data_pointers:
					self.ptr_map[pointer.hash] = pointer

	def get_aux_path(self, suffix):
		# no way of knowing the ovl prefix here
		ovl_basename = ""
		end_str = f"{ovl_basename}_{self.bnk_name_bare}_bnk_{suffix}.aux"
		logging.debug(f"Looking for {end_str} in {self.bnk_dir}")
		aux_file_names = [f for f in os.listdir(self.bnk_dir) if f.lower().endswith(end_str)]
		# print(os.listdir(bnk_dir))
		# print(aux_file_names)
		# aux_path = os.path.join(bnk_dir, f"{ovl_basename}_{bnk_name}_bnk_{suffix}.aux")
		if not aux_file_names:
			logging.error(f"AUX file '{suffix}' expected in {self.bnk_dir}!")
			return None, None
		if len(aux_file_names) > 1:
			logging.warning(f"Multiple aux files qualified!")
		aux_file_name = aux_file_names[0]
		aux_file_name_bare = os.path.splitext(aux_file_name)[0]
		aux_path = os.path.join(self.bnk_dir, aux_file_name)
		return aux_file_name_bare, aux_path

	def save(self, filepath):
		# save aux
		self.aux_b.save(self.aux_b_path)
		# ensure update of bnk_file.bnk_header.size_b, apparently both external or internal
		self.bnk_header.size_b = self.aux_b.size_for_ovl
		# logging.debug(f"bnk_file.bnk_header.size_b = {self.bnk_header.size_b}")
		# save bnk
		super().save(filepath)


class AuxFile(AuxFileContainer, IoFile):

	def __init__(self):
		super().__init__(OvlContext())

