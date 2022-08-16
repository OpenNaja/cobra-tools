from generated.formats.base.basic import ZString
from io import BytesIO
from generated.formats.particle.compounds.ParticleAtlasHeader import ParticleAtlasHeader
from modules.formats.BaseFormat import MemStructLoader


class ParticleAtlasLoader(MemStructLoader):
	target_class = ParticleAtlasHeader
	extension = ".particleatlas"

	# def create(self):
	# 	self.create_root_entry()
	# 	self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
	# 	self.create_data_entry((self.update_names_buffer(),))
	# 	# need to update before writing ptrs
	# 	self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)
	#
	# # @staticmethod
	# def read_z_str(self, stream, pos):
	# 	stream.seek(pos)
	# 	return ZString.from_stream(stream, self.ovl.context)
	#
	# def collect(self):
	# 	super().collect()
	# 	self.get_names()
	# 	# print(self.header)
	#
	# def get_names(self):
	# 	"""Assigns names from the data buffer"""
	# 	buffer_data = self.data_entry.buffer_datas[0]
	# 	with BytesIO(buffer_data) as stream:
	# 		self.header.shader_name = self.read_z_str(stream, 0)
	# 		for arr in (self.header.attributes.data, self.header.textures.data):
	# 			if arr:
	# 				for member in arr:
	# 					member.name = self.read_z_str(stream, member._name_offset)
	#
	# def update_names_buffer(self):
	# 	"""Rewrites the name buffer and updates the offsets"""
	# 	self.header._attribute_count = len(self.header.attributes.data)
	# 	self.header._texture_count = len(self.header.textures.data)
	# 	with BytesIO() as names_writer:
	# 		# shader name is at 0
	# 		ZString.to_stream(names_writer, self.header.shader_name)
	# 		names_writer.write(b"\x00")
	# 		# attribs are written first
	# 		for arr in (self.header.attributes.data, self.header.textures.data):
	# 			if arr:
	# 				for member in arr:
	# 					member._name_offset = names_writer.tell()
	# 					ZString.to_stream(names_writer, member.name)
	#
	# 		for i, tex in enumerate([t for t in self.header.textures.data if t.dtype == FgmDtype.TEXTURE]):
	# 			tex.value[0]._tex_index = i
	# 		value_offset = 0
	# 		for attrib, attrib_data in zip(self.header.attributes.data, self.header.attributes.data):
	# 			attrib._value_offset = value_offset
	# 			value_offset += attrib_sizes[attrib.dtype]
	# 		return names_writer.getvalue()
