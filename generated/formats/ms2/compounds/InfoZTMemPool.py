import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ushort


class InfoZTMemPool(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ?
		self.unk_count = 0

		# ?
		self.unks = Array((0,), Ushort, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk_count = 0
		self.unks = numpy.zeros((self.unk_count, 2,), dtype=numpy.dtype('uint16'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.unk_count = Ushort.from_stream(stream, instance.context, 0, None)
		instance.unks = Array.from_stream(stream, instance.context, 0, None, (instance.unk_count, 2,), Ushort)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Ushort.to_stream(stream, instance.unk_count)
		Array.to_stream(stream, instance.unks, (instance.unk_count, 2,), Ushort, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'unk_count', Ushort, (0, None), (False, None)
		yield 'unks', Array, ((instance.unk_count, 2,), Ushort, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'InfoZTMemPool [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk_count = {self.fmt_member(self.unk_count, indent+1)}'
		s += f'\n	* unks = {self.fmt_member(self.unks, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
