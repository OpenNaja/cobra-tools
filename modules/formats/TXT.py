import struct


def write_txt(archive, sized_str_entry, out_dir):
	# a bare sized str
	b = sized_str_entry.pointers[0].data
	size = struct.unpack("<I", b[:4])[0]
	out_path = out_dir(sized_str_entry.name)
	with open(out_path, "wb") as f:
		f.write(b[4:4+size])
	return out_path,


def load_txt(ovl_data, txt_file_path, txt_sized_str_entry):
	txt_pointer = txt_sized_str_entry.pointers[0]
	# first make sure that the padding has been separated from the data
	size = struct.unpack("<I", txt_pointer.data[:4])[0]
	txt_pointer.split_data_padding(4+size)
	with open(txt_file_path, 'rb') as stream:
		raw_txt_bytes = stream.read()
		data = struct.pack("<I", len(raw_txt_bytes)) + raw_txt_bytes
	# make sure all are updated, and pad to 8 bytes, using old padding
	txt_pointer.update_data(data, update_copies=True, pad_to=8, include_old_pad=True)