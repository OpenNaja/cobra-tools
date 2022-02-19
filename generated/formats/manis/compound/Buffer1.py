import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.manis.compound.PadAlign import PadAlign


class Buffer1:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.bone_hashes = numpy.zeros((), dtype='uint')
		self.bone_names = Array(self.context)

		# ?
		self.bone_pad = PadAlign(self.context, self.bone_names, 4)
		self.set_defaults()

	def set_defaults(self):
		self.bone_hashes = numpy.zeros((), dtype='uint')
		self.bone_names = Array(self.context)
		self.bone_pad = PadAlign(self.context, self.bone_names, 4)

	def read(self, stream):
		self.io_start = stream.tell()
		self.bone_hashes = stream.read_uints((self.arg))
		self.bone_names = stream.read_zstrings((self.arg))
		self.bone_pad = stream.read_type(PadAlign, (self.context, self.bone_names, 4))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uints(self.bone_hashes)
		stream.write_zstrings(self.bone_names)
		stream.write_type(self.bone_pad)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Buffer1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* bone_hashes = {self.bone_hashes.__repr__()}'
		s += f'\n	* bone_names = {self.bone_names.__repr__()}'
		s += f'\n	* bone_pad = {self.bone_pad.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
