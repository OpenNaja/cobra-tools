from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class CommonChunk(MemStruct):

	"""
	PZ and PC: 104 bytes, core
	PZ and PC: 112 bytes, wrapped
	"""

	__name__ = 'CommonChunk'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float_1 = name_type_map['Float'](self.context, 0, None)
		self.float_2 = name_type_map['Float'](self.context, 0, None)
		self.top = name_type_map['FrontMidBack'](self.context, 0, None)
		self.unk_flags_0 = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.base = name_type_map['FrontMidBack'](self.context, 0, None)
		self.unk_flags_1 = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.supports = name_type_map['FrontMidBack'](self.context, 0, None)
		self.zero_1 = name_type_map['Uint64'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'float_1', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'float_2', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'top', name_type_map['FrontMidBack'], (0, None), (False, None), (None, None)
		yield 'unk_flags_0', Array, (0, None, (8,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'base', name_type_map['FrontMidBack'], (0, None), (False, None), (None, None)
		yield 'unk_flags_1', Array, (0, None, (8,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'supports', name_type_map['FrontMidBack'], (0, None), (False, None), (None, None)
		yield 'zero_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'float_1', name_type_map['Float'], (0, None), (False, None)
		yield 'float_2', name_type_map['Float'], (0, None), (False, None)
		yield 'top', name_type_map['FrontMidBack'], (0, None), (False, None)
		yield 'unk_flags_0', Array, (0, None, (8,), name_type_map['Ubyte']), (False, None)
		yield 'base', name_type_map['FrontMidBack'], (0, None), (False, None)
		yield 'unk_flags_1', Array, (0, None, (8,), name_type_map['Ubyte']), (False, None)
		yield 'supports', name_type_map['FrontMidBack'], (0, None), (False, None)
		yield 'zero_1', name_type_map['Uint64'], (0, None), (False, None)
