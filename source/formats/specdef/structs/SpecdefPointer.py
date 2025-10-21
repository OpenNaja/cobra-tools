# START_GLOBALS
import struct
import xml.etree.ElementTree as ET
import logging

import numpy as np

from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.basic import ZStringObfuscated
from generated.formats.ovl_base.structs.Pointer import Pointer

ZERO = b"\x00"
# these attributes present on the MemStruct will not be stored on the XML
SKIPS = ("_context", "arg", "name", "io_start", "io_size", "template")
POOL_TYPE = "pool_type"
DTYPE = "dtype"
XML_STR = "xml_string"
DEPENDENCY_TAG = "dependency"

# END_GLOBALS


class SpecdefPointer(Pointer):

	"""
	a pointer in an ovl memory layout
	"""

# START_CLASS

	def write_ptr_all(self, parent_memstruct, children, f_name, loader, pool):
		# when an array is entered
		# locates the read address, attaches the frag entry, and reads the template as ptr.data
		offset = self.io_start
		rel_offset = offset - parent_memstruct.io_start
		# logging.debug(f"Pointer {f_name}, has_data {ptr.has_data} at {ptr.io_start}, relative {rel_offset}")
		# when it's a pointer in an array, f_name is the array index
		# if isinstance(self.data, str) and DEPENDENCY_TAG in f_name:
		if isinstance(f_name, str) and isinstance(self.data, str):
			if self.data:
				# loader.dependencies[ptr.data] = (pool, offset)
				loader.dependencies.append((self.data, (pool, offset)))
				pool.offset_2_link[offset] = self.data
		elif self.has_data:
			self.write_ptr(loader, pool)
			# store relative offset from this memstruct
			children[rel_offset] = (self.target_pool, self.target_offset)
			# keep writing pointers in ptr.data
			for memstruct in parent_memstruct.structs_from_ptr(self):
				memstruct.write_ptrs(loader, self.target_pool)

	@classmethod
	def _from_xml(cls, instance, elem):
		try:
			if elem.text.strip() and elem.text != "None":
				logging.debug(f"Setting dependency {type(instance).__name__}.data = {elem.text}")
				instance.data = elem.text.strip()
				return
			elif instance.template in (ZString, ZStringObfuscated):
				if elem.text:
					instance.data = elem.text
			else:
				instance.data = instance.template(instance.context, instance.arg, None)
				instance.template._from_xml(instance.data, elem)
			return instance
		except:
			logging.exception(f"Error on ptr {elem} {elem.attrib}")
			# raise
