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

from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.voxelskirt.imports import name_type_map


class DataSlot(BaseStruct):

	__name__ = 'DataSlot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# offset into buffer to start of data - only given if some count is nonzero
		self._offset = name_type_map['Uint64'](self.context, 0, None)

		# count of data
		self._count = name_type_map['Uint64'](self.context, 0, None)
		self.data = Array(self.context, 0, None, (0,), self.template)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield '_offset', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield '_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'data', Array, (0, None, (None,), None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield '_offset', name_type_map['Uint64'], (0, None), (False, None)
		yield '_count', name_type_map['Uint64'], (0, None), (False, None)
		if include_abstract:
			yield 'data', Array, (0, None, (instance._count,), instance.template), (False, None)
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

