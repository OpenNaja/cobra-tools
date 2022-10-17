from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SubBraceStruct(MemStruct):

	__name__ = 'SubBraceStruct'

	_import_key = 'path.compounds.SubBraceStruct'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.padding = 0
		self.sub_brace_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('sub_brace_name', Pointer, (0, ZString), (False, None), None),
		('padding', Uint64, (0, None), (False, 0), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'sub_brace_name', Pointer, (0, ZString), (False, None)
		yield 'padding', Uint64, (0, None), (False, 0)
