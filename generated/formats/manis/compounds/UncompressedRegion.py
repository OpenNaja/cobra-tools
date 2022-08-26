import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort


class UncompressedRegion(BaseStruct):

	__name__ = 'UncompressedRegion'

	_import_path = 'generated.formats.manis.compounds.UncompressedRegion'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros_0 = Array((0,), Uint, self.context, 0, None)
		self.unk_0 = 0
		self.unk_1 = 0
		self.zeros_1 = Array((0,), Uint, self.context, 0, None)
		self.unk_2 = 0
		self.unk_3 = 0
		self.zeros_2 = Array((0,), Uint, self.context, 0, None)
		self.unk_4 = 0
		self.unk_5 = 0
		self.zeros_3 = Array((0,), Uint, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zeros_0 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		self.unk_0 = 0
		self.unk_1 = 0
		self.zeros_1 = numpy.zeros((3,), dtype=numpy.dtype('uint32'))
		self.unk_2 = 0
		self.unk_3 = 0
		self.zeros_2 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		self.unk_4 = 0
		self.unk_5 = 0
		self.zeros_3 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zeros_0 = Array.from_stream(stream, instance.context, 0, None, (2,), Uint)
		instance.unk_0 = Ushort.from_stream(stream, instance.context, 0, None)
		instance.unk_1 = Ushort.from_stream(stream, instance.context, 0, None)
		instance.zeros_1 = Array.from_stream(stream, instance.context, 0, None, (3,), Uint)
		instance.unk_2 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_3 = Uint.from_stream(stream, instance.context, 0, None)
		instance.zeros_2 = Array.from_stream(stream, instance.context, 0, None, (2,), Uint)
		instance.unk_4 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_5 = Uint.from_stream(stream, instance.context, 0, None)
		instance.zeros_3 = Array.from_stream(stream, instance.context, 0, None, (2,), Uint)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.zeros_0, (2,), Uint, instance.context, 0, None)
		Ushort.to_stream(stream, instance.unk_0)
		Ushort.to_stream(stream, instance.unk_1)
		Array.to_stream(stream, instance.zeros_1, (3,), Uint, instance.context, 0, None)
		Uint.to_stream(stream, instance.unk_2)
		Uint.to_stream(stream, instance.unk_3)
		Array.to_stream(stream, instance.zeros_2, (2,), Uint, instance.context, 0, None)
		Uint.to_stream(stream, instance.unk_4)
		Uint.to_stream(stream, instance.unk_5)
		Array.to_stream(stream, instance.zeros_3, (2,), Uint, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'zeros_0', Array, ((2,), Uint, 0, None), (False, None)
		yield 'unk_0', Ushort, (0, None), (False, None)
		yield 'unk_1', Ushort, (0, None), (False, None)
		yield 'zeros_1', Array, ((3,), Uint, 0, None), (False, None)
		yield 'unk_2', Uint, (0, None), (False, None)
		yield 'unk_3', Uint, (0, None), (False, None)
		yield 'zeros_2', Array, ((2,), Uint, 0, None), (False, None)
		yield 'unk_4', Uint, (0, None), (False, None)
		yield 'unk_5', Uint, (0, None), (False, None)
		yield 'zeros_3', Array, ((2,), Uint, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'UncompressedRegion [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zeros_0 = {self.fmt_member(self.zeros_0, indent+1)}'
		s += f'\n	* unk_0 = {self.fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* unk_1 = {self.fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* zeros_1 = {self.fmt_member(self.zeros_1, indent+1)}'
		s += f'\n	* unk_2 = {self.fmt_member(self.unk_2, indent+1)}'
		s += f'\n	* unk_3 = {self.fmt_member(self.unk_3, indent+1)}'
		s += f'\n	* zeros_2 = {self.fmt_member(self.zeros_2, indent+1)}'
		s += f'\n	* unk_4 = {self.fmt_member(self.unk_4, indent+1)}'
		s += f'\n	* unk_5 = {self.fmt_member(self.unk_5, indent+1)}'
		s += f'\n	* zeros_3 = {self.fmt_member(self.zeros_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
