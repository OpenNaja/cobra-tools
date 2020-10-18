import struct


def write_fdb(archive, sized_str_entry, out_dir):
	name = sized_str_entry.name
	print("\nWriting",name)

	try:
		buff = sized_str_entry.data_entry.buffer_datas[1]
	except:
		print("Found no buffer data for", name)
		return
	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		# write the buffer, only buffer 1
		# buffer 0 is just the bare file name, boring
		# sizedstr data is just size of the buffer
		outfile.write(buff)
	return out_path,


def load_fdb(ovl_data, fdb_file_path, fdb_sized_str_entry, fdb_name):
	# read fdb
	# inject fdb buffers
	# update sized string

	with open(fdb_file_path, "rb") as fdb_stream:
		# load the new buffers
		buffer1_bytes = fdb_stream.read()
		buffer0_bytes = fdb_name.encode()
		# update the buffers
		fdb_sized_str_entry.data_entry.update_data( (buffer0_bytes, buffer1_bytes) )
		# update the sizedstring entry
		data = struct.pack("<8I", len(buffer1_bytes), 0, 0, 0, 0, 0, 0, 0)
		fdb_sized_str_entry.pointers[0].update_data(data, update_copies=True)