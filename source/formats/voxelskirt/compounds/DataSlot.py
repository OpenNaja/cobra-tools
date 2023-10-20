# START_GLOBALS
import struct
import xml.etree.ElementTree as ET
import logging

from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.basic import ZStringObfuscated

ZERO = b"\x00"
# these attributes present on the MemStruct will not be stored on the XML
SKIPS = ("_context", "arg", "name", "io_start", "io_size", "template")
POOL_TYPE = "pool_type"
DTYPE = "dtype"
XML_STR = "xml_string"
DEPENDENCY_TAG = "dependency"

# END_GLOBALS


class DataSlot(BaseStruct):

# START_CLASS
	pass
	# @classmethod
	# def to_xml(cls, elem, prop, instance, arg, template, debug):
	# 	"""Adds this struct to 'elem', recursively"""
	# 	sub = ET.SubElement(elem, prop)
	# 	if instance.data is not None:
	# 		Array._to_xml(instance.data, sub, debug)
	# 	cls._to_xml(instance, sub, debug)
	#
	# @classmethod
	# def from_xml(cls, target, elem, prop, arg, template):
	# 	"""Creates object for parent object 'target', from parent element elem."""
	# 	sub = elem.find(f'./{prop}')
	# 	if sub is None:
	# 		logging.warning(f"Missing sub-element '{prop}' on XML element '{elem.tag}'")
	# 		return
	# 	instance = cls(target.context, arg, template, set_default=False)
	# 	cls._from_xml(instance, sub)
	# 	arr = Array(instance.context, 0, None, (len(sub)), instance.template, set_default=False)
	# 	instance.data = Array._from_xml(arr, sub)
	# 	return instance
