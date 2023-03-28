import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.manis.compounds.Vector3 import Vector3
from generated.formats.manis.compounds.Vector4H import Vector4H


class UncompressedManiData(BaseStruct):

	__name__ = 'UncompressedManiData'

	_import_key = 'manis.compounds.UncompressedManiData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.pos_bones = Array(self.context, 0, None, (0,), Vector3)
		self.ori_bones = Array(self.context, 0, None, (0,), Vector4H)
		self.floats = Array(self.context, 0, None, (0,), Float)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('pos_bones', Array, (0, None, (None, None,), Vector3), (False, None), (None, None))
		yield ('ori_bones', Array, (0, None, (None, None,), Vector4H), (False, None), (None, None))
		yield ('floats', Array, (0, None, (None, None,), Float), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pos_bones', Array, (0, None, (instance.arg.pos_bone_count, instance.arg.frame_count,), Vector3), (False, None)
		yield 'ori_bones', Array, (0, None, (instance.arg.ori_bone_count, instance.arg.frame_count,), Vector4H), (False, None)
		yield 'floats', Array, (0, None, (instance.arg.float_count, instance.arg.frame_count,), Float), (False, None)


UncompressedManiData.init_attributes()
