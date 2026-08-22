import logging
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.motiongraph.imports import name_type_map

from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Activity(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'Activity'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# rarely used
		self.num_sub_activities = name_type_map['Uint'].from_value(0)

		# only seen in sub-activities
		self.num_other_activities = name_type_map['Uint'].from_value(0)
		self.index_a = name_type_map['Int'].from_value(-1)
		self.index_b = name_type_map['Int'].from_value(-1)
		self.data_type = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])

		# template has to be defined according to data type ie 'AnimationActivity' + 'Data'
		self.data = name_type_map['Pointer'](self.context, 0, None)
		self.sub_activities = name_type_map['ArrayPointer'](self.context, self.num_sub_activities, name_type_map['ActivityReference'])
		self.other_activities = name_type_map['ArrayPointer'](self.context, self.num_other_activities, name_type_map['ActivityReference'])
		self.name_b = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'data_type', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'data', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'num_sub_activities', name_type_map['Uint'], (0, None), (True, 0), (None, None)
		yield 'num_other_activities', name_type_map['Uint'], (0, None), (True, 0), (None, None)
		yield 'sub_activities', name_type_map['ArrayPointer'], (None, name_type_map['ActivityReference']), (False, None), (None, None)
		yield 'index_a', name_type_map['Int'], (0, None), (True, -1), (None, True)
		yield 'index_b', name_type_map['Int'], (0, None), (True, -1), (None, True)
		yield 'other_activities', name_type_map['ArrayPointer'], (None, name_type_map['ActivityReference']), (False, None), (None, True)
		yield 'name_b', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'data_type', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'data', name_type_map['Pointer'], (0, None), (False, None)
		yield 'num_sub_activities', name_type_map['Uint'], (0, None), (True, 0)
		yield 'num_other_activities', name_type_map['Uint'], (0, None), (True, 0)
		yield 'sub_activities', name_type_map['ArrayPointer'], (instance.num_sub_activities, name_type_map['ActivityReference']), (False, None)
		if not instance.num_other_activities:
			yield 'index_a', name_type_map['Int'], (0, None), (True, -1)
			yield 'index_b', name_type_map['Int'], (0, None), (True, -1)
		if instance.num_other_activities:
			yield 'other_activities', name_type_map['ArrayPointer'], (instance.num_other_activities, name_type_map['ActivityReference']), (False, None)
		yield 'name_b', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)

	@classmethod
	def _from_xml(cls, instance, elem):
		"""Infer optional activity counts from their serialized array bodies."""
		if "num_sub_activities" not in elem.attrib:
			sub_activities = elem.find("./sub_activities")
			if sub_activities is not None:
				instance.num_sub_activities = name_type_map['Uint'].from_value(len(sub_activities))
		if "num_other_activities" not in elem.attrib:
			other_activities = elem.find("./other_activities")
			if other_activities is not None:
				instance.num_other_activities = name_type_map['Uint'].from_value(len(other_activities))
		return super()._from_xml(instance, elem)

	def get_ptr_template(self, prop):
		"""Returns the appropriate template for a pointer named 'prop', if exists.
		Must be overwritten in subclass"""
		if prop == "data":
			activity = self.data_type.data
			key = f"{activity}Data"
			try:
				return name_type_map[key]
			except KeyError:
				logging.debug(f"Motiongraph.{activity} is not supported")

