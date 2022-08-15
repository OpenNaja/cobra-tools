# START_GLOBALS
import struct
import xml.etree.ElementTree as ET
import logging
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


class Pointer(BaseStruct):

	"""
	a pointer in an ovl memory layout
	"""

# START_CLASS

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		# set to -1 here so that read_ptr doesn't get a wrong frag by chance if the entry has not been read -> get at 0
		self.io_start = -1
		self.offset = 0
		self.data = None
		self.frag = None
		self.pool_type = None
		if set_default:
			self.set_defaults()

	def get_info_str(self):
		return f'Pointer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* data = {self.data.__repr__()}'
		return s

	def read_ptr(self, pool):
		"""Looks up the address of the pointer, checks if a frag points to pointer and reads the data at its address as
		the specified template."""
		# find the frag entry with matching link_ptr.data_offset
		self.frag = pool.offset_2_link_entry.get(self.io_start, None)
		# pointer may be a nullptr, so ignore
		if not self.frag:
			# print("is a nullptr")
			return
		# it is a fragment, not a dependency
		if hasattr(self.frag, "struct_ptr"):
			# now read an instance of template class at the offset
			self.read_template()
		else:
			# store dependency name
			self.data = self.frag.name

	def read_template(self):
		if self.template:
			self.data = self.template.from_stream(self.frag.struct_ptr.stream, self.context, self.arg)

	def write_pointer(self):
		assert (self.data is not None) and self.frag
		# if bytes have been set (usually manually), don't ask, just write
		if isinstance(self.data, (bytes, bytearray)):
			# seek to end, set data_offset, write
			self.frag.struct_ptr.write_to_pool(self.data)
		else:
			# process the generated data
			try:
				self.write_template()
			except TypeError:
				raise TypeError(f"Failed to write pointer data {self.data} type: {type(self.data)} as {self.template}")
			except struct.error:
				raise TypeError(f"Failed to write pointer data {self.data} type: {type(self.data)} as {self.template}")

	def write_template(self):
		assert self.template is not None
		self.frag.struct_ptr.write_instance(self.template, self.data)

	@classmethod
	def to_xml(cls, elem, prop, instance, arguments, debug):
		"""Adds this struct to 'elem', recursively"""
		sub = ET.SubElement(elem, prop)
		cls.pool_type_to_xml(sub, instance, debug)
		if instance.data is not None:
			# xml string
			if prop == XML_STR:
				sub.append(ET.fromstring(instance.data))
			else:
				cls._to_xml(instance, sub, debug)

	@classmethod
	def pool_type_to_xml(cls, elem, instance, debug):
		"""Sets the pool type of instance to elem's attrib"""
		if instance.frag and hasattr(instance.frag, "struct_ptr"):
			f_ptr = instance.frag.struct_ptr
			if debug:
				elem.set("_address", f"{f_ptr.pool_index} {f_ptr.data_offset}")
				elem.set("_size", f"{f_ptr.data_size}")
			cls._set_pool_type(elem, f_ptr.pool.type, instance.template)
		elif hasattr(instance, POOL_TYPE):
			if instance.pool_type is not None:
				cls._set_pool_type(elem, instance.pool_type, instance.template)

	@staticmethod
	def _set_pool_type(elem, pool_type, template):
		"""Set the pool type, unless it is obvious"""
		# if template not in (ZString, ZStringObfuscated):
		if pool_type != 2:
			elem.set(POOL_TYPE, f"{pool_type}")

	@classmethod
	def _to_xml(cls, instance, elem, debug):
		"""Assigns data self to xml elem"""
		# catch Zstr Pointers and dependencies (template=None)
		# if instance.template in (ZString, ZStringObfuscated):
		if isinstance(instance.data, str):
			elem.text = instance.data
		else:
			if instance.template is not None:
				instance.template._to_xml(instance.data, elem, debug)

	@classmethod
	def pool_type_from_xml(cls, elem, instance):
		if POOL_TYPE in elem.attrib:
			instance.pool_type = int(elem.attrib[POOL_TYPE])
			logging.debug(f"Set pool type {instance.pool_type} for pointer {elem.tag}")
		else:
			instance.pool_type = 2

	@classmethod
	def from_xml(cls, target, elem, prop, arguments):
		"""Creates object for parent object 'target', from parent element elem."""
		sub = elem.find(f'.//{prop}')
		if sub is None:
			logging.warning(f"Missing sub-element '{prop}' on XML element '{elem.tag}'")
			return
		instance = cls(target.context, *arguments, set_default=False)

		cls.pool_type_from_xml(elem, instance)
		if prop == XML_STR:
			instance.data = ET.tostring(sub[0], encoding="unicode").replace("\t", "").replace("\n", "")
		else:
			cls._from_xml(instance, sub)
		return instance

	@classmethod
	def _from_xml(cls, instance, elem):
		if instance.template is None:
			if DEPENDENCY_TAG in elem.tag:
				if elem.text and elem.text != "None":
					logging.debug(f"Setting dependency {type(instance).__name__}.data = {elem.text}")
					instance.data = elem.text
			return
		elif instance.template in (ZString, ZStringObfuscated):
			if elem.text:
				instance.data = elem.text
		else:
			instance.data = instance.template(instance.context, instance.arg, None)
			instance.template._from_xml(instance.data, elem)
		return instance

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
