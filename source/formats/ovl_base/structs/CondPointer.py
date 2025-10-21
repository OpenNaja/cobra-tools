# START_GLOBALS
import xml.etree.ElementTree as ET
from generated.array import Array
from generated.formats.ovl_base.structs.Pointer import Pointer

XML_STR = "xml_string"
# END_GLOBALS


class CondPointer(Pointer):

	"""
	a pointer to an array in an ovl memory layout
	"""

# START_CLASS

	@classmethod
	def to_xml(cls, elem, prop, instance, arg, template, debug):
		"""Adds this struct to 'elem', recursively"""
		if instance.has_data:
			sub = ET.SubElement(elem, prop)
			cls.pool_type_to_xml(sub, instance, debug)
			# xml string
			if prop == XML_STR:
				sub.append(ET.fromstring(instance.data))
			else:
				cls._to_xml(instance, sub, debug)
