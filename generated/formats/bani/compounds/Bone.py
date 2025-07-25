from generated.base_struct import BaseStruct
from generated.formats.bani.imports import name_type_map


class Bone(BaseStruct):

	"""
	PC2: 12 bytes
	"""

	__name__ = 'Bone'

	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.rot = name_type_map['Vector3Short'](self.context, 0, None)
		self.loc = name_type_map['Vector3Ushort'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'rot', name_type_map['Vector3Short'], (0, None), (False, None), (None, None)
		yield 'loc', name_type_map['Vector3Ushort'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'rot', name_type_map['Vector3Short'], (0, None), (False, None)
		yield 'loc', name_type_map['Vector3Ushort'], (0, None), (False, None)
