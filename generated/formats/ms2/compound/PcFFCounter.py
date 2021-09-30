import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class PcFFCounter:

	"""
	count is nonzero in PZ broken birch model
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.count = 0
		self.f_fs = numpy.zeros((self.count), dtype='byte')

	def read(self, stream):

		self.io_start = stream.tell()
		self.count = stream.read_uint()
		self.f_fs = stream.read_bytes((self.count))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.count)
		stream.write_bytes(self.f_fs)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PcFFCounter [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* count = {self.count.__repr__()}'
		s += f'\n	* f_fs = {self.f_fs.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
