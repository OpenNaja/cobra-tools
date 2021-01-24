from modules.formats.shared import pack_header


def write_motiongraphvars(archive, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print(f"\nWriting {name}")

	ovl_header = pack_header(archive, b"MOTV")
	out_path = out_dir(name)
	# buffers = sized_str_entry.data_entry.buffer_datas
	# write voxelskirt
	with open(out_path, 'wb') as outfile:
		# write the sized str and buffers
		# print(sized_str_entry.pointers[0].data)
		outfile.write(ovl_header)
		outfile.write(sized_str_entry.pointers[0].data)
		# print(sized_str_entry.pointers[0].address)
		print("frag data 0")
		for f in sized_str_entry.vars:
			# print(f)
			# print(f.pointers[1].data)
			outfile.write(f.pointers[1].data)
		print("frag data 1")
		for f in sized_str_entry.vars:
			outfile.write(f.pointers[0].data)
	return out_path,


