# START_GLOBALS
import struct
import xml.etree.ElementTree as ET
from generated.base_struct import BaseStruct
# from generated.formats.ovl.compounds.Fragment import Fragment

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
		print("to_xml", cls, prop, arguments, debug)
		# sub = ET.SubElement(elem, cls.__name__)
		sub = ET.SubElement(elem, prop)
		if instance.frag and hasattr(instance.frag, "struct_ptr"):
			f_ptr = instance.frag.struct_ptr
			if debug:
				sub.set("_address", f"{f_ptr.pool_index} {f_ptr.data_offset}")
				sub.set("_size", f"{f_ptr.data_size}")
			sub.set(POOL_TYPE, f"{f_ptr.pool.type}")
		elif hasattr(instance, POOL_TYPE):
			if instance.pool_type is not None:
				# todo - make conditional on dtype
				sub.set(POOL_TYPE, f"{instance.pool_type}")
		cls._to_xml(instance, sub, debug)

	@classmethod
	def _to_xml(cls, instance, elem, debug):
		"""Assigns data self to xml elem"""
		# elem, prop, instance, arguments, debug
		# instance.template.to_xml(elem, instance._handle_xml_str(prop), instance.data, arguments, debug)
		# instance.template.to_xml(elem, "data", instance.data, (), debug)
		instance.template._to_xml(instance.data, elem, debug)

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
