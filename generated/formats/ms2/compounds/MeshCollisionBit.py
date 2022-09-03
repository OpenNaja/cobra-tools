import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort


class MeshCollisionBit(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ?
		self.countd = Array((0,), Ushort, self.context, 0, None)

		# always 2954754766?
		self.consts = Array((0,), Uint, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.countd = numpy.zeros((34,), dtype=numpy.dtype('uint16'))
		self.consts = numpy.zeros((3,), dtype=numpy.dtype('uint32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.countd = Array.from_stream(stream, instance.context, 0, None, (34,), Ushort)
		instance.consts = Array.from_stream(stream, instance.context, 0, None, (3,), Uint)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.countd, (34,), Ushort, instance.context, 0, None)
		Array.to_stream(stream, instance.consts, (3,), Uint, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'countd', Array, ((34,), Ushort, 0, None), (False, None)
		yield 'consts', Array, ((3,), Uint, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'MeshCollisionBit [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* countd = {self.fmt_member(self.countd, indent+1)}'
		s += f'\n	* consts = {self.fmt_member(self.consts, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
