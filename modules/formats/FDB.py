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
