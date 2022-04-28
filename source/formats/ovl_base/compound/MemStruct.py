# START_GLOBALS
import logging
import struct

from numpy.core.multiarray import ndarray

from generated.array import Array, _class_to_name
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.ForEachPointer import ForEachPointer
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



# END_GLOBALS

class MemStruct:
	"""this is a struct that is capable of having pointers"""
# START_CLASS

	# used for the ptr alignment mapping
	ptr_al_dict = {}

	def get_props_and_ptrs(self):
		return [(prop, val) for prop, val in vars(self).items() if isinstance(val, Pointer)]

	def get_arrays(self):
		return [val for prop, val in vars(self).items() if isinstance(val, Array)]

	def get_memstructs(self):
		return [val for prop, val in vars(self).items() if isinstance(val, MemStruct)]

	def write_ptrs(self, loader, ovs, ref_ptr, is_member=False):
		# todo - get / set pool type
		pool_type_key = 4

		print("ref_ptr before", ref_ptr)

		# get all ptrs of this MemStruct, but only create them if they have data assigned
		ptrs = self.get_props_and_ptrs()
		ptrs_with_data = [ptr for prop, ptr in ptrs if ptr.data is not None]
		print(f"{len(ptrs)} pointers, {len(ptrs_with_data)} with data")
		# create frags for them
		ptr_frags = loader.create_fragments(loader.sized_str_entry, len(ptrs_with_data))
		# print("frags immediate", ptr_frags)
		# write their data and update frags
		for ptr, frag in zip(ptrs_with_data, ptr_frags):
			if isinstance(ptr.data, MemStruct):
				ptr.data.write_ptrs(loader, ovs, frag.struct_ptr)
			else:
				# basic pointer
				frag.struct_ptr.pool = loader.get_pool(pool_type_key, ovs=ovs.arg.name)
				ptr.write_pointer(frag)
				# handle ArrayPointer
				if isinstance(ptr.data, Array):
					for member in ptr.data:
						if isinstance(member, MemStruct):
							member.write_ptrs(loader, ovs, frag.struct_ptr, is_member=True)

		# don't write array members again, they have already been written!
		if not is_member:
			# write this struct's data
			ref_ptr.pool = loader.get_pool(pool_type_key, ovs=ovs.arg.name)
			# print("ref_ptr.pool", ref_ptr.pool)
			ref_ptr.write_instance(type(self), self)
			print("ref_ptr after", ref_ptr)
		# update positions for frag ptrs 0
		for ptr, frag in zip(ptrs_with_data, ptr_frags):
			p = frag.link_ptr
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
				if isinstance(member, MemStruct):
					member.write_ptrs(loader, ovs, ref_ptr, is_member=True)
				# elif isinstance(member, Pointer):
				# 	logging.warning(f"Missing write_ptrs for ArrayPointer")

		# print(ovs.fragments)
		for frag in ovs.fragments:
			print(frag, frag.struct_ptr.data_size, frag.struct_ptr.data)
		# print(ref_ptr.pool.data.getvalue())

	def read_ptrs(self, pool, sized_str_entry):
		# print("read_ptrs")
		# get all pointers in this struct
		for prop, ptr in self.get_props_and_ptrs():
			self.handle_ptr(prop, ptr, pool, sized_str_entry)
		# read arrays attached to this memstruct
		arrays = self.get_arrays()
		for array in arrays:
			# print(f"array, start at at {array.io_start}")
			for member in array:
				if isinstance(member, MemStruct):
					# print("member is a memstruct")
					member.read_ptrs(pool, sized_str_entry)
				elif isinstance(member, Pointer):
					self.handle_ptr(None, member, pool, sized_str_entry)
		# continue reading sub-memstructs directly attached to this memstruct
		for memstr in self.get_memstructs():
			memstr.read_ptrs(pool, sized_str_entry)

	def get_ptr_template(self, prop):
		"""Returns the appropriate template for a pointer named 'prop', if exists.
		Must be overwritten in subclass"""
		return None

	def handle_ptr(self, prop, ptr, pool, sized_str_entry):
		"""Ensures a pointer has a valid template, load it, and continue processing the linked memstruct."""
		if not ptr.template:
			# try the lookup function
			ptr.template = self.get_ptr_template(prop)
		# reads the template
		ptr.read_ptr(pool, sized_str_entry)
		if isinstance(ptr.data, MemStruct):
			# print("ptr to a memstruct")
			ptr.data.read_ptrs(ptr.frag.struct_ptr.pool, sized_str_entry)
		# ArrayPointer
		elif isinstance(ptr.data, Array):
			assert isinstance(ptr, (ArrayPointer, ForEachPointer))
			# print("ArrayPointer")
			for member in ptr.data:
				if isinstance(member, MemStruct):
					# print(f"member {member.__class__} of ArrayPointer is a MemStruct")
					member.read_ptrs(ptr.frag.struct_ptr.pool, sized_str_entry)
		else:
			# points to a normal struct or basic type, which can't have any pointers
			pass

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
				# print("val.template", val.template)
				if isinstance(val, ArrayPointer):
					logging.warning(f"Setting ArrayPointer '{prop}' not supported yet")
					pass
					# val.data[:] = [val.data.dtype(self._context) for i in range(len(subelement))]
					# # subelement with subelements
					# for subelem, member in zip(elem, val.data):
					# 	self._from_xml(subelem, member, val.data.dtype)
				else:
					self._from_xml(subelement, val, val.template)
			elif isinstance(val, Array):
				# print(f"array, len {len(elem)}")
				# create array elements
				val[:] = [val.dtype(self._context) for i in range(len(elem))]
				# subelement with subelements
				for subelem, member in zip(elem, val):
					self._from_xml(subelem, member, val.dtype)
			else:
				# set basic attribute
				cls = type(val)
				if isinstance(val, ndarray):
					logging.warning(f"Ignoring basic array '{prop}'")
					continue
				try:
					setattr(self, prop, cls(elem.attrib[prop]))
				except TypeError:
					raise TypeError(f"Could not convert attribute {prop} = '{elem.attrib[prop]}' to {cls.__name__}")

	def _from_xml(self, subelement, val, val_cls):
		"""Populates this MemStruct from the xml elem"""
		# print("\n_from_xml", subelement, subelement.attrib, type(val))
		# print("cls", val_cls)
		if not val_cls:
			assert isinstance(val, Pointer)
			assert not val.template
			logging.warning(f"No template set for pointer on XML element '{subelement.tag}'")
			return
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

	def _to_xml(self, elem, prop, val, frag=None):
		"""Create a subelement named 'prop' that represents object 'val'"""
		subelement = ET.SubElement(elem, prop)
		# value is a memstruct
		if isinstance(val, MemStruct):
			# print("memstruct")
			val.to_xml(subelement)
		# it is a basic type
		else:
			if isinstance(val, Array):
				# print(f"_to_xml array {val.dtype}")
				# print(f"_to_xml array {val}")
				# subelement with subelements
				for member in val:
					if isinstance(member, Pointer):
						self._to_xml(subelement, val.class_name, member.data, member.frag)
					else:
						self._to_xml(subelement, val.class_name, member)
			# print("basic")
			else:
				# special case for xml data - make it a sub element
				if prop == "xml_string":
					# print(val)
					subelement.append(ET.fromstring(val))
				else:
					subelement.set("data", str(val))
		# set address for debugging
		if frag and hasattr(frag, "struct_ptr"):
			f_ptr = frag.struct_ptr
			subelement.set("_address", f"{f_ptr.pool_index} {f_ptr.data_offset}")
			subelement.set("_size", f"{f_ptr.data_size}")

	def to_xml(self, elem):
		"""Adds data of this MemStruct to 'elem', recursively"""
		# go over all fields of this MemStruct
		for prop, val in vars(self).items():
			# skip dummy properties
			if prop in ("_context", "arg", "name", "io_start", "io_size", "template"):
				continue
			if isinstance(val, Pointer):
				# print("pointer")
				# subelementptr.frag
				# print(val.template)
				self._to_xml(elem, prop, val.data, val.frag)
			elif isinstance(val, Array):
				print(f"to_xml array {val.dtype}")
				# subelement with subelements
				for member in val:
					if isinstance(member, Pointer):
						self._to_xml(elem, val.class_name, member.data, member.frag)
					else:
						self._to_xml(elem, val.class_name, member)
			else:
				# todo - add this distinction for from_xml
				# a MemStruct
				if isinstance(val, MemStruct):
					subelement = ET.SubElement(elem, prop)
					val.to_xml(subelement)
				# basic attribute
				else:
					elem.set(prop, str(val))

	def debug_ptrs(self):
		"""Iteratively debugs all pointers of a struct"""
		cls_name = self.__class__.__name__
		if cls_name not in self.ptr_al_dict:
			self.ptr_al_dict[cls_name] = {}
		cls_al_dict = self.ptr_al_dict[cls_name]
		props_arrays = [(prop, val) for prop, val in vars(self).items() if isinstance(val, Array)]
		props_ptrs = self.get_props_and_ptrs() + [(prop, ptr) for prop, arr in props_arrays for ptr in arr if isinstance(ptr, Pointer)]
		for prop, ptr in props_ptrs:
			# dtype = ptr.template.__name__ if ptr.template else None
			# al = None
			if ptr.frag:
				# if isinstance(ptr.frag,)
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
						# is data_offset of struct ptr aligned at al bytes?
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
