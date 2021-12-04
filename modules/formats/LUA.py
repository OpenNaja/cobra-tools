import logging
import struct

from generated.formats.ovl.versions import *
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import zstr
from ovl_util import texconv
from ovl_util.interaction import showdialog


class LuaLoader(BaseFile):
	
	def create(self):
		ss, buffer_0 = self._get_data(self.file_entry.path)
		file_name_bytes = self.file_entry.basename.encode(encoding='utf8')
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.create_data_entry(self.sized_str_entry, (buffer_0,))
		f_0, f_1 = self.create_fragments(self.sized_str_entry, 2)

		# first these
		self.write_to_pool(f_0.pointers[1], 2, zstr(file_name_bytes))
		self.write_to_pool(f_1.pointers[1], 2, b'\x00')
		# now pad
		f_1.pointers[0].pool.data.write(get_padding(f_1.pointers[0].pool.data.tell(), 4))
		# finally the rest, already alignd
		self.write_to_pool(self.sized_str_entry.pointers[0], 2, ss)
		self.write_to_pool(f_0.pointers[0], 2, b'\x00' * 8)
		self.write_to_pool(f_1.pointers[0], 2, b'\x00' * 24)

	def collect(self):
		self.assign_ss_entry()
		if is_jwe(self.ovl) or is_pz(self.ovl) or is_pc(self.ovl) or is_jwe2(self.ovl):
			self.assign_fixed_frags(2)

	def load(self, file_path):
		# all meta data of the lua except the sized str entries lua size value seems to just be meta data, can be zeroed
		ss, buffer_0 = self._get_data(file_path)
		self.sized_str_entry.data_entry.update_data((buffer_0,))
		self.sized_str_entry.pointers[0].update_data(ss, update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		buffer_data = self.sized_str_entry.data_entry.buffer_datas[0]
		logging.debug(f"buffer size: {len(buffer_data)}")
		# write lua
		out_path = out_dir(name)
		# print(out_path)
		# clip away the start (fragment data at start of buffer?)
		if is_ztuac(self.ovl):
			buffer_data = buffer_data[8:]
		else:
			if len(self.sized_str_entry.fragments) != 2:
				logging.warning("must have 2 fragments")
		out_files = []
		if buffer_data[1:4] == b"Lua":
			logging.debug("compiled lua")
			bin_path = out_path + ".bin"
			with open(bin_path, 'wb') as outfile:
				# write the buffer
				outfile.write(buffer_data)
			# see if it worked
			if texconv.bin_to_lua(bin_path):
				out_files.append(out_path)
				# optional bin
				if show_temp_files:
					out_files.append(bin_path)
			# no conversion, just get bin
			else:
				out_files.append(bin_path)
		else:
			logging.debug("uncompiled lua")
			with open(out_path, 'wb') as outfile:
				# write the buffer
				outfile.write(buffer_data)
			out_files.append(out_path)
		return out_files

	def _get_data(self, file_path):
		"""Loads and returns the data for a LUA"""
		buffer_0 = self.get_content(file_path)
		if b"DECOMPILER ERROR" in buffer_0:
			confirmed = showdialog(
				f"{file_path} has not been successfully decompiled and may crash your game. Inject anyway?", ask=True)
			if not confirmed:
				raise UserWarning(f"Injection aborted for {file_path}")
		ss = struct.pack("IIII", len(buffer_0), 16000, 0x00, 0x00)
		return ss, buffer_0
