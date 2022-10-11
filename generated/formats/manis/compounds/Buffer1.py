import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.base.compounds.PadAlign import PadAlign


class Buffer1(BaseStruct):

	__name__ = 'Buffer1'

	_import_key = 'manis.compounds.Buffer1'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.bone_hashes = Array(self.context, 0, None, (0,), Uint)
		self.bone_names = Array(self.context, 0, None, (0,), ZString)

		# ?
		self.bone_pad = PadAlign(self.context, 4, self.bone_names)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('bone_hashes', Array, (0, None, (None,), Uint), (False, None), None),
		('bone_names', Array, (0, None, (None,), ZString), (False, None), None),
		('bone_pad', PadAlign, (4, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'bone_hashes', Array, (0, None, (instance.arg,), Uint), (False, None)
		yield 'bone_names', Array, (0, None, (instance.arg,), ZString), (False, None)
		yield 'bone_pad', PadAlign, (4, instance.bone_names), (False, None)
