import struct

from modules.formats.shared import get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import zstr


def load_assetpkg(ovl_data, assetpkg_file_path, sized_str_entry):
	with open(assetpkg_file_path, "rb") as stream:
		b = stream.read()
		sized_str_entry.fragments[0].pointers[1].update_data(zstr(b), update_copies=True, pad_to=64)


def write_assetpkg(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print("\nWriting", name)
	f_0 = sized_str_entry.fragments[0]
	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		f_0.pointers[1].strip_zstring_padding()
		outfile.write(f_0.pointers[1].data[:-1])
	return out_path,


class AssetpkgLoader(BaseFile):

	def create(self, ovs, file_entry):
		self.ovs = ovs
		# assetpkg.. copy content, pad to 64b, then assign 1 fragment and 1 empty sized str.
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		dbuffer = self.getContent(file_entry.path)
		dbuffer = zstr(dbuffer) + get_padding(len(zstr(dbuffer)), 64)
		pool.data.write(dbuffer)  # fragment pointer 1 data
		pool.data.write(struct.pack('16s', b''))  # fragment pointer 0 data
		new_frag = self.create_fragment()
		new_frag.pointers[0].pool_index = pool_index
		new_frag.pointers[0].data_offset = offset + len(dbuffer)
		new_frag.pointers[1].pool_index = pool_index
		new_frag.pointers[1].data_offset = offset
		new_ss = self.create_ss_entry(file_entry)
		new_ss.pointers[0].pool_index = pool_index
		new_ss.pointers[0].data_offset = offset + len(dbuffer)

	def collect(self, ovl, file_entry):
		self.ovl = ovl
		self.ovs = ovl.static_archive.content
		sized_str_entry = self.ovl.ss_dict[file_entry.name]
		ss_pointer = sized_str_entry.pointers[0]
		frags = self.ovs.pools[ss_pointer.pool_index].fragments
		sized_str_entry.fragments = self.ovs.get_frags_after_count(frags, sized_str_entry.pointers[0].address, 1)
