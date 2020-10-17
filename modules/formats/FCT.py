import struct


def write_fct(archive, sized_str_entry, out_dir):
	name = sized_str_entry.name
	print("\nWriting",name)
	buff = b"".join(sized_str_entry.data_entry.buffer_datas)
	ss_len = len(sized_str_entry.pointers[0].data)/4
	ss_data = struct.unpack("<4f{}I".format(int(ss_len - 4)),sized_str_entry.pointers[0].data)
	pad_size = ss_data[8]

	data_sizes = (ss_data[10],ss_data[12],ss_data[14],ss_data[16])
	adder = 0
	paths = []
	for x, data_size in enumerate(data_sizes):
		if data_size != 0:
			type_check = buff[pad_size+adder:pad_size+adder+4]
			print(type_check)
			if b"OTTO" in type_check:
				ext = ".otf"
			else:
				ext = ".ttf"
			path = out_dir(name)+str(x)+ext
			paths.append(path)
			with open(path, 'wb') as outfile:
				outfile.write(buff[pad_size+adder:data_size+pad_size+adder])
		adder += data_size
	return paths
