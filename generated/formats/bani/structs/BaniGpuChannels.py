from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bani.imports import name_type_map


class BaniGpuChannels(BaseStruct):

	"""
	Each item creates an animation channel which defines the read/write indices for bones
	PC2: multiples of 32 bytes for each bani, data per bone index
	"""

	__name__ = 'BaniGpuChannels'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = name_type_map['Empty'](self.context, 0, None)
		self.data = Array(self.context, 0, None, (0,), name_type_map['BaniGpuChannelBones'])

		# Non-LOD channels appear to be 32-byte aligned regardless of skeleton size
		self.padding = name_type_map['PadAlign'](self.context, 32, self.ref)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ref', name_type_map['Empty'], (0, None), (False, None), (None, None)
		yield 'data', Array, (0, None, (None,), name_type_map['BaniGpuChannelBones']), (False, None), (None, None)
		yield 'padding', name_type_map['PadAlign'], (32, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', name_type_map['Empty'], (0, None), (False, None)
		yield 'data', Array, (0, None, (instance.arg.packed_offset_bones.num_bones,), name_type_map['BaniGpuChannelBones']), (False, None)
		yield 'padding', name_type_map['PadAlign'], (32, instance.ref), (False, None)
