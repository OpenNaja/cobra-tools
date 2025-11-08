from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FootPlantActivityData(MemStruct):

	"""
	differs by game
	PZ 40 bytes
	"""

	__name__ = 'FootPlantActivityData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.flags = name_type_map['Uint64'](self.context, 0, None)
		self.weight = name_type_map['FloatInputData'](self.context, 0, None)
		self.rotation_no_i_k_weight = name_type_map['FloatInputData'](self.context, 0, None)
		self.sticky_feet_weight = name_type_map['FloatInputData'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'flags', name_type_map['Uint64'], (0, None), (False, None), (lambda context: (not context.user_version.use_djb) and (context.version >= 19), None)
		yield 'weight', name_type_map['FloatInputData'], (0, None), (False, None), (None, None)
		yield 'rotation_no_i_k_weight', name_type_map['FloatInputData'], (0, None), (False, None), (None, None)
		yield 'sticky_feet_weight', name_type_map['FloatInputData'], (0, None), (False, None), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if (not instance.context.user_version.use_djb) and (instance.context.version >= 19):
			yield 'flags', name_type_map['Uint64'], (0, None), (False, None)
		yield 'weight', name_type_map['FloatInputData'], (0, None), (False, None)
		yield 'rotation_no_i_k_weight', name_type_map['FloatInputData'], (0, None), (False, None)
		if not ((not instance.context.user_version.use_djb) and (instance.context.version >= 19)):
			yield 'sticky_feet_weight', name_type_map['FloatInputData'], (0, None), (False, None)
