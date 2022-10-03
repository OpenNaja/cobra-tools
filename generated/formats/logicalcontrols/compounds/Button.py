from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Button(MemStruct):

	__name__ = 'Button'

	_import_key = 'logicalcontrols.compounds.Button'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.datas_count = 0
		self.flags = 0
		self.button_name = Pointer(self.context, 0, ZString)
		self.datas = ArrayPointer(self.context, self.datas_count, Button._import_map["logicalcontrols.compounds.ButtonData"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('button_name', Pointer, (0, ZString), (False, None), None),
		('datas', ArrayPointer, (None, None), (False, None), None),
		('datas_count', Uint, (0, None), (False, None), None),
		('flags', Uint, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'button_name', Pointer, (0, ZString), (False, None)
		yield 'datas', ArrayPointer, (instance.datas_count, Button._import_map["logicalcontrols.compounds.ButtonData"]), (False, None)
		yield 'datas_count', Uint, (0, None), (False, None)
		yield 'flags', Uint, (0, None), (False, None)
