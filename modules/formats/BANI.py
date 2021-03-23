from modules.helpers import write_sized_str


def write_banis(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	if not sized_str_entry.data_entry:
		print("No data entry for ",name)
		return
	buffers = sized_str_entry.data_entry.buffer_datas
	if len(buffers) != 1:
		print("Wrong amount of buffers for",name)
		return
	print("\nWriting",name)
	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		outfile.write(buffers[0])
	return out_path,


def write_bani(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print("\nWriting", name)
	if len(sized_str_entry.fragments) != 1:
		print("must have 1 fragment")
		return
	for file_entry in ovl.files:
		if file_entry.ext == ".banis":
			banis_name = file_entry.name
			break
	else:
		print("Found no banis file for bani animation!")
		return

	f = sized_str_entry.fragments[0]

	# write banis file
	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		outfile.write(b"BANI")
		write_sized_str(outfile, banis_name)
		outfile.write(f.pointers[0].data)
		outfile.write(f.pointers[1].data)
	return out_path,
