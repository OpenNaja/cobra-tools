import struct


def write_manis(archive, sized_str_entry, out_dir):
	name = sized_str_entry.name
	print("\nWriting", name)
	if not sized_str_entry.data_entry:
		print("No data entry for ", name)
		return
	ss_data = sized_str_entry.pointers[0].data
	print(len(ss_data),ss_data)
	buffers = sized_str_entry.data_entry.buffer_datas
	print(len(buffers))
	# if len(buffers) != 3:
	# 	print("Wrong amount of buffers for", name)
	# 	return
	names = [c.name for c in sized_str_entry.children]
	manis_header = struct.pack("<4s3I", b"MANI", archive.ovl.version, archive.ovl.flag_2, len(names) )

	# sizedstr data + 3 buffers
	# sized str data gives general info
	# buffer 0 holds all mani infos - weirdly enough, its first 10 bytes come from the sized str data!
	# buffer 1 is list of hashes and zstrs for each bone name
	# buffer 2 has the actual keys
	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		outfile.write(manis_header)
		for mani in names:
			outfile.write(mani.encode()+b"\x00")
		outfile.write(ss_data)
		for buff in sized_str_entry.data_entry.buffers:
			outfile.write(buff.data)

	# for i, buff in enumerate(sized_str_entry.data_entry.buffers):
	# 	with open(archive.indir(name)+str(i), 'wb') as outfile:
	# 		outfile.write(buff.data)
	# if "partials" in name:
		# data = ManisFormat.Data()
		# with open(archive.indir(name), "rb") as stream:
		# 	data.read(stream)

	return out_path,
