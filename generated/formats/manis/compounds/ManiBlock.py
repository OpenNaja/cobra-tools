import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.manis.compounds.CompressedManiData import CompressedManiData
from generated.formats.manis.compounds.UncompressedManiData import UncompressedManiData
from generated.formats.ovl_base.compounds.Empty import Empty


class ManiBlock(BaseStruct):

	__name__ = 'ManiBlock'

	_import_key = 'manis.compounds.ManiBlock'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = Empty(self.context, 0, None)
		self.pos_bones = Array(self.context, 0, None, (0,), Uint)
		self.ori_bones = Array(self.context, 0, None, (0,), Uint)
		self.scl_bones = Array(self.context, 0, None, (0,), Uint)
		self.floats = Array(self.context, 0, None, (0,), Uint)
		self.pos_bones_p = Array(self.context, 0, None, (0,), Ubyte)
		self.ori_bones_p = Array(self.context, 0, None, (0,), Ubyte)
		self.scl_bones_p = Array(self.context, 0, None, (0,), Ubyte)
		self.pos_bones_delta = Array(self.context, 0, None, (0,), Ubyte)
		self.ori_bones_delta = Array(self.context, 0, None, (0,), Ubyte)
		self.scl_bones_delta = Array(self.context, 0, None, (0,), Ubyte)
		self.pad = PadAlign(self.context, 4, self.ref)
		self.key_data = CompressedManiData(self.context, self.arg, None)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('ref', Empty, (0, None), (False, None), None),
		('pos_bones', Array, (0, None, (None,), Ushort), (False, None), True),
		('pos_bones', Array, (0, None, (None,), Uint), (False, None), True),
		('ori_bones', Array, (0, None, (None,), Ushort), (False, None), True),
		('ori_bones', Array, (0, None, (None,), Uint), (False, None), True),
		('scl_bones', Array, (0, None, (None,), Ushort), (False, None), True),
		('scl_bones', Array, (0, None, (None,), Uint), (False, None), True),
		('floats', Array, (0, None, (None,), Ushort), (False, None), True),
		('floats', Array, (0, None, (None,), Uint), (False, None), True),
		('pos_bones_p', Array, (0, None, (None,), Ubyte), (False, None), None),
		('ori_bones_p', Array, (0, None, (None,), Ubyte), (False, None), None),
		('scl_bones_p', Array, (0, None, (None,), Ubyte), (False, None), None),
		('pos_bones_delta', Array, (0, None, (None,), Ubyte), (False, None), True),
		('ori_bones_delta', Array, (0, None, (None,), Ubyte), (False, None), True),
		('scl_bones_delta', Array, (0, None, (None,), Ubyte), (False, None), True),
		('pad', PadAlign, (4, None), (False, None), None),
		('key_data', UncompressedManiData, (None, None), (False, None), True),
		('key_data', CompressedManiData, (None, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', Empty, (0, None), (False, None)
		if instance.context.version <= 257:
			yield 'pos_bones', Array, (0, None, (instance.arg.pos_bone_count,), Ushort), (False, None)
		if instance.context.version >= 258:
			yield 'pos_bones', Array, (0, None, (instance.arg.pos_bone_count,), Uint), (False, None)
		if instance.context.version <= 257:
			yield 'ori_bones', Array, (0, None, (instance.arg.ori_bone_count,), Ushort), (False, None)
		if instance.context.version >= 258:
			yield 'ori_bones', Array, (0, None, (instance.arg.ori_bone_count,), Uint), (False, None)
		if instance.context.version <= 257:
			yield 'scl_bones', Array, (0, None, (instance.arg.scl_bone_count,), Ushort), (False, None)
		if instance.context.version >= 258:
			yield 'scl_bones', Array, (0, None, (instance.arg.scl_bone_count,), Uint), (False, None)
		if instance.context.version <= 257:
			yield 'floats', Array, (0, None, (instance.arg.float_count,), Ushort), (False, None)
		if instance.context.version >= 258:
			yield 'floats', Array, (0, None, (instance.arg.float_count,), Uint), (False, None)
		yield 'pos_bones_p', Array, (0, None, (instance.arg.pos_bone_count,), Ubyte), (False, None)
		yield 'ori_bones_p', Array, (0, None, (instance.arg.ori_bone_count,), Ubyte), (False, None)
		yield 'scl_bones_p', Array, (0, None, (instance.arg.scl_bone_count,), Ubyte), (False, None)
		if instance.arg.pos_bone_min >= 0:
			yield 'pos_bones_delta', Array, (0, None, ((instance.arg.pos_bone_max - instance.arg.pos_bone_min) + 1,), Ubyte), (False, None)
		if instance.arg.ori_bone_min >= 0:
			yield 'ori_bones_delta', Array, (0, None, ((instance.arg.ori_bone_max - instance.arg.ori_bone_min) + 1,), Ubyte), (False, None)
		if instance.arg.scl_bone_min >= 0:
			yield 'scl_bones_delta', Array, (0, None, ((instance.arg.scl_bone_max - instance.arg.scl_bone_min) + 1,), Ubyte), (False, None)
		yield 'pad', PadAlign, (4, instance.ref), (False, None)
		if instance.arg.b == 0:
			yield 'key_data', UncompressedManiData, (instance.arg, None), (False, None)
		if instance.arg.b > 0:
			yield 'key_data', CompressedManiData, (instance.arg, None), (False, None)
