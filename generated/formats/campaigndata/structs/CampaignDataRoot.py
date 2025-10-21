from generated.formats.campaigndata.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class CampaignDataRoot(MemStruct):

	__name__ = 'CampaignDataRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.campaign_unknown = name_type_map['Uint64'](self.context, 0, None)
		self.chapter_count = name_type_map['Uint64'](self.context, 0, None)
		self.chapter_unknown = name_type_map['Uint64'](self.context, 0, None)
		self.campaign_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.campaign_description = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.chapter_list = name_type_map['ArrayPointer'](self.context, self.chapter_count, name_type_map['MissionData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'campaign_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'campaign_description', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'campaign_unknown', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'chapter_list', name_type_map['ArrayPointer'], (None, name_type_map['MissionData']), (False, None), (None, None)
		yield 'chapter_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'chapter_unknown', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'campaign_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'campaign_description', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'campaign_unknown', name_type_map['Uint64'], (0, None), (False, None)
		yield 'chapter_list', name_type_map['ArrayPointer'], (instance.chapter_count, name_type_map['MissionData']), (False, None)
		yield 'chapter_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'chapter_unknown', name_type_map['Uint64'], (0, None), (False, None)
