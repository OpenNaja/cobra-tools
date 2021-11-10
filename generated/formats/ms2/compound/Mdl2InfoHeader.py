import typing
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

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index of this model inside the ms2
		self.index = 0

		# used to find bone info
		self.bone_info_index = 0

		# name of ms2
		self.ms_2_name = 0

		# gives relevant info on the mdl, including counts and pack base
		self.model_info = CoreModelInfo(self.context, None, None)

		# name pointers for each material
		self.materials = Array(self.context)

		# lod info for each level, only present if models are present (despite the count sometimes saying otherwise!)
		self.lods = Array(self.context)

		# instantiate the meshes with materials
		self.objects = Array(self.context)

		# model data blocks for this mdl2
		self.models = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.index = 0
		self.bone_info_index = 0
		self.ms_2_name = 0
		if not (self.context.version < 19):
			self.model_info = CoreModelInfo(self.context, None, None)
		if not (self.context.version < 19):
			self.materials = Array(self.context)
		if not (self.context.version < 19) and self.model_info.num_models:
			self.lods = Array(self.context)
		if not (self.context.version < 19):
			self.objects = Array(self.context)
		if not (self.context.version < 19):
			self.models = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.index = stream.read_uint()
		self.bone_info_index = stream.read_uint()
		self.ms_2_name = stream.read_string()
		if not (self.context.version < 19):
			self.model_info = stream.read_type(CoreModelInfo, (self.context, None, None))
			self.materials.read(stream, MaterialName, self.model_info.num_materials, None)
		if not (self.context.version < 19) and self.model_info.num_models:
			self.lods.read(stream, LodInfo, self.model_info.num_lods, None)
		if not (self.context.version < 19):
			self.objects.read(stream, MeshLink, self.model_info.num_objects, None)
			self.models.read(stream, ModelData, self.model_info.num_models, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_uint(self.index)
		stream.write_uint(self.bone_info_index)
		stream.write_string(self.ms_2_name)
		if not (self.context.version < 19):
			stream.write_type(self.model_info)
			self.materials.write(stream, MaterialName, self.model_info.num_materials, None)
		if not (self.context.version < 19) and self.model_info.num_models:
			self.lods.write(stream, LodInfo, self.model_info.num_lods, None)
		if not (self.context.version < 19):
			self.objects.write(stream, MeshLink, self.model_info.num_objects, None)
			self.models.write(stream, ModelData, self.model_info.num_models, None)

		self.io_size = stream.tell() - self.io_start

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
