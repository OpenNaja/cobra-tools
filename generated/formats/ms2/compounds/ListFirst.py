import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.ms2.compounds.Descriptor import Descriptor


class ListFirst(Descriptor):

	__name__ = 'ListFirst'

	_import_path = 'generated.formats.ms2.compounds.ListFirst'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.floats = Array(self.context, 0, None, (0,), Float)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'floats', Array, (0, None, (3,), Float), (False, None)

	def get_info_str(self, indent=0):
		return f'ListFirst [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
