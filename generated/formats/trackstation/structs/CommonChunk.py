from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class CommonChunk(MemStruct):

	"""
	PZ and PC: 104 bytes, core
	PZ and PC: 112 bytes, wrapped
	"""

	__name__ = 'CommonChunk'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.width = name_type_map['Float'](self.context, 0, None)
		self.height = name_type_map['Float'].from_value(0)
		self.top = name_type_map['FrontMidBack'](self.context, 0, None)
		self.base = name_type_map['FrontMidBack'](self.context, 0, None)
		self.supports = name_type_map['FrontMidBack'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'width', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'height', name_type_map['Float'], (0, None), (True, 0), (None, None)
		yield 'top', name_type_map['FrontMidBack'], (0, None), (False, None), (None, None)
		yield 'base', name_type_map['FrontMidBack'], (0, None), (False, None), (None, None)
		yield 'supports', name_type_map['FrontMidBack'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'width', name_type_map['Float'], (0, None), (False, None)
		yield 'height', name_type_map['Float'], (0, None), (True, 0)
		yield 'top', name_type_map['FrontMidBack'], (0, None), (False, None)
		yield 'base', name_type_map['FrontMidBack'], (0, None), (False, None)
		yield 'supports', name_type_map['FrontMidBack'], (0, None), (False, None)
