from generated.array import Array
from generated.formats.bnk.imports import name_type_map
from generated.formats.bnk.structs.HircObject import HircObject


class EventAction(HircObject):

	__name__ = 'EventAction'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.scope = name_type_map['ActionScope'](self.context, 0, None)
		self.action_type = name_type_map['ActionType'](self.context, 0, None)
		self.children = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.id_ext_4 = name_type_map['Ubyte'](self.context, 0, None)
		self.node_initial_params = name_type_map['NodeInitialParams'](self.context, 0, None)
		self.raw = Array(self.context, 0, None, (0,), name_type_map['Byte'])
		self.by_bit_vector = name_type_map['Ubyte'].from_value(4)
		self.bank_i_d = name_type_map['Uint'](self.context, 0, None)
		self.bank_type = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'scope', name_type_map['ActionScope'], (0, None), (False, None), (None, None)
		yield 'action_type', name_type_map['ActionType'], (0, None), (False, None), (None, None)
		yield 'children', Array, (0, None, (1,), name_type_map['Uint']), (False, None), (None, None)
		yield 'id_ext_4', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'node_initial_params', name_type_map['NodeInitialParams'], (0, None), (False, None), (None, None)
		yield 'raw', Array, (0, None, (None,), name_type_map['Byte']), (False, None), (None, True)
		yield 'by_bit_vector', name_type_map['Ubyte'], (0, None), (False, 4), (None, True)
		yield 'bank_i_d', name_type_map['Uint'], (0, None), (False, None), (None, True)
		yield 'bank_type', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 144, True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'scope', name_type_map['ActionScope'], (0, None), (False, None)
		yield 'action_type', name_type_map['ActionType'], (0, None), (False, None)
		yield 'children', Array, (0, None, (1,), name_type_map['Uint']), (False, None)
		yield 'id_ext_4', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'node_initial_params', name_type_map['NodeInitialParams'], (0, None), (False, None)
		if instance.action_type != 4:
			yield 'raw', Array, (0, None, (instance.arg - (11 + instance.node_initial_params.io_size),), name_type_map['Byte']), (False, None)
		if instance.action_type == 4:
			yield 'by_bit_vector', name_type_map['Ubyte'], (0, None), (False, 4)
			yield 'bank_i_d', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version >= 144 and instance.action_type == 4:
			yield 'bank_type', name_type_map['Uint'], (0, None), (False, None)
