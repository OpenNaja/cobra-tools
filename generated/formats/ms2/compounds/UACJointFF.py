import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint


class UACJointFF(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# must be 11
		self.eleven = 0

		# bunch of -1's, and constants
		self.f_fs = numpy.zeros((4,), dtype=numpy.dtype('int32'))
		self.name_offset = 0
		self.hitcheck_count = 0

		# 12 bytes of zeros
		self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.eleven = 0
		self.f_fs = numpy.zeros((4,), dtype=numpy.dtype('int32'))
		self.name_offset = 0
		self.hitcheck_count = 0
		self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint32'))

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
		instance.eleven = stream.read_uint()
		instance.f_fs = stream.read_ints((4,))
		instance.name_offset = stream.read_uint()
		instance.hitcheck_count = stream.read_uint()
		instance.zeros = stream.read_uints((3,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.eleven)
		stream.write_ints(instance.f_fs)
		stream.write_uint(instance.name_offset)
		stream.write_uint(instance.hitcheck_count)
		stream.write_uints(instance.zeros)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'eleven', Uint, (0, None)
		yield 'f_fs', Array, ((4,), Int, 0, None)
		yield 'name_offset', Uint, (0, None)
		yield 'hitcheck_count', Uint, (0, None)
		yield 'zeros', Array, ((3,), Uint, 0, None)

	def get_info_str(self, indent=0):
		return f'UACJointFF [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* eleven = {self.fmt_member(self.eleven, indent+1)}'
		s += f'\n	* f_fs = {self.fmt_member(self.f_fs, indent+1)}'
		s += f'\n	* name_offset = {self.fmt_member(self.name_offset, indent+1)}'
		s += f'\n	* hitcheck_count = {self.fmt_member(self.hitcheck_count, indent+1)}'
		s += f'\n	* zeros = {self.fmt_member(self.zeros, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
