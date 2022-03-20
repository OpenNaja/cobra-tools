
from generated.array import Array, _class_to_name
from generated.formats.ovl_base.compound.Pointer import Pointer
import xml.etree.ElementTree as ET

ZERO = b"\x00"


def indent(e, level=0):
	i = "\n" + level*"	"
	if len(e):
		if not e.text or not e.text.strip():
			e.text = i + "	"
		if not e.tail or not e.tail.strip():
			e.tail = i
		for e in e:
			indent(e, level+1)
		if not e.tail or not e.tail.strip():
			e.tail = i
	else:
		if level and (not e.tail or not e.tail.strip()):
			e.tail = i



from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class MemStruct:

	"""
	this is a struct that is capable of having pointers
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		pass

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		pass

	@classmethod
	def write_fields(cls, stream, instance):
		pass

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_ptrs(self):
		return [val for prop, val in vars(self).items() if isinstance(val, Pointer)]

	def get_arrays(self):
		return [val for prop, val in vars(self).items() if isinstance(val, Array)]

	def read_ptrs(self, ovs, ref_ptr, io_start=None):
		if not io_start:
			io_start = self.io_start
		# print("read_ptrs")
		# get all pointers in this struct
		ptrs = self.get_ptrs()
		for ptr in ptrs:
			self.handle_ptr(ptr, ovs, ref_ptr, io_start)
		arrays = self.get_arrays()
		for array in arrays:
			# print("array")
			for member in array:
				if isinstance(member, MemStruct):
					# print("member is a memstruct")
					member.read_ptrs(ovs, ref_ptr, array.io_start)

	def handle_ptr(self, ptr, ovs, ref_ptr, io_start):
		rel_offset = ptr.io_start-io_start
		# print(f"handle_ptr dtype: {ptr.template.__name__} relative: {rel_offset} count: {ptr.arg}")
		# get a fragment that is relative to pointer + offset
		f = ovs.frag_at_pointer(ref_ptr, offset=rel_offset)
		# ptr may be a nullptr, so ignore
		if not f:
			# print("is a nullptr")
			return
		f_ptr = f.pointers[1]
		ptr.data = ptr.template.from_stream(f_ptr.stream, ptr.context, ptr.arg)
		if isinstance(ptr.data, MemStruct):
			# print("is a memstruct")
			ptr.data.read_ptrs(ovs, f_ptr)

	def to_xml_file(self, out_path):
		"""Create an xml elem representing this MemStruct, recursively set its data, indent and save to 'out_path'"""
		xml = ET.Element(_class_to_name(type(self)))
		self.to_xml(xml)
		indent(xml)
		with open(out_path, 'wb') as outfile:
			outfile.write(ET.tostring(xml))

	def _to_xml(self, elem, prop, val):
		"""Create a subelement named 'prop' that represents object 'val'"""
		subelement = ET.SubElement(elem, prop)
		# value is a memstruct
		if isinstance(val, MemStruct):
			# print("memstruct")
			val.to_xml(subelement)
		# it is a basic type
		else:
			# print("basic")
			subelement.set("data", str(val))

	def to_xml(self, elem):
		"""Adds data of this MemStruct to 'elem', recursively"""
		# go over all fields of this MemStruct
		for prop, val in vars(self).items():
			# skip dummy properties
			if prop in ("_context", "arg", "name", "io_start", "io_size", "template"):
				continue
			if isinstance(val, Pointer):
				# print("pointer")
				# subelement
				self._to_xml(elem, prop, val.data)
			elif isinstance(val, Array):
				# print("array")
				# subelement with subelements
				# print(val.dtype)
				for member in val:
					self._to_xml(elem, val.class_name, member)
			else:
				# a basic attribute
				elem.set(prop, str(val))

	def get_info_str(self):
		return f'\nMemStruct'

	def get_fields_str(self):
		return ""

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return ""

