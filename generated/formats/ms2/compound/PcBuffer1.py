import typing
from generated.array import Array
from generated.formats.ms2.compound.Onefiftytwo import Onefiftytwo


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
		self.zeros_1 = Array()

		# Total size of vertex buffer for PC, starting with the 0 - 16 byte indices
		self.vertex_buffer_size = 0
		self.zero_2 = 0
		self.model_infos = Array()

		# the padding between end of the modelinfo array and start of lodinfos
		self.some_zero = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zeros_1 = stream.read_uint64s((2))
		self.vertex_buffer_size = stream.read_uint64()
		self.zero_2 = stream.read_uint64()
		self.model_infos.read(stream, Onefiftytwo, self.arg.mdl_2_count, None)
		self.some_zero = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64s(self.zeros_1)
		stream.write_uint64(self.vertex_buffer_size)
		stream.write_uint64(self.zero_2)
		self.model_infos.write(stream, Onefiftytwo, self.arg.mdl_2_count, None)
		stream.write_uint(self.some_zero)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PcBuffer1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* vertex_buffer_size = {self.vertex_buffer_size.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		s += f'\n	* model_infos = {self.model_infos.__repr__()}'
		s += f'\n	* some_zero = {self.some_zero.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
