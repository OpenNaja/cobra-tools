from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MotiongraphRootFrag(MemStruct):

	"""
	64 bytes
	"""

	__name__ = 'MotiongraphRootFrag'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_activities = name_type_map['Uint64'](self.context, 0, None)
		self.num_mrf_1 = name_type_map['Uint64'](self.context, 0, None)
		self.num_mrf_2 = name_type_map['Uint64'](self.context, 0, None)
		self.num_xmls = name_type_map['Uint64'](self.context, 0, None)
		self.activities = name_type_map['ArrayPointer'](self.context, self.num_activities, name_type_map['ActivityReference'])
		self.mrf_1 = name_type_map['ArrayPointer'](self.context, self.num_mrf_1, name_type_map['MrfReference1'])
		self.mrf_2 = name_type_map['ArrayPointer'](self.context, self.num_mrf_2, name_type_map['MrfReference2'])
		self.xmls = name_type_map['ArrayPointer'](self.context, self.num_xmls, name_type_map['XMLEntry'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'num_activities', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'activities', name_type_map['ArrayPointer'], (None, name_type_map['ActivityReference']), (False, None), (None, None)
		yield 'num_mrf_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'mrf_1', name_type_map['ArrayPointer'], (None, name_type_map['MrfReference1']), (False, None), (None, None)
		yield 'num_mrf_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'mrf_2', name_type_map['ArrayPointer'], (None, name_type_map['MrfReference2']), (False, None), (None, None)
		yield 'num_xmls', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'xmls', name_type_map['ArrayPointer'], (None, name_type_map['XMLEntry']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'num_activities', name_type_map['Uint64'], (0, None), (False, None)
		yield 'activities', name_type_map['ArrayPointer'], (instance.num_activities, name_type_map['ActivityReference']), (False, None)
		yield 'num_mrf_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'mrf_1', name_type_map['ArrayPointer'], (instance.num_mrf_1, name_type_map['MrfReference1']), (False, None)
		yield 'num_mrf_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'mrf_2', name_type_map['ArrayPointer'], (instance.num_mrf_2, name_type_map['MrfReference2']), (False, None)
		yield 'num_xmls', name_type_map['Uint64'], (0, None), (False, None)
		yield 'xmls', name_type_map['ArrayPointer'], (instance.num_xmls, name_type_map['XMLEntry']), (False, None)
