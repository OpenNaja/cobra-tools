from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class ManiBlock(BaseStruct):

	__name__ = 'ManiBlock'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.pos_bones = Array(self.context, 0, None, (0,), name_type_map['Channelname'])
		self.ori_bones = Array(self.context, 0, None, (0,), name_type_map['Channelname'])
		self.scl_bones = Array(self.context, 0, None, (0,), name_type_map['Channelname'])
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Channelname'])
		self.pos_bones_p = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.ori_bones_p = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.scl_bones_p = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.pos_bones_delta = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.ori_bones_delta = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.scl_bones_delta = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.pad = name_type_map['PadAlign'](self.context, 4, self.ref)
		self.key_data = name_type_map['CompressedManiData'](self.context, self.arg, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'pos_bones', Array, (0, None, (None,), name_type_map['Channelname']), (False, None), (None, None)
		yield 'ori_bones', Array, (0, None, (None,), name_type_map['Channelname']), (False, None), (None, None)
		yield 'scl_bones', Array, (0, None, (None,), name_type_map['Channelname']), (False, None), (None, None)
		yield 'floats', Array, (0, None, (None,), name_type_map['Channelname']), (False, None), (None, None)
		yield 'pos_bones_p', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'ori_bones_p', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'scl_bones_p', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'pos_bones_delta', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, True)
		yield 'ori_bones_delta', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, True)
		yield 'scl_bones_delta', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, True)
		yield 'pad', name_type_map['PadAlign'], (4, None), (False, None), (None, None)
		yield 'key_data', name_type_map['UncompressedManiData'], (None, None), (False, None), (None, True)
		yield 'key_data', name_type_map['CompressedManiData'], (None, None), (False, None), (None, True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'pos_bones', Array, (0, None, (instance.arg.pos_bone_count,), name_type_map['Channelname']), (False, None)
		yield 'ori_bones', Array, (0, None, (instance.arg.ori_bone_count,), name_type_map['Channelname']), (False, None)
		yield 'scl_bones', Array, (0, None, (instance.arg.scl_bone_count,), name_type_map['Channelname']), (False, None)
		yield 'floats', Array, (0, None, (instance.arg.float_count,), name_type_map['Channelname']), (False, None)
		yield 'pos_bones_p', Array, (0, None, (instance.arg.pos_bone_count,), name_type_map['Ubyte']), (False, None)
		yield 'ori_bones_p', Array, (0, None, (instance.arg.ori_bone_count,), name_type_map['Ubyte']), (False, None)
		yield 'scl_bones_p', Array, (0, None, (instance.arg.scl_bone_count,), name_type_map['Ubyte']), (False, None)
		if instance.arg.pos_bone_min >= 0:
			yield 'pos_bones_delta', Array, (0, None, ((instance.arg.pos_bone_max - instance.arg.pos_bone_min) + 1,), name_type_map['Ubyte']), (False, None)
		if instance.arg.ori_bone_min >= 0:
			yield 'ori_bones_delta', Array, (0, None, ((instance.arg.ori_bone_max - instance.arg.ori_bone_min) + 1,), name_type_map['Ubyte']), (False, None)
		if instance.arg.scl_bone_min >= 0:
			yield 'scl_bones_delta', Array, (0, None, ((instance.arg.scl_bone_max - instance.arg.scl_bone_min) + 1,), name_type_map['Ubyte']), (False, None)
		yield 'pad', name_type_map['PadAlign'], (4, instance.ref), (False, None)
		if instance.arg.b == 0:
			yield 'key_data', name_type_map['UncompressedManiData'], (instance.arg, None), (False, None)
		if instance.arg.b > 0:
			yield 'key_data', name_type_map['CompressedManiData'], (instance.arg, None), (False, None)
