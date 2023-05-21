from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class CompressedManiData(BaseStruct):

	__name__ = 'CompressedManiData'


	@property
	def arg_1(self):
		return self.arg[0]
	@property
	def arg_2(self):
		return self.arg[1]

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# uncompressed, possibly because ACL didn't support scalars
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.uncompressed_pad = name_type_map['PadAlign'](self.context, 16, self.arg_1.ref)
		self.frame_count = name_type_map['Uint'](self.context, 0, None)
		self.ori_bone_count = name_type_map['Uint'](self.context, 0, None)
		self.pos_bone_count = name_type_map['Uint'](self.context, 0, None)
		self.scl_bone_count = name_type_map['Ushort'](self.context, 0, None)
		self.morph_bone_count = name_type_map['Ushort'](self.context, 0, None)

		# fixed
		self.zeros_18 = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.scale_min = name_type_map['Vector3'](self.context, 0, None)
		self.scale_max = name_type_map['Vector3'](self.context, 0, None)

		# fixed
		self.zeros_4 = Array(self.context, 0, None, (0,), name_type_map['Uint'])

		# counts temporal segments
		self.segment_count = name_type_map['Ushort'](self.context, 0, None)

		# usually 420 or 52905
		self.quantisation_level = name_type_map['Ushort'](self.context, 0, None)
		self.ref_2 = name_type_map['Empty'](self.context, 0, None)
		self.some_indices = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.flag_0 = name_type_map['Ubyte'](self.context, 0, None)
		self.flag_1 = name_type_map['Ubyte'](self.context, 0, None)
		self.flag_2 = name_type_map['Ubyte'](self.context, 0, None)
		self.flag_3 = name_type_map['Ubyte'](self.context, 0, None)
		self.anoth_pad = name_type_map['PadAlign'](self.context, 4, self.ref_2)
		self.loc_min = name_type_map['Vector3'](self.context, 0, None)
		self.loc_max = name_type_map['Vector3'](self.context, 0, None)

		# not sure
		self.loc_related_floats = name_type_map['FloatsGrabber'](self.context, 0, None)
		self.anoth_pad_2 = name_type_map['PadAlign'](self.context, 16, self.arg_1.ref)

		# give the byte size of the various temporal segments
		self.segments = Array(self.context, 0, None, (0,), name_type_map['Repeat'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'floats', Array, (0, None, (None, None,), name_type_map['Float']), (False, None), (None, None)
		yield 'uncompressed_pad', name_type_map['PadAlign'], (16, None), (False, None), (None, None)
		yield 'frame_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'ori_bone_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'pos_bone_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'scl_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'morph_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'zeros_18', Array, (0, None, (8,), name_type_map['Uint']), (False, None), (None, None)
		yield 'scale_min', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'scale_max', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'zeros_4', Array, (0, None, (4,), name_type_map['Uint']), (False, None), (None, None)
		yield 'segment_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'quantisation_level', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'some_indices', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'flag_0', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'flag_1', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'flag_2', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'flag_3', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'anoth_pad', name_type_map['PadAlign'], (4, None), (False, None), (None, None)
		yield 'loc_min', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'loc_max', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'loc_related_floats', name_type_map['FloatsGrabber'], (0, None), (False, None), (None, None)
		yield 'anoth_pad_2', name_type_map['PadAlign'], (16, None), (False, None), (None, None)
		yield 'segments', Array, (0, None, (None,), name_type_map['Repeat']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'floats', Array, (0, None, (instance.arg_2.frame_count, instance.arg_2.float_count,), name_type_map['Float']), (False, None)
		yield 'uncompressed_pad', name_type_map['PadAlign'], (16, instance.arg_1.ref), (False, None)
		yield 'frame_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'ori_bone_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'pos_bone_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'scl_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'morph_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zeros_18', Array, (0, None, (8,), name_type_map['Uint']), (False, None)
		yield 'scale_min', name_type_map['Vector3'], (0, None), (False, None)
		yield 'scale_max', name_type_map['Vector3'], (0, None), (False, None)
		yield 'zeros_4', Array, (0, None, (4,), name_type_map['Uint']), (False, None)
		yield 'segment_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'quantisation_level', name_type_map['Ushort'], (0, None), (False, None)
		yield 'ref_2', name_type_map['Empty'], (0, None), (False, None)
		yield 'some_indices', Array, (0, None, (instance.pos_bone_count,), name_type_map['Ubyte']), (False, None)
		yield 'flag_0', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'flag_1', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'flag_2', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'flag_3', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'anoth_pad', name_type_map['PadAlign'], (4, instance.ref_2), (False, None)
		yield 'loc_min', name_type_map['Vector3'], (0, None), (False, None)
		yield 'loc_max', name_type_map['Vector3'], (0, None), (False, None)
		yield 'loc_related_floats', name_type_map['FloatsGrabber'], (0, None), (False, None)
		yield 'anoth_pad_2', name_type_map['PadAlign'], (16, instance.arg_1.ref), (False, None)
		yield 'segments', Array, (0, None, (instance.segment_count,), name_type_map['Repeat']), (False, None)
