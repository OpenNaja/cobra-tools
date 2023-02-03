# START_GLOBALS
import logging

from generated.array import Array
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.compounds.Pointer import Pointer

DEPENDENCY_TAG = "dependency"


# END_GLOBALS

class MemStruct:
	"""this is a struct that is capable of having pointers"""
	# START_CLASS

	def get_props_and_ptrs(self):
		return [(prop, val) for prop, val in vars(self).items() if isinstance(val, Pointer)]

	def get_arrays(self):
		return [(prop, val) for prop, val in vars(self).items() if isinstance(val, Array)]

	def handle_write(self, prop, val, struct_ptr, loader, pool_type, is_member=False):
		# logging.debug(f"handle_write {prop} {type(self).__name__}, {len(loader.fragments)} frags")
		if isinstance(val, MemStruct):
			val.write_ptrs(loader, struct_ptr, pool_type, is_member=is_member)
		elif isinstance(val, Array):
			for member in val:
				self.handle_write(prop, member, struct_ptr, loader, pool_type, is_member=True)
		elif isinstance(val, Pointer):
			# usually we add a pointer for empty arrays
			if val.has_data:
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

	@classmethod
	def get_instances_recursive(cls, instance, dtype):
		for s_type, s_inst, (f_name, f_type, arguments, _) in cls.get_condition_attributes_recursive(instance, instance, lambda x: issubclass(x[1], dtype)):
			f_inst = s_type.get_field(s_inst, f_name)
			yield f_inst, f_name, arguments

	@classmethod
	def get_instances(cls, instance, dtype):
		for attribute in cls.get_conditioned_attributes(instance, instance, lambda x: issubclass(x[1], dtype)):
			f_name, f_type, f_arguments = attribute[0:3]
			f_inst = instance.get_field(instance, f_name)
			yield f_inst, f_name, f_arguments

	def read_ptrs(self, pool):
		"""Process all pointers in the structure and recursively load pointers in the sub-structs."""
		# need to recurse here, because we may have substructs that are part of this MemStruct (not via ptrs)
		for ptr, f_name, arguments in MemStruct.get_instances_recursive(self, Pointer):
			# update the pointer's arg, as it is sometimes read after the pointer
			ptr.arg, template = arguments
			if not ptr.template:
				# try the lookup function to get a suitable template for this field
				ptr.template = self.get_ptr_template(f_name)
			# locates the read address, attaches the frag entry, and reads the template as ptr.data
			ptr.read_ptr(pool)
			self.handle_pointer(ptr)

	def get_ptr_template(self, prop):
		"""Returns the appropriate template for a pointer named 'prop', if exists.
		Must be overwritten in subclass"""
		return None

	def handle_pointer(self, ptr):
		"""Continue processing the linked memstructs."""
		if ptr.frag and hasattr(ptr.frag, "struct_ptr"):
			# we are now (potentially) in a new pool
			pool = ptr.frag.struct_ptr.pool
			ptr.pool_type = pool.type
			# keep reading pointers in the newly read ptr.data
			if isinstance(ptr.data, MemStruct):
				ptr.data.read_ptrs(pool)
			elif isinstance(ptr.data, Array):
				assert isinstance(ptr, (ArrayPointer, ForEachPointer))
				for member in ptr.data:
					if isinstance(member, MemStruct):
						member.read_ptrs(pool)
			# # not sure why it doesn't work like this
			# for memstruct, f_name, arguments in MemStruct.get_instances_recursive(ptr.data, MemStruct):
			# 	memstruct.read_ptrs(pool)

