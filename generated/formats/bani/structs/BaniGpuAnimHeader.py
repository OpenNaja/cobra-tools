from generated.base_struct import BaseStruct
from generated.formats.bani.imports import name_type_map


class BaniGpuAnimHeader(BaseStruct):

	"""
	GPU Anim Header
	PC2: 16 bytes
	"""

	__name__ = 'BaniGpuAnimHeader'

	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# For translation de-quantization
		self.quantization_info = name_type_map['QuantizationInfo'](self.context, 0, None)

		# Packed 24-bit chunk offset and 8-bit bone count
		self.packed_offset_bones = name_type_map['PackedOffsetBones'](self.context, 0, None)

		# Offset in 16-byte chunks to the keyframe block
		self.keyframes_offset = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'quantization_info', name_type_map['QuantizationInfo'], (0, None), (False, None), (None, None)
		yield 'packed_offset_bones', name_type_map['PackedOffsetBones'], (0, None), (False, None), (None, None)
		yield 'keyframes_offset', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'quantization_info', name_type_map['QuantizationInfo'], (0, None), (False, None)
		yield 'packed_offset_bones', name_type_map['PackedOffsetBones'], (0, None), (False, None)
		yield 'keyframes_offset', name_type_map['Uint'], (0, None), (False, None)
