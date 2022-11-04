import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte


class DLAPreBones(BaseStruct):

	__name__ = 'DLAPreBones'

	_import_key = 'ms2.compounds.DLAPreBones'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk = Array(self.context, 0, None, (0,), Ubyte)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('unk', Array, (0, None, (120,), Ubyte), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk', Array, (0, None, (120,), Ubyte), (False, None)
