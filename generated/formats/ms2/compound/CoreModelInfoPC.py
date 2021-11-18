import numpy
from generated.array import Array
from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo


class CoreModelInfoPC(CoreModelInfo):

	"""
	152 bytes
	"""

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros = numpy.zeros((5), dtype='uint64')
		self.zeros = numpy.zeros((9), dtype='uint64')
		self.one = 0
		self.zero = 0
		self.zero_zt = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version == 18:
			self.zeros = numpy.zeros((5), dtype='uint64')
		if self.context.version == 17:
			self.zeros = numpy.zeros((9), dtype='uint64')
		self.one = 0
		self.zero = 0
		if self.context.version == 17:
			self.zero_zt = 0

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		if self.context.version == 18:
			self.zeros = stream.read_uint64s((5))
		if self.context.version == 17:
			self.zeros = stream.read_uint64s((9))
		self.one = stream.read_uint64()
		self.zero = stream.read_uint64()
		if self.context.version == 17:
			self.zero_zt = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		if self.context.version == 18:
			stream.write_uint64s(self.zeros)
		if self.context.version == 17:
			stream.write_uint64s(self.zeros)
		stream.write_uint64(self.one)
		stream.write_uint64(self.zero)
		if self.context.version == 17:
			stream.write_uint64(self.zero_zt)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'CoreModelInfoPC [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* one = {self.one.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* zero_zt = {self.zero_zt.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
