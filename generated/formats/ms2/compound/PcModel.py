from generated.formats.ms2.compound.PcModelData import PcModelData
from generated.formats.ms2.compound.Material1 import Material1
from generated.formats.ms2.compound.Ms2BoneInfo import Ms2BoneInfo
from generated.formats.ms2.compound.LodInfo import LodInfo
import typing


class PcModel:
	lod_infos: typing.List[LodInfo]
	materials_1: typing.List[Material1]
	model_data: typing.List[PcModelData]
	padding: typing.List[int]
	bone_info: Ms2BoneInfo

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.lod_infos = []
		self.materials_1 = []
		self.model_data = []
		self.padding = []
		self.bone_info = Ms2BoneInfo()

	def read(self, stream):

		io_start = stream.tell()
		self.lod_infos = [stream.read_type(LodInfo) for _ in range(self.arg.model_info.lod_count)]
		self.materials_1 = [stream.read_type(Material1) for _ in range(self.arg.model_info.mat_1_count)]
		self.model_data = [stream.read_type(PcModelData) for _ in range(self.arg.model_info.model_count)]
		self.padding = [stream.read_uint() for _ in range(3)]
		self.bone_info = stream.read_type(Ms2BoneInfo)

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		for item in self.lod_infos: stream.write_type(item)
		for item in self.materials_1: stream.write_type(item)
		for item in self.model_data: stream.write_type(item)
		for item in self.padding: stream.write_uint(item)
		stream.write_type(self.bone_info)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'PcModel [Size: '+str(self.io_size)+']'
		s += '\n	* lod_infos = ' + self.lod_infos.__repr__()
		s += '\n	* materials_1 = ' + self.materials_1.__repr__()
		s += '\n	* model_data = ' + self.model_data.__repr__()
		s += '\n	* padding = ' + self.padding.__repr__()
		s += '\n	* bone_info = ' + self.bone_info.__repr__()
		s += '\n'
		return s
