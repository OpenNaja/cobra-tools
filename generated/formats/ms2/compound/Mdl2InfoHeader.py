from generated.array import Array
from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.MaterialName import MaterialName
from generated.formats.ms2.compound.MeshLink import MeshLink
from generated.formats.ms2.compound.ModelData import ModelData
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader


class Mdl2InfoHeader(GenericHeader):

	"""
	Custom header struct
	
	This reads a whole custom mdl2 file
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index of this model inside the ms2
		self.index = 0

		# used to find bone info
		self.bone_info_index = 0

		# name of ms2
		self.ms_2_name = ''

		# gives relevant info on the mdl, including counts and pack base
		self.model_info = CoreModelInfo(self.context, 0, None)

		# name pointers for each material
		self.materials = Array((self.model_info.num_materials,), MaterialName, self.context, 0, None)

		# lod info for each level, only present if models are present (despite the count sometimes saying otherwise!)
		self.lods = Array((self.model_info.num_lods,), LodInfo, self.context, 0, None)

		# instantiate the meshes with materials
		self.objects = Array((self.model_info.num_objects,), MeshLink, self.context, 0, None)

		# model data blocks for this mdl2
		self.models = Array((self.model_info.num_models,), ModelData, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.index = 0
		self.bone_info_index = 0
		self.ms_2_name = ''
		if not (self.context.version < 19):
			self.model_info = CoreModelInfo(self.context, 0, None)
		if not (self.context.version < 19):
			self.materials = Array((self.model_info.num_materials,), MaterialName, self.context, 0, None)
		if not (self.context.version < 19) and self.model_info.num_models:
			self.lods = Array((self.model_info.num_lods,), LodInfo, self.context, 0, None)
		if not (self.context.version < 19):
			self.objects = Array((self.model_info.num_objects,), MeshLink, self.context, 0, None)
		if not (self.context.version < 19):
			self.models = Array((self.model_info.num_models,), ModelData, self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.index = stream.read_uint()
		instance.bone_info_index = stream.read_uint()
		instance.ms_2_name = stream.read_string()
		if not (instance.context.version < 19):
			instance.model_info = CoreModelInfo.from_stream(stream, instance.context, 0, None)
			instance.materials = Array.from_stream(stream, (instance.model_info.num_materials,), MaterialName, instance.context, 0, None)
		if not (instance.context.version < 19) and instance.model_info.num_models:
			instance.lods = Array.from_stream(stream, (instance.model_info.num_lods,), LodInfo, instance.context, 0, None)
		if not (instance.context.version < 19):
			instance.objects = Array.from_stream(stream, (instance.model_info.num_objects,), MeshLink, instance.context, 0, None)
			instance.models = Array.from_stream(stream, (instance.model_info.num_models,), ModelData, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.index)
		stream.write_uint(instance.bone_info_index)
		stream.write_string(instance.ms_2_name)
		if not (instance.context.version < 19):
			CoreModelInfo.to_stream(stream, instance.model_info)
			Array.to_stream(stream, instance.materials, (instance.model_info.num_materials,), MaterialName, instance.context, 0, None)
		if not (instance.context.version < 19) and instance.model_info.num_models:
			Array.to_stream(stream, instance.lods, (instance.model_info.num_lods,), LodInfo, instance.context, 0, None)
		if not (instance.context.version < 19):
			Array.to_stream(stream, instance.objects, (instance.model_info.num_objects,), MeshLink, instance.context, 0, None)
			Array.to_stream(stream, instance.models, (instance.model_info.num_models,), ModelData, instance.context, 0, None)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self):
		return f'Mdl2InfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* index = {self.index.__repr__()}'
		s += f'\n	* bone_info_index = {self.bone_info_index.__repr__()}'
		s += f'\n	* ms_2_name = {self.ms_2_name.__repr__()}'
		s += f'\n	* model_info = {self.model_info.__repr__()}'
		s += f'\n	* materials = {self.materials.__repr__()}'
		s += f'\n	* lods = {self.lods.__repr__()}'
		s += f'\n	* objects = {self.objects.__repr__()}'
		s += f'\n	* models = {self.models.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
