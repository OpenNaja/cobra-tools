from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Locomotion2BlendSpaceNode(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'Locomotion2BlendSpaceNode'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.speed = name_type_map['Float'](self.context, 0, None)
		self.orientation = name_type_map['Float'](self.context, 0, None)
		self.anim_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'anim_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'speed', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'orientation', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'anim_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'speed', name_type_map['Float'], (0, None), (False, None)
		yield 'orientation', name_type_map['Float'], (0, None), (False, None)
