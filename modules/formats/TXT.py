import struct

from generated.formats.ovl import is_dla
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import zstr


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


class TxtLoader(BaseFile):

	def create(self, ovs, file_entry):
		self.ovs = ovs
		dbuffer = self.getContent(file_entry.path)
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		new_ss = self.create_ss_entry(file_entry)
		new_ss.pointers[0].pool_index = pool_index
		new_ss.pointers[0].data_offset = offset
		data = struct.pack("I", len(dbuffer)) + zstr(dbuffer)
		pool.data.write(data + get_padding(len(data), alignment=8))
		pool.num_files += 1

	def collect(self, ovl, file_entry):
		# no fragments
		pass
