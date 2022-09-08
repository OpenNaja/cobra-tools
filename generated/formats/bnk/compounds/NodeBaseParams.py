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

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'raw', Array, (0, None, (30,), Byte), (False, None)

	def get_info_str(self, indent=0):
		return f'NodeBaseParams [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
