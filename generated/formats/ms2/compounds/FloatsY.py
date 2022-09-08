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
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'floats', Array, (0, None, (8,), Float), (False, None)
		yield 'index', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'FloatsY [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
