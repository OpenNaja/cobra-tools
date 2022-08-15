from generated.formats.fgm.compounds.FgmHeader import FgmHeader
from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.ovl_base.basic import ConvStream
from modules.formats.BaseFormat import MemStructLoader

attrib_sizes = {
	0: 4,  # FgmDtype.Float
	1: 8,  # FgmDtype.Float2
	2: 12,  # FgmDtype.FLOAT_3
	3: 16,  # FgmDtype.Float4
	5: 4,  # FgmDtype.Int
	6: 4,  # FgmDtype.Bool
}


class FgmLoader(MemStructLoader):
	target_class = FgmHeader
	extension = ".fgm"

	def create(self):
		super().create()
		# print(self.header)
		self.create_data_entry((self.update_names_buffer(),))

	@staticmethod
	def read_z_str(stream, pos):
		stream.seek(pos)
		return stream.read_zstring()

	def collect(self):
		super().collect()
		self.get_names()
		# print(self.header)

	def get_names(self):
		"""Assigns names from the data buffer"""
		buffer_data = self.data_entry.buffer_datas[0]
		stream = ConvStream(buffer_data)
		self.header.shader_name = self.read_z_str(stream, 0)
		for arr in (self.header.attributes.data, self.header.textures.data):
			if arr:
				for member in arr:
					member.name = self.read_z_str(stream, member._name_offset)

	def update_names_buffer(self):
		"""Rewrites the name buffer and updates the offsets"""
		self.header._attribute_count = len(self.header.attributes.data)
		self.header._texture_count = len(self.header.textures.data)
		names_writer = ConvStream()
		# shader name is at 0
		names_writer.write_zstring(self.header.shader_name)
		names_writer.write(b"\x00")
		# attribs are written first
		for arr in (self.header.attributes.data, self.header.textures.data):
			if arr:
				for member in arr:
					member._name_offset = names_writer.tell()
					names_writer.write_zstring(member.name)

		for i, tex in enumerate([t for t in self.header.textures.data if t.dtype == FgmDtype.TEXTURE]):
			tex.value[0]._tex_index = i
		value_offset = 0
		for attrib, attrib_data in zip(self.header.attributes.data, self.header.attributes.data):
			attrib._value_offset = value_offset
			value_offset += attrib_sizes[attrib.dtype]
		return names_writer.getvalue()
