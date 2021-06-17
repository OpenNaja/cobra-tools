import struct

from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import zstr


def load_userinterfaceicondata(ovl_data, userinterfaceicondata_file_path, sized_str_entry):
	with open(userinterfaceicondata_file_path, "rb") as stream:
		icname, icpath = [line.strip() for line in stream.read().split(b'\n') if line.strip()]
		f0 = icname + b'\x00'
		f1 = icpath + b'\x00'
		sized_str_entry.fragments[0].pointers[1].update_data(f0, update_copies=True)
		sized_str_entry.fragments[1].pointers[1].update_data(f1, update_copies=True, pad_to=64-len(f0))


def write_userinterfaceicondata(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print("\nWriting", name)
	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		for frag in sized_str_entry.fragments:
			frag.pointers[1].strip_zstring_padding()
			outfile.write(frag.pointers[1].data[:-1])
			outfile.write(b"\n")
	return out_path,


class UserinterfaceicondataLoader(BaseFile):

	def create(self, ovs, file_entry):
		self.ovs = ovs
		dbuffer = self.get_content(file_entry.path)
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()

		# userinterfaceicondata, 2 frags
		icname, icpath = [line.strip() for line in dbuffer.split(b'\n') if line.strip()]
		outb = zstr(icname) + zstr(icpath)
		pool.data.write(outb + get_padding(len(outb), 64) + struct.pack('8s', b''))
		newoffset = pool.data.tell()
		pool.data.write(struct.pack('16s', b''))
		new_frag0 = self.create_fragment()
		new_frag0.pointers[0].pool_index = pool_index
		new_frag0.pointers[0].data_offset = newoffset
		new_frag0.pointers[1].pool_index = pool_index
		new_frag0.pointers[1].data_offset = offset
		new_frag1 = self.create_fragment()
		new_frag1.pointers[0].pool_index = pool_index
		new_frag1.pointers[0].data_offset = newoffset + 8
		new_frag1.pointers[1].pool_index = pool_index
		new_frag1.pointers[1].data_offset = offset + len(icname) + 1
		new_ss = self.create_ss_entry(file_entry)
		new_ss.pointers[0].pool_index = pool_index
		new_ss.pointers[0].data_offset = newoffset

	def collect(self, ovl, file_entry):
		self.assign_fixed_frags(ovl, file_entry, 2)


