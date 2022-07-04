# START_GLOBALS
import logging
import xml.etree.ElementTree as ET

import numpy as np
from numpy.core.multiarray import ndarray

from generated.array import Array
from generated.base_enum import BaseEnum
from generated.formats.ovl import get_game
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.compound.Pointer import Pointer

ZERO = b"\x00"
# these attributes present on the MemStruct will not be stored on the XML
SKIPS = ("_context", "arg", "name", "io_start", "io_size", "template")
POOL_TYPE = "pool_type"
DTYPE = "dtype"
XML_STR = "xml_string"
DEPENDENCY_TAG = "dependency"


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

	# used for the pointer alignment mapping
	ptr_al_dict = {}

	def get_props_and_ptrs(self):
		return [(prop, val) for prop, val in vars(self).items() if isinstance(val, Pointer)]

	def get_arrays(self):
		return [(prop, val) for prop, val in vars(self).items() if isinstance(val, Array)]

	def get_memstructs(self):
		return [val for prop, val in vars(self).items() if isinstance(val, MemStruct)]

	def handle_write(self, prop, val, struct_ptr, loader, pool_type, is_member=False):
		logging.debug(f"handle_write {prop} {type(val).__name__}, {len(loader.fragments)} frags")
		if isinstance(val, MemStruct):
			val.write_ptrs(loader, struct_ptr, pool_type, is_member=is_member)
		elif isinstance(val, Array):
			for member in val:
				self.handle_write(prop, member, struct_ptr, loader, pool_type, is_member=True)
		elif isinstance(val, Pointer):
			# usually we add a pointer for empty arrays
			if val.data is not None:
				if DEPENDENCY_TAG in prop:
					logging.debug(f"Created dependency for {prop} = {val.data}")
					val.frag = loader.create_dependency(val.data)
				else:
					val.frag = loader.create_fragment()

				if DEPENDENCY_TAG not in prop:
					# when generated from XML, the pool type is stored as metadata
					# it's not stored in binary, so for those, keep the root pool type
					if val.pool_type is not None:
						pool_type = val.pool_type
					val.frag.struct_ptr.pool = loader.get_pool(pool_type)
					# this writes pointer.data to the pool
					val.write_pointer()
					# now repeat with pointer.data
					self.handle_write(prop, val.data, val.frag.struct_ptr, loader, pool_type, is_member=True)
				# set link_ptr
				p = val.frag.link_ptr
				p.data_offset = val.io_start
				p.pool = struct_ptr.pool

	def write_ptrs(self, loader, struct_ptr, pool_type, is_member=False):
		logging.debug(f"write_ptrs, member={is_member}")
		# don't write array members again, they have already been written!
		if not is_member:
			# write this struct's data
			struct_ptr.pool = loader.get_pool(pool_type)
			struct_ptr.write_instance(type(self), self)
			logging.debug(f"memstruct's struct_ptr after {struct_ptr}")

		# write their data and update frags
		for prop, pointer in self.get_props_and_ptrs():
			self.handle_write(prop, pointer, struct_ptr, loader, pool_type)
		# get all arrays of this MemStruct
		for prop, array in self.get_arrays():
			self.handle_write(prop, array, struct_ptr, loader, pool_type)

	def read_ptrs(self, pool):
		logging.debug(f"read_ptrs for {self.__class__.__name__}")
		# get all pointers in this struct
		for prop, ptr in self.get_props_and_ptrs():
			self.handle_pointer(prop, ptr, pool)
		# read arrays attached to this memstruct
		arrays = self.get_arrays()
		for prop, array in arrays:
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
		logging.debug(f"handle_pointer for {self.__class__.__name__}.{prop}")
		if not pointer.template:
			# try the lookup function
			pointer.template = self.get_ptr_template(prop)
		# reads the template and grabs the frag
		pointer.read_ptr(pool)
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
		# cast to tuple to avoid 'dictionary changed size during iteration'
		vars_dict = vars(self)
		# special case - handle dtype first to set defaults on struct before setting any other data
		if DTYPE in vars_dict:
			self._from_xml(self, elem, DTYPE, vars_dict[DTYPE])
			logging.debug(f"Set defaults on {self.__class__.__name__}")
			self.set_defaults()
		# special cases - these are not added to the xml definition, but need to be converted
		for prop in ("name", "game"):
			if prop in elem.attrib:
				setattr(self, prop, elem.attrib[prop])
		for prop, val in tuple(vars_dict.items()):
			# skip dummy properties
			if prop in SKIPS:
				continue
			if isinstance(val, (MemStruct, Array, ndarray, Pointer)):
				sub = elem.find(f'.//{prop}')
				if sub is None:
					logging.warning(f"Missing sub-element '{prop}' on XML element '{elem.tag}'")
					return
				self._from_xml(self, sub, prop, val)
			else:
				self._from_xml(self, elem, prop, val)
		# also add any meta-data that is not directly part of the struct generated by the codegen
		for attr, value in elem.attrib.items():
			if attr not in vars(self).keys():
				logging.debug(f"Adding string metadata '{attr} = {value}' from XML element '{elem.tag}'")
				setattr(self, attr, value)

	@staticmethod
	def _handle_xml_str(prop):
		return "data" if prop != XML_STR else XML_STR

	def _from_xml(self, target, elem, prop, val):
		"""Populates this MemStruct from the xml elem"""
		# print("_from_xml", elem, prop, val)
		if isinstance(val, Pointer):
			if DEPENDENCY_TAG in prop:
				data = elem.text
				if data != "None":
					logging.debug(f"Setting dependency {type(val).__name__}.data = {data}")
					val.data = data
			if val.template is None:
				logging.debug(f"No template set for pointer '{prop}' on XML element '{elem.tag}'")
				return
			if POOL_TYPE in elem.attrib:
				val.pool_type = int(elem.attrib[POOL_TYPE])
				logging.debug(f"Set pool type {val.pool_type} for pointer {prop}")
			# else:
			# 	logging.debug(f"Missing pool type for pointer '{prop}' on '{elem.tag}'")
			# print("val.template", val.template)
			if isinstance(val, ArrayPointer):
				# print("ArrayPointer", elem, len(elem))
				val.data = Array((len(elem)), val.template, val.context, set_default=False)
			elif isinstance(val, ForEachPointer):
				# print("ArrayPointer", elem, len(elem))
				val.data = Array((len(elem)), val.template, val.context, arg=val.arg.data, set_default=False)
				# need set_default to fix dtype
				val.data[:] = [val.template(self._context, sub, val.template, set_default=True) for sub in val.arg.data]
				for subelem, member in zip(elem, val.data):
					self._from_xml(self, subelem, subelem.tag, member)
				return
			else:
				# print("other pointer")
				logging.debug(f"Creating pointer.data = {val.template.__name__}()")
				val.data = val.template(self._context, val.arg, None)
			self._from_xml(val, elem, self._handle_xml_str(prop), val.data)
		elif isinstance(val, Array):
			# create array elements
			# print(f"array {prop}, len {len(elem)}")
			val[:] = [val.dtype(self._context, 0, val.template, set_default=False) for i in range(len(elem))]
			# subelement with subelements
			for subelem, member in zip(elem, val):
				self._from_xml(self, subelem, subelem.tag, member)
		elif isinstance(val, ndarray):
			# data = elem.attrib[prop]
			if elem.text:
				# create ndarray from data, assign value
				arr = np.fromstring(elem.text, dtype=val.dtype, sep=' ')
				setattr(target, prop, arr)
				logging.debug(f"ndarray {arr}, {val.dtype}, {type(arr)}")
			else:
				# todo - for some reason, setting the empty array (fine here) causes trouble in Pointer.write_template
				setattr(target, prop, None)
		elif isinstance(val, MemStruct):
			# print("MemStruct")
			val.from_xml(elem)
		elif isinstance(val, BaseEnum):
			# print("BaseEnum")
			setattr(target, prop, val.from_str(elem.attrib[prop]))
		else:
			# print("basic")
			# set basic attribute
			cls = type(val)
			if prop == XML_STR:
				# logging.debug(f"Can't handle {XML_STR} inside '{elem.tag}'")
				data = ET.tostring(elem[0], encoding="unicode").replace("\t", "").replace("\n", "")
				# override for setattr
				prop = "data"
			# strings stored as element text for readability
			elif prop == "data" and prop not in elem.attrib:
				data = elem.text
			# basic attributes
			elif prop in elem.attrib:
				data = elem.attrib[prop]
			else:
				logging.warning(f"Missing attribute '{prop}' in element '{elem.tag}'")
				return
			if data != "None":
				try:
					logging.debug(f"Setting {type(target).__name__}.{prop} = {data}")
					setattr(target, prop, cls(data))
				except TypeError:
					raise TypeError(f"Could not convert attribute {prop} = '{data}' to {cls.__name__}")

	def to_xml_file(self, file_path, debug=False):
		"""Create an xml elem representing this MemStruct, recursively set its data, indent and save to 'file_path'"""
		xml = ET.Element(self.__class__.__name__)
		self.to_xml(xml, debug)
		xml.attrib["game"] = str(get_game(self.context)[0])
		indent(xml)
		with open(file_path, 'wb') as outfile:
			outfile.write(ET.tostring(xml))

	def _to_xml(self, elem, prop, val, debug):
		"""Assigns data val to xml elem"""
		# logging.debug(f"_to_xml {elem.tag} - {prop}")
		if isinstance(val, Pointer):
			if val.frag and hasattr(val.frag, "struct_ptr"):
				f_ptr = val.frag.struct_ptr
				if debug:
					elem.set("_address", f"{f_ptr.pool_index} {f_ptr.data_offset}")
					elem.set("_size", f"{f_ptr.data_size}")
				elem.set(POOL_TYPE, f"{f_ptr.pool.type}")
			elif hasattr(val, POOL_TYPE):
				if val.pool_type is not None:
					elem.set(POOL_TYPE, f"{val.pool_type}")
			self._to_xml(elem, self._handle_xml_str(prop), val.data, debug)
		elif isinstance(val, Array):
			for member in val:
				cls_name = member.__class__.__name__.lower()
				member_elem = ET.SubElement(elem, cls_name)
				self._to_xml(member_elem, cls_name, member, debug)
		elif isinstance(val, ndarray):
			# elem.attrib[prop] = " ".join([str(member) for member in val])
			elem.text = " ".join([str(member) for member in val])
		elif isinstance(val, MemStruct):
			val.to_xml(elem, debug)
		# basic attribute
		else:
			if prop == XML_STR:
				if val is not None:
					elem.append(ET.fromstring(val))
				else:
					logging.warning(f"bug, val should not be None for XML_STR")
			# for better readability, set ztsr pointer data as xml text
			elif prop == "data":
				if val:
					elem.text = str(val)
			# actual basic attributes
			else:
				elem.set(prop, str(val))

	def to_xml(self, elem, debug):
		"""Adds data of this MemStruct to 'elem', recursively"""
		# go over all fields of this MemStruct
		for prop, val in vars(self).items():
			if prop == "name" and val:
				elem.attrib[prop] = val
			# skip dummy properties
			if prop in SKIPS:
				continue
			# add a sub-element if these are child of a MemStruct
			if isinstance(val, (MemStruct, Array, ndarray, Pointer)):
				sub = ET.SubElement(elem, prop)
				self._to_xml(sub, prop, val, debug)
			else:
				self._to_xml(elem, prop, val, debug)

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
