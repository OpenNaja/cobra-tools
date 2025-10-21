from generated.formats.logicalcontrols.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Button(MemStruct):

	__name__ = 'Button'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.datas_count = name_type_map['Uint'](self.context, 0, None)
		self.flags = name_type_map['Uint'](self.context, 0, None)
		self.button_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.datas = name_type_map['ArrayPointer'](self.context, self.datas_count, name_type_map['ButtonData'])
		self.pcdatas = name_type_map['ArrayPointer'](self.context, self.datas_count, name_type_map['PCButtonData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'button_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'datas', name_type_map['ArrayPointer'], (None, name_type_map['ButtonData']), (False, None), (lambda context: not (context.version == 18), None)
		yield 'pcdatas', name_type_map['ArrayPointer'], (None, name_type_map['PCButtonData']), (False, None), (lambda context: context.version == 18, None)
		yield 'datas_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'button_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if not (instance.context.version == 18):
			yield 'datas', name_type_map['ArrayPointer'], (instance.datas_count, name_type_map['ButtonData']), (False, None)
		if instance.context.version == 18:
			yield 'pcdatas', name_type_map['ArrayPointer'], (instance.datas_count, name_type_map['PCButtonData']), (False, None)
		yield 'datas_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None)
