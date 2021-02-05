import typing
from generated.array import Array
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.Material1 import Material1
from generated.formats.ms2.compound.PcModelData import PcModelData


class PcModel:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# uses uint here, uint64 elsewhere
		self.materials_0 = Array()
		self.lod_infos = Array()
		self.materials_1 = Array()
		self.model_data = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.materials_0 = stream.read_uints((self.arg.mat_count))
		self.lod_infos.read(stream, LodInfo, self.arg.lod_count, None)
		self.materials_1.read(stream, Material1, self.arg.mat_1_count, None)
		self.model_data.read(stream, PcModelData, self.arg.model_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uints(self.materials_0)
		self.lod_infos.write(stream, LodInfo, self.arg.lod_count, None)
		self.materials_1.write(stream, Material1, self.arg.mat_1_count, None)
		self.model_data.write(stream, PcModelData, self.arg.model_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PcModel [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* materials_0 = {self.materials_0.__repr__()}'
		s += f'\n	* lod_infos = {self.lod_infos.__repr__()}'
		s += f'\n	* materials_1 = {self.materials_1.__repr__()}'
		s += f'\n	* model_data = {self.model_data.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
