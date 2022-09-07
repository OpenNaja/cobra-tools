import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Vector3(MemStruct):

	"""
	12 bytes
	"""

	__name__ = 'Vector3'

	_import_path = 'generated.formats.trackedridecar.compounds.Vector3'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.floats = Array(self.context, 0, None, (0,), Float)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.floats = numpy.zeros((3,), dtype=numpy.dtype('float32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.floats = Array.from_stream(stream, instance.context, 0, None, (3,), Float)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.floats, instance.context, 0, None, (3,), Float)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'floats', Array, (0, None, (3,), Float), (False, None)

	def get_info_str(self, indent=0):
		return f'Vector3 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
