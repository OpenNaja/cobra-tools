from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class TriggeredActivityActivityData(MemStruct):

	"""
	differs by game version
	"""

	__name__ = 'TriggeredActivityActivityData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.blend_in_time = name_type_map['Float'](self.context, 0, None)
		self.blend_out_time = name_type_map['Float'](self.context, 0, None)
		self.m_auto_start = name_type_map['Ubyte'].from_value(0)
		self.m_allow_restart = name_type_map['Ubyte'].from_value(0)
		self.m_allow_mortal = name_type_map['Ubyte'].from_value(0)
		self.trigger = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.activity = name_type_map['Pointer'](self.context, 0, name_type_map['Activity'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'trigger', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'activity', name_type_map['Pointer'], (0, name_type_map['Activity']), (False, None), (None, None)
		yield 'blend_in_time', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'blend_out_time', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'm_auto_start', name_type_map['Ubyte'], (0, None), (False, 0), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)
		yield 'm_allow_restart', name_type_map['Ubyte'], (0, None), (False, 0), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)
		yield 'm_allow_mortal', name_type_map['Ubyte'], (0, None), (False, 0), (lambda context: not ((not context.user_version.use_djb) and (context.version >= 19)), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'trigger', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'activity', name_type_map['Pointer'], (0, name_type_map['Activity']), (False, None)
		yield 'blend_in_time', name_type_map['Float'], (0, None), (False, None)
		yield 'blend_out_time', name_type_map['Float'], (0, None), (False, None)
		if not ((not instance.context.user_version.use_djb) and (instance.context.version >= 19)):
			yield 'm_auto_start', name_type_map['Ubyte'], (0, None), (False, 0)
			yield 'm_allow_restart', name_type_map['Ubyte'], (0, None), (False, 0)
			yield 'm_allow_mortal', name_type_map['Ubyte'], (0, None), (False, 0)
