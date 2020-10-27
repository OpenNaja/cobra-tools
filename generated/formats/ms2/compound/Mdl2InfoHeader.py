import typing
from generated.array import Array
from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo
from generated.formats.ms2.compound.FixedString import FixedString
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.Material0 import Material0
from generated.formats.ms2.compound.Material1 import Material1
from generated.formats.ms2.compound.ModelData import ModelData


class Mdl2InfoHeader:

	"""
	Custom header struct
	
	This reads a whole custom mdl2 file
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'MS2 '
		self.magic = FixedString()
		self.version = 0
		self.user_version = 0

		# index of this model inside the ms2, used to find bone info
		self.index = 0

		# name of ms2
		self.name = 0

		# gives relevant info on the mdl, including counts and pack base
		self.model_info = CoreModelInfo()

		# name pointers for each material
		self.materials_0 = Array()

		# lod info for each level
		self.lods = Array()

		# material links for each model
		self.materials_1 = Array()

		# model data blocks for this mdl2
		self.models = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic = stream.read_type(FixedString, (4,))
		self.version = stream.read_uint()
		stream.version = self.version
		self.user_version = stream.read_uint()
		stream.user_version = self.user_version
		self.index = stream.read_uint()
		self.name = stream.read_string()
		if not (stream.version == 18):
			self.model_info = stream.read_type(CoreModelInfo)
			self.materials_0.read(stream, Material0, self.model_info.mat_count, None)
			self.lods.read(stream, LodInfo, self.model_info.lod_count, None)
			self.materials_1.read(stream, Material1, self.model_info.mat_1_count, None)
			self.models.read(stream, ModelData, self.model_info.model_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.magic)
		stream.write_uint(self.version)
		stream.version = self.version
		stream.write_uint(self.user_version)
		stream.user_version = self.user_version
		stream.write_uint(self.index)
		stream.write_string(self.name)
		if not (stream.version == 18):
			stream.write_type(self.model_info)
			self.materials_0.write(stream, Material0, self.model_info.mat_count, None)
			self.lods.write(stream, LodInfo, self.model_info.lod_count, None)
			self.materials_1.write(stream, Material1, self.model_info.mat_1_count, None)
			self.models.write(stream, ModelData, self.model_info.model_count, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Mdl2InfoHeader [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* magic = ' + self.magic.__repr__()
		s += '\n	* version = ' + self.version.__repr__()
		s += '\n	* user_version = ' + self.user_version.__repr__()
		s += '\n	* index = ' + self.index.__repr__()
		s += '\n	* name = ' + self.name.__repr__()
		s += '\n	* model_info = ' + self.model_info.__repr__()
		s += '\n	* materials_0 = ' + self.materials_0.__repr__()
		s += '\n	* lods = ' + self.lods.__repr__()
		s += '\n	* materials_1 = ' + self.materials_1.__repr__()
		s += '\n	* models = ' + self.models.__repr__()
		s += '\n'
		return s
