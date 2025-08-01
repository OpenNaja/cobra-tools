from generated.formats.janitorsettings.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class JanitorEnd(MemStruct):

	"""
	back to the "data" part
	slightly different layout, but end up at same size
	PC 22 bytes mostly floats
	PZ 22 bytes mostly floats
	"""

	__name__ = 'JanitorEnd'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_11 = name_type_map['Float'].from_value(4.0)
		self.unk_12 = name_type_map['Float'].from_value(8.0)
		self.unk_13 = name_type_map['Float'](self.context, 0, None)
		self.unk_14 = name_type_map['Float'](self.context, 0, None)
		self.unk_15 = name_type_map['Float'](self.context, 0, None)
		self.unk_16 = name_type_map['Float'](self.context, 0, None)
		self.unk_17 = name_type_map['Float'](self.context, 0, None)
		self.unk_18 = name_type_map['Float'](self.context, 0, None)
		self.unk_19 = name_type_map['Float'](self.context, 0, None)
		self.unk_20 = name_type_map['Float'](self.context, 0, None)
		self.unk_21 = name_type_map['Float'](self.context, 0, None)
		self.unk_22 = name_type_map['Float'](self.context, 0, None)
		self.unk_23 = name_type_map['Float'](self.context, 0, None)
		self.unk_24 = name_type_map['Float'](self.context, 0, None)
		self.unk_25 = name_type_map['Float'](self.context, 0, None)
		self.unk_26 = name_type_map['Float'](self.context, 0, None)
		self.unk_27 = name_type_map['Float'](self.context, 0, None)
		self.unk_28 = name_type_map['Float'](self.context, 0, None)
		self.unk_29 = name_type_map['Float'](self.context, 0, None)
		self.unk_30 = name_type_map['Float'](self.context, 0, None)
		self.unk_31 = name_type_map['Float'](self.context, 0, None)
		self.unk_32 = name_type_map['Float'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unk_11', name_type_map['Float'], (0, None), (False, 4.0), (None, None)
		yield 'unk_12', name_type_map['Float'], (0, None), (False, 8.0), (None, None)
		yield 'unk_13', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_14', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_15', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_16', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_17', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_18', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_19', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_20', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_21', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_22', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_23', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_24', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_25', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_26', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_27', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_28', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_29', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_30', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_31', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_32', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_11', name_type_map['Float'], (0, None), (False, 4.0)
		yield 'unk_12', name_type_map['Float'], (0, None), (False, 8.0)
		yield 'unk_13', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_14', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_15', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_16', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_17', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_18', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_19', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_20', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_21', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_22', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_23', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_24', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_25', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_26', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_27', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_28', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_29', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_30', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_31', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_32', name_type_map['Float'], (0, None), (False, None)
