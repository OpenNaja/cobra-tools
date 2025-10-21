from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackelement.imports import name_type_map


class TrackElementRoot(MemStruct):

	"""
	PC: 32 bytes
	"""

	__name__ = 'TrackElementRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.track_data_count = name_type_map['Uint64'](self.context, 0, None)
		self.track_data = name_type_map['ArrayPointer'](self.context, self.track_data_count, name_type_map['TrackElementData'])

		# Used as visual prefab
		self.visual_prefab_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])

		# Used as support prefab
		self.support_prefab_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'track_data', name_type_map['ArrayPointer'], (None, name_type_map['TrackElementData']), (False, None), (None, None)
		yield 'track_data_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'visual_prefab_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'support_prefab_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'track_data', name_type_map['ArrayPointer'], (instance.track_data_count, name_type_map['TrackElementData']), (False, None)
		yield 'track_data_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'visual_prefab_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'support_prefab_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
