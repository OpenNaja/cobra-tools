from generated.formats.fgm.compound.FgmHeader import FgmHeader
from generated.formats.ovl_base.basic import ConvStream
from modules.formats.BaseFormat import MemStructLoader


class FgmLoader(MemStructLoader):
	target_class = FgmHeader
	extension = ".fgm"

	def create(self):
		super().create()
		self.create_data_entry(self.sized_str_entry, (self.update_names_buffer(),))

	@staticmethod
	def read_z_str(stream, pos):
		stream.seek(pos)
		return stream.read_zstring()

	def collect(self):
		super().collect()
		self.header.debug_ptrs()
		self.get_names()
		# print(self.header)

	def get_names(self):
		"""Assigns names from the data buffer"""
		buffer_data = self.sized_str_entry.data_entry.buffer_datas[0]
		stream = ConvStream(buffer_data)
		self.header.shader_name = self.read_z_str(stream, 0)
		for texture in self.header.textures.data:
			texture.texture_name = self.read_z_str(stream, texture.offset)
		for attrib in self.header.attributes.data:
			attrib.attrib_name = self.read_z_str(stream, attrib.offset)

	def update_names_buffer(self):
		"""Rewrites the name buffer and updates the offsets"""
		names_writer = ConvStream()
		# shader name is at 0
		names_writer.write_zstring(self.header.shader_name)
		names_writer.write(b"\x00")
		# attribs are written first
		for attrib in self.header.attributes.data:
			attrib.offset = names_writer.tell()
			names_writer.write_zstring(attrib.texture_name)
		for texture in self.header.textures.data:
			texture.offset = names_writer.tell()
			names_writer.write_zstring(texture.attrib_name)
		return names_writer.getvalue()

	def load(self, file_path):
		# clear dependencies
		self.file_entry.dependencies.clear()
		super().load(file_path)
		# todo - set shader_name, texture_name, attrib_name to be able to update the buffer
		# self.sized_str_entry.data_entry.update_data((self.update_names_buffer(),))

		# todo - automatically create dependency from MemStruct
		for tex_name in self.get_deps_names():
			self.create_dependency(f"{tex_name}.tex")

	def get_deps_names(self):
		return [dep.data for dep in self.header.dependencies.data if dep.data]

