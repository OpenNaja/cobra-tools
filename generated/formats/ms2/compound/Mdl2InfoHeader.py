from generated.formats.ms2.compound.Model import Model
from generated.formats.ms2.compound.ModelInfo import ModelInfo
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader


class Mdl2InfoHeader(GenericHeader):

	"""
	This reads a whole exported mdl2 file
	"""

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# ms2 version
		self.ms_2_version = 0

		# index of this model inside the ms2
		self.index = 0

		# used to find bone info
		self.bone_info_index = 0

		# name of ms2
		self.ms_2_name = 0

		# gives relevant info on the mdl, including counts and pack base
		self.model_info = ModelInfo(self.context, None, None)

		# describes a model
		self.model = Model(self.context, self.model_info, None)
		self.set_defaults()

	def set_defaults(self):
		self.ms_2_version = 0
		self.index = 0
		self.bone_info_index = 0
		self.ms_2_name = 0
		if not (self.context.version < 19):
			self.model_info = ModelInfo(self.context, None, None)
		if not (self.context.version < 19):
			self.model = Model(self.context, self.model_info, None)

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.ms_2_version = stream.read_uint()
		self.context.ms_2_version = self.ms_2_version
		self.index = stream.read_uint()
		self.bone_info_index = stream.read_uint()
		self.ms_2_name = stream.read_zstring()
		if not (self.context.version < 19):
			self.model_info = stream.read_type(ModelInfo, (self.context, None, None))
			self.model = stream.read_type(Model, (self.context, self.model_info, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_uint(self.ms_2_version)
		stream.write_uint(self.index)
		stream.write_uint(self.bone_info_index)
		stream.write_zstring(self.ms_2_name)
		if not (self.context.version < 19):
			stream.write_type(self.model_info)
			stream.write_type(self.model)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Mdl2InfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ms_2_version = {self.ms_2_version.__repr__()}'
		s += f'\n	* index = {self.index.__repr__()}'
		s += f'\n	* bone_info_index = {self.bone_info_index.__repr__()}'
		s += f'\n	* ms_2_name = {self.ms_2_name.__repr__()}'
		s += f'\n	* model_info = {self.model_info.__repr__()}'
		s += f'\n	* model = {self.model.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
