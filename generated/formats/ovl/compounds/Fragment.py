from generated.base_struct import BaseStruct
from generated.formats.ovl.compounds.HeaderPointer import HeaderPointer


class Fragment(BaseStruct):

	"""
	These are to be thought of as instructions for loading. Their order is irrelevant.
	"""

	__name__ = 'Fragment'

	_import_path = 'generated.formats.ovl.compounds.Fragment'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# determines where to write a pointer address
		self.link_ptr = HeaderPointer(self.context, 0, None)

		# the struct that is pointed to can be found here
		self.struct_ptr = HeaderPointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'link_ptr', HeaderPointer, (0, None), (False, None)
		yield 'struct_ptr', HeaderPointer, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Fragment [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
