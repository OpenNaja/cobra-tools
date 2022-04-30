
import logging
import xml.etree.ElementTree as ET
from numpy.core.multiarray import ndarray

from generated.array import Array
from generated.base_enum import BaseEnum
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.compound.Pointer import Pointer

ZERO = b"\x00"
SKIPS = ("_context", "arg", "name", "io_start", "io_size", "template")
POOL_TYPE = "_pool_type"


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

	# used for the pointer alignment mapping
	ptr_al_dict = {}

	def get_props_and_ptrs(self):
		return [(prop, val) for prop, val in vars(self).items() if isinstance(val, Pointer)]

	def get_arrays(self):
		return [val for prop, val in vars(self).items() if isinstance(val, Array)]

	def get_memstructs(self):
		return [val for prop, val in vars(self).items() if isinstance(val, MemStruct)]

	def write_ptrs(self, loader, ovs, struct_ptr, pool_type, is_member=False):
		print("struct_ptr before", struct_ptr)
		# get all ptrs of this MemStruct, but only create them if they have data assigned
		ptrs = self.get_props_and_ptrs()
		ptrs_with_data = [ptr for prop, ptr in ptrs if ptr.data is not None]
		print(f"{len(ptrs)} pointers, {len(ptrs_with_data)} with data")
		# create frags for them
		ptr_frags = loader.create_fragments(loader.sized_str_entry, len(ptrs_with_data))
		# print("frags immediate", ptr_frags)
		# write their data and update frags
		for pointer, frag in zip(ptrs_with_data, ptr_frags):
			if isinstance(pointer.data, MemStruct):
				pointer.data.write_ptrs(loader, ovs, frag.struct_ptr, pool_type)
			else:
				# basic pointer
				frag.struct_ptr.pool = loader.get_pool(pointer.pool_type, ovs=ovs.arg.name)
				pointer.write_pointer(frag)
				# handle ArrayPointer
				if isinstance(pointer.data, Array):
					for member in pointer.data:
						if isinstance(member, MemStruct):
							member.write_ptrs(loader, ovs, frag.struct_ptr, pointer.pool_type, is_member=True)

		# don't write array members again, they have already been written!
		if not is_member:
			# write this struct's data
			struct_ptr.pool = loader.get_pool(pool_type, ovs=ovs.arg.name)
			# print("struct_ptr.pool", struct_ptr.pool)
			struct_ptr.write_instance(type(self), self)
			print("struct_ptr after", struct_ptr)
		# update positions for frag ptrs 0
		for pointer, frag in zip(ptrs_with_data, ptr_frags):
			p = frag.link_ptr
			p.pool_index = struct_ptr.pool_index
			p.data_offset = pointer.io_start
			p.pool = struct_ptr.pool

		# get all arrays of this MemStruct
		arrays = self.get_arrays()
		print("arrays", arrays)
		for array in arrays:
			print(f"found array, len {len(array)}")
			for member in array:
				print("member")
				if isinstance(member, MemStruct):
					member.write_ptrs(loader, ovs, struct_ptr, pool_type, is_member=True)
				# elif isinstance(member, Pointer):
				# 	logging.warning(f"Missing write_ptrs for ArrayPointer")

		# print(ovs.fragments)
		for frag in ovs.fragments:
			print(frag, frag.struct_ptr.data_size, frag.struct_ptr.data)
		# print(struct_ptr.pool.data.getvalue())

	def read_ptrs(self, pool):
		logging.debug(f"read_ptrs for {self.__class__.__name__}")
		# get all pointers in this struct
		for prop, ptr in self.get_props_and_ptrs():
			self.handle_pointer(prop, ptr, pool)
		# read arrays attached to this memstruct
		arrays = self.get_arrays()
		for array in arrays:
			# print(f"array, start at at {array.io_start}")
			for member in array:
				if isinstance(member, MemStruct):
					# print("member is a memstruct")
					member.read_ptrs(pool)
				elif isinstance(member, Pointer):
					self.handle_pointer(None, member, pool)
		# continue reading sub-memstructs directly attached to this memstruct
		for memstr in self.get_memstructs():
			memstr.read_ptrs(pool)

	def get_ptr_template(self, prop):
		"""Returns the appropriate template for a pointer named 'prop', if exists.
		Must be overwritten in subclass"""
		return None

	def handle_pointer(self, prop, pointer, pool):
		"""Ensures a pointer has a valid template, load it, and continue processing the linked memstruct."""
		logging.debug(f"handle_pointer for {self.__class__.__name__}")
		if not pointer.template:
			# try the lookup function
			pointer.template = self.get_ptr_template(prop)
		# reads the template and grabs the frag
		pointer.read_ptr(pool)  # , sized_str_entry)
		if pointer.frag and hasattr(pointer.frag, "struct_ptr"):
			pool = pointer.frag.struct_ptr.pool
			pointer.pool_type = pool.type
			logging.debug(f"Set pool type {pointer.pool_type} for pointer {prop}")
			if isinstance(pointer.data, MemStruct):
				# print("pointer to a memstruct")
				pointer.data.read_ptrs(pool)
			# ArrayPointer
			elif isinstance(pointer.data, Array):
				assert isinstance(pointer, (ArrayPointer, ForEachPointer))
				# print("ArrayPointer")
				for member in pointer.data:
					if isinstance(member, MemStruct):
						# print(f"member {member.__class__} of ArrayPointer is a MemStruct")
						member.read_ptrs(pool)
			else:
				# points to a normal struct or basic type, which can't have any pointers
				pass

	def _array_from_xml(self, elem, val):
		# create array elements
		# print(f"array, len {len(elem)}")
		val[:] = [val.dtype(self._context) for i in range(len(elem))]
		# subelement with subelements
		for subelem, member in zip(elem, val):
			self._from_xml(subelem, val.class_name, member)

	def _array_to_xml(self, elem, val):
		# print(f"to_xml array {val.dtype}")
		# subelement with subelements
		for member in val:
			cls_name = member.__class__.__name__
			subelement = ET.SubElement(elem, cls_name)
			if isinstance(member, Pointer):
				member = member.data
			# self._to_xml(elem, cls_name, member)
			self._to_xml(subelement, cls_name, member)

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
		for prop, val in vars(self).items():
			# skip dummy properties
			if prop in SKIPS:
				continue
			self._from_xml(elem, prop, val)

	def _from_xml(self, elem, prop, val):
		"""Populates this MemStruct from the xml elem"""
		# print("_from_xml", elem, prop, val)
		if isinstance(val, Pointer):
			subelement = elem.find(f'.//{prop}')
			if not subelement:
				logging.warning(f"Missing sub-element '{prop}' on XML element '{elem.tag}'")
				return
			if not val.template:
				logging.warning(f"No template set for pointer {prop} on XML element '{subelement.tag}'")
				return
			if POOL_TYPE in subelement.attrib:
				val.pool_type = subelement.attrib[POOL_TYPE]
				logging.debug(f"Set pool type {val.pool_type} for pointer {prop}")
			else:
				logging.warning(f"Missing pool type for pointer {prop}")
			# print("val.template", val.template)
			if isinstance(val, ArrayPointer):
				# print("ArrayPointer", subelement, len(subelement))
				val.data = Array((len(subelement)), val.template, val.context, set_default=False)
				self._array_from_xml(subelement, val.data)
			else:
				# print("other pointer")
				val.data = val.template(self._context)
				self._from_xml(subelement, prop, val.data)
		elif isinstance(val, Array):
			# print("Array")
			self._array_from_xml(elem, val)
		elif isinstance(val, MemStruct):
			# print("MemStruct")
			# when called from array or pointer, the subelement is already given
			# finding the subelem may not actually be needed
			if elem.tag != prop:
				# get it if a memstruct is a child of a memstruct
				elem = elem.find(f'.//{prop}')
			val.from_xml(elem)
		elif isinstance(val, BaseEnum):
			# print("BaseEnum")
			setattr(self, prop, val.from_str(elem.attrib[prop]))
		elif isinstance(val, ndarray):
			logging.warning(f"Ignoring basic array '{prop}'")
			return
		else:
			# print("basic")
			# set basic attribute
			cls = type(val)
			# todo - str pointer's data is called data by convention - handle this
			if prop in elem.attrib:
				data = elem.attrib[prop]
				if data != "None":
					# val.data = elem.attrib["data"]
					try:
						setattr(self, prop, cls(data))
					except TypeError:
						raise TypeError(f"Could not convert attribute {prop} = '{elem.attrib[prop]}' to {cls.__name__}")
					except KeyError:
						logging.warning(f"Missing '{prop}' in {elem.tag} attributes")
					except AttributeError:
						logging.warning(f"Missing something on property '{prop}' in element {elem}")

	def to_xml_file(self, file_path):
		"""Create an xml elem representing this MemStruct, recursively set its data, indent and save to 'file_path'"""
		xml = ET.Element(self.__class__.__name__)
		self.to_xml(xml)
		indent(xml)
		with open(file_path, 'wb') as outfile:
			outfile.write(ET.tostring(xml))

	def _to_xml(self, elem, prop, val):
		"""Create a subelement named 'prop' that represents object 'val'"""
		logging.info(f"_to_xml {elem.tag} - {prop}")
		if isinstance(val, Pointer):
			subelement = ET.SubElement(elem, prop)
			if val.frag and hasattr(val.frag, "struct_ptr"):
				f_ptr = val.frag.struct_ptr
				subelement.set("_address", f"{f_ptr.pool_index} {f_ptr.data_offset}")
				subelement.set("_size", f"{f_ptr.data_size}")
				subelement.set(POOL_TYPE, f"{f_ptr.pool.type}")
			self._to_xml(subelement, prop, val.data)
		# todo - ndarray of basic types, subelements or as xml list? multiple dimensions?
		elif isinstance(val, (Array, ndarray)):
			self._array_to_xml(elem, val)
		elif isinstance(val, MemStruct):
			if elem.tag != prop:
				elem = ET.SubElement(elem, prop)
			val.to_xml(elem)
		# basic attribute
		else:
			if prop == "xml_string":
				elem.append(ET.fromstring(val))
			else:
				# this indicates we're looking at a pointer's basic type, usually str
				if elem.tag == prop:
					elem.set("data", str(val))
				# just a regular basic type on a MemStruct
				else:
					elem.set(prop, str(val))

	def to_xml(self, elem):
		"""Adds data of this MemStruct to 'elem', recursively"""
		# go over all fields of this MemStruct
		for prop, val in vars(self).items():
			# skip dummy properties
			if prop in SKIPS:
				continue
			self._to_xml(elem, prop, val)

	def debug_ptrs(self):
		"""Iteratively debugs all pointers of a struct"""
		cls_name = self.__class__.__name__
		if cls_name not in self.ptr_al_dict:
			self.ptr_al_dict[cls_name] = {}
		cls_al_dict = self.ptr_al_dict[cls_name]
		props_arrays = [(prop, val) for prop, val in vars(self).items() if isinstance(val, Array)]
		props_ptrs = self.get_props_and_ptrs() + [(prop, ptr) for prop, arr in props_arrays for ptr in arr if isinstance(ptr, Pointer)]
		for prop, ptr in props_ptrs:
			# dtype = pointer.template.__name__ if pointer.template else None
			# al = None
			if ptr.frag:
				# if isinstance(pointer.frag,)
				# skip dependency
				if not hasattr(ptr.frag, "struct_ptr"):
					continue
				d_off = ptr.frag.struct_ptr.data_offset
				if d_off:
					# go over decreasing possible alignments
					# 64, 32, 16, 8, 4, 2, 1
					for x in reversed(range(6)):
						al = 2 ** x
						# logging.debug(f"Testing alignment: {al}")
						# is data_offset of struct pointer aligned at al bytes?
						if d_off % al == 0:
							# add or overwrite if new al is smaller than stored al
							if prop not in cls_al_dict or al < cls_al_dict[prop]:
								cls_al_dict[prop] = al
							# don't test smaller alignments
							break
				# else:
				# 	al = "can't tell, data_offset=0"
				# test children
				if isinstance(ptr.data, MemStruct):
					ptr.data.debug_ptrs()
				elif isinstance(ptr.data, Array):
					for member in ptr.data:
						if isinstance(member, Pointer):
							member = member.data
						if isinstance(member, MemStruct):
							member.debug_ptrs()

			# logging.debug(f"Pointer: {prop} Dtype: {dtype} Alignment: {al}")
		logging.debug(f"MemStruct: {self.__class__.__name__} {cls_al_dict}")

	def get_info_str(self):
		return f'\nMemStruct'

	def get_fields_str(self):
		return ""

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return ""

