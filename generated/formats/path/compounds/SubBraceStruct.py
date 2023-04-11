from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.path.imports import name_type_map


class SubBraceStruct(MemStruct):

	__name__ = 'SubBraceStruct'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.padding = name_type_map['Uint64'].from_value(0)
		self.sub_brace_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('sub_brace_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None))
		yield ('padding', name_type_map['Uint64'], (0, None), (False, 0), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'sub_brace_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'padding', name_type_map['Uint64'], (0, None), (False, 0)
