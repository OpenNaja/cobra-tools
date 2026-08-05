from generated.base_struct import BaseStruct
from generated.formats.bani.imports import name_type_map


class BaniGpuChannelBones(BaseStruct):

	"""
	WRITE non-255, READ     255 === Normal Channel
	WRITE non-255, READ non-255 === Channel Group, bone(s) are reusing a parent bone's transform
	WRITE     255, READ     255 === Skip Channel, bone(s) are not being animated at all
	PC2: 2 bytes
	"""

	__name__ = 'BaniGpuChannelBones'

	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Bone write index. 0xFF = None/Sentinel
		self.write_index = name_type_map['Ubyte'](self.context, 0, None)

		# Parent read index. 0xFF = None/Sentinel
		self.read_index = name_type_map['Ubyte'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'write_index', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'read_index', name_type_map['Ubyte'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'write_index', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'read_index', name_type_map['Ubyte'], (0, None), (False, None)
