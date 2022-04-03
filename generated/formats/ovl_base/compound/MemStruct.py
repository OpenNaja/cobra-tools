
import logging

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

	def write_ptrs(self, loader, ovs, ref_ptr, is_member=False):
		# todo - get / set pool type
		pool_type_key = 4

		print("ref_ptr before", ref_ptr)

		# get all ptrs of this MemStruct
		ptrs = self.get_ptrs()

		# we only create them if they have data assigned
		ptrs_with_data = [ptr for ptr in ptrs if ptr.data is not None]
		print(f"{len(ptrs)} pointers, {len(ptrs_with_data)} with data")
		# create frags for them
		ptr_frags = loader.create_fragments(loader.sized_str_entry, len(ptrs_with_data))
		# print("frags immediate", ptr_frags)
		# write their data and update frags
		for ptr, frag in zip(ptrs_with_data, ptr_frags):
			if isinstance(ptr.data, MemStruct):
				ptr.data.write_ptrs(loader, ovs, frag.pointers[1])
			else:
				# basic pointer
				frag.pointers[1].pool = loader.get_pool(pool_type_key, ovs=ovs.arg.name)
				frag.pointers[1].write_instance(ptr.template, ptr.data)
		# don't write array members again, they have already been written!
		if not is_member:
			# write this struct's data
			ref_ptr.pool = loader.get_pool(pool_type_key, ovs=ovs.arg.name)
			# print("ref_ptr.pool", ref_ptr.pool)
			ref_ptr.write_instance(type(self), self)
			print("ref_ptr after", ref_ptr)
		# update positions for frag ptrs 0
		for ptr, frag in zip(ptrs, ptr_frags):
			# rel_offset = ptr.io_start - self.io_start
			# loader.ptr_relative(frag.pointers[0], ref_ptr, rel_offset=rel_offset)
			p = frag.pointers[0]
			p.pool_index = ref_ptr.pool_index
			p.data_offset = ptr.io_start
			p.pool = ref_ptr.pool

		# get all arrays of this MemStruct
		arrays = self.get_arrays()
		print("arrays", arrays)
		for array in arrays:
			print(f"found array, len {len(array)}")
			for member in array:
				print("member")
				member.write_ptrs(loader, ovs, ref_ptr, is_member=True)

		# print(ovs.fragments)
		for frag in ovs.fragments:
			print(frag, frag.pointers[1].data_size, frag.pointers[1].data)
		# print(ref_ptr.pool.data.getvalue())

	def read_ptrs(self, ovs, ref_ptr, sized_str_entry, io_start=None):
		if io_start is None:
			io_start = self.io_start
		# print("read_ptrs")
		# get all pointers in this struct
		ptrs = self.get_ptrs()
		for ptr in ptrs:
			self.handle_ptr(ptr, ovs, ref_ptr, io_start, sized_str_entry)
		arrays = self.get_arrays()
		for array in arrays:
			# print(f"array, start at at {array.io_start}")
			for member in array:
				if isinstance(member, MemStruct):
					# print("member is a memstruct")
					member.read_ptrs(ovs, ref_ptr, sized_str_entry, array.io_start)

	def handle_ptr(self, ptr, ovs, ref_ptr, io_start, sized_str_entry):
		rel_offset = ptr.io_start-io_start
		# print(f"handle_ptr dtype: {ptr.template.__name__} io_ref: {io_start} relative: {rel_offset} count: {ptr.arg}")
		# get a fragment that is relative to pointer + offset
		f = ovs.frag_at_pointer(ref_ptr, offset=rel_offset)
		# ptr may be a nullptr, so ignore
		if not f:
			# print("is a nullptr")
			return
		sized_str_entry.fragments.append(f)
		f_ptr = f.pointers[1]
		ptr.data = ptr.template.from_stream(f_ptr.stream, ptr.context, ptr.arg)
		if isinstance(ptr.data, MemStruct):
			# print("ptr is a memstruct")
			ptr.data.read_ptrs(ovs, f_ptr, sized_str_entry)

	@classmethod
	def from_xml_file(cls, file_path, context, arg=0, template=None):
		"""Load MemStruct represented by the xml in 'file_path'"""
		instance = cls(context, arg, template, set_default=False)
		tree = ET.parse(file_path)
		xml = tree.getroot()
		instance.from_xml(xml)
		return instance

	def from_xml(self, elem):
		"""Sets the data from the XML to this MemStruct"""
		# go over all fields of this MemStruct
		items = list(vars(self).items())
		for prop, val in items:
			# skip dummy properties
			if prop in ("_context", "arg", "name", "io_start", "io_size", "template"):
				continue
			if isinstance(val, Pointer):
				# print("pointer")
				# subelement
				subelement = elem.find(f'.//{prop}')
				self._from_xml(subelement, val, val.template)
			elif isinstance(val, Array):
				# print(f"array, len {len(elem)}")
				# create array elements
				val[:] = [val.dtype(self._context) for i in range(len(elem))]
				# subelement with subelements
				# print(val.dtype)
				for subelem, member in zip(elem, val):
					self._from_xml(subelem, member, val.dtype)
			else:
				# set basic attribute
				cls = type(val)
				setattr(self, prop, cls(elem.attrib[prop]))

	def _from_xml(self, subelement, val, val_cls):
		"""Populates this MemStruct from the xml elem"""
		# print("\n_from_xml", subelement, subelement.attrib, type(val))
		# print("cls", val_cls)
		# template class inherits from memstruct
		if issubclass(val_cls, MemStruct):
			if isinstance(val, Pointer):
				# print("ptr to memstruct")
				# todo - test if it is better to already create the template here, or on demand from MemStruct
				val.data = val_cls(self._context)
				val.data.from_xml(subelement)
			# array
			else:
				# print("member is memstruct")
				val.from_xml(subelement)
		# it is a basic type, and a ptr
		else:
			# print("ptr to basic")
			assert isinstance(val, Pointer)
			# cls = type(val.template)
			# val.data = cls(subelement.attrib["data"])
			# todo - convert string to proper basic dtype here, if needed
			# it seems however like only strings would land here at the moment
			if "data" in subelement.attrib:
				data = subelement.attrib["data"]
				# only set data that is not 'None'
				if data != "None":
					val.data = subelement.attrib["data"]
			else:
				logging.warning(f"Expected attribute 'data' for pointer '{subelement.tag}'")

	def to_xml_file(self, file_path):
		"""Create an xml elem representing this MemStruct, recursively set its data, indent and save to 'file_path'"""
		xml = ET.Element(_class_to_name(type(self)))
		self.to_xml(xml)
		indent(xml)
		with open(file_path, 'wb') as outfile:
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

