import io
import logging
import os

from generated.formats.fct.structs.FctRoot import FctRoot
from modules.formats.BaseFormat import MemStructLoader


class FctLoader(MemStructLoader):
	extension = ".fct"
	target_class = FctRoot

	def get_font_name(self, i, ext):
		return f"{self.basename}_font_{i}{ext}"

	def extract(self, out_dir):
		out_files = super().extract(out_dir)
		paths = [*out_files]
		buff = b"".join(self.data_entry.buffer_datas)

		# save data from start of buffer
		offset = self.header.offset
		file_path = out_dir(self.get_font_name("buffer", ".dmp"))
		paths.append(file_path)
		with open(file_path, 'wb') as outfile:
			outfile.write(buff[:offset])

		# extract fonts
		for i, font in enumerate(self.header.fonts):
			if font.data_size:
				type_check = buff[offset:offset + 4]
				if b"OTTO" in type_check:
					ext = ".otf"
				else:
					ext = ".ttf"
				file_path = out_dir(self.get_font_name(i, ext))
				paths.append(file_path)
				with open(file_path, 'wb') as outfile:
					outfile.write(buff[offset:offset + font.data_size])
			offset += font.data_size
		return paths

	def create(self, file_path):
		self.header = self.target_class.from_xml_file(file_path, self.ovl.context)
		file_dir = os.path.dirname(file_path)
		with io.BytesIO() as buff_stream:
			# restore the stuff at the start of the stream
			file_name = self.get_font_name("buffer", ".dmp")
			file_path = os.path.join(file_dir, file_name)
			if not os.path.isfile(file_path):
				logging.warning(f"FCT dump {file_path} is missing")
			with open(file_path, "rb") as f:
				start_bytes = f.read()
			buff_stream.write(start_bytes)
			self.header.offset = buff_stream.tell()

			# load the possible fonts
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
		self.write_memory_data()

