import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class CommonJointInfo:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# must be 11
		self.eleven = 0

		# bunch of -1's
		self.f_fs = numpy.zeros((3), dtype='int')
		self.name_offset = 0
		self.hitcheck_count = 0
		self.set_defaults()

	def set_defaults(self):
		self.eleven = 0
		self.f_fs = numpy.zeros((3), dtype='int')
		self.name_offset = 0
		self.hitcheck_count = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.eleven = stream.read_uint()
		self.f_fs = stream.read_ints((3))
		self.name_offset = stream.read_uint()
		self.hitcheck_count = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.eleven)
		stream.write_ints(self.f_fs)
		stream.write_uint(self.name_offset)
		stream.write_uint(self.hitcheck_count)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'CommonJointInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* eleven = {self.eleven.__repr__()}'
		s += f'\n	* f_fs = {self.f_fs.__repr__()}'
		s += f'\n	* name_offset = {self.name_offset.__repr__()}'
		s += f'\n	* hitcheck_count = {self.hitcheck_count.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
