import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint


class FloatsY(BaseStruct):

	__name__ = 'FloatsY'

	_import_path = 'generated.formats.ms2.compounds.FloatsY'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.floats = Array(self.context, 0, None, (0,), Float)
		self.index = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.floats = numpy.zeros((8,), dtype=numpy.dtype('float32'))
		self.index = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.floats = Array.from_stream(stream, instance.context, 0, None, (8,), Float)
		instance.index = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.floats, instance.context, 0, None, (8,), Float)
		Uint.to_stream(stream, instance.index)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'floats', Array, (0, None, (8,), Float), (False, None)
		yield 'index', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'FloatsY [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
