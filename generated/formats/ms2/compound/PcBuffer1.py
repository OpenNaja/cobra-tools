import typing
from generated.array import Array
from generated.formats.ms2.compound.CoreModelInfoPC import CoreModelInfoPC
from generated.formats.ms2.compound.Ms2BufferInfoPC import Ms2BufferInfoPC


class PcBuffer1:

	"""
	cond="general info \ ms2 version == 32"
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.buffer_info_pc = Ms2BufferInfoPC()
		self.model_infos = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.buffer_info_pc = stream.read_type(Ms2BufferInfoPC)
		self.model_infos.read(stream, CoreModelInfoPC, self.arg.mdl_2_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.buffer_info_pc)
		self.model_infos.write(stream, CoreModelInfoPC, self.arg.mdl_2_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PcBuffer1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* buffer_info_pc = {self.buffer_info_pc.__repr__()}'
		s += f'\n	* model_infos = {self.model_infos.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
