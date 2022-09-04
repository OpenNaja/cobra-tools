import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte


class DLAPreBones(BaseStruct):

	__name__ = 'DLAPreBones'

	_import_path = 'generated.formats.ms2.compounds.DLAPreBones'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk = Array(self.context, 0, None, (0,), Ubyte)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk = numpy.zeros((120,), dtype=numpy.dtype('uint8'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.unk = Array.from_stream(stream, instance.context, 0, None, (120,), Ubyte)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.unk, instance.context, 0, None, (120,), Ubyte)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'unk', Array, (0, None, (120,), Ubyte), (False, None)

	def get_info_str(self, indent=0):
		return f'DLAPreBones [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
