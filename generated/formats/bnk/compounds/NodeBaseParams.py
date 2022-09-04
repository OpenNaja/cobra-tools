import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte


class NodeBaseParams(BaseStruct):

	__name__ = 'NodeBaseParams'

	_import_path = 'generated.formats.bnk.compounds.NodeBaseParams'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.raw = Array(self.context, 0, None, (0,), Byte)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.raw = numpy.zeros((30,), dtype=numpy.dtype('int8'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.raw = Array.from_stream(stream, instance.context, 0, None, (30,), Byte)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.raw, instance.context, 0, None, (30,), Byte)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'raw', Array, (0, None, (30,), Byte), (False, None)

	def get_info_str(self, indent=0):
		return f'NodeBaseParams [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
