import struct

from generated.formats.ovl.versions import *
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import zstr
from ovl_util import texconv
from ovl_util.interaction import showdialog


def write_lua(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print("\nWriting", name)
	# print(sized_str_entry.fragments)

	buffer_data = sized_str_entry.data_entry.buffer_datas[0]
	print("buffer size", len(buffer_data))
	# write lua
	out_path = out_dir(name)
	# print(out_path)
	# clip away the start (fragment data at start of buffer?)
	if is_ztuac(ovl):
		buffer_data = buffer_data[8:]
	else:
		if len(sized_str_entry.fragments) != 2:
			print("must have 2 fragments")
	out_files = []
	if buffer_data[1:4] == b"Lua":
		print("compiled lua")
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
		print("uncompiled lua")
		with open(out_path, 'wb') as outfile:
			# write the buffer
			outfile.write(buffer_data)
		out_files.append(out_path)
	return out_files


def load_lua(ovl_data, lua_file_path, lua_sized_str_entry):
	# read lua
	# inject lua buffer
	# update sized string
	# IMPORTANT: all meta data of the lua except the sized str entries lua size value seems to just be meta data, can be zeroed
	with open(lua_file_path, "rb") as lua_stream:
		# load the new buffer
		buffer_bytes = lua_stream.read()
	if b"DECOMPILER ERROR" in buffer_bytes:
		confirmed = showdialog(
			f"{lua_file_path} has not been successfully decompiled and may crash your game. Inject anyway?", ask=True)
		if not confirmed:
			return

	buff_size = len(buffer_bytes)
	# update the buffer
	lua_sized_str_entry.data_entry.update_data((buffer_bytes,))

	ss_len = len(lua_sized_str_entry.pointers[0].data) / 4
	ss_data = struct.unpack("<{}I".format(int(ss_len)), lua_sized_str_entry.pointers[0].data)
	ss_new = struct.pack("<{}I".format(int(ss_len)), buff_size, *ss_data[1:])

	lua_sized_str_entry.pointers[0].update_data(ss_new, update_copies=True)


class LuaLoader(BaseFile):

	def create(self, ovs, file_entry):
		self.ovs = ovs
		dbuffer = self.get_content(file_entry.path)
		file_name_bytes = file_entry.basename.encode(encoding='utf8')
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		# lua, ss, 2 frag + buffer
		pool.data.write(struct.pack("IIII", len(dbuffer), 16000, 0x00, 0x00))  # ss data
		pool.data.write(struct.pack("24s", b''))  # room for 3 pointers
		pool.data.write(struct.pack("8s", b''))  # room for 2 ints
		pool.data.write(b'\x00')  # one more char for the 2nd ptr
		pool.data.write(zstr(file_name_bytes))
		pool.data.write(get_padding(pool.data.tell(), 4))

		new_frag0 = self.create_fragment()
		new_frag0.pointers[0].pool_index = pool_index
		new_frag0.pointers[0].data_offset = offset + 0x10
		new_frag0.pointers[1].pool_index = pool_index
		new_frag0.pointers[1].data_offset = offset + 0x31
		new_frag1 = self.create_fragment()
		new_frag1.pointers[0].pool_index = pool_index
		new_frag1.pointers[0].data_offset = offset + 0x18
		new_frag1.pointers[1].pool_index = pool_index
		new_frag1.pointers[1].data_offset = offset + 0x30
		new_ss = self.create_ss_entry(file_entry)
		new_ss.pointers[0].pool_index = pool_index
		new_ss.pointers[0].data_offset = offset
		new_data = self.create_data_entry(new_ss, (dbuffer,))
		new_data.set_index = 0

	def collect(self, ovl, file_entry):
		if is_jwe(ovl) or is_pz(ovl) or is_pc(ovl) or is_jwe2(ovl):
			self.assign_fixed_frags(ovl, file_entry, 2)
