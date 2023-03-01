import logging

from generated.array import Array
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.compounds.Pointer import Pointer

DEPENDENCY_TAG = "dependency"


from generated.base_struct import BaseStruct


class MemStruct(BaseStruct):

	"""
	this is a struct that is capable of having pointers
	"""

	__name__ = 'MemStruct'

	_import_key = 'ovl_base.compounds.MemStruct'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	def get_props_and_ptrs(self):
		return [(prop, val) for prop, val in vars(self).items() if isinstance(val, Pointer)]

	def get_arrays(self):
		return [(prop, val) for prop, val in vars(self).items() if isinstance(val, Array)]

	def write_ptrs(self, loader, pool):
		"""Process all pointers in the structure and recursively load pointers in the sub-structs."""
		# todo - not sure how recursive fares here, since we theoretically have the whole structure set up already?
		# could work if the order is good
		for ptr, f_name, arguments in MemStruct.get_instances_recursive(self, Pointer):
			# locates the read address, attaches the frag entry, and reads the template as ptr.data
			offset = ptr.io_start
			if DEPENDENCY_TAG in f_name:
				loader.dependencies[ptr.data] = (pool, offset)
			elif ptr.has_data:
				# when generated from XML, the pool type is stored as metadata
				# it's not stored in binary, so for those, keep the root pool type
				if ptr.pool_type is not None:
					pool_type = ptr.pool_type
				else:
					pool_type = pool.type
				ptr.target_pool = loader.get_pool(pool_type)
				ptr.write_ptr()
				loader.fragments.add(((pool, offset), (ptr.target_pool, ptr.target_offset)))

	@classmethod
	def get_instances_recursive(cls, instance, dtype):
		for s_type, s_inst, (f_name, f_type, arguments, _) in cls.get_condition_attributes_recursive(instance, instance, lambda x: issubclass(x[1], dtype)):
			f_inst = s_type.get_field(s_inst, f_name)
			yield f_inst, f_name, arguments

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
			if ptr.target_pool:
				# keep reading pointers in the newly read ptr.data
				for memstruct in self.structs_from_ptr(ptr):
					memstruct.read_ptrs(ptr.target_pool)

	@staticmethod
	def structs_from_ptr(ptr):
		"""Get all direct memstruct children of this ptr"""
		if isinstance(ptr.data, MemStruct):
			yield ptr.data
		elif isinstance(ptr.data, Array):
			assert isinstance(ptr, (ArrayPointer, ForEachPointer))
			for member in ptr.data:
				if isinstance(member, MemStruct):
					yield member

	def get_ptr_template(self, prop):
		"""Returns the appropriate template for a pointer named 'prop', if exists.
		Must be overwritten in subclass"""
		return None


