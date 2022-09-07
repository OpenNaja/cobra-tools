import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort


class MeshCollisionBit(BaseStruct):

	__name__ = 'MeshCollisionBit'

	_import_path = 'generated.formats.ms2.compounds.MeshCollisionBit'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ?
		self.countd = Array(self.context, 0, None, (0,), Ushort)

		# always 2954754766?
		self.consts = Array(self.context, 0, None, (0,), Uint)
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
		Array.to_stream(stream, instance.countd, Ushort)
		Array.to_stream(stream, instance.consts, Uint)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'countd', Array, (0, None, (34,), Ushort), (False, None)
		yield 'consts', Array, (0, None, (3,), Uint), (False, None)

	def get_info_str(self, indent=0):
		return f'MeshCollisionBit [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
