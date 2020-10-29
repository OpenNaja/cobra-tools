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


def load_fct(ovl_data, file_path, sized_str_entry, index):
	# read fct
	# inject fct buffers
	# update sized string
	ss_len = len(sized_str_entry.pointers[0].data)/4
	ss_data = list(struct.unpack("<4f{}I".format(int(ss_len - 4)),sized_str_entry.pointers[0].data))
	pad_size = ss_data[8]
	data_sizes = (ss_data[10],ss_data[12],ss_data[14],ss_data[16])
	old_buffer_bytes = sized_str_entry.data_entry.buffer_datas[0]
	print("old",len(old_buffer_bytes))
	pad_bytes = old_buffer_bytes[0:pad_size]
	d0 = old_buffer_bytes[pad_size:data_sizes[0]+pad_size]
	d1 = old_buffer_bytes[data_sizes[0]+pad_size:data_sizes[0]+pad_size+data_sizes[1]]
	d2 = old_buffer_bytes[data_sizes[0]+pad_size+data_sizes[1]:data_sizes[0]+pad_size+data_sizes[1]+data_sizes[2]]
	d3 = old_buffer_bytes[data_sizes[0]+pad_size+data_sizes[1]+data_sizes[2]:]
	print("old2",len(pad_bytes+d0+d1+d2+d3))

	#data_size = ss_data[10]
	print("updating index: ",index)

	with open(file_path, "rb") as stream:
		# load the new buffer
		new_buffer_bytes = stream.read()


		buffer_bytes=pad_bytes# update the correct ss entry size
		if int(index) == 0:
			ss_data[10] = len(new_buffer_bytes)
			buffer_bytes+=new_buffer_bytes
			buffer_bytes+= d1
			buffer_bytes+= d2
			buffer_bytes+=d3
		elif int(index) == 1:
			ss_data[12] = len(new_buffer_bytes)
			buffer_bytes+=d0
			buffer_bytes+=new_buffer_bytes
			buffer_bytes+= d2
			buffer_bytes+=d3
		elif int(index) == 2:
			ss_data[14] = len(new_buffer_bytes)
			buffer_bytes+=d0
			buffer_bytes+= d1
			buffer_bytes+=new_buffer_bytes
			buffer_bytes+=d3
		elif int(index) == 3:
			ss_data[16] = len(new_buffer_bytes)
			buffer_bytes+=d0
			buffer_bytes+= d1
			buffer_bytes+= d2
			buffer_bytes+=new_buffer_bytes


		print(len(buffer_bytes))

		# update the buffers
		sized_str_entry.data_entry.update_data( (buffer_bytes,) )

		data = struct.pack("<4f{}I".format(int(ss_len - 4)), *ss_data)
		sized_str_entry.pointers[0].update_data(data, update_copies=True)