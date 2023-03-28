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

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('button_name', Pointer, (0, ZString), (False, None), None)
		yield ('datas', ArrayPointer, (None, Button._import_map["logicalcontrols.compounds.ButtonData"]), (False, None), None)
		yield ('datas_count', Uint, (0, None), (False, None), None)
		yield ('flags', Uint, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'button_name', Pointer, (0, ZString), (False, None)
		yield 'datas', ArrayPointer, (instance.datas_count, Button._import_map["logicalcontrols.compounds.ButtonData"]), (False, None)
		yield 'datas_count', Uint, (0, None), (False, None)
		yield 'flags', Uint, (0, None), (False, None)


Button.init_attributes()
