import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Short


class MinusPadding(BaseStruct):

	"""
	Used in PC
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# -1
		self.indices = 0

		# 0
		self.padding = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.indices = numpy.zeros((self.arg,), dtype=numpy.dtype('int16'))
		self.padding = numpy.zeros(((16 - ((self.arg * 2) % 16)) % 16,), dtype=numpy.dtype('int8'))

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.indices = stream.read_shorts((instance.arg,))
		instance.padding = stream.read_bytes(((16 - ((instance.arg * 2) % 16)) % 16,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_shorts(instance.indices)
		stream.write_bytes(instance.padding)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('indices', Array, ((instance.arg,), Short, 0, None))
		yield ('padding', Array, (((16 - ((instance.arg * 2) % 16)) % 16,), Byte, 0, None))

	def get_info_str(self, indent=0):
		return f'MinusPadding [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* indices = {self.fmt_member(self.indices, indent+1)}'
		s += f'\n	* padding = {self.fmt_member(self.padding, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
