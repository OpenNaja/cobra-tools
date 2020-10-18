import struct


def write_fct(archive, sized_str_entry, out_dir):
	name = sized_str_entry.name
	print("\nWriting", name)
	buff = b"".join(sized_str_entry.data_entry.buffer_datas)
	ss_len = (len(sized_str_entry.pointers[0].data)//4)-4
	ss_data = struct.unpack(f"<4f{ss_len}I", sized_str_entry.pointers[0].data)
	offset = ss_data[8]

	data_sizes = (ss_data[10], ss_data[12], ss_data[14], ss_data[16])
	paths = []
	for x, data_size in enumerate(data_sizes):
		if data_size != 0:
			type_check = buff[offset:offset+4]
			if b"OTTO" in type_check:
				ext = ".otf"
			else:
				ext = ".ttf"
			path = out_dir(name)+str(x)+ext
			paths.append(path)
			with open(path, 'wb') as outfile:
				outfile.write(buff[offset:offset+data_size])
		offset += data_size
	return paths
