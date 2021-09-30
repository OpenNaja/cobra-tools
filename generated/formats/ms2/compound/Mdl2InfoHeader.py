import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo
from generated.formats.ms2.compound.FixedString import FixedString
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.MaterialName import MaterialName
from generated.formats.ms2.compound.MeshLink import MeshLink
from generated.formats.ms2.compound.ModelData import ModelData


class Mdl2InfoHeader:

	"""
	Custom header struct
	
	This reads a whole custom mdl2 file
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'MS2 '
		self.magic = FixedString(context, 4, None)

		# if 0x08 then 64bit, 0x01 for JWE, PZ, 0x08 for PC
		self.version_flag = 0

		# 0x12 = PC, 0x13 = JWE, PZ
		self.version = 0

		# endianness?, usually zero
		self.bitswap = 0

		# always = 1
		self.seventh_byte = 1
		self.user_version = 0

		# index of this model inside the ms2
		self.index = 0

		# used to find bone info
		self.bone_info_index = 0

		# name of ms2
		self.ms_2_name = 0

		# gives relevant info on the mdl, including counts and pack base
		if not (self.context.version < 19):
			self.model_info = CoreModelInfo(context, None, None)

		# name pointers for each material
		if not (self.context.version < 19):
			self.materials = Array()

		# lod info for each level, only present if models are present (despite the count sometimes saying otherwise!)
		if not (self.context.version < 19):
			self.lods = Array()

		# instantiate the meshes with materials
		if not (self.context.version < 19):
			self.objects = Array()

		# model data blocks for this mdl2
		if not (self.context.version < 19):
			self.models = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic = stream.read_type(FixedString, (4, None))
		self.version_flag = stream.read_byte()
		stream.version_flag = self.version_flag
		self.version = stream.read_byte()
		stream.version = self.version
		self.bitswap = stream.read_byte()
		self.seventh_byte = stream.read_byte()
		self.user_version = stream.read_uint()
		stream.user_version = self.user_version
		self.index = stream.read_uint()
		self.bone_info_index = stream.read_uint()
		self.ms_2_name = stream.read_string()
		if not (self.context.version < 19):
			self.model_info = stream.read_type(CoreModelInfo)
			self.materials.read(stream, MaterialName, self.model_info.num_materials, None)
		if not (self.context.version < 19):
			self.lods.read(stream, LodInfo, self.model_info.num_lods, None)
			self.objects.read(stream, MeshLink, self.model_info.num_objects, None)
		if not (self.context.version < 19):
			self.models.read(stream, ModelData, self.model_info.num_models, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.magic)
		stream.write_byte(self.version_flag)
		stream.version_flag = self.version_flag
		stream.write_byte(self.version)
		stream.version = self.version
		stream.write_byte(self.bitswap)
		stream.write_byte(self.seventh_byte)
		stream.write_uint(self.user_version)
		stream.user_version = self.user_version
		stream.write_uint(self.index)
		stream.write_uint(self.bone_info_index)
		stream.write_string(self.ms_2_name)
		if not (self.context.version < 19):
			stream.write_type(self.model_info)
			self.materials.write(stream, MaterialName, self.model_info.num_materials, None)
		if not (self.context.version < 19):
			self.lods.write(stream, LodInfo, self.model_info.num_lods, None)
			self.objects.write(stream, MeshLink, self.model_info.num_objects, None)
		if not (self.context.version < 19):
			self.models.write(stream, ModelData, self.model_info.num_models, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Mdl2InfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* magic = {self.magic.__repr__()}'
		s += f'\n	* version_flag = {self.version_flag.__repr__()}'
		s += f'\n	* version = {self.version.__repr__()}'
		s += f'\n	* bitswap = {self.bitswap.__repr__()}'
		s += f'\n	* seventh_byte = {self.seventh_byte.__repr__()}'
		s += f'\n	* user_version = {self.user_version.__repr__()}'
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
