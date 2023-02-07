import logging
from generated.formats.base.compounds.PadAlign import get_padding
from generated.formats.lua.compounds.LuaRoot import LuaRoot
from modules.formats.BaseFormat import MemStructLoader
from ovl_util import texconv

error_flag = b"DECOMPILER ERROR"


class LuaLoader(MemStructLoader):
	extension = ".lua"
	target_class = LuaRoot
	temp_extensions = ".bin"
	
	def create(self):
		buffer_0 = self._get_data(self.file_entry.path)
		self.create_root_entry()
		self.create_data_entry((buffer_0,))

		self.header = LuaRoot(self.ovl.context)
		self.header.lua_size = len(buffer_0)
		self.header.source_path.data = self.file_entry.basename
		# even if the lua + zstr terminator was padded to 4, keep at least 1 byte for this ptr
		self.header.likely_alignment.data = b"\x00" + get_padding(len(self.file_entry.basename)+2, alignment=4)
		self.header.write_ptrs(self, self.root_entry.struct_ptr, self.file_entry.pool_type)

	def extract(self, out_dir):
		name = self.name
		logging.info(f"Writing {name}")
		buffer_data = self.data_entry.buffer_datas[0]
		logging.debug(f"buffer size: {len(buffer_data)}")
		# write lua
		out_path = out_dir(name)
		# print(out_path)
		# DLA & ZTUAC - clip away the start (fragment data at start of buffer?)
		if self.ovl.context.version <= 17:
			buffer_data = buffer_data[8:]
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
		if error_flag in buffer_0:
			raise UserWarning(f"{file_path} has not been successfully decompiled and may crash your game. Remove {error_flag} from the file to inject anyway.")
		# check for errors in plaintext lua
		elif buffer_0[1:4] != b"Lua":
			texconv.check_lua_syntax(file_path)
		return buffer_0

	def rename_content(self, name_tuples):
		logging.info(f"Renaming in {self.file_entry.name}")
		buffer_data = self.data_entry.buffer_datas[0]
		for old, new in name_tuples:
			buffer_data = buffer_data.replace(old.encode(), new.encode())
		self.data_entry.update_data((buffer_data,))
