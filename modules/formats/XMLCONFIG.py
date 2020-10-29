def write_xmlconfig(archive, sized_str_entry, out_dir):
	name = sized_str_entry.name
	print("\nWriting",name)

	if len(sized_str_entry.fragments) == 1:
		f_0 = sized_str_entry.fragments[0]
	else:
		print("Found wrong amount of frags for",name)
		return
	# write xml
	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		# 8 x b00
		# sized_str_entry.pointers[0].data
		# 8 x b00
		# outfile.write( f_0.pointers[0].data )
		# the actual xml data
		# often with extra junk at the end (probably z str)
		f_0.pointers[1].strip_zstring_padding()
		# strip the b00 zstr terminator byte
		outfile.write(f_0.pointers[1].data[:-1])
	return out_path,


def load_xmlconfig(ovl_data, xml_file_path, xml_sized_str_entry):
	with open(xml_file_path, 'rb') as stream:
		# add zero terminator
		data = stream.read() + b"\x00"
		# make sure all are updated, and pad to 8 bytes
		xml_sized_str_entry.fragments[0].pointers[1].update_data(data, update_copies=True, pad_to=8)