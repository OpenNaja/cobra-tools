import struct


def write_txt(archive, sized_str_entry, out_dir):
	# a bare sized str
	b = sized_str_entry.pointers[0].data
	size = struct.unpack("<I", b[:4])[0]
	out_path = out_dir(sized_str_entry.name)
	with open(out_path, "wb") as f:
		f.write(b[4:4+size])
	return out_path,
