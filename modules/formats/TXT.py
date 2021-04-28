import struct

from generated.formats.ovl import is_dla


def write_txt(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	# a bare sized str
	# print("write txt")
	b = sized_str_entry.pointers[0].data
	# print(b)
	if is_dla(ovl):
		# not sure, not standard sized strings
		size, unk = struct.unpack("<2B", b[:2])
		data = b[2:2+size*2]
	else:
		size = struct.unpack("<I", b[:4])[0]
		data = b[4:4+size]
	out_path = out_dir(sized_str_entry.name)
	with open(out_path, "wb") as f:
		f.write(data)
	return out_path,


def load_txt(ovl_data, txt_file_path, txt_sized_str_entry):
	txt_pointer = txt_sized_str_entry.pointers[0]
	with open(txt_file_path, 'rb') as stream:
		raw_txt_bytes = stream.read()
		data = struct.pack("<I", len(raw_txt_bytes)) + raw_txt_bytes + b"\x00"
	# make sure all are updated, and pad to 8 bytes
	txt_pointer.update_data(data, update_copies=True, pad_to=8)
