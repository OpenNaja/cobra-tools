# START_GLOBALS
import logging
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.motiongraph.imports import name_type_map

# END_GLOBALS


class Activity(MemStruct):

	"""
	48 bytes
	"""

# START_CLASS

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
