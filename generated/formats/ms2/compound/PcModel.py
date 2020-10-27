import typing
from generated.array import Array
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.Material1 import Material1
from generated.formats.ms2.compound.PcModelData import PcModelData


class PcModel:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.lod_infos = Array()
		self.materials_1 = Array()
		self.model_data = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.lod_infos.read(stream, LodInfo, self.arg.model_info.lod_count, None)
		self.materials_1.read(stream, Material1, self.arg.model_info.mat_1_count, None)
		self.model_data.read(stream, PcModelData, self.arg.model_info.model_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.lod_infos.write(stream, LodInfo, self.arg.model_info.lod_count, None)
		self.materials_1.write(stream, Material1, self.arg.model_info.mat_1_count, None)
		self.model_data.write(stream, PcModelData, self.arg.model_info.model_count, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'PcModel [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* lod_infos = ' + self.lod_infos.__repr__()
		s += '\n	* materials_1 = ' + self.materials_1.__repr__()
		s += '\n	* model_data = ' + self.model_data.__repr__()
		s += '\n'
		return s
