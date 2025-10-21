from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class CompressedManiDataPC2(BaseStruct):

	"""
	in compressed manis
	"""

	__name__ = 'CompressedManiDataPC2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.size = name_type_map['Uint'](self.context, 0, None)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.u_0 = name_type_map['Uint'](self.context, 0, None)
		self.constant = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.bone_count = name_type_map['Uint'](self.context, 0, None)
		self.frame_count = name_type_map['Uint'](self.context, 0, None)
		self.fps = name_type_map['Float'](self.context, 0, None)
		self.unk_float = name_type_map['Float'](self.context, 0, None)
		self.frame_segments_count = name_type_map['Uint'](self.context, 0, None)
		self.u_3 = name_type_map['Uint'](self.context, 0, None)
		self.ori_bone_count = name_type_map['Uint'](self.context, 0, None)
		self.pos_bone_count = name_type_map['Uint'](self.context, 0, None)
		self.scl_bone_count = name_type_map['Ushort'](self.context, 0, None)
		self.morph_bone_count = name_type_map['Ushort'](self.context, 0, None)
		self.unk_count_1 = name_type_map['Uint'](self.context, 0, None)
		self.unk_count_2 = name_type_map['Uint'](self.context, 0, None)
		self.unk_count_3 = name_type_map['Uint'](self.context, 0, None)
		self.ff = name_type_map['Int'](self.context, 0, None)
		self.count = name_type_map['Uint'](self.context, 0, None)
		self.s_1 = name_type_map['Uint'](self.context, 0, None)
		self.s_2 = name_type_map['Uint'](self.context, 0, None)
		self.s_3 = name_type_map['Uint'](self.context, 0, None)
		self.frame_segments = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.ff_2 = name_type_map['Int'](self.context, 0, None)
		self.chunks = Array(self.context, 0, None, (0,), name_type_map['SmallChunk'])
		self.ref_2 = name_type_map['Empty'](self.context, 0, None)
		self.databytes = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.ref_3 = name_type_map['Empty'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'size', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'u_0', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'constant', Array, (0, None, (8,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'bone_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'frame_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'fps', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_float', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'frame_segments_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'u_3', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'ori_bone_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'pos_bone_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'scl_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'morph_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk_count_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_count_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_count_3', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'ff', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 's_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 's_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 's_3', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'frame_segments', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'ff_2', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'chunks', Array, (0, None, (None,), name_type_map['SmallChunk']), (False, None), (None, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'databytes', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'ref_3', name_type_map['Empty'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'size', name_type_map['Uint'], (0, None), (False, None)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'u_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'constant', Array, (0, None, (8,), name_type_map['Ubyte']), (False, None)
		yield 'bone_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'frame_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'fps', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_float', name_type_map['Float'], (0, None), (False, None)
		yield 'frame_segments_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'u_3', name_type_map['Uint'], (0, None), (False, None)
		yield 'ori_bone_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'pos_bone_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'scl_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'morph_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unk_count_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_count_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_count_3', name_type_map['Uint'], (0, None), (False, None)
		yield 'ff', name_type_map['Int'], (0, None), (False, None)
		yield 'count', name_type_map['Uint'], (0, None), (False, None)
		yield 's_1', name_type_map['Uint'], (0, None), (False, None)
		yield 's_2', name_type_map['Uint'], (0, None), (False, None)
		yield 's_3', name_type_map['Uint'], (0, None), (False, None)
		yield 'frame_segments', Array, (0, None, (instance.frame_segments_count,), name_type_map['Uint']), (False, None)
		yield 'ff_2', name_type_map['Int'], (0, None), (False, None)
		yield 'chunks', Array, (0, None, (instance.frame_segments_count,), name_type_map['SmallChunk']), (False, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None)
		yield 'databytes', Array, (0, None, (instance.size - ((instance.ref_2.io_start - instance.ref.io_start) + 4),), name_type_map['Ubyte']), (False, None)
		yield 'ref_3', name_type_map['Empty'], (0, None), (False, None)
