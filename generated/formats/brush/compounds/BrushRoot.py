from generated.formats.brush.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class BrushRoot(MemStruct):

	"""
	24 bytes
	"""

	__name__ = 'BrushRoot'

	_import_key = 'brush.compounds.BrushRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self._zero = 0
		self.num_pixels = 0
		self.x = 0
		self.y = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('_zero', name_type_map['Uint64'], (0, None), (False, None), (None, None))
		yield ('num_pixels', name_type_map['Uint64'], (0, None), (False, None), (None, None))
		yield ('x', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('y', name_type_map['Uint'], (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield '_zero', name_type_map['Uint64'], (0, None), (False, None)
		yield 'num_pixels', name_type_map['Uint64'], (0, None), (False, None)
		yield 'x', name_type_map['Uint'], (0, None), (False, None)
		yield 'y', name_type_map['Uint'], (0, None), (False, None)
