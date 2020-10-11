import typing
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

	# 'MS2 '
	magic: FixedString
	version: int
	user_version: int

	# index of this model inside the ms2, used to find bone info
	index: int

	# name of ms2
	name: str

	# gives relevant info on the mdl, including counts and pack base
	model_info: CoreModelInfo

	# name pointers for each material
	materials_0: typing.List[Material0]

	# lod info for each level
	lods: typing.List[LodInfo]

	# material links for each model
	materials_1: typing.List[Material1]

	# model data blocks for this mdl2
	models: typing.List[ModelData]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.magic = FixedString()
		self.version = 0
		self.user_version = 0
		self.index = 0
		self.name = 0
		self.model_info = CoreModelInfo()
		self.materials_0 = []
		self.lods = []
		self.materials_1 = []
		self.models = []

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
			self.materials_0 = [stream.read_type(Material0) for _ in range(self.model_info.mat_count)]
			self.lods = [stream.read_type(LodInfo) for _ in range(self.model_info.lod_count)]
			self.materials_1 = [stream.read_type(Material1) for _ in range(self.model_info.mat_1_count)]
			self.models = [stream.read_type(ModelData) for _ in range(self.model_info.model_count)]

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
			for item in self.materials_0: stream.write_type(item)
			for item in self.lods: stream.write_type(item)
			for item in self.materials_1: stream.write_type(item)
			for item in self.models: stream.write_type(item)

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
