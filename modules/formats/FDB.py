import struct

from modules.formats.BaseFormat import BaseFile


def write_fdb(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print("\nWriting", name)

	try:
		buff = sized_str_entry.data_entry.buffer_datas[1]
	except:
		print("Found no buffer data for", name)
		return
	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		# write the buffer, only buffer 1
		# buffer 0 is just the bare file name, boring
		# sizedstr data is just size of the buffer
		outfile.write(buff)
	return out_path,


def load_fdb(ovl_data, fdb_file_path, fdb_sized_str_entry, fdb_name):
	# read fdb
	# inject fdb buffers
	# update sized string

	with open(fdb_file_path, "rb") as fdb_stream:
		# load the new buffers
		buffer1_bytes = fdb_stream.read()
		buffer0_bytes = fdb_name.encode()
		# update the buffers
		fdb_sized_str_entry.data_entry.update_data( (buffer0_bytes, buffer1_bytes) )
		# update the sizedstring entry
		data = struct.pack("<8I", len(buffer1_bytes), 0, 0, 0, 0, 0, 0, 0)
		fdb_sized_str_entry.pointers[0].update_data(data, update_copies=True)


class FdbLoader(BaseFile):

	def create(self, ovs, file_entry):
		self.ovs = ovs
		dbuffer = self.getContent(file_entry.path)
		file_name_bytes = file_entry.basename.encode(encoding='utf8')
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		pool.data.write(struct.pack("I28s", len(dbuffer), b''))
		new_ss = self.create_ss_entry(file_entry)
		new_ss.pointers[0].pool_index = pool_index
		new_ss.pointers[0].data_offset = offset
		new_data = self.create_data_entry(file_entry, (file_name_bytes, dbuffer))
		# new_data.set_index = 0

	def collect(self, ovl, file_entry):
		pass
