import struct

from util import texconv


def write_lua(archive, sized_str_entry, out_dir):
	name = sized_str_entry.name
	print("\nWriting", name)

	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size",len(buffer_data))
	except:
		print("Found no buffer data for",name)
		buffer_data = b""
	if len(sized_str_entry.fragments) != 2:
		print("must have 2 fragments")
		return
	# write lua
	out_path = out_dir(name)
	print(out_path)
	with open(out_path+".bin", 'wb') as outfile:
		# write the buffer
		outfile.write(buffer_data)
	texconv.bin_to_lua(out_path+".bin")
	with open(out_path+"meta", 'wb') as outfile:
		# write each of the fragments
		# print(sized_str_entry.pointers[0].data)
		outfile.write(sized_str_entry.pointers[0].data)
		for frag in sized_str_entry.fragments:
			# print(frag.pointers[0].data)
			# print(frag.pointers[1].data)
			outfile.write(frag.pointers[0].data)
			outfile.write(frag.pointers[1].data)

	return out_path, out_path+".bin", out_path+"meta"


def load_lua(ovl_data, lua_file_path, lua_sized_str_entry):
	# read lua
	# inject lua buffer
	# update sized string
	# IMPORTANT: all meta data of the lua except the sized str entries lua size value seems to just be meta data, can be zeroed
	with open(lua_file_path, "rb") as lua_stream:
		# load the new buffer
		buffer_bytes = lua_stream.read()
	if b"DECOMPILER ERROR" in buffer_bytes:
		raise SyntaxError(f"{lua_file_path} has not been successfully decompiled and can not be injected!")
	buff_size = len(buffer_bytes)
	# update the buffer
	lua_sized_str_entry.data_entry.update_data((buffer_bytes,))

	ss_len = len(lua_sized_str_entry.pointers[0].data)/4
	ss_data = struct.unpack("<{}I".format(int(ss_len)), lua_sized_str_entry.pointers[0].data)
	ss_new = struct.pack("<{}I".format(int(ss_len)), buff_size, *ss_data[1:])

	lua_sized_str_entry.pointers[0].update_data(ss_new, update_copies=True)
