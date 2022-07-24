from generated.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.formats.base.basic import Ushort
from generated.struct import StructBase


class InfoZTMemPool(StructBase):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# ?
		self.unk_count = 0

		# ?
		self.unks = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.unk_count = 0
		self.unks = numpy.zeros((self.unk_count, 2,), dtype=numpy.dtype('uint16'))

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
		instance.unk_count = stream.read_ushort()
		instance.unks = stream.read_ushorts((instance.unk_count, 2,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_ushort(instance.unk_count)
		stream.write_ushorts(instance.unks)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('unk_count', Ushort, (0, None))
		yield ('unks', Array, ((instance.unk_count, 2,), Ushort, 0, None))

	def get_info_str(self, indent=0):
		return f'InfoZTMemPool [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk_count = {fmt_member(self.unk_count, indent+1)}'
		s += f'\n	* unks = {fmt_member(self.unks, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
