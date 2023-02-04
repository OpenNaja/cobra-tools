import os

from generated.base_struct import BaseStruct
from generated.formats.ovl.compounds.HeaderPointer import HeaderPointer


class Fragment(BaseStruct):

	"""
	These are to be thought of as instructions for loading. Their order is irrelevant.
	"""

	__name__ = 'Fragment'

	_import_key = 'ovl.compounds.Fragment'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# determines where to write a pointer address
		self.link_ptr = HeaderPointer(self.context, 0, None)

		# the struct that is pointed to can be found here
		self.struct_ptr = HeaderPointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('link_ptr', HeaderPointer, (0, None), (False, None), None),
		('struct_ptr', HeaderPointer, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'link_ptr', HeaderPointer, (0, None), (False, None)
		yield 'struct_ptr', HeaderPointer, (0, None), (False, None)

	@classmethod
	def read_array(cls, stream, shape, context=None, arg=0, template=None):
		return cls._read_array(stream, shape, context, arg, template)

	@property
	def ext(self):
		return self.ext_raw.replace(":", ".")

	@ext.setter
	def ext(self, e):
		self.ext_raw = e.replace(".", ":")

	def register(self, pools):
		self.struct_ptr.add_struct(self, pools)
		target_pool = pools[self.struct_ptr.pool_index]
		self.link_ptr.add_link((target_pool, self.struct_ptr.data_offset), pools)

