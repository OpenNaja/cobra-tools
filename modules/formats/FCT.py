from generated.formats.fct.compound.FctRoot import FctRoot
from modules.formats.BaseFormat import MemStructLoader


class FctLoader(MemStructLoader):
	extension = ".fct"
	target_class = FctRoot

	def extract(self, out_dir, show_temp_files, progress_callback):
		out_files = super().extract(out_dir, show_temp_files, progress_callback)
		paths = [*out_files]
		buff = b"".join(self.data_entry.buffer_datas)

		offset = self.header.offset
		for i, font in enumerate(self.header.fonts):
			if font.data_size:
				type_check = buff[offset:offset + 4]
				if b"OTTO" in type_check:
					ext = ".otf"
				else:
					ext = ".ttf"
				path = f"{out_dir(self.file_entry.basename)}_font_{i}{ext}"
				paths.append(path)
				with open(path, 'wb') as outfile:
					outfile.write(buff[offset:offset + font.data_size])
			offset += font.data_size
		return paths

	# def load(self, file_path):
	# 	# todo - fixme
	# 	# read fct
	# 	# inject fct buffers
	# 	# update sized string
	# 	ss_len = len(self.root_entry.struct_ptr.data) / 4
	# 	ss_data = list(struct.unpack("<4f{}I".format(int(ss_len - 4)), self.root_entry.struct_ptr.data))
	# 	pad_size = ss_data[8]
	# 	data_sizes = (ss_data[10], ss_data[12], ss_data[14], ss_data[16])
	# 	old_buffer_bytes = self.data_entry.buffer_datas[0]
	# 	print("old", len(old_buffer_bytes))
	# 	pad_bytes = old_buffer_bytes[0:pad_size]
	# 	d0 = old_buffer_bytes[pad_size:data_sizes[0] + pad_size]
	# 	d1 = old_buffer_bytes[data_sizes[0] + pad_size:data_sizes[0] + pad_size + data_sizes[1]]
	# 	d2 = old_buffer_bytes[
	# 		 data_sizes[0] + pad_size + data_sizes[1]:data_sizes[0] + pad_size + data_sizes[1] + data_sizes[2]]
	# 	d3 = old_buffer_bytes[data_sizes[0] + pad_size + data_sizes[1] + data_sizes[2]:]
	# 	print("old2", len(pad_bytes + d0 + d1 + d2 + d3))
	#
	# 	# data_size = ss_data[10]
	# 	name_ext, name, ext = split_path(file_path)
	# 	ind = int(name[-1])
	# 	print("updating index: ", ind)
	#
	# 	with open(file_path, "rb") as stream:
	# 		# load the new buffer
	# 		new_buffer_bytes = stream.read()
	#
	# 		buffer_bytes = pad_bytes  # update the correct root_entry entry size
	# 		if ind == 0:
	# 			ss_data[10] = len(new_buffer_bytes)
	# 			buffer_bytes += new_buffer_bytes
	# 			buffer_bytes += d1
	# 			buffer_bytes += d2
	# 			buffer_bytes += d3
	# 		elif ind == 1:
	# 			ss_data[12] = len(new_buffer_bytes)
	# 			buffer_bytes += d0
	# 			buffer_bytes += new_buffer_bytes
	# 			buffer_bytes += d2
	# 			buffer_bytes += d3
	# 		elif ind == 2:
	# 			ss_data[14] = len(new_buffer_bytes)
	# 			buffer_bytes += d0
	# 			buffer_bytes += d1
	# 			buffer_bytes += new_buffer_bytes
	# 			buffer_bytes += d3
	# 		elif ind == 3:
	# 			ss_data[16] = len(new_buffer_bytes)
	# 			buffer_bytes += d0
	# 			buffer_bytes += d1
	# 			buffer_bytes += d2
	# 			buffer_bytes += new_buffer_bytes
	#
	# 		print(len(buffer_bytes))
	#
	# 		# update the buffers
	# 		self.data_entry.update_data((buffer_bytes,))
	#
	# 		data = struct.pack("<4f{}I".format(int(ss_len - 4)), *ss_data)
	# 		self.write_data_to_pool(self.root_entry.struct_ptr, 2, data)
