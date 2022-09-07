import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ushort


class InfoZTMemPool(BaseStruct):

	__name__ = 'InfoZTMemPool'

	_import_path = 'generated.formats.ms2.compounds.InfoZTMemPool'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ?
		self.unk_count = 0

		# ?
		self.unks = Array(self.context, 0, None, (0,), Ushort)
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
		Array.to_stream(stream, instance.unks, instance.context, 0, None, (instance.unk_count, 2,), Ushort)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_count', Ushort, (0, None), (False, None)
		yield 'unks', Array, (0, None, (instance.unk_count, 2,), Ushort), (False, None)

	def get_info_str(self, indent=0):
		return f'InfoZTMemPool [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
