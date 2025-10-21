import logging
from generated.formats.base.structs.PadAlign import get_padding
from generated.formats.lua.structs.LuaRoot import LuaRoot
from modules.formats.BaseFormat import MemStructLoader
from ovl_util import texconv

error_flag = b"DECOMPILER ERROR"


class LuaLoader(MemStructLoader):
	extension = ".lua"
	target_class = LuaRoot
	# temp_extensions = ".bin"

	def __init__(self, ovl, file_name, mime_version):
		super().__init__(ovl, file_name, mime_version)
		if self.lua_flatten:
			self.name = file_name.replace("/", ".")

	@property
	def lua_decompile(self):
		return self.ovl.cfg.get("lua_decompile", False)
	
	@property
	def lua_flatten(self):
		return self.ovl.cfg.get("lua_flatten", False)

	def create(self, file_path):
		buffer_0 = self._get_data(file_path)
		self.create_data_entry((buffer_0,))
		self.header = LuaRoot(self.ovl.context)
		self.update_header(buffer_0, self.basename)

	def update_header(self, buffer_0, name):
		self.header.lua_size = len(buffer_0)
		self.header.source_path.data = name
		# even if the lua + zstr terminator was padded to 4, keep at least 1 byte for this ptr
		self.header.likely_alignment.data = b"\x00" + get_padding(len(name) + 2, alignment=4)
		self.write_memory_data()

	def extract(self, out_dir):
		buffer_data = self.data_entry.buffer_datas[0]

		if self.lua_flatten:
			split_path = self.name.split(".")
			new_path = "/".join(split_path[:-1]) + "." + split_path[-1]
			lua_path = out_dir(new_path)
		else:
			lua_path = out_dir(self.name)

		# DLA & ZTUAC - clip away the start (fragment data at start of buffer?)
		if self.ovl.context.version <= 17:
			buffer_data = buffer_data[8:]
		out_files = []
		if buffer_data[1:4] == b"Lua":
			# Compiled Lua, attempt to decompile
			bin_path = lua_path + ".bin"
			with open(bin_path, 'wb') as outfile:
				outfile.write(buffer_data)

			decompiled_bytes, err = (None, None)
			if self.lua_decompile:
				decompiled_bytes, err = texconv.bin_to_lua(bin_path)

			if decompiled_bytes:
				with open(lua_path, 'wb') as outfile:
					outfile.write(decompiled_bytes)
				out_files.append(lua_path)

			if not decompiled_bytes or err or self.show_temp_files:
				out_files.append(bin_path)
		else:
			# Uncompiled Lua, write the plaintext buffer
			with open(lua_path, 'wb') as outfile:
				outfile.write(buffer_data)
			out_files.append(lua_path)
		return out_files

	def _get_data(self, file_path):
		"""Loads and returns the data for a LUA"""
		buffer_0 = self.get_content(file_path)
		if error_flag in buffer_0:
			raise SyntaxError(f"{file_path} has not been successfully decompiled and may crash your game. Remove {error_flag} from the file to inject anyway.")
		# check for errors in plaintext lua
		elif buffer_0[1:4] != b"Lua":
			texconv.check_lua_syntax(file_path)
		return buffer_0

	def rename_content(self, name_tuples):
		logging.info(f"Renaming in {self.name}")
		buffer_0 = self.data_entry.buffer_datas[0]
		for old, new in name_tuples:
			buffer_0 = buffer_0.replace(old.encode(), new.encode())
		self.data_entry.update_data((buffer_0,))
		self.clear_stack()
		self.fragments.clear()
		# updating size is mandatory
		self.update_header(buffer_0, self.basename)
