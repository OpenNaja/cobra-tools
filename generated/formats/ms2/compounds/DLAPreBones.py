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

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk', Array, (0, None, (120,), Ubyte), (False, None)

	def get_info_str(self, indent=0):
		return f'DLAPreBones [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
