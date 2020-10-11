import typing
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.Material1 import Material1
from generated.formats.ms2.compound.PcModelData import PcModelData


class PcModel:
	lod_infos: typing.List[LodInfo]
	materials_1: typing.List[Material1]
	model_data: typing.List[PcModelData]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.lod_infos = []
		self.materials_1 = []
		self.model_data = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.lod_infos = [stream.read_type(LodInfo) for _ in range(self.arg.model_info.lod_count)]
		self.materials_1 = [stream.read_type(Material1) for _ in range(self.arg.model_info.mat_1_count)]
		self.model_data = [stream.read_type(PcModelData) for _ in range(self.arg.model_info.model_count)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		for item in self.lod_infos: stream.write_type(item)
		for item in self.materials_1: stream.write_type(item)
		for item in self.model_data: stream.write_type(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'PcModel [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* lod_infos = ' + self.lod_infos.__repr__()
		s += '\n	* materials_1 = ' + self.materials_1.__repr__()
		s += '\n	* model_data = ' + self.model_data.__repr__()
		s += '\n'
		return s
