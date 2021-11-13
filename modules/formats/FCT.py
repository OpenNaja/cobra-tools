import struct

from modules.formats.BaseFormat import BaseFile
from modules.helpers import split_path


class FctLoader(BaseFile):

	def create(self):
		pass
	
	def collect(self):
		self.assign_ss_entry()
	
	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print("\nWriting", name)
		buff = b"".join(self.sized_str_entry.data_entry.buffer_datas)
		ss_len = (len(self.sized_str_entry.pointers[0].data) // 4) - 4
		ss_data = struct.unpack(f"<4f{ss_len}I", self.sized_str_entry.pointers[0].data)
		offset = ss_data[8]

		data_sizes = (ss_data[10], ss_data[12], ss_data[14], ss_data[16])
		paths = []
		for x, data_size in enumerate(data_sizes):
			if data_size != 0:
				type_check = buff[offset:offset + 4]
				if b"OTTO" in type_check:
					ext = ".otf"
				else:
					ext = ".ttf"
				# todo - this create several suffixed files, which have to be retrieved for injection, handle in inject
				path = out_dir(name) + str(x) + ext
				paths.append(path)
				with open(path, 'wb') as outfile:
					outfile.write(buff[offset:offset + data_size])
			offset += data_size
		return paths

	def load(self, file_path):
		# read fct
		# inject fct buffers
		# update sized string
		ss_len = len(self.sized_str_entry.pointers[0].data) / 4
		ss_data = list(struct.unpack("<4f{}I".format(int(ss_len - 4)), self.sized_str_entry.pointers[0].data))
		pad_size = ss_data[8]
		data_sizes = (ss_data[10], ss_data[12], ss_data[14], ss_data[16])
		old_buffer_bytes = self.sized_str_entry.data_entry.buffer_datas[0]
		print("old", len(old_buffer_bytes))
		pad_bytes = old_buffer_bytes[0:pad_size]
		d0 = old_buffer_bytes[pad_size:data_sizes[0] + pad_size]
		d1 = old_buffer_bytes[data_sizes[0] + pad_size:data_sizes[0] + pad_size + data_sizes[1]]
		d2 = old_buffer_bytes[
			 data_sizes[0] + pad_size + data_sizes[1]:data_sizes[0] + pad_size + data_sizes[1] + data_sizes[2]]
		d3 = old_buffer_bytes[data_sizes[0] + pad_size + data_sizes[1] + data_sizes[2]:]
		print("old2", len(pad_bytes + d0 + d1 + d2 + d3))

		# data_size = ss_data[10]
		name_ext, name, ext = split_path(file_path)
		ind = int(name[-1])
		print("updating index: ", ind)

		with open(file_path, "rb") as stream:
			# load the new buffer
			new_buffer_bytes = stream.read()

			buffer_bytes = pad_bytes  # update the correct ss entry size
			if ind == 0:
				ss_data[10] = len(new_buffer_bytes)
				buffer_bytes += new_buffer_bytes
				buffer_bytes += d1
				buffer_bytes += d2
				buffer_bytes += d3
			elif ind == 1:
				ss_data[12] = len(new_buffer_bytes)
				buffer_bytes += d0
				buffer_bytes += new_buffer_bytes
				buffer_bytes += d2
				buffer_bytes += d3
			elif ind == 2:
				ss_data[14] = len(new_buffer_bytes)
				buffer_bytes += d0
				buffer_bytes += d1
				buffer_bytes += new_buffer_bytes
				buffer_bytes += d3
			elif ind == 3:
				ss_data[16] = len(new_buffer_bytes)
				buffer_bytes += d0
				buffer_bytes += d1
				buffer_bytes += d2
				buffer_bytes += new_buffer_bytes

			print(len(buffer_bytes))

			# update the buffers
			self.sized_str_entry.data_entry.update_data((buffer_bytes,))

			data = struct.pack("<4f{}I".format(int(ss_len - 4)), *ss_data)
			self.sized_str_entry.pointers[0].update_data(data, update_copies=True)
