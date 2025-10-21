from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class Start(MemStruct):

	__name__ = 'Start'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.element = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.entrance = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.rear = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.middle = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.front = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.front_gate = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'element', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'entrance', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'rear', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'middle', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'front', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'front_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'element', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'entrance', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'rear', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'middle', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'front', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'front_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
