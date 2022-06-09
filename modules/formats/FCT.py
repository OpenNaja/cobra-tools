import io
import os

from generated.formats.fct.compound.FctRoot import FctRoot
from modules.formats.BaseFormat import MemStructLoader


class FctLoader(MemStructLoader):
	extension = ".fct"
	target_class = FctRoot

	def get_font_name(self, i, ext):
		return f"{self.file_entry.basename}_font_{i}{ext}"

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
				path = out_dir(self.get_font_name(i, ext))
				paths.append(path)
				with open(path, 'wb') as outfile:
					outfile.write(buff[offset:offset + font.data_size])
			offset += font.data_size
		return paths

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		file_dir = os.path.dirname(self.file_entry.path)
		with io.BytesIO() as buff_stream:
			buff_stream.write(b'\x00' * self.header.offset)
			for i, font in enumerate(self.header.fonts):
				# see if a matching font exists
				for ext in (".otf", ".ttf"):
					file_name = self.get_font_name(i, ext)
					file_path = os.path.join(file_dir, file_name)
					if os.path.isfile(file_path):
						# load and store its data
						with open(file_path, "rb") as f:
							font_bytes = f.read()
						buff_stream.write(font_bytes)
						font.data_size = len(font_bytes)
						break
				else:
					font.data_size = 0
			# write data
			self.create_data_entry((buff_stream.getvalue(),))
			self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)

