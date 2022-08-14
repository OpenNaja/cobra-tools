# START_GLOBALS
from generated.array import Array
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.compounds.Pointer import Pointer

DEPENDENCY_TAG = "dependency"


def indent(e, level=0):
	i = "\n" + level * "	"
	if len(e):
		if not e.text or not e.text.strip():
			e.text = i + "	"
		if not e.tail or not e.tail.strip():
			e.tail = i
		for e in e:
			indent(e, level + 1)
		if not e.tail or not e.tail.strip():
			e.tail = i
	else:
		if level and (not e.tail or not e.tail.strip()):
			e.tail = i


def str_to_bool(s):
	if s.lower() == 'true':
		return True
	elif s.lower() == 'false':
		return False
	else:
		raise ValueError


# END_GLOBALS

class MemStruct:
	"""this is a struct that is capable of having pointers"""
	# START_CLASS

	def get_props_and_ptrs(self):
		return [(prop, val) for prop, val in vars(self).items() if isinstance(val, Pointer)]

	def get_arrays(self):
		return [(prop, val) for prop, val in vars(self).items() if isinstance(val, Array)]

	def get_memstructs(self):
		return [val for prop, val in vars(self).items() if isinstance(val, MemStruct)]

	def handle_write(self, prop, val, struct_ptr, loader, pool_type, is_member=False):
		# logging.debug(f"handle_write {prop} {type(self).__name__}, {len(loader.fragments)} frags")
		if isinstance(val, MemStruct):
			val.write_ptrs(loader, struct_ptr, pool_type, is_member=is_member)
		elif isinstance(val, Array):
			for member in val:
				self.handle_write(prop, member, struct_ptr, loader, pool_type, is_member=True)
		elif isinstance(val, Pointer):
			# usually we add a pointer for empty arrays
			if val.data is not None:
				if DEPENDENCY_TAG in prop:
					# logging.debug(f"Created dependency for {prop} = {self.data}")
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
		# logging.debug(f"write_ptrs, member={is_member}")
		# don't write array members again, they have already been written!
		if not is_member:
			# write this struct's data
			struct_ptr.pool = loader.get_pool(pool_type)
			struct_ptr.write_instance(type(self), self)
			# logging.debug(f"memstruct's struct_ptr after {struct_ptr}")

		# write their data and update frags
		for prop, pointer in self.get_props_and_ptrs():
			self.handle_write(prop, pointer, struct_ptr, loader, pool_type)
		# get all arrays of this MemStruct
		for prop, array in self.get_arrays():
			self.handle_write(prop, array, struct_ptr, loader, pool_type)

	def read_ptrs(self, pool):
		# logging.debug(f"read_ptrs for {self.__class__.__name__}")
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
		# continue reading elem-memstructs directly attached to this memstruct
		for memstr in self.get_memstructs():
			memstr.read_ptrs(pool)

	def get_ptr_template(self, prop):
		"""Returns the appropriate template for a pointer named 'prop', if exists.
		Must be overwritten in subclass"""
		return None

	def handle_pointer(self, prop, pointer, pool):
		"""Ensures a pointer has a valid template, load it, and continue processing the linked memstruct."""
		# logging.debug(f"handle_pointer for {self.__class__.__name__}.{prop}")
		if not pointer.template:
			# try the lookup function
			pointer.template = self.get_ptr_template(prop)
		# reads the template and grabs the frag
		pointer.read_ptr(pool)
		if pointer.frag and hasattr(pointer.frag, "struct_ptr"):
			pool = pointer.frag.struct_ptr.pool
			pointer.pool_type = pool.type
			# logging.debug(f"Set pool type {pointer.pool_type} for pointer {prop}")
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

	def get_info_str(self):
		return f'\nMemStruct'

	def get_fields_str(self):
		return ""

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return ""
