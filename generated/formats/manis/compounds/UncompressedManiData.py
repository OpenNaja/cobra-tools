from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class UncompressedManiData(BaseStruct):

	__name__ = 'UncompressedManiData'


	@property
	def arg_1(self):
		return self.arg[0]
	@property
	def arg_2(self):
		return self.arg[1]

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.pos_bones = Array(self.context, 0, None, (0,), name_type_map['Vector3'])
		self.ori_bones = Array(self.context, 0, None, (0,), name_type_map['Vector4H'])
		self.shr_bones = Array(self.context, 0, None, (0,), name_type_map['Vector2'])
		self.scl_bones = Array(self.context, 0, None, (0,), name_type_map['Vector3'])
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'pos_bones', Array, (0, None, (None, None,), name_type_map['Vector3']), (False, None), (None, None)
		yield 'ori_bones', Array, (0, None, (None, None,), name_type_map['Vector4H']), (False, None), (None, None)
		yield 'shr_bones', Array, (0, None, (None, None,), name_type_map['Vector2']), (False, None), (None, None)
		yield 'scl_bones', Array, (0, None, (None, None,), name_type_map['Vector3']), (False, None), (None, None)
		yield 'floats', Array, (0, None, (None, None,), name_type_map['Float']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pos_bones', Array, (0, None, (instance.arg_2.frame_count, instance.arg_2.pos_bone_count,), name_type_map['Vector3']), (False, None)
		yield 'ori_bones', Array, (0, None, (instance.arg_2.frame_count, instance.arg_2.ori_bone_count,), name_type_map['Vector4H']), (False, None)
		yield 'shr_bones', Array, (0, None, (instance.arg_2.frame_count, instance.arg_2.scl_bone_count,), name_type_map['Vector2']), (False, None)
		yield 'scl_bones', Array, (0, None, (instance.arg_2.frame_count, instance.arg_2.scl_bone_count,), name_type_map['Vector3']), (False, None)
		yield 'floats', Array, (0, None, (instance.arg_2.frame_count, instance.arg_2.float_count,), name_type_map['Float']), (False, None)
