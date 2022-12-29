import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.manis.compounds.Vector3 import Vector3
from generated.formats.manis.compounds.Vector4H import Vector4H
from generated.formats.ovl_base.compounds.Empty import Empty


class UncompressedManiData(BaseStruct):

	__name__ = 'UncompressedManiData'

	_import_key = 'manis.compounds.UncompressedManiData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = Empty(self.context, 0, None)
		self.pos_keys = Array(self.context, 0, None, (0,), Vector3)
		self.unk_array_1 = Array(self.context, 0, None, (0,), Vector4H)
		self.unk_array_2 = Array(self.context, 0, None, (0,), Float)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('ref', Empty, (0, None), (False, None), None),
		('pos_keys', Array, (0, None, (None, None,), Vector3), (False, None), True),
		('unk_array_1', Array, (0, None, (None, None,), Vector4H), (False, None), True),
		('unk_array_2', Array, (0, None, (None, None,), Float), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', Empty, (0, None), (False, None)
		if instance.arg.pos_bone_count > 0:
			yield 'pos_keys', Array, (0, None, (instance.arg.pos_bone_count, instance.arg.frame_count,), Vector3), (False, None)
		if instance.arg.ori_bone_count > 0:
			yield 'unk_array_1', Array, (0, None, (instance.arg.ori_bone_count, instance.arg.frame_count,), Vector4H), (False, None)
		if instance.arg.float_count > 0:
			yield 'unk_array_2', Array, (0, None, (instance.arg.float_count, instance.arg.frame_count,), Float), (False, None)
